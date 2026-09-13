from datetime import datetime

from pydantic import BaseModel, Field


# ============================================================
# Banner
# ============================================================

class BannerOut(BaseModel):
    id: int
    title: str
    image_url: str | None = None
    link_url: str | None = None
    display_order: int
    is_active: bool

    model_config = {"from_attributes": True}


class BannerCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    image_url: str | None = None
    link_url: str | None = None
    display_order: int = 0
    is_active: bool = True


class BannerUpdate(BaseModel):
    title: str | None = None
    image_url: str | None = None
    link_url: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


# ============================================================
# Announcement
# ============================================================

class AnnouncementOut(BaseModel):
    id: int
    message: str
    link_url: str | None = None
    is_active: bool

    model_config = {"from_attributes": True}


class AnnouncementCreate(BaseModel):
    message: str = Field(min_length=1, max_length=300)
    link_url: str | None = None
    is_active: bool = True


class AnnouncementUpdate(BaseModel):
    message: str | None = None
    link_url: str | None = None
    is_active: bool | None = None


# ============================================================
# Offer
# ============================================================

class OfferOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    discount_label: str | None = None
    is_active: bool

    model_config = {"from_attributes": True}


class OfferCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    discount_label: str | None = None
    is_active: bool = True


class OfferUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    discount_label: str | None = None
    is_active: bool | None = None


# ============================================================
# Project
# ============================================================

class ProjectOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None = None
    tech_stack: str | None = None
    live_url: str | None = None
    status: str
    is_featured: bool
    is_active: bool
    display_order: int

    model_config = {"from_attributes": True}


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=220)
    summary: str | None = None
    tech_stack: str | None = None
    live_url: str | None = None
    status: str = "completed"
    is_featured: bool = False
    is_active: bool = True
    display_order: int = 0


class ProjectUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    summary: str | None = None
    tech_stack: str | None = None
    live_url: str | None = None
    status: str | None = None
    is_featured: bool | None = None
    is_active: bool | None = None
    display_order: int | None = None


# ============================================================
# Team member
# ============================================================

class TeamMemberOut(BaseModel):
    id: int
    full_name: str
    role_title: str | None = None
    bio: str | None = None
    photo_url: str | None = None
    display_order: int
    is_active: bool

    model_config = {"from_attributes": True}


class TeamMemberCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    role_title: str | None = None
    bio: str | None = None
    photo_url: str | None = None
    display_order: int = 0
    is_active: bool = True


class TeamMemberUpdate(BaseModel):
    full_name: str | None = None
    role_title: str | None = None
    bio: str | None = None
    photo_url: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


# ============================================================
# Testimonial
# ============================================================

class TestimonialOut(BaseModel):
    id: int
    client_name: str
    client_company: str | None = None
    quote: str
    rating: int | None = None
    is_active: bool
    display_order: int

    model_config = {"from_attributes": True}


class TestimonialCreate(BaseModel):
    client_name: str = Field(min_length=1, max_length=150)
    client_company: str | None = None
    quote: str = Field(min_length=1)
    rating: int | None = None
    is_active: bool = True
    display_order: int = 0


class TestimonialUpdate(BaseModel):
    client_name: str | None = None
    client_company: str | None = None
    quote: str | None = None
    rating: int | None = None
    is_active: bool | None = None
    display_order: int | None = None


# ============================================================
# Theme settings (site branding / default look)
# ============================================================

class ThemeSettings(BaseModel):
    site_name: str = "Saurabh Shukla."
    tagline: str = "Build. Automate. Grow."
    primary_color: str = "#3B82F6"       # 'electric' — buttons, links, accents
    primary_dark_color: str = "#1D4ED8"  # 'electricdim' — hover state for primary
    accent_color: str = "#22D3EE"        # 'cyan' — secondary accent / highlights


class ThemeSettingsUpdate(BaseModel):
    site_name: str | None = None
    tagline: str | None = None
    primary_color: str | None = None
    primary_dark_color: str | None = None
    accent_color: str | None = None
