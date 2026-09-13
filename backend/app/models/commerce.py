from sqlalchemy import String, Text, ForeignKey, Numeric, Enum, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base
from app.models.mixins import TimestampMixin


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"


class Coupon(Base, TimestampMixin):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255))
    discount_type: Mapped[str] = mapped_column(String(20), default="percent")  # percent | flat
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    max_uses: Mapped[int | None] = mapped_column(Integer)
    valid_from: Mapped[DateTime | None] = mapped_column(DateTime)
    valid_until: Mapped[DateTime | None] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    usages: Mapped[list["CouponUsage"]] = relationship(back_populates="coupon")


class CouponUsage(Base, TimestampMixin):
    __tablename__ = "coupon_usages"

    id: Mapped[int] = mapped_column(primary_key=True)
    coupon_id: Mapped[int] = mapped_column(ForeignKey("coupons.id", ondelete="CASCADE"))
    order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.id", ondelete="SET NULL"))
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"))

    coupon: Mapped["Coupon"] = relationship(back_populates="usages")


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="RESTRICT"))
    service_package_id: Mapped[int | None] = mapped_column(ForeignKey("service_packages.id", ondelete="SET NULL"))
    subscription_plan_id: Mapped[int | None] = mapped_column(ForeignKey("subscription_plans.id", ondelete="SET NULL"))

    order_number: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    subtotal_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    coupon_id: Mapped[int | None] = mapped_column(ForeignKey("coupons.id", ondelete="SET NULL"))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)

    payments: Mapped[list["Payment"]] = relationship(back_populates="order")
    invoice: Mapped["Invoice | None"] = relationship(back_populates="order", uselist=False)


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    gateway: Mapped[str] = mapped_column(String(50), nullable=False)  # razorpay | other
    gateway_order_id: Mapped[str | None] = mapped_column(String(150))
    gateway_payment_id: Mapped[str | None] = mapped_column(String(150))
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING, index=True)

    order: Mapped["Order"] = relationship(back_populates="payments")
    transactions: Mapped[list["PaymentTransaction"]] = relationship(back_populates="payment")


class PaymentTransaction(Base, TimestampMixin):
    """Raw gateway webhook/verification events for audit purposes.
    Only non-sensitive reference data is stored (never card numbers / CVV / credentials)."""

    __tablename__ = "payment_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id", ondelete="CASCADE"))
    event_type: Mapped[str] = mapped_column(String(50))  # created | verified | failed | refunded
    gateway_reference: Mapped[str | None] = mapped_column(String(150))
    raw_response_summary: Mapped[str | None] = mapped_column(Text)  # sanitized summary, not raw secrets

    payment: Mapped["Payment"] = relationship(back_populates="transactions")


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), unique=True)
    invoice_number: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    issued_at: Mapped[DateTime] = mapped_column(DateTime)
    pdf_url: Mapped[str | None] = mapped_column(String(500))

    order: Mapped["Order"] = relationship(back_populates="invoice")
