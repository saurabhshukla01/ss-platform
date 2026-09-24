from pydantic import BaseModel, Field, ConfigDict

class SeoMetaOut(BaseModel):
    id: int
    path: str
    title: str | None
    description: str | None
    canonical_url: str | None
    og_image_url: str | None
    schema_data: dict | None = Field(default=None, alias="schema_json")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class SeoMetaIn(BaseModel):
    path: str = Field(min_length=1, max_length=300)

    title: str | None = None
    description: str | None = None
    canonical_url: str | None = None
    og_image_url: str | None = None

    # Keep API field name "schema_json"
    # but avoid conflict with Pydantic BaseModel.schema_json()
    schema_data: dict | None = Field(
        default=None,
        alias="schema_json",
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )


class RedirectOut(BaseModel):
    id: int
    from_path: str
    to_path: str
    status_code: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RedirectIn(BaseModel):
    from_path: str = Field(min_length=1, max_length=300)
    to_path: str = Field(min_length=1, max_length=300)
    status_code: int = 301
    is_active: bool = True
