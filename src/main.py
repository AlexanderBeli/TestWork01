"""Application Entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.db import client
from logger import logging, setup_logging
from routers.router import router

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan."""
    try:
        client.admin.command("ping")
        logging.info("✅ MongoDB connection verified")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
    yield
    client.close()
    logging.info("🔴 MongoDB disconnected")


app = FastAPI(lifespan=lifespan)

app.include_router(router)
