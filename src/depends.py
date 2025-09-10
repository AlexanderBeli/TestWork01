"""FastAPI DI."""

from pymongo.database import Database

from database.db import db


def get_db() -> Database:
    """Returns the MongoDB database instance."""
    return db
