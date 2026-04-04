from backend.modules.products.repository import ProductsRepository
from backend.modules.cart.repository import CartRepository

from backend.modules.cart.model import Cart
from backend.modules.cart.events import CartEvents

from backend.core.event_bus import EventBus

from fastapi import HTTPException, status

class CartService:
    def __init__(self, repo: CartRepository, product_repo: ProductsRepository, event_bus: EventBus ):
        self.repo = repo
        self.product_repo = product_repo
        self.event_bus = event_bus

    async def get_or_create_cart(self, user_id: int):
        cart = await self.repo.get_cart_by_user_id(user_id)
        if cart:
            return cart

        cart = Cart(user_id=user_id)

        return await self.repo.create_cart(cart)

    async def add_to_cart(self, user_id: int, product_id: int):
        cart = await self.get_or_create_cart(user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart do not exist"
            )

        product = await self.product_repo.get_product_by_id(product_id) 
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        cart_item = await self.repo.get_cart_item(cart.id, product.id)

        new_quantity = 1

        if cart_item:
            new_quantity = cart_item.quantity + 1

        if new_quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )

        if cart_item:
            cart_item.quantity = new_quantity
            await self.repo.update(cart_item)
        else:
            await self.repo.create_cart_item(
                cart_id=cart.id,
                product_id=product_id,
                quantity=1
            )

        await self.event_bus.publish(
            CartEvents.ITEM_ADDED,
            {
                "user_id": user_id,
                "product_id": product_id,
                "quantity": new_quantity
            },
        )
        
        return {"message": "Product added to cart"}

    async def remove_from_cart(self, user_id: int, product_id: int):
        cart = await self.get_or_create_cart(user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart do not exist"
            )

        product = await self.product_repo.get_product_by_id(product_id) 
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        cart_item = await self.repo.get_cart_item(cart.id, product.id)

        if not cart_item:
            raise HTTPException(
                status_code=404,
                detail="Product not in cart"
            )

        
        new_quantity = cart_item.quantity - 1

        if new_quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart already empty"
                )
        
        if new_quantity == 0:
            await self.repo.clear_cart(cart_item.cart_id)
        else: 
            cart_item.quantity = new_quantity
            await self.repo.update(cart_item)

        await self.event_bus.publish(
            CartEvents.ITEM_REMOVED,
            {
                "user_id": user_id,
                "product_id": product_id,
                "quantity": new_quantity
            },
        )

        return {"message": "Product removed from card"}

    
    async def get_cart(self, user_id: int):
        cart = await self.get_or_create_cart(user_id)

        items = await self.repo.get_cart_items(cart_id=cart.id)

        total_price = 0

        result = []

        for item in items:
            product = await self.product_repo.get_product_by_id(item.product_id)

            item_total = product.price * item.quantity
            total_price += item_total

            result.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "total": item_total
            })

        return {
            "items": result,
            "total_price": total_price
        }

    async def clear_cart(self, user_id: int):
        cart = await self.get_or_create_cart(user_id)
        items = await self.repo.get_cart_items(cart.id)
        if not items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart already empty"
                )

        await self.repo.clear_cart(cart_id=cart.id)

        await self.event_bus.publish(
            CartEvents.CART_CLEARED,
            {
                "user_id": user_id,
                "cart_id": cart.id
            },
        )

        return cart