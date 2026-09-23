from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.models.identity import Admin
from app.models.brand import Setting
from app.schemas.settings import SettingOut, SettingUpsert

router = APIRouter(prefix="/settings", tags=["Settings"])


def _mask(setting: Setting) -> SettingOut:
    """Builds a masked response DTO without mutating the tracked ORM instance —
    mutating setting.value directly risked persisting the mask over the real
    secret on the next session flush."""
    out = SettingOut.model_validate(setting)
    if out.is_secret and out.value:
        out.value = "•" * 8
    return out


@router.get("", response_model=list[SettingOut], dependencies=[Depends(require_permission("settings.manage"))])
def list_settings(group: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Setting)
    if group:
        query = query.filter(Setting.group == group)
    return [_mask(s) for s in query.order_by(Setting.group, Setting.key).all()]


@router.put("", response_model=SettingOut, dependencies=[Depends(require_permission("settings.manage"))])
def upsert_setting(payload: SettingUpsert, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    """Create or update a single group/key setting (e.g. group=company, key=phone)."""
    row = db.query(Setting).filter(Setting.group == payload.group, Setting.key == payload.key).first()
    if row:
        row.value = payload.value
        row.is_secret = payload.is_secret
    else:
        row = Setting(**payload.model_dump())
        db.add(row)
    db.flush()
    log_action(db, admin.id, "upsert", "settings", f"{payload.group}.{payload.key}",
               new_value={"has_value": bool(payload.value)} if payload.is_secret else {"value": payload.value}, request=request)
    db.commit()
    db.refresh(row)
    return _mask(row)
