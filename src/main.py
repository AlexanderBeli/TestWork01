"""Application Entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse, RedirectResponse

from database.db import client
from logger import logging, setup_logging
from routers.router import router
from src.database.indexes import ensure_indexes

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan."""
    try:
        client.admin.command("ping")
        logging.info("✅ MongoDB connection verified")
        ensure_indexes()
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
    yield
    client.close()
    logging.info("🔴 MongoDB disconnected")


app = FastAPI(title="Quotes Scraper API", version="1.0.0", lifespan=lifespan)

app.include_router(router)


@app.get("/", include_in_schema=False)
async def home() -> RedirectResponse:
    """Redirect home to docs."""
    return RedirectResponse("/docs")


@app.get("/healthcheck", include_in_schema=False)
@app.head("/healthcheck", include_in_schema=False)
async def healthcheck() -> PlainTextResponse:
    """Healthcheck endpoint."""
    return PlainTextResponse("OK", status_code=status.HTTP_200_OK)
