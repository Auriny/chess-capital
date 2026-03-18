from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from anyio import Path
from fastapi import FastAPI

from config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    folder = Path(settings.PGN_FILES_FOLDER)
    if not await folder.exists():
        await folder.mkdir()
    yield
