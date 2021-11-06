from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


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


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/createPosts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000)
    my_posts.append(post_dict)
    print(post)
    return {"data": post}


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
    post = find_post(id)
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"{id} was no found")
    return {"post_ detail": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"message": "updated post"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        return {"message": "dante"}

    my_posts.pop(index)
    return Response(status_code=204)
