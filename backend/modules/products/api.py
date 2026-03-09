from fastapi import APIRouter, Depends

from .schemas import ProductSearch
from .service import ProductsService
from .dependencies import get_products_service

from ..auth.dependencies import get_current_user
from ..user.models import User

products_api = APIRouter(prefix="/products", tags=["Products"])


@products_api.post("/search")
async def search_product(
    product_in: ProductSearch,
    service: ProductsService = Depends(get_products_service),
):
    product = await service.search_product(product_in)
    return product
