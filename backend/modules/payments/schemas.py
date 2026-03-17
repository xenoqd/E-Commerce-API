from pydantic import BaseModel
from enum import Enum


class PaymentMethod(str, Enum):
    card = "card"
    paypal = "paypal"
    crypto = "crypto"


class PaymentRequest(BaseModel):
    method: PaymentMethod