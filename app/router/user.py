from fastapi import HTTPException,  Depends, status, APIRouter, Response
from .. import database
from ..database import get_session
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..utils import hash
from .. import models
from .. import oauth2


router = APIRouter(tags=["User"], prefix="/user")

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=models.UserPublic)
def create_user(user: models.UserCreate, session: Session = Depends(get_session)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User.model_validate(user)
    
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError as e:
        session.rollback()
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
        

@router.get("/", response_model=list[models.UserPublic])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(models.User)).all()
    return users

@router.delete("/{id:int}")
def delete_user(id, session: Session = Depends(get_session), current_user = Depends(oauth2.get_current_user)):
    db_record = session.get(models.User, id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with that id")
    
    if current_user.id != db_record.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    session.delete(db_record)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)