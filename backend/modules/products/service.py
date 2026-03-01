from .repository import ProductsRepository
from .model import Product
from .schemas import ProductCreate


class ProductsService:
    def __init__(self, repo: ProductsRepository):
        self.repo = repo

    async def create_product(self, product_in: ProductCreate):
        product = Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            stock=product_in.stock,
            is_active=product_in.is_active,
        )
        await self.repo.create_product(product)

        return product
