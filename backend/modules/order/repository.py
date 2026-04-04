from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update

from backend.modules.order.model import Order, OrderItem


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order: Order):
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update_order(self, order: Order):
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update_total_price(self, order_id: int, total_price: float):
        query = (
            update(Order).where(Order.id == order_id).values(total_price=total_price)
        )
        await self.session.execute(query)

    async def create_order_item(self, item: OrderItem):
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_order(self, order_id: int):
        query = select(Order).where(Order.id == order_id)
        result = await self.session.execute(query)
        order = result.scalar_one_or_none()
        return order

    async def get_orders_by_user(self, user_id: int):
        query = select(Order).where(Order.user_id == user_id)
        result = await self.session.execute(query)
        orders = result.scalars().all()
        return orders

    async def get_order_items(self, order_id: int):
        query = select(OrderItem).where(OrderItem.order_id == order_id)
        result = await self.session.execute(query)
        items = result.scalars().all()
        return items
