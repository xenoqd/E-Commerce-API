from fastapi import Depends
from backend.db.session import get_session

from backend.modules.products.repository import ProductsRepository
from backend.modules.products.service import ProductsService


async def get_products_service(session=Depends(get_session)) -> ProductsService:
    repo = ProductsRepository(session)
    service = ProductsService(repo)
    return service
