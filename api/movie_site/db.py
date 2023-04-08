from typing import List

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./movies.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    img_url = Column(String)
    description = Column(String)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)
    rating = Column(Float)
    text = Column(String)


def create_movie(title: str, year: int, img_url: str, description: str) -> Movie:
    movie = Movie(title=title, year=year, img_url=img_url, description=description)
    db.add(movie)
    db.commit()
    return movie


def read_movie(movie_id: int) -> Movie | None:
    return db.query(Movie).get(movie_id)


def create_user(username: str, password: str) -> User:
    hasher = PasswordHasher()
    hashed_password = hasher.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return user


def authenticate_user(username: str, password: str) -> User | None:
    user = db.query(User).where(User.username == username).one_or_none()

    if user is None:
        return None
    
    hasher = PasswordHasher()
    try:
         hasher.verify(user.hashed_password, password)
         return user
    except Argon2Error:
        return None


def read_user(user_id: int) -> User | None:
    return db.query(User).get(user_id)


def create_review(user_id: int, movie_id: int, rating: float, text: str) -> Review:
    review = Review(user_id=user_id, movie_id=movie_id, rating=rating, text=text)
    db.add(review)
    db.commit()
    return review


def read_reviews_by_movie(movie_id: int) -> List[Review]:
    return db.query(Review).where(Review.movie_id == movie_id)
