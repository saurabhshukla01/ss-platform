from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.services import Service, ServiceCategory
from app.schemas.services import ServiceListItem, ServiceDetail, ServiceCreate, ServiceUpdate

router = APIRouter(prefix="/services", tags=["Services"])


# ---------- Public endpoints ----------

@router.get("", response_model=list[ServiceListItem])
def list_services(category_slug: str | None = None, db: Session = Depends(get_db)):
    """Public service catalogue, optionally filtered by category."""
    query = db.query(Service).options(joinedload(Service.category)).filter(Service.is_active.is_(True))
    if category_slug:
        query = query.join(ServiceCategory).filter(ServiceCategory.slug == category_slug)
    return query.order_by(Service.display_order).all()


@router.get("/{slug}", response_model=ServiceDetail)
def get_service_detail(slug: str, db: Session = Depends(get_db)):
    service = (
        db.query(Service)
        .options(
            joinedload(Service.category),
            joinedload(Service.packages),
            joinedload(Service.features),
            joinedload(Service.technologies),
        )
        .filter(Service.slug == slug, Service.is_active.is_(True))
        .first()
    )
    if not service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    return service


# ---------- Admin endpoints ----------

@router.post("/admin", response_model=ServiceDetail, dependencies=[Depends(require_permission("services.manage"))])
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    if db.query(Service).filter(Service.slug == payload.slug).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug already exists")
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.put("/admin/{service_id}", response_model=ServiceDetail, dependencies=[Depends(require_permission("services.manage"))])
def update_service(service_id: int, payload: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service


@router.delete("/admin/{service_id}", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[Depends(require_permission("services.manage"))])
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    db.delete(service)
    db.commit()
