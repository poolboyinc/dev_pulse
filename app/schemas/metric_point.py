from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MetricPointIn(BaseModel):
    name: str
    value: float
    unit: str | None = None
    tags: dict[str, str] | None = None
    ts: datetime | None = None


class MetricPointBatchIn(BaseModel):
    points: list[MetricPointIn] = Field(min_length=1, max_length=1000)


class MetricPointRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    name: str
    value: float
    unit: str | None
    tags: dict[str, str] | None
    ts: datetime
