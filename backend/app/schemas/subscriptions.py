from datetime import datetime
from pydantic import BaseModel, Field

from app.models.subscriptions import BillingInterval, SubscriptionStatus


class PlanOut(BaseModel):
    id: int
    service_id: int | None
    name: str
    price: float
    billing_interval: BillingInterval
    features: str | None
    is_active: bool

    model_config = {"from_attributes": True}


class PlanCreate(BaseModel):
    service_id: int | None = None
    name: str = Field(min_length=2, max_length=120)
    price: float
    billing_interval: BillingInterval
    features: str | None = None


class PlanUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    billing_interval: BillingInterval | None = None
    features: str | None = None
    is_active: bool | None = None


class SubscriptionOut(BaseModel):
    id: int
    customer_id: int
    plan_id: int
    status: SubscriptionStatus
    start_date: datetime
    end_date: datetime | None
    next_renewal_date: datetime | None
    auto_renew: bool

    model_config = {"from_attributes": True}


class SubscriptionCreate(BaseModel):
    customer_id: int
    plan_id: int
    start_date: datetime
    next_renewal_date: datetime | None = None
    auto_renew: bool = True


class SubscriptionStatusUpdate(BaseModel):
    status: SubscriptionStatus


class WalletOut(BaseModel):
    id: int
    customer_id: int
    token_balance: int

    model_config = {"from_attributes": True}


class TokenAdjustment(BaseModel):
    change_amount: int = Field(description="Positive to credit, negative to debit")
    reason: str | None = None
