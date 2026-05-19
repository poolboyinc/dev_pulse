from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source import Source


class SourceRepository:
    def __init__(self, session: AsyncSession):
        self._db = session

    async def list(self, skip: int = 0, limit: int = 100) -> list[Source]:
        stmt = select(Source).offset(skip).limit(limit)
        result = await self._db.execute(stmt)
        return list(result.scalars().all())

    async def get(self, source_id: int) -> Source | None:
        stmt = select(Source).where(Source.id == source_id)
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Source | None:
        stmt = select(Source).where(Source.name == name)
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, source: Source) -> Source:
        self._db.add(source)
        await self._db.flush()
        return source

    async def update(self, source: Source, patch: dict) -> Source:
        for key, value in patch.items():
            setattr(source, key, value)
        await self._db.flush()
        return source

    async def delete(self, source: Source) -> None:
        await self._db.delete(source)
