from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MetricPoint


class MetricRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def bulk_insert(self, points: list[MetricPoint]) -> None:
        self._db.add_all(points)
        await self._db.flush()

    async def query(
        self,
        source_id: int,
        name: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> list[MetricPoint]:
        stmt = select(MetricPoint).where(MetricPoint.source_id == source_id)

        if name is not None:
            stmt = stmt.where(MetricPoint.name == name)
        if start is not None:
            stmt = stmt.where(MetricPoint.ts >= start)
        if end is not None:
            stmt = stmt.where(MetricPoint.ts <= end)

        stmt = stmt.order_by(MetricPoint.ts.desc()).limit(limit)

        result = await self._db.execute(stmt)
        return list(result.scalars().all())
