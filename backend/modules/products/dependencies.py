from fastapi import Depends
from backend.db.session import get_session
from .repository import ProductsRepository
from .service import ProductsService


async def get_products_service(session=Depends(get_session)) -> ProductsService:
    repo = ProductsRepository(session)
    service = ProductsService(repo)
    return service
