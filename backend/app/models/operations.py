from sqlalchemy import String, Text, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Notification(Base, TimestampMixin):
    """In-admin-panel notifications (new lead, payment received, etc.)."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str | None] = mapped_column(Text)
    link_url: Mapped[str | None] = mapped_column(String(500))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)


class CommunicationLog(Base, TimestampMixin):
    """Outbound email / WhatsApp / call-request log tied to a customer or lead."""

    __tablename__ = "communication_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"))
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))
    channel: Mapped[str] = mapped_column(String(30), nullable=False)  # email | whatsapp | call | sms
    direction: Mapped[str] = mapped_column(String(10), default="outbound")  # outbound | inbound
    subject: Mapped[str | None] = mapped_column(String(255))
    body: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(String(30))  # sent | failed | delivered


class AuditLog(Base, TimestampMixin):
    """Records every meaningful admin action for accountability."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))
    action: Mapped[str] = mapped_column(String(100), nullable=False)  # create | update | delete | login
    module: Mapped[str] = mapped_column(String(100), nullable=False)  # services | leads | payments ...
    record_id: Mapped[str | None] = mapped_column(String(100))
    old_value: Mapped[dict | None] = mapped_column(JSON)
    new_value: Mapped[dict | None] = mapped_column(JSON)
    ip_address: Mapped[str | None] = mapped_column(String(64))


class SeoMeta(Base, TimestampMixin):
    """Per-URL SEO overrides, editable from Admin without frontend deploys."""

    __tablename__ = "seo_meta"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(300), unique=True, nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(300))
    canonical_url: Mapped[str | None] = mapped_column(String(500))
    og_image_url: Mapped[str | None] = mapped_column(String(500))
    schema_json: Mapped[dict | None] = mapped_column(JSON)


class Redirect(Base, TimestampMixin):
    __tablename__ = "redirects"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_path: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    to_path: Mapped[str] = mapped_column(String(300), nullable=False)
    status_code: Mapped[int] = mapped_column(default=301)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
