from functools import cached_property
from typing import List

from movie_site.db import (
    authenticate_user,
    create_movie,
    create_user,
    create_review,
    read_movie,
    read_movies,
    read_reviews_by_movie,
    read_user,
)
from movie_site.session import generate_user_session_token, get_user_id_from_token

import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType


@strawberry.type
class Movie:
    id: int
    title: str
    year: int
    img_url: str
    description: str
    avg_rating: float | None


@strawberry.type
class User:
    id: int
    username: str


@strawberry.type
class Review:
    id: int
    user_id: int
    movie_id: int
    rating: float
    text: str


@strawberry.type
class LoginSuccess:
    user: User
    token: str


@strawberry.type
class LoginError:
    message: str


LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))


class Context(BaseContext):
    @cached_property
    def user(self) -> User | None:
        if not self.request:
            return None

        token = self.request.headers.get("Authorization")
        if not token:
            return None

        user_id = get_user_id_from_token(token)
        return read_user(user_id)


Info = _Info[Context, RootValueType]


@strawberry.type
class Query:
    @strawberry.field
    def movies() -> List[Movie]:
        return read_movies()

    @strawberry.field
    def movie(movie_id: int) -> Movie:
        return read_movie(movie_id)
    
    @strawberry.field
    def reviews(movie_id: int) -> List[Review]:
        return read_reviews_by_movie(movie_id)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, username: str, password: str) -> User:
        user = create_user(username, password)
        return User(id=user.id, username=user.username)

    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginResult:
        user = authenticate_user(username, password)

        if not user:
            return LoginError(message="Invalid credentials")
        
        token = generate_user_session_token(user.id)
        return LoginSuccess(user=User(id=user.id, username=user.username), token=token)

    @strawberry.mutation
    def add_movie(self, title: str, year: int, img_url: str, description: str) -> Movie:
        return create_movie(title, year, img_url, description)
    
    @strawberry.mutation
    def add_review(self, info: Info, movie_id: int, rating: float, text: str) -> Review:
        if not info.context.user:
            raise Exception("Unauthorized")
        
        return create_review(info.context.user.id, movie_id, rating, text)

    
async def get_context() -> Context:
    return Context()


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
