from functools import cached_property

from movie_site.db import authenticate_user, create_movie, create_user, read_movie, read_user
from movie_site.session import generate_user_session_token, get_user_id_from_token

import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType


@strawberry.type
class Movie:
    title: str
    year: int
    img_url: str
    description: str


@strawberry.type
class User:
    id: int
    username: str


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

        token = self.request.headers.get("Authorization", None)
        user_id = get_user_id_from_token(token)
        return read_user(user_id)


Info = _Info[Context, RootValueType]


@strawberry.type
class Query:
    @strawberry.field
    def movie(title: str) -> Movie:
        movie = read_movie(title)
        return Movie(
            title=movie.title,
            year=movie.year,
            img_url=movie.img_url,
            description=movie.description
        )

    @strawberry.field
    def get_authenticated_user(self, info: Info) -> User | None:
        return info.context.user


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
        movie = create_movie(title, year, img_url, description)
        return Movie(
            title=movie.title,
            year=movie.year,
            img_url=movie.img_url,
            description=movie.description
        )

    
async def get_context() -> Context:
    return Context()


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
