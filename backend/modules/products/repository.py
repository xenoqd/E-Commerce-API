from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .model import Product
from .schemas import ProductSearch


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

    async def search_products(self, product: ProductSearch):
        query = select(Product)

        if product.search:
            query = query.where(Product.name.ilike(f"%{product.search}%"))

        if product.min_price:
            query = query.where(Product.price >= product.min_price)

        if product.max_price:
            query = query.where(Product.price <= product.max_price)

        offset = (product.page - 1) * product.limit
        query = query.offset(offset).limit(product.limit)

        result = await self.session.execute(query)

        return result.scalars().all()
