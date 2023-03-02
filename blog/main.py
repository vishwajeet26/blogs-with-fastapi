from fastapi import FastAPI, Depends, Response, status, HTTPException 
from typing import List
from . import schemas, models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session
from .hasing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()  




@app.post('/blog', status_code=201, tags=["blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)): 
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=204, tags=["blogs"])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=202, tags=["blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'

@app.get('/blog', response_model=List[schemas.showBlog], tags=["blogs"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.showBlog, tags=["blogs"])
def show(id, response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog

@app.post('/user', response_model=schemas.ShowUser, tags=["user"])
def create_user(request: schemas.User, db: Session = Depends(get_db)): 
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=["user"])
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} does not exist")
    return user 