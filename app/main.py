from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import session
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/createPosts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post.title, post.content, post.published)
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"{id} was no found")
    return {"data": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""",
        (post.title, post.content, post.published),
    )
    post = cursor.fetchone()
    conn.commit()
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"{id} was no found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""", (str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"{id} was no found")
    return Response(status_code=204)
