from pydantic import BaseModel, Field


class SeoMetaOut(BaseModel):
    id: int
    path: str
    title: str | None
    description: str | None
    canonical_url: str | None
    og_image_url: str | None
    model_config = {"from_attributes": True}


class SeoMetaIn(BaseModel):
    path: str = Field(min_length=1, max_length=300)
    title: str | None = None
    description: str | None = None
    canonical_url: str | None = None
    og_image_url: str | None = None
    schema_json: dict | None = None


class RedirectOut(BaseModel):
    id: int
    from_path: str
    to_path: str
    status_code: int
    is_active: bool
    model_config = {"from_attributes": True}


class RedirectIn(BaseModel):
    from_path: str = Field(min_length=1, max_length=300)
    to_path: str = Field(min_length=1, max_length=300)
    status_code: int = 301
    is_active: bool = True
