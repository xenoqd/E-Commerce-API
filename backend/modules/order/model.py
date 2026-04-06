from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending" # Order created, waiting to be processed
    processing = "processing" # Worker started processing
    confirmed = "confirmed" # Items reserved, order is ready for payment
    paid = "paid" # Payment successfully received
    cancelled = "cancelled" # Cancelled by user or system
    expired = "expired" # Order expired due to time limit
    failed ="failed" # Processing failed


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: OrderStatus = Field(default=OrderStatus.pending)
    total_price: float

    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    price: float
