from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
