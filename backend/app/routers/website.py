from fastapi import APIRouter

from app.core.crud_factory import simple_crud_router
from app.models.content import Banner, Announcement, Offer
from app.models.brand import Project, TeamMember, Testimonial
from app.schemas.website import (
    BannerOut, BannerIn, AnnouncementOut, AnnouncementIn, OfferOut, OfferIn,
    ProjectOut, ProjectIn, TeamMemberOut, TeamMemberIn, TestimonialOut, TestimonialIn,
)

router = APIRouter(prefix="/website", tags=["Website"])

router.include_router(simple_crud_router("banners", Banner, BannerOut, BannerIn, "content.manage"))
router.include_router(simple_crud_router("announcements", Announcement, AnnouncementOut, AnnouncementIn, "content.manage"))
router.include_router(simple_crud_router("offers", Offer, OfferOut, OfferIn, "content.manage"))
router.include_router(simple_crud_router("projects", Project, ProjectOut, ProjectIn, "content.manage"))
router.include_router(simple_crud_router("team", TeamMember, TeamMemberOut, TeamMemberIn, "content.manage"))
router.include_router(simple_crud_router("testimonials", Testimonial, TestimonialOut, TestimonialIn, "content.manage"))
