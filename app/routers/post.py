from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"{id} was no found")
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"{id} was no found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        # response.status_code = 404
        raise HTTPException(status_code=404, detail=f"{id} was no found")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)
