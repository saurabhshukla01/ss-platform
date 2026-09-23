from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.models.identity import Admin
from app.models.services import ServiceCategory
from app.schemas.catalog import ServiceCategoryOut, ServiceCategoryCreate, ServiceCategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[ServiceCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """Public: used by the website's service filters and the admin's service form."""
    return db.query(ServiceCategory).filter(ServiceCategory.is_active.is_(True)).order_by(ServiceCategory.display_order).all()


@router.get("/admin", response_model=list[ServiceCategoryOut], dependencies=[Depends(require_permission("services.manage"))])
def list_categories_admin(db: Session = Depends(get_db)):
    return db.query(ServiceCategory).order_by(ServiceCategory.display_order).all()


@router.post("/admin", response_model=ServiceCategoryOut, dependencies=[Depends(require_permission("services.manage"))])
def create_category(payload: ServiceCategoryCreate, request: Request, db: Session = Depends(get_db),
                     admin: Admin = Depends(get_current_admin)):
    if db.query(ServiceCategory).filter(ServiceCategory.slug == payload.slug).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug already exists")
    category = ServiceCategory(**payload.model_dump())
    db.add(category)
    db.flush()
    log_action(db, admin.id, "create", "categories", category.id, new_value=payload.model_dump(), request=request)
    db.commit()
    db.refresh(category)
    return category


@router.put("/admin/{category_id}", response_model=ServiceCategoryOut, dependencies=[Depends(require_permission("services.manage"))])
def update_category(category_id: int, payload: ServiceCategoryUpdate, request: Request, db: Session = Depends(get_db),
                     admin: Admin = Depends(get_current_admin)):
    category = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    old = {"name": category.name, "is_active": category.is_active}
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    log_action(db, admin.id, "update", "categories", category_id, old_value=old, new_value=payload.model_dump(exclude_unset=True), request=request)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/admin/{category_id}", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[Depends(require_permission("services.manage"))])
def delete_category(category_id: int, request: Request, db: Session = Depends(get_db),
                     admin: Admin = Depends(get_current_admin)):
    category = db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    log_action(db, admin.id, "delete", "categories", category_id, old_value={"name": category.name}, request=request)
    db.delete(category)
    db.commit()
