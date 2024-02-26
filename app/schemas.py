from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

class Posts(Post):
    id: int


class User(BaseModel):
    email: EmailStr
    password : str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    