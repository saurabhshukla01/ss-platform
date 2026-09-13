from datetime import datetime

from pydantic import BaseModel


class SessionStartRequest(BaseModel):
    visitor_uuid: str
    session_uuid: str
    landing_page: str | None = None
    referrer: str | None = None
    browser: str | None = None
    browser_version: str | None = None
    os: str | None = None
    device: str | None = None
    screen_width: int | None = None
    screen_height: int | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_term: str | None = None
    utm_content: str | None = None


class PageViewRequest(BaseModel):
    session_uuid: str
    page_url: str
    entry_time: datetime | None = None


class PageViewEndRequest(BaseModel):
    session_uuid: str
    page_url: str
    exit_time: datetime | None = None
    duration_seconds: int | None = None


class EventRequest(BaseModel):
    session_uuid: str
    event_type: str  # service_view | pricing_view | quote_click | whatsapp_click | call_click | email_click | form_submit
    page_url: str | None = None
    metadata_json: dict | None = None


class TrackAck(BaseModel):
    ok: bool = True
