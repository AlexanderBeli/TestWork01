"""MongoDB indexes management."""

from pymongo import ASCENDING, TEXT

from src.database.db import collection_name
from src.logger import logging

logger = logging.getLogger(__name__)

REQUIRED_INDEXES = ["author_index", "tags_index", "time_added_index", "author_tags_compound_index", "text_search_index"]


async def create_indexes() -> None:
    """Create indexes for the quotes collection."""
    try:
        logger.info("Starting index creation process...")

        # Simple indexes
        await collection_name.create_index([("author", ASCENDING)], name="author_index")
        await collection_name.create_index([("tags", ASCENDING)], name="tags_index")
        await collection_name.create_index([("time_added", ASCENDING)], name="time_added_index")

        # Author and tags index
        await collection_name.create_index(
            [("author", ASCENDING), ("tags", ASCENDING)], name="author_tags_compound_index"
        )

        # Author, quote and tags index
        await collection_name.create_index(
            [("author", TEXT), ("quote", TEXT), ("tags", TEXT)], name="text_search_index"
        )

        logger.info("All indexes created successfully")

        # List indexes
        indexes = await collection_name.list_indexes()
        logger.info("Current indexes in the collection:")

        # indexes = await collection_name.list_indexes().to_list(length=None)
        async for index in indexes:
            logger.info(f"Index: {index.get('name', 'N/A')}")

    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        raise


async def ensure_indexes() -> None:
    """Ensure indexes exist, create if they don't."""
    try:
        # existing_indexes = [index["name"] async for index in await collection_name.list_indexes().to_list()]
        existing_indexes = []

        indexes_cursor = await collection_name.list_indexes()
        async for index in indexes_cursor:
            existing_indexes.append(index["name"])

        # required_indexes = ["author_index", "tags_index", "time_added_index", "author_tags_compound_index"]
        missing_index = False
        for index_name in REQUIRED_INDEXES:
            if index_name not in existing_indexes:
                logger.info(f"Creating missing index: {index_name}")
                missing_index = True
        if missing_index:
            logger.info("One or more required indexes are missing. Running full index creation...")
            await create_indexes()
        else:
            logger.info("All required indexes already exist")

    except Exception as e:
        logger.error(f"Error checking indexes: {e}")
        raise
