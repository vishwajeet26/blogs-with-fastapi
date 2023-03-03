from fastapi import APIRouter, Depends
from .. import schemas, database
from ..repository import blog
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=["Blogs"], prefix="/blog")

get_db = database.get_db

@router.get('/', response_model=List[schemas.showBlog])
def all(db: Session = Depends(get_db)):
   return blog.get_all(db)

@router.post('/blog', status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)): 
    return blog.create(request, db)


@router.delete('/{id}', status_code=204)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)

@router.put('/{id}', status_code=202)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.showBlog)
def show(id: int,  db: Session = Depends(get_db)):
    return blog.get(id, db)