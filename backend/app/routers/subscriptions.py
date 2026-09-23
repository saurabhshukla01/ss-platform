from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.models.identity import Admin
from app.models.subscriptions import (
    SubscriptionPlan, Subscription, CustomerWallet, TokenUsageLog,
)
from app.schemas.subscriptions import (
    PlanOut, PlanCreate, PlanUpdate, SubscriptionOut, SubscriptionCreate,
    SubscriptionStatusUpdate, WalletOut, TokenAdjustment,
)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


# ---------- Plans ----------

@router.get("/plans", response_model=list[PlanOut])
def list_plans(db: Session = Depends(get_db)):
    """Public: used by the Pricing page."""
    return db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active.is_(True)).all()


@router.post("/plans/admin", response_model=PlanOut, dependencies=[Depends(require_permission("subscriptions.manage"))])
def create_plan(payload: PlanCreate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    plan = SubscriptionPlan(**payload.model_dump())
    db.add(plan)
    db.flush()
    log_action(db, admin.id, "create", "subscription_plans", plan.id, new_value=payload.model_dump(mode="json"), request=request)
    db.commit()
    db.refresh(plan)
    return plan


@router.put("/plans/admin/{plan_id}", response_model=PlanOut, dependencies=[Depends(require_permission("subscriptions.manage"))])
def update_plan(plan_id: int, payload: PlanUpdate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Plan not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(plan, field, value)
    log_action(db, admin.id, "update", "subscription_plans", plan_id, new_value=payload.model_dump(exclude_unset=True, mode="json"), request=request)
    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/plans/admin/{plan_id}", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[Depends(require_permission("subscriptions.manage"))])
def delete_plan(plan_id: int, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Plan not found")
    log_action(db, admin.id, "delete", "subscription_plans", plan_id, old_value={"name": plan.name}, request=request)
    db.delete(plan)
    db.commit()


# ---------- Subscriptions ----------

@router.get("/admin", response_model=list[SubscriptionOut], dependencies=[Depends(require_permission("subscriptions.manage"))])
def list_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).order_by(Subscription.created_at.desc()).all()


@router.post("/admin", response_model=SubscriptionOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permission("subscriptions.manage"))])
def create_subscription(payload: SubscriptionCreate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    sub = Subscription(**payload.model_dump())
    db.add(sub)
    db.flush()
    log_action(db, admin.id, "create", "subscriptions", sub.id, new_value=payload.model_dump(mode="json"), request=request)
    db.commit()
    db.refresh(sub)
    return sub


@router.patch("/admin/{subscription_id}/status", response_model=SubscriptionOut,
              dependencies=[Depends(require_permission("subscriptions.manage"))])
def update_subscription_status(subscription_id: int, payload: SubscriptionStatusUpdate, request: Request,
                                db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not sub:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subscription not found")
    old_status = sub.status
    sub.status = payload.status
    log_action(db, admin.id, "update_status", "subscriptions", subscription_id,
               old_value={"status": old_status.value}, new_value={"status": payload.status.value}, request=request)
    db.commit()
    db.refresh(sub)
    return sub


# ---------- Wallets / Tokens ----------

@router.get("/wallets/{customer_id}", response_model=WalletOut, dependencies=[Depends(require_permission("subscriptions.manage"))])
def get_wallet(customer_id: int, db: Session = Depends(get_db)):
    wallet = db.query(CustomerWallet).filter(CustomerWallet.customer_id == customer_id).first()
    if not wallet:
        wallet = CustomerWallet(customer_id=customer_id, token_balance=0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


@router.post("/wallets/{customer_id}/adjust", response_model=WalletOut,
             dependencies=[Depends(require_permission("subscriptions.manage"))])
def adjust_wallet(customer_id: int, payload: TokenAdjustment, request: Request, db: Session = Depends(get_db),
                   admin: Admin = Depends(get_current_admin)):
    """Manually credit/debit a customer's token wallet, with a full audit trail (section 6)."""
    wallet = db.query(CustomerWallet).filter(CustomerWallet.customer_id == customer_id).first()
    if not wallet:
        wallet = CustomerWallet(customer_id=customer_id, token_balance=0)
        db.add(wallet)
        db.flush()

    wallet.token_balance += payload.change_amount
    db.add(TokenUsageLog(
        wallet_id=wallet.id, admin_id=admin.id, change_amount=payload.change_amount,
        reason=payload.reason, balance_after=wallet.token_balance,
    ))
    log_action(db, admin.id, "adjust", "customer_wallets", wallet.id,
               new_value={"change_amount": payload.change_amount, "balance_after": wallet.token_balance}, request=request)
    db.commit()
    db.refresh(wallet)
    return wallet
