from sqlalchemy import String, ForeignKey, DateTime, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Visitor(Base, TimestampMixin):
    """First-party visitor identity (cookie-less friendly UUID, not PII)."""

    __tablename__ = "visitors"

    id: Mapped[int] = mapped_column(primary_key=True)
    visitor_uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(64))
    browser: Mapped[str | None] = mapped_column(String(80))
    browser_version: Mapped[str | None] = mapped_column(String(30))
    os: Mapped[str | None] = mapped_column(String(80))
    device: Mapped[str | None] = mapped_column(String(40))  # desktop | mobile | tablet
    screen_width: Mapped[int | None] = mapped_column(Integer)
    screen_height: Mapped[int | None] = mapped_column(Integer)

    sessions: Mapped[list["VisitorSession"]] = relationship(back_populates="visitor", cascade="all, delete-orphan")


class VisitorSession(Base, TimestampMixin):
    __tablename__ = "visitor_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    visitor_id: Mapped[int] = mapped_column(ForeignKey("visitors.id", ondelete="CASCADE"))
    session_uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, index=True)

    landing_page: Mapped[str | None] = mapped_column(String(500))
    exit_page: Mapped[str | None] = mapped_column(String(500))
    referrer: Mapped[str | None] = mapped_column(String(500))

    utm_source: Mapped[str | None] = mapped_column(String(150))
    utm_medium: Mapped[str | None] = mapped_column(String(150))
    utm_campaign: Mapped[str | None] = mapped_column(String(150))
    utm_term: Mapped[str | None] = mapped_column(String(150))
    utm_content: Mapped[str | None] = mapped_column(String(150))

    started_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    ended_at: Mapped[DateTime | None] = mapped_column(DateTime)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)

    visitor: Mapped["Visitor"] = relationship(back_populates="sessions")
    page_views: Mapped[list["PageView"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    events: Mapped[list["AnalyticsEvent"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class PageView(Base, TimestampMixin):
    __tablename__ = "page_views"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("visitor_sessions.id", ondelete="CASCADE"))
    page_url: Mapped[str] = mapped_column(String(500), nullable=False)
    entry_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    exit_time: Mapped[DateTime | None] = mapped_column(DateTime)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)

    session: Mapped["VisitorSession"] = relationship(back_populates="page_views")


class AnalyticsEvent(Base, TimestampMixin):
    """Business events: service_view, pricing_view, quote_click, whatsapp_click, call_click, email_click, form_submit."""

    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("visitor_sessions.id", ondelete="CASCADE"))
    event_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    page_url: Mapped[str | None] = mapped_column(String(500))
    metadata_json: Mapped[dict | None] = mapped_column(JSON)  # e.g. {"service_slug": "website-development"}

    session: Mapped["VisitorSession"] = relationship(back_populates="events")
