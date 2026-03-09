from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from .model import Product


class ProductsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product: Product):
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_product_by_id(self, product_id: int):
        query = select(Product).where(Product.id == product_id)
        result = await self.session.execute(query)
        product = result.scalar_one_or_none()
        return product
