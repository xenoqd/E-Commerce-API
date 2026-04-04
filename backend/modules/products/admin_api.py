from fastapi import APIRouter, Depends

from backend.modules.products.schemas import ProductCreate, ProductEdit
from backend.modules.products.service import ProductsService
from backend.modules.products.dependencies import get_products_service

from backend.modules.auth.dependencies import get_admin_user
from backend.modules.user.models import User

products_admin_api = APIRouter(prefix="/admin/products", tags=["Admin products"])


@products_admin_api.post("")
async def create_product(
    product_in: ProductCreate,
    service: ProductsService = Depends(get_products_service),
    admin_user: User = Depends(get_admin_user),
):
    product = await service.create_product(product_in)
    return product


@products_admin_api.patch("")
async def edit_product(
    product_id: int,
    product_in: ProductEdit,
    service: ProductsService = Depends(get_products_service),
    admin_user: User = Depends(get_admin_user),
):
    product = await service.edit_product(product_id, product_in)
    return product
