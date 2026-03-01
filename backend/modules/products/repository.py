from sqlalchemy.ext.asyncio import AsyncSession
from .model import Product


class ProductsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product: Product):
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product
