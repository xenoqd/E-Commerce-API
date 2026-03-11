from fastapi import HTTPException, status

from .repository import ProductsRepository
from .model import Product
from .schemas import ProductCreate, ProductSearch, ProductEdit


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

    async def edit_product(self, product_id: int, product_in: ProductEdit):

        product = await self.repo.get_product_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        updated_data = product_in.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(product, field, value)

        await self.repo.update(product)

        return product

    async def get_product_by_id(self, product_id: int):
        product = await self.repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    async def search_product(self, product_in: ProductSearch):
        product = await self.repo.search_products(product_in)
        return product
