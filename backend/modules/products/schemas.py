from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int = 0
    is_active: bool = True


class ProductSearch(BaseModel):
    search: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    page: int = 1
    limit: int = 20
