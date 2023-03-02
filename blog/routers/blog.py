from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=["Blogs"], prefix="/blog")

get_db = database.get_db

@router.get('/', response_model=List[schemas.showBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)): 
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/{id}', status_code=204)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/{id}', status_code=202)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'


@router.get('/{id}', status_code=200, response_model=schemas.showBlog)
def show(id,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog