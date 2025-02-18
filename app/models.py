from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func



class PostBase(SQLModel):
    title: str = Field(index=True)
    content: str = Field()
    published: bool | None = Field(default=True)
    created_at: datetime = Field(default=datetime.utcnow())
    
class Posts(PostBase, table=True, extend_existing=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id",ondelete="CASCADE")


class PostCreate(PostBase):
    pass

class PostPublic(PostBase):
    id: int
    user_id: int

class PostUpdate(SQLModel):
    id: int | None = None
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    email : EmailStr = Field(index=True, unique=True)
    password : str = Field()


class User(UserBase, table=True, extend_existing=True):
    created_at: datetime = Field(default=datetime.utcnow())

class UserCreate(UserBase):
    pass
    
class UserPublic(SQLModel):
    id: int
    email: EmailStr

class Token(SQLModel):
    access_token: str
    type: str

class Token_Data(SQLModel):
    id: int