from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission, get_current_admin
from app.core.audit import log_action
from app.core.crud_factory import simple_crud_router
from app.models.identity import Admin
from app.models.content import Blog, BlogCategory, Faq
from app.schemas.content import (
    BlogOut, BlogDetail, BlogCreate, BlogUpdate, BlogCategoryOut, BlogCategoryIn, FaqOut, FaqIn,
)

router = APIRouter(prefix="/content", tags=["Content"])


# ---------- Blogs (dedicated: slug uniqueness + publish workflow) ----------

@router.get("/blogs", response_model=list[BlogOut])
def list_published_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).filter(Blog.is_published.is_(True)).order_by(Blog.published_at.desc()).all()


@router.get("/blogs/{slug}", response_model=BlogDetail)
def get_blog(slug: str, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.slug == slug, Blog.is_published.is_(True)).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Blog post not found")
    return blog


@router.get("/blogs/admin/all", response_model=list[BlogOut], dependencies=[Depends(require_permission("content.manage"))])
def list_all_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).order_by(Blog.created_at.desc()).all()


@router.post("/blogs/admin", response_model=BlogDetail, dependencies=[Depends(require_permission("content.manage"))])
def create_blog(payload: BlogCreate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    if db.query(Blog).filter(Blog.slug == payload.slug).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Slug already exists")
    data = payload.model_dump()
    published_at = datetime.utcnow() if data.get("is_published") else None
    blog = Blog(**data, admin_id=admin.id, published_at=published_at)
    db.add(blog)
    db.flush()
    log_action(db, admin.id, "create", "blogs", blog.id, new_value={"title": payload.title}, request=request)
    db.commit()
    db.refresh(blog)
    return blog


@router.put("/blogs/admin/{blog_id}", response_model=BlogDetail, dependencies=[Depends(require_permission("content.manage"))])
def update_blog(blog_id: int, payload: BlogUpdate, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Blog post not found")
    data = payload.model_dump(exclude_unset=True)
    if data.get("is_published") and not blog.published_at:
        blog.published_at = datetime.utcnow()
    for field, value in data.items():
        setattr(blog, field, value)
    log_action(db, admin.id, "update", "blogs", blog_id, new_value=data, request=request)
    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/blogs/admin/{blog_id}", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[Depends(require_permission("content.manage"))])
def delete_blog(blog_id: int, request: Request, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Blog post not found")
    log_action(db, admin.id, "delete", "blogs", blog_id, old_value={"title": blog.title}, request=request)
    db.delete(blog)
    db.commit()


# ---------- Blog categories & FAQs (simple content, via shared factory) ----------

router.include_router(simple_crud_router("blog-categories", BlogCategory, BlogCategoryOut, BlogCategoryIn, "content.manage", public_filter=False))
router.include_router(simple_crud_router("faqs", Faq, FaqOut, FaqIn, "content.manage"))
