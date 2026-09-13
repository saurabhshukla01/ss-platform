from sqlalchemy import String, Text, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base
from app.models.mixins import TimestampMixin


class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    PROPOSAL_SENT = "PROPOSAL_SENT"
    NEGOTIATION = "NEGOTIATION"
    CONVERTED = "CONVERTED"
    CLOSED = "CLOSED"


class Customer(Base, TimestampMixin):
    """A converted lead / paying or engaged customer, distinct from a portal 'User' login."""

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(30))
    company_name: Mapped[str | None] = mapped_column(String(200))
    notes: Mapped[str | None] = mapped_column(Text)

    inquiries: Mapped[list["Inquiry"]] = relationship(back_populates="customer")
    leads: Mapped[list["Lead"]] = relationship(back_populates="customer")


class Inquiry(Base, TimestampMixin):
    """Raw form submission from Contact Us or Get Quote pages."""

    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"))

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30))
    service_id: Mapped[int | None] = mapped_column(ForeignKey("services.id", ondelete="SET NULL"))
    budget_range: Mapped[str | None] = mapped_column(String(100))
    timeline: Mapped[str | None] = mapped_column(String(100))
    preferred_contact_method: Mapped[str | None] = mapped_column(String(30))  # email | phone | whatsapp
    message: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(100))  # e.g. utm/referrer summary

    customer: Mapped["Customer | None"] = relationship(back_populates="inquiries")
    lead: Mapped["Lead | None"] = relationship(back_populates="inquiry", uselist=False)


class Lead(Base, TimestampMixin):
    """Trackable pipeline object derived from (or created directly for) an inquiry."""

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    inquiry_id: Mapped[int | None] = mapped_column(ForeignKey("inquiries.id", ondelete="SET NULL"), unique=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"))
    assigned_admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))

    status: Mapped[LeadStatus] = mapped_column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    source: Mapped[str | None] = mapped_column(String(100))  # Instagram, Google, Referral, etc.
    estimated_value: Mapped[float | None] = mapped_column(Numeric(12, 2))

    inquiry: Mapped["Inquiry | None"] = relationship(back_populates="lead")
    customer: Mapped["Customer | None"] = relationship(back_populates="leads")
    notes_list: Mapped[list["LeadNote"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    followups: Mapped[list["LeadFollowup"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    status_history: Mapped[list["LeadStatusHistory"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan"
    )


class LeadNote(Base, TimestampMixin):
    __tablename__ = "lead_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))
    note: Mapped[str] = mapped_column(Text, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="notes_list")


class LeadFollowup(Base, TimestampMixin):
    __tablename__ = "lead_followups"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))
    scheduled_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    channel: Mapped[str | None] = mapped_column(String(30))  # call | whatsapp | email
    completed: Mapped[bool] = mapped_column(default=False)
    outcome: Mapped[str | None] = mapped_column(Text)

    lead: Mapped["Lead"] = relationship(back_populates="followups")


class LeadStatusHistory(Base, TimestampMixin):
    __tablename__ = "lead_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))
    from_status: Mapped[LeadStatus | None] = mapped_column(Enum(LeadStatus))
    to_status: Mapped[LeadStatus] = mapped_column(Enum(LeadStatus), nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="status_history")
