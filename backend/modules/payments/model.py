from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

from typing import Optional


class PaymentStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int
    amount: float

    method: str
    status: PaymentStatus = PaymentStatus.pending

    transaction_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
