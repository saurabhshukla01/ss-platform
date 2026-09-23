from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.models.identity import Admin


def simple_crud_router(entity_path: str, model, out_schema, in_schema, permission: str, public_filter: bool = True) -> APIRouter:
    """
    Registers GET (public, active-only) / GET admin (all) / POST / PUT / DELETE
    for a straightforward content model with no nested relations.
    """
    sub = APIRouter()

    @sub.get(f"/{entity_path}", response_model=list[out_schema])
    def list_public(db: Session = Depends(get_db)):
        q = db.query(model)
        if public_filter and hasattr(model, "is_active"):
            q = q.filter(model.is_active.is_(True))
        return q.all()

    @sub.get(f"/{entity_path}/admin", response_model=list[out_schema], dependencies=[Depends(require_permission(permission))])
    def list_admin(db: Session = Depends(get_db)):
        return db.query(model).order_by(model.id.desc()).all()

    @sub.post(f"/{entity_path}/admin", response_model=out_schema, dependencies=[Depends(require_permission(permission))])
    def create(payload: in_schema, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
        row = model(**payload.model_dump())
        db.add(row)
        db.flush()
        log_action(db, admin.id, "create", entity_path, row.id, new_value=payload.model_dump(mode="json"), request=request)
        db.commit()
        db.refresh(row)
        return row

    @sub.put(f"/{entity_path}/admin/{{item_id}}", response_model=out_schema, dependencies=[Depends(require_permission(permission))])
    def update(item_id: int, payload: in_schema, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
        row = db.query(model).filter(model.id == item_id).first()
        if not row:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        for field, value in payload.model_dump().items():
            setattr(row, field, value)
        log_action(db, admin.id, "update", entity_path, item_id, new_value=payload.model_dump(mode="json"), request=request)
        db.commit()
        db.refresh(row)
        return row

    @sub.delete(f"/{entity_path}/admin/{{item_id}}", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[Depends(require_permission(permission))])
    def delete(item_id: int, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
        row = db.query(model).filter(model.id == item_id).first()
        if not row:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        log_action(db, admin.id, "delete", entity_path, item_id, request=request)
        db.delete(row)
        db.commit()

    return sub
