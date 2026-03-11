from fastapi import APIRouter, Depends

from .schemas import ProductSearch
from .service import ProductsService
from .dependencies import get_products_service


products_api = APIRouter(prefix="/products", tags=["Products"])


@products_api.get("")
async def search_products(
    data: ProductSearch = Depends(),
    service: ProductsService = Depends(get_products_service),
):
    product = await service.search_product(data)
    return product


@products_api.get("/{product_id}")
async def get_product(
    product_id: int, service: ProductsService = Depends(get_products_service)
):
    product = await service.get_product_by_id(product_id)
    return product
