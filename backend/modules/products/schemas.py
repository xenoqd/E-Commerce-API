from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int = 0
    is_active: bool = True
