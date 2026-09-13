from sqlalchemy import String, Text, ForeignKey, Numeric, Enum, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base
from app.models.mixins import TimestampMixin


class BillingInterval(str, enum.Enum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class SubscriptionPlan(Base, TimestampMixin):
    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int | None] = mapped_column(ForeignKey("services.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    billing_interval: Mapped[BillingInterval] = mapped_column(Enum(BillingInterval), nullable=False)
    features: Mapped[str | None] = mapped_column(Text)  # JSON-encoded feature list, admin-editable
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="plan")


class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("subscription_plans.id", ondelete="RESTRICT"))

    status: Mapped[SubscriptionStatus] = mapped_column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[DateTime | None] = mapped_column(DateTime)
    next_renewal_date: Mapped[DateTime | None] = mapped_column(DateTime)
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)

    plan: Mapped["SubscriptionPlan"] = relationship(back_populates="subscriptions")
    items: Mapped[list["SubscriptionItem"]] = relationship(back_populates="subscription", cascade="all, delete-orphan")


class SubscriptionItem(Base, TimestampMixin):
    """Line items within a subscription (e.g. add-ons, extra hosting slots)."""

    __tablename__ = "subscription_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"))
    label: Mapped[str] = mapped_column(String(150), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    subscription: Mapped["Subscription"] = relationship(back_populates="items")


class CustomerWallet(Base, TimestampMixin):
    """Service-credit/token wallet balance per customer."""

    __tablename__ = "customer_wallets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), unique=True)
    token_balance: Mapped[int] = mapped_column(Integer, default=0)

    usage_logs: Mapped[list["TokenUsageLog"]] = relationship(back_populates="wallet", cascade="all, delete-orphan")


class ServiceToken(Base, TimestampMixin):
    """Definition of a token/credit type — e.g. 'Maintenance Hour', 'API Call Credit'."""

    __tablename__ = "service_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    token_value_inr: Mapped[float | None] = mapped_column(Numeric(10, 2))


class TokenUsageLog(Base, TimestampMixin):
    """Every credit/token consumption or manual admin adjustment, with audit trail."""

    __tablename__ = "token_usage_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("customer_wallets.id", ondelete="CASCADE"))
    service_token_id: Mapped[int | None] = mapped_column(ForeignKey("service_tokens.id", ondelete="SET NULL"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))  # set if manual adjustment
    change_amount: Mapped[int] = mapped_column(Integer, nullable=False)  # positive = credit, negative = debit
    reason: Mapped[str | None] = mapped_column(String(255))
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)

    wallet: Mapped["CustomerWallet"] = relationship(back_populates="usage_logs")
