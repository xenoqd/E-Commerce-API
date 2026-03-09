from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, delete
from .model import Cart, CartItem

from typing import List

class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cart_by_user_id(self, user_id: int):
        query = select(Cart).where(Cart.user_id == user_id)
        result = await self.session.execute(query)
        cart = result.scalar_one_or_none()
        return cart

    async def get_cart_item(self, cart_id: int, product_id: int):
        query = select(CartItem).where(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_cart_items(self, cart_id: int) -> List[CartItem]:
        query = select(CartItem).where(CartItem.cart_id == cart_id)
        result = await self.session.execute(query)
        cart = result.scalars().all()
        return cart

    async def create_cart(self, cart: Cart):
        self.session.add(cart)
        await self.session.commit()
        await self.session.refresh(cart)
        return cart

    async def clear_cart(self, cart_id: int):
        query = delete(CartItem).where(CartItem.cart_id == cart_id)
        await self.session.execute(query)
        await self.session.commit()

    async def create_cart_item(self, cart_id: int, product_id: int, quantity: int):
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )
        self.session.add(cart_item)
        await self.session.commit()
        await self.session.refresh(cart_item)
        return cart_id
    
    async def update(self, entity):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
