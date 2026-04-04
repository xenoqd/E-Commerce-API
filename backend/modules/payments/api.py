from fastapi import APIRouter, Depends

from backend.modules.auth.dependencies import get_current_user
from backend.modules.user.models import User

from backend.modules.payments.service import PaymentService
from backend.modules.payments.dependencies import get_payment_service
from backend.modules.payments.schemas import PaymentRequest

payment_router = APIRouter(prefix="/payment", tags=["Payment"])

@payment_router.post("/orders/{order_id}/pay")
async def pay_order(
    order_id: int,
    payment: PaymentRequest,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service)
):
    payment = await service.pay_order(order_id, payment.method)
    return payment