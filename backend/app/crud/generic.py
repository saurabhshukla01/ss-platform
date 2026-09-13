"""
Generic CRUD router factory.

Builds an APIRouter that matches the convention already used by the
frontend's CrudManager component (website/src/components/CrudManager.jsx)
and by the existing services/inquiries routers:

    GET    {prefix}            -> public list (active items only, ordered)
    GET    {prefix}/admin      -> admin: list everything
    POST   {prefix}/admin      -> admin: create
    PUT    {prefix}/admin/{id} -> admin: update
    DELETE {prefix}/admin/{id} -> admin: delete

Using one factory keeps every "simple content list" model (banners,
announcements, offers, projects, team members, testimonials, ...)
consistent instead of hand-writing the same five endpoints repeatedly.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission


def build_crud_router(
    *,
    model,
    prefix: str,
    tag: str,
    permission: str,
    out_schema: type[BaseModel],
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
    order_field: str = "display_order",
    active_field: str | None = "is_active",
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    # ---------- Public ----------

    @router.get("", response_model=list[out_schema])
    def list_public(db: Session = Depends(get_db)):
        query = db.query(model)
        if active_field is not None and hasattr(model, active_field):
            query = query.filter(getattr(model, active_field).is_(True))
        if hasattr(model, order_field):
            query = query.order_by(getattr(model, order_field))
        return query.all()

    # ---------- Admin ----------

    @router.get(
        "/admin",
        response_model=list[out_schema],
        dependencies=[Depends(require_permission(permission))],
    )
    def list_admin(db: Session = Depends(get_db)):
        query = db.query(model)
        if hasattr(model, order_field):
            query = query.order_by(getattr(model, order_field))
        return query.all()

    @router.post(
        "/admin",
        response_model=out_schema,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(require_permission(permission))],
    )
    def create_admin(payload: create_schema, db: Session = Depends(get_db)):
        item = model(**payload.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @router.put(
        "/admin/{item_id}",
        response_model=out_schema,
        dependencies=[Depends(require_permission(permission))],
    )
    def update_admin(item_id: int, payload: update_schema, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"{tag[:-1] if tag.endswith('s') else tag} not found")
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @router.delete(
        "/admin/{item_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(require_permission(permission))],
    )
    def delete_admin(item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"{tag[:-1] if tag.endswith('s') else tag} not found")
        db.delete(item)
        db.commit()

    return router
