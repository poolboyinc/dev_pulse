from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401 — ensure models register on Base.metadata
from app.db.base import Base
from app.db.session import engine
from app.routers.metrics import router as metrics_router
from app.routers.source import router as source_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="DevPulse API", lifespan=lifespan)
app.include_router(source_router)
app.include_router(metrics_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
