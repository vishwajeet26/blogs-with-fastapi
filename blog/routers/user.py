from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import userRepository

router = APIRouter(tags=["Users"], prefix='/user')

get_db = database.get_db

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)): 
    return userRepository.create(request, db)
    
@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
   return userRepository.get_user(id, db)