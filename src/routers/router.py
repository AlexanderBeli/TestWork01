"""Router."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from redis.exceptions import ConnectionError as RedisConnectionError

from depends import get_db
from logger import logging

# from src.database.db import collection_name
from src.proj.tasks import start_parsing_task

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/parse_quotes_task", tags=["Parsing"])
async def parse_quotes_task(_db: Database = Depends(get_db)) -> dict[str, str]:  # noqa: B008
    "Start quotes parsing task"
    try:
        # Call the Celery task and get the task ID
        task = start_parsing_task.delay()
        logger.info(f"Task with ID {task.id} started.")
        return {"task_id": task.id}
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable: Database connection failed."
        ) from e
    except RedisConnectionError as e:
        logger.error(f"Failed to start Celery task (Broker connection failed): {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service Unavailable: Celery Broker connection failed.",
        ) from e
    except Exception as e:
        logger.error(f"Failed to start Celery task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error: Could not start task."
        ) from e


@router.get("/quotes", tags=["Searching"])
async def get_quotes(
    db: Database = Depends(get_db),
    author: Optional[str] = Query(None, description="Filter quotes by author name."),
    tag: Optional[str] = Query(None, description="Filter quotes by a specific tag."),
    # search: Optional[str] = Query(None, description="Full-text search in quotes, authors, and tags."),
    limit: int = Query(25, ge=1, le=100),
    skip: int = Query(0, ge=0),
) -> dict[str, str] | list:
    "Get quotes with filtering"
    try:
        filter_query = {}
        if author:
            filter_query["author"] = author.strip()
        if tag:
            filter_query["tags"] = tag.strip()

        # if search:
        #     filter_query["$text"] = {"$search": search}

        quotes_collection = db["quotes"]

        cursor = quotes_collection.find(filter_query)
        cursor = cursor.sort("time_added", -1).skip(skip).limit(limit)

        quotes = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            quotes.append(doc)

        if not quotes:
            return {"message": "No quotes found matching the criteria."}

        return quotes
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error: Failed to retrieve quotes.",
        ) from e
