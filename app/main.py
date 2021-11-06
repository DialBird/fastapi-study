from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .routers import post, user, auth, vote
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Database connection was succesfull!")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error),

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
