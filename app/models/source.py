from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    source_type: Mapped[str]
    endpoint: Mapped[str | None]
    poll_interval_seconds: Mapped[int] = mapped_column(default=60)
    enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    metric_points: Mapped[list["MetricPoint"]] = relationship(back_populates="source", cascade="all, delete-orphan")
