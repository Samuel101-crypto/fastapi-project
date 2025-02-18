from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select, Session
from .. import models
from ..database import get_session
from ..utils import verify_password
from ..oauth2 import create_jwt
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/login')
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    db_record = session.exec(select(models.User).where(models.User.email == user_credentials.username)).first()
    if not db_record:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not verify_password(user_credentials.password, db_record.password):
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = create_jwt({"user_id": db_record.id})
    return{"access_token": access_token,  "type": "bearer"}

    