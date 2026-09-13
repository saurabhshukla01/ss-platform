from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.analytics import Visitor, VisitorSession, PageView, AnalyticsEvent
from app.schemas.analytics import (
    SessionStartRequest, PageViewRequest, PageViewEndRequest, EventRequest, TrackAck,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _get_or_create_visitor(db: Session, payload: SessionStartRequest, ip: str | None) -> Visitor:
    visitor = db.query(Visitor).filter(Visitor.visitor_uuid == payload.visitor_uuid).first()
    if visitor:
        return visitor
    visitor = Visitor(
        visitor_uuid=payload.visitor_uuid,
        ip_address=ip,
        browser=payload.browser,
        browser_version=payload.browser_version,
        os=payload.os,
        device=payload.device,
        screen_width=payload.screen_width,
        screen_height=payload.screen_height,
    )
    db.add(visitor)
    db.flush()
    return visitor


# ---------- Public tracking endpoints (called from the website) ----------

@router.post("/session", response_model=TrackAck)
def start_session(payload: SessionStartRequest, request: Request, db: Session = Depends(get_db)):
    """First-party session start. No third-party cookies; visitor_uuid/session_uuid generated client-side."""
    visitor = _get_or_create_visitor(db, payload, request.client.host if request.client else None)

    existing = db.query(VisitorSession).filter(VisitorSession.session_uuid == payload.session_uuid).first()
    if existing:
        return TrackAck()

    session_row = VisitorSession(
        visitor_id=visitor.id,
        session_uuid=payload.session_uuid,
        landing_page=payload.landing_page,
        referrer=payload.referrer,
        utm_source=payload.utm_source,
        utm_medium=payload.utm_medium,
        utm_campaign=payload.utm_campaign,
        utm_term=payload.utm_term,
        utm_content=payload.utm_content,
        started_at=datetime.utcnow(),
    )
    db.add(session_row)
    db.commit()
    return TrackAck()


@router.post("/page-view", response_model=TrackAck)
def track_page_view(payload: PageViewRequest, db: Session = Depends(get_db)):
    session_row = db.query(VisitorSession).filter(VisitorSession.session_uuid == payload.session_uuid).first()
    if not session_row:
        return TrackAck(ok=False)
    db.add(PageView(
        session_id=session_row.id,
        page_url=payload.page_url,
        entry_time=payload.entry_time or datetime.utcnow(),
    ))
    db.commit()
    return TrackAck()


@router.post("/page-view/end", response_model=TrackAck)
def end_page_view(payload: PageViewEndRequest, db: Session = Depends(get_db)):
    session_row = db.query(VisitorSession).filter(VisitorSession.session_uuid == payload.session_uuid).first()
    if not session_row:
        return TrackAck(ok=False)
    page_view = (
        db.query(PageView)
        .filter(PageView.session_id == session_row.id, PageView.page_url == payload.page_url)
        .order_by(PageView.id.desc())
        .first()
    )
    if page_view:
        page_view.exit_time = payload.exit_time or datetime.utcnow()
        page_view.duration_seconds = payload.duration_seconds
        db.commit()
    return TrackAck()


@router.post("/event", response_model=TrackAck)
def track_event(payload: EventRequest, db: Session = Depends(get_db)):
    """Business events: service_view, pricing_view, quote_click, whatsapp_click, call_click, email_click, form_submit."""
    session_row = db.query(VisitorSession).filter(VisitorSession.session_uuid == payload.session_uuid).first()
    if not session_row:
        return TrackAck(ok=False)
    db.add(AnalyticsEvent(
        session_id=session_row.id,
        event_type=payload.event_type,
        page_url=payload.page_url,
        metadata_json=payload.metadata_json,
    ))
    db.commit()
    return TrackAck()


# ---------- Admin reporting endpoints ----------

@router.get("/admin/summary", dependencies=[Depends(require_permission("analytics.view"))])
def analytics_summary(db: Session = Depends(get_db)):
    total_visitors = db.query(func.count(Visitor.id)).scalar()
    total_sessions = db.query(func.count(VisitorSession.id)).scalar()
    total_page_views = db.query(func.count(PageView.id)).scalar()

    top_events = (
        db.query(AnalyticsEvent.event_type, func.count(AnalyticsEvent.id).label("count"))
        .group_by(AnalyticsEvent.event_type)
        .order_by(func.count(AnalyticsEvent.id).desc())
        .limit(10)
        .all()
    )
    top_utm_sources = (
        db.query(VisitorSession.utm_source, func.count(VisitorSession.id).label("count"))
        .filter(VisitorSession.utm_source.isnot(None))
        .group_by(VisitorSession.utm_source)
        .order_by(func.count(VisitorSession.id).desc())
        .limit(10)
        .all()
    )

    return {
        "total_visitors": total_visitors,
        "total_sessions": total_sessions,
        "total_page_views": total_page_views,
        "top_events": [{"event_type": e, "count": c} for e, c in top_events],
        "top_utm_sources": [{"source": s, "count": c} for s, c in top_utm_sources],
    }
