from fastapi import HTTPException,  Depends, status, APIRouter
from .. import database
from ..database import get_session
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..utils import hash
from .. import models


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