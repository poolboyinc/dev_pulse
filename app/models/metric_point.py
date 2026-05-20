from datetime import datetime

from sqlalchemy import ForeignKey, func, Index
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class MetricPoint(Base):
    __tablename__ = "metric_point"
    __table_args__ = (Index("ix_metric_points_source_name_ts", "source_id", "name", "ts"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(index=True)
    value: Mapped[float]
    unit: Mapped[str | None]
    tags: Mapped[dict | None] = mapped_column(JSONB)
    ts: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)