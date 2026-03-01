from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    id: int
    created_at: datetime


class UserLogin(BaseModel):
    username: str
    password: str
