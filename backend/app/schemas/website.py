from datetime import datetime
from pydantic import BaseModel, Field


class BannerOut(BaseModel):
    id: int
    title: str
    image_url: str | None
    link_url: str | None
    display_order: int
    is_active: bool
    model_config = {"from_attributes": True}


class BannerIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    image_url: str | None = None
    link_url: str | None = None
    display_order: int = 0
    is_active: bool = True


class AnnouncementOut(BaseModel):
    id: int
    message: str
    link_url: str | None
    is_active: bool
    model_config = {"from_attributes": True}


class AnnouncementIn(BaseModel):
    message: str = Field(min_length=1, max_length=300)
    link_url: str | None = None
    is_active: bool = True


class OfferOut(BaseModel):
    id: int
    title: str
    description: str | None
    discount_label: str | None
    is_active: bool
    model_config = {"from_attributes": True}


class OfferIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    service_id: int | None = None
    discount_label: str | None = None
    is_active: bool = True


class ProjectOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None
    tech_stack: str | None
    status: str
    is_featured: bool
    is_active: bool
    model_config = {"from_attributes": True}


class ProjectIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=220)
    summary: str | None = None
    description: str | None = None
    tech_stack: str | None = None
    cover_image_url: str | None = None
    live_url: str | None = None
    status: str = "completed"
    is_featured: bool = False


class TeamMemberOut(BaseModel):
    id: int
    full_name: str
    role_title: str | None
    photo_url: str | None
    is_active: bool
    model_config = {"from_attributes": True}


class TeamMemberIn(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    role_title: str | None = None
    bio: str | None = None
    photo_url: str | None = None
    display_order: int = 0


class TestimonialOut(BaseModel):
    id: int
    client_name: str
    client_company: str | None
    quote: str
    rating: int | None
    is_active: bool
    model_config = {"from_attributes": True}


class TestimonialIn(BaseModel):
    client_name: str = Field(min_length=1, max_length=150)
    client_company: str | None = None
    photo_url: str | None = None
    quote: str
    rating: int | None = None
