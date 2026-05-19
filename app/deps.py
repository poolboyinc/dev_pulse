from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.source_repo import SourceRepository
from app.services.source_service import SourceService


def get_source_repo(
    session: AsyncSession = Depends(get_db),
) -> SourceRepository:
    return SourceRepository(session)


def get_source_service(
    session: AsyncSession = Depends(get_db),
    repo: SourceRepository = Depends(get_source_repo),
) -> SourceService:
    return SourceService(repo, session)
