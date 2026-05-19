from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SourceBase(BaseModel):
    name: str
    source_type: str
    endpoint: str | None = None
    poll_interval_seconds: int = 60
    enabled: bool = True


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: str | None = None
    source_type: str | None = None
    endpoint: str | None = None
    poll_interval_seconds: int | None = None
    enabled: bool | None = None


class SourceRead(SourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
