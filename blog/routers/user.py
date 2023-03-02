from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..hasing import Hash

router = APIRouter(tags=["Users"], prefix='/user')

get_db = database.get_db

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)): 
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} does not exist")
    return user 