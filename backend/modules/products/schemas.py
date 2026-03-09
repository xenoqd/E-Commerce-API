from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int = 0
    is_active: bool = True


class ProductSearch(BaseModel):
    search: Optional[str]
    min_price: Optional[float]
    max_price: Optional[float]
    page: int = 1
    limit: int = 20
