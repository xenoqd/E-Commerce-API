from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    role: UserRole = Field(default=UserRole.USER)

    cart: Optional["Cart"] = Relationship(back_populates="user")
