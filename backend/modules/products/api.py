from fastapi import APIRouter, Depends

from .schemas import ProductSearch
from .service import ProductsService
from .dependencies import get_products_service


products_api = APIRouter(prefix="/products", tags=["Products"])


@products_api.get("/search")
async def get_products(
    data: ProductSearch = Depends(),
    service: ProductsService = Depends(get_products_service),
):
    product = await service.search_product(data)
    return product
