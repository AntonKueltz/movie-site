from movie_site.graphql import graphql_app

from fastapi import FastAPI

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
