from pydantic import BaseModel, Field


class TechnologyOut(BaseModel):
    id: int
    name: str
    icon: str | None = None

    model_config = {"from_attributes": True}


class ServiceFeatureOut(BaseModel):
    id: int
    title: str
    display_order: int

    model_config = {"from_attributes": True}


class ServicePackageOut(BaseModel):
    id: int
    name: str
    price: float | None = None
    is_custom_quote: bool
    billing_interval: str
    description: str | None = None

    model_config = {"from_attributes": True}


class ServiceCategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    icon: str | None = None

    model_config = {"from_attributes": True}


class ServiceListItem(BaseModel):
    id: int
    name: str
    slug: str
    short_description: str | None = None
    starting_price: float | None = None
    is_custom_quote_only: bool
    category: ServiceCategoryOut

    model_config = {"from_attributes": True}


class ServiceDetail(ServiceListItem):
    long_description: str | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    packages: list[ServicePackageOut] = []
    features: list[ServiceFeatureOut] = []
    technologies: list[TechnologyOut] = []


class ServiceCreate(BaseModel):
    category_id: int
    name: str = Field(min_length=2, max_length=150)
    slug: str = Field(min_length=2, max_length=170)
    short_description: str | None = None
    long_description: str | None = None
    starting_price: float | None = None
    is_custom_quote_only: bool = False
    meta_title: str | None = None
    meta_description: str | None = None


class ServiceUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    short_description: str | None = None
    long_description: str | None = None
    starting_price: float | None = None
    is_custom_quote_only: bool | None = None
    is_active: bool | None = None
    meta_title: str | None = None
    meta_description: str | None = None
