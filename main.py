from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.db.init import db_lifespan
from backend.infrastructure.redis.lifespan import redis_lifespan

from backend.modules.products.api import products_api
from backend.modules.auth.api import auth_router
from backend.modules.cart.api import cart_router
from backend.modules.order.api import order_router
from backend.modules.payments.api import payment_router

from backend.modules.products.admin_api import products_admin_api


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with redis_lifespan(app):
        async with db_lifespan(app):
            print("All resources are initialized")
            yield
            print("All resources closed")


app = FastAPI(lifespan=app_lifespan)

app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(products_api)
app.include_router(order_router)
app.include_router(payment_router)

app.include_router(products_admin_api)
