"""FastAPI DI."""

from typing import AsyncGenerator

from pymongo.database import Database

from database.db import db


async def get_db() -> AsyncGenerator[Database, None]:
    """Returns the MongoDB database instance."""
    try:
        yield db
    finally:
        pass
