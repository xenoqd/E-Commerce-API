from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .model import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, payment: Payment):
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment