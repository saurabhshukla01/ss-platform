from pydantic import BaseModel


class SettingOut(BaseModel):
    id: int
    group: str
    key: str
    value: str | None
    is_secret: bool
    model_config = {"from_attributes": True}


class SettingUpsert(BaseModel):
    group: str
    key: str
    value: str | None = None
    is_secret: bool = False
