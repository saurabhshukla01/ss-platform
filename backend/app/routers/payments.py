from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.models.identity import Admin
from app.models.commerce import Coupon, Order, Payment
from app.schemas.commerce import (
    CouponOut, CouponCreate, CouponUpdate, OrderOut, PaymentOut, OrderStatusUpdate,
)

router = APIRouter(prefix="/payments", tags=["Payments"])


# ---------- Coupons ----------

@router.get("/coupons", response_model=list[CouponOut])
def list_active_coupons(db: Session = Depends(get_db)):
    """Public: used to validate a coupon code at checkout."""
    return db.query(Coupon).filter(Coupon.is_active.is_(True)).all()


@router.get("/coupons/admin", response_model=list[CouponOut], dependencies=[Depends(require_permission("payments.manage"))])
def list_coupons_admin(db: Session = Depends(get_db)):
    return db.query(Coupon).order_by(Coupon.created_at.desc()).all()


@router.post("/coupons/admin", response_model=CouponOut, dependencies=[Depends(require_permission("payments.manage"))])
def create_coupon(payload: CouponCreate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    if db.query(Coupon).filter(Coupon.code == payload.code).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Coupon code already exists")
    coupon = Coupon(**payload.model_dump())
    db.add(coupon)
    db.flush()
    log_action(db, admin.id, "create", "coupons", coupon.id, new_value=payload.model_dump(mode="json"), request=request)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.put("/coupons/admin/{coupon_id}", response_model=CouponOut, dependencies=[Depends(require_permission("payments.manage"))])
def update_coupon(coupon_id: int, payload: CouponUpdate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Coupon not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(coupon, field, value)
    log_action(db, admin.id, "update", "coupons", coupon_id, new_value=payload.model_dump(exclude_unset=True, mode="json"), request=request)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.delete("/coupons/admin/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[Depends(require_permission("payments.manage"))])
def delete_coupon(coupon_id: int, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Coupon not found")
    log_action(db, admin.id, "delete", "coupons", coupon_id, old_value={"code": coupon.code}, request=request)
    db.delete(coupon)
    db.commit()


# ---------- Orders & Payments ----------

@router.get("/orders/admin", response_model=list[OrderOut], dependencies=[Depends(require_permission("payments.manage"))])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).all()


@router.patch("/orders/admin/{order_id}/status", response_model=OrderOut,
              dependencies=[Depends(require_permission("payments.manage"))])
def update_order_status(order_id: int, payload: OrderStatusUpdate, request: Request, db: Session = Depends(get_db),
                         admin: Admin = Depends(get_current_admin)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    old_status = order.status
    order.status = payload.status
    log_action(db, admin.id, "update_status", "orders", order_id,
               old_value={"status": old_status.value}, new_value={"status": payload.status.value}, request=request)
    db.commit()
    db.refresh(order)
    return order


@router.get("/transactions/admin", response_model=list[PaymentOut], dependencies=[Depends(require_permission("payments.manage"))])
def list_payments(db: Session = Depends(get_db)):
    """Note: only gateway references are stored — never card/bank details (see Payment model)."""
    return db.query(Payment).order_by(Payment.created_at.desc()).all()
