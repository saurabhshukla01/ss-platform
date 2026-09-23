from datetime import datetime
from pydantic import BaseModel, Field

from app.models.commerce import OrderStatus, PaymentStatus


class CouponOut(BaseModel):
    id: int
    code: str
    description: str | None
    discount_type: str
    discount_value: float
    max_uses: int | None
    valid_from: datetime | None
    valid_until: datetime | None
    is_active: bool

    model_config = {"from_attributes": True}


class CouponCreate(BaseModel):
    code: str = Field(min_length=3, max_length=50)
    description: str | None = None
    discount_type: str = "percent"  # percent | flat
    discount_value: float
    max_uses: int | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None


class CouponUpdate(BaseModel):
    description: str | None = None
    discount_value: float | None = None
    max_uses: int | None = None
    valid_until: datetime | None = None
    is_active: bool | None = None


class OrderOut(BaseModel):
    id: int
    order_number: str
    customer_id: int
    subtotal_amount: float
    discount_amount: float
    total_amount: float
    status: OrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentOut(BaseModel):
    id: int
    order_id: int
    gateway: str
    gateway_payment_id: str | None
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
