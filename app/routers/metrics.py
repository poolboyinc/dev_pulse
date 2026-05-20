from datetime import datetime

from fastapi import APIRouter, Depends, status

from app.deps import get_ingest_service
from app.schemas.metric_point import MetricPointBatchIn, MetricPointRead
from app.services.ingest_service import IngestService

router = APIRouter(prefix="/sources/{source_id}/metrics", tags=["metrics"])


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def ingest_metrics(
    source_id: int,
    batch: MetricPointBatchIn,
    service: IngestService = Depends(get_ingest_service),
):
    count = await service.ingest(source_id, batch)
    return {"ingested": count}


@router.get("/", response_model=list[MetricPointRead])
async def query_metrics(
    source_id: int,
    name: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = 100,
    service: IngestService = Depends(get_ingest_service),
):
    return await service.query(
        source_id=source_id,
        name=name,
        start=start,
        end=end,
        limit=limit,
    )
