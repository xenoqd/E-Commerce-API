import random
import uuid

from fastapi import HTTPException, status

from backend.modules.order.repository import OrderRepository
from backend.modules.payments.repository import PaymentRepository

from backend.modules.order.model import OrderStatus
from backend.modules.payments.model import Payment

class PaymentService:
    def __init__(self, order_repo: OrderRepository, payment_repo: PaymentRepository,):
        self.order_repo = order_repo
        self.payment_repo = payment_repo

    async def pay_order(self, order_id: int, payment: str):
        order = await self.order_repo.get_order(order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order not found"
            )

        if order.status != OrderStatus.confirmed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order already processed"
            )

        success = random.random() > 0.1

        payment = Payment(
            order_id=order.id,
            amount=order.total_price,
            status="success" if success else "failed",
            transaction_id=str(uuid.uuid4()),
            method=payment
        )

        await self.payment_repo.create_payment(payment)

        if success:
            order.status = "paid"
            await self.order_repo.update_order(order)

        return payment