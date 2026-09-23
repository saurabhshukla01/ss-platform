from datetime import datetime
from pydantic import BaseModel, Field


class BlogCategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    model_config = {"from_attributes": True}


class BlogCategoryIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slug: str = Field(min_length=1, max_length=140)


class BlogOut(BaseModel):
    id: int
    category_id: int | None
    title: str
    slug: str
    excerpt: str | None
    is_published: bool
    published_at: datetime | None
    created_at: datetime
    model_config = {"from_attributes": True}


class BlogDetail(BlogOut):
    content: str | None
    cover_image_url: str | None
    meta_title: str | None
    meta_description: str | None


class BlogCreate(BaseModel):
    category_id: int | None = None
    title: str = Field(min_length=2, max_length=250)
    slug: str = Field(min_length=2, max_length=270)
    excerpt: str | None = None
    content: str | None = None
    cover_image_url: str | None = None
    is_published: bool = False
    meta_title: str | None = None
    meta_description: str | None = None


class BlogUpdate(BaseModel):
    category_id: int | None = None
    title: str | None = None
    excerpt: str | None = None
    content: str | None = None
    cover_image_url: str | None = None
    is_published: bool | None = None
    meta_title: str | None = None
    meta_description: str | None = None


class FaqOut(BaseModel):
    id: int
    question: str
    answer: str
    service_id: int | None
    is_active: bool
    model_config = {"from_attributes": True}


class FaqIn(BaseModel):
    question: str = Field(min_length=2, max_length=300)
    answer: str
    service_id: int | None = None
    display_order: int = 0
    is_active: bool = True
