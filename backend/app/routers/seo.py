from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.core.crud_factory import simple_crud_router
from app.models.identity import Admin
from app.models.operations import SeoMeta, Redirect
from app.schemas.seo import SeoMetaOut, SeoMetaIn, RedirectOut, RedirectIn

router = APIRouter(prefix="/seo", tags=["SEO"])


@router.get("/meta", response_model=SeoMetaOut)
def get_meta_for_path(path: str, db: Session = Depends(get_db)):
    """Public: the frontend calls this with the current route to populate <head> tags."""
    meta = db.query(SeoMeta).filter(SeoMeta.path == path).first()
    if not meta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No SEO override for this path")
    return meta


@router.get("/meta/admin", response_model=list[SeoMetaOut], dependencies=[Depends(require_permission("content.manage"))])
def list_meta_admin(db: Session = Depends(get_db)):
    return db.query(SeoMeta).order_by(SeoMeta.path).all()


@router.post("/meta/admin", response_model=SeoMetaOut, dependencies=[Depends(require_permission("content.manage"))])
def create_meta(payload: SeoMetaIn, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    if db.query(SeoMeta).filter(SeoMeta.path == payload.path).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "SEO meta already exists for this path")
    row = SeoMeta(**payload.model_dump())
    db.add(row)
    db.flush()
    log_action(db, admin.id, "create", "seo_meta", row.id, new_value=payload.model_dump(mode="json"), request=request)
    db.commit()
    db.refresh(row)
    return row


@router.put("/meta/admin/{meta_id}", response_model=SeoMetaOut, dependencies=[Depends(require_permission("content.manage"))])
def update_meta(meta_id: int, payload: SeoMetaIn, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    row = db.query(SeoMeta).filter(SeoMeta.id == meta_id).first()
    if not row:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    for field, value in payload.model_dump().items():
        setattr(row, field, value)
    log_action(db, admin.id, "update", "seo_meta", meta_id, new_value=payload.model_dump(mode="json"), request=request)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/meta/admin/{meta_id}", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[Depends(require_permission("content.manage"))])
def delete_meta(meta_id: int, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    row = db.query(SeoMeta).filter(SeoMeta.id == meta_id).first()
    if not row:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    log_action(db, admin.id, "delete", "seo_meta", meta_id, request=request)
    db.delete(row)
    db.commit()


router.include_router(simple_crud_router("redirects", Redirect, RedirectOut, RedirectIn, "content.manage", public_filter=False))
