from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metric_point import MetricPoint
from app.models.source import Source
from app.repositories.metric_repo import MetricRepository
from app.repositories.source_repo import SourceRepository
from app.schemas.metric_point import MetricPointBatchIn


class IngestService:
    def __init__(
        self,
        metric_repo: MetricRepository,
        source_repo: SourceRepository,
        session: AsyncSession,
    ):
        self._metric_repo = metric_repo
        self._source_repo = source_repo
        self._session = session

    async def _load_source(self, source_id: int) -> Source:
        source = await self._source_repo.get(source_id)
        if source is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source {source_id} not found",
            )
        return source

    async def ingest(self, source_id: int, batch: MetricPointBatchIn) -> int:
        source = await self._load_source(source_id)
        if not source.enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Source {source_id} is disabled",
            )

        now = datetime.now(UTC)
        points = [
            MetricPoint(
                source_id=source_id,
                name=p.name,
                value=p.value,
                unit=p.unit,
                tags=p.tags,
                ts=p.ts or now,
            )
            for p in batch.points
        ]

        await self._metric_repo.bulk_insert(points)
        await self._session.commit()
        return len(points)

    async def query(
        self,
        source_id: int,
        name: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> list[MetricPoint]:
        await self._load_source(source_id)
        return await self._metric_repo.query(
            source_id=source_id,
            name=name,
            start=start,
            end=end,
            limit=limit,
        )
