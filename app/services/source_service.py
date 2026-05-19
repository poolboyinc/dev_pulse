from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source import Source
from app.repositories.source_repo import SourceRepository
from app.schemas.source import SourceCreate, SourceUpdate


class SourceService:
    def __init__(self, repo: SourceRepository, session: AsyncSession):
        self._repo = repo
        self._session = session

    async def list(self, skip: int = 0, limit: int = 100) -> list[Source]:
        return await self._repo.list(skip=skip, limit=limit)

    async def get(self, source_id: int) -> Source:
        source = await self._repo.get(source_id)
        if source is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source {source_id} not found",
            )
        return source

    async def create(self, data: SourceCreate) -> Source:
        if await self._repo.get_by_name(data.name) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Source with name '{data.name}' already exists",
            )
        source = Source(**data.model_dump())
        source = await self._repo.add(source)
        await self._session.commit()
        await self._session.refresh(source)
        return source

    async def update(self, source_id: int, patch: SourceUpdate) -> Source:
        source = await self.get(source_id)
        patch_dict = patch.model_dump(exclude_unset=True)

        new_name = patch_dict.get("name")
        if new_name is not None and new_name != source.name:
            if await self._repo.get_by_name(new_name) is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Source with name '{new_name}' already exists",
                )

        source = await self._repo.update(source, patch_dict)
        await self._session.commit()
        await self._session.refresh(source)
        return source

    async def delete(self, source_id: int) -> None:
        source = await self.get(source_id)
        await self._repo.delete(source)
        await self._session.commit()
