from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_session

from ..order.repository import OrderRepository
from .repository import PaymentRepository

from .service import PaymentService


async def get_payment_service(
    session: AsyncSession = Depends(get_session),
):
    order_repo = OrderRepository(session)
    payment_repo = PaymentRepository(session)

    return PaymentService(order_repo, payment_repo)