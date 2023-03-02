from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/blog')
def index(limit: int = 0, published: bool = False, sort: Optional[str] = None):
    return {'data': f'{limit} blogs from the db {published}'}

@app.get('/blog/unpublished')
def unpublished(): 
    return {'data': 'all unpublished blogs'}

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id):
    return {"data": {'1', '2'}}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f"Blog is created with title {request.title}"}