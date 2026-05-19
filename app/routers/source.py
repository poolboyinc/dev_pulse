from fastapi import APIRouter, Depends, status

from app.deps import get_source_service
from app.schemas.source import SourceCreate, SourceRead, SourceUpdate
from app.services.source_service import SourceService

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("/", response_model=SourceRead, status_code=status.HTTP_201_CREATED)
async def create_source(
    data: SourceCreate,
    service: SourceService = Depends(get_source_service),
):
    return await service.create(data)


@router.get("/", response_model=list[SourceRead])
async def list_sources(
    skip: int = 0,
    limit: int = 100,
    service: SourceService = Depends(get_source_service),
):
    return await service.list(skip=skip, limit=limit)


@router.get("/{source_id}", response_model=SourceRead)
async def get_source(
    source_id: int,
    service: SourceService = Depends(get_source_service),
):
    return await service.get(source_id)


@router.patch("/{source_id}", response_model=SourceRead)
async def update_source(
    source_id: int,
    patch: SourceUpdate,
    service: SourceService = Depends(get_source_service),
):
    return await service.update(source_id, patch)


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: int,
    service: SourceService = Depends(get_source_service),
):
    await service.delete(source_id)
