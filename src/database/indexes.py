"""MongoDB indexes management."""

from pymongo import ASCENDING, TEXT

from src.database.db import collection_name
from src.logger import logging

logger = logging.getLogger(__name__)


def create_indexes() -> None:
    """Create indexes for the quotes collection."""
    try:
        # Simple indexes
        collection_name.create_index([("author", ASCENDING)], name="author_index")
        collection_name.create_index([("tags", ASCENDING)], name="tags_index")
        collection_name.create_index([("time_added", ASCENDING)], name="time_added_index")

        # Author and tags index
        collection_name.create_index([("author", ASCENDING), ("tags", ASCENDING)], name="author_tags_compound_index")

        # Author, quote and tags index
        collection_name.create_index([("author", TEXT), ("quote", TEXT), ("tags", TEXT)], name="text_search_index")

        logger.info("All indexes created successfully")

        # List indexes
        indexes = list(collection_name.list_indexes())
        for index in indexes:
            logger.info(f"Index: {index}")

    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        raise


def ensure_indexes() -> None:
    """Ensure indexes exist, create if they don't."""
    try:
        existing_indexes = [index["name"] for index in collection_name.list_indexes()]

        required_indexes = ["author_index", "tags_index", "time_added_index", "author_tags_compound_index"]

        for index_name in required_indexes:
            if index_name not in existing_indexes:
                logger.info(f"Creating missing index: {index_name}")
                create_indexes()
                break
        else:
            logger.info("All required indexes already exist")

    except Exception as e:
        logger.error(f"Error checking indexes: {e}")
