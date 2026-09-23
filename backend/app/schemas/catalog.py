from pydantic import BaseModel, Field


class ServiceCategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    icon: str | None = None
    display_order: int
    is_active: bool

    model_config = {"from_attributes": True}


class ServiceCategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=140)
    description: str | None = None
    icon: str | None = None
    display_order: int = 0


class ServiceCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    icon: str | None = None
    display_order: int | None = None
    is_active: bool | None = None
