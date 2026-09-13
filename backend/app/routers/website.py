from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.crud.generic import build_crud_router
from app.models.brand import Project, TeamMember, Testimonial, Setting
from app.models.content import Banner, Announcement, Offer
from app.schemas.website import (
    BannerOut, BannerCreate, BannerUpdate,
    AnnouncementOut, AnnouncementCreate, AnnouncementUpdate,
    OfferOut, OfferCreate, OfferUpdate,
    ProjectOut, ProjectCreate, ProjectUpdate,
    TeamMemberOut, TeamMemberCreate, TeamMemberUpdate,
    TestimonialOut, TestimonialCreate, TestimonialUpdate,
    ThemeSettings, ThemeSettingsUpdate,
)

# ============================================================
# Simple content CRUD — one router per model, all following the
# same {prefix}[/admin[/{id}]] convention (see app/crud/generic.py)
# ============================================================

banners_router = build_crud_router(
    model=Banner, prefix="/website/banners", tag="Website Banners",
    permission="content.manage",
    out_schema=BannerOut, create_schema=BannerCreate, update_schema=BannerUpdate,
)

announcements_router = build_crud_router(
    model=Announcement, prefix="/website/announcements", tag="Website Announcements",
    permission="content.manage",
    out_schema=AnnouncementOut, create_schema=AnnouncementCreate, update_schema=AnnouncementUpdate,
    order_field="id",
)

offers_router = build_crud_router(
    model=Offer, prefix="/website/offers", tag="Website Offers",
    permission="content.manage",
    out_schema=OfferOut, create_schema=OfferCreate, update_schema=OfferUpdate,
    order_field="id",
)

projects_router = build_crud_router(
    model=Project, prefix="/website/projects", tag="Website Projects",
    permission="content.manage",
    out_schema=ProjectOut, create_schema=ProjectCreate, update_schema=ProjectUpdate,
)

team_router = build_crud_router(
    model=TeamMember, prefix="/website/team", tag="Website Team",
    permission="content.manage",
    out_schema=TeamMemberOut, create_schema=TeamMemberCreate, update_schema=TeamMemberUpdate,
)

testimonials_router = build_crud_router(
    model=Testimonial, prefix="/website/testimonials", tag="Website Testimonials",
    permission="content.manage",
    out_schema=TestimonialOut, create_schema=TestimonialCreate, update_schema=TestimonialUpdate,
)


# ============================================================
# Theme / branding settings
#
# Stored as rows in the generic key-value `settings` table
# (group="theme"). Exposed as a single flat object so the public
# site can fetch it once and the Admin Panel can edit it as a form.
# ============================================================

settings_router = APIRouter(prefix="/settings", tags=["Site Settings"])

THEME_GROUP = "theme"


@settings_router.get("/theme", response_model=ThemeSettings)
def get_theme(db: Session = Depends(get_db)):
    """Public endpoint — the website reads this on load to apply admin-managed colors."""
    defaults = ThemeSettings()
    rows = db.query(Setting).filter(Setting.group == THEME_GROUP).all()
    values = {row.key: row.value for row in rows if row.value is not None}
    return defaults.model_copy(update=values)


@settings_router.put(
    "/theme",
    response_model=ThemeSettings,
    dependencies=[Depends(require_permission("settings.manage"))],
)
def update_theme(payload: ThemeSettingsUpdate, db: Session = Depends(get_db)):
    """Admin endpoint — updates only the fields provided."""
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        row = (
            db.query(Setting)
            .filter(Setting.group == THEME_GROUP, Setting.key == key)
            .first()
        )
        if row:
            row.value = str(value)
        else:
            db.add(Setting(group=THEME_GROUP, key=key, value=str(value)))
    db.commit()
    return get_theme(db)
