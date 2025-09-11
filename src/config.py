"""Application Config."""

import os
from typing import Any

from pydantic_settings import BaseSettings

TESTING_FLAG = os.getenv("TESTING_FLAG", "").lower() in ("1", "true", "yes", "on")


class Settings(BaseSettings):
    """Settings."""

    REDIS_HOST: str = "redis" if TESTING_FLAG else os.getenv("REDIS_HOST")
    REDIS_PORT: str = "6379" if TESTING_FLAG else os.getenv("REDIS_PORT")
    REDIS_DB: str = "0" if TESTING_FLAG else os.getenv("REDIS_DB")
    REDIS_PASSWORD: str = "" if TESTING_FLAG else os.getenv("REDIS_PASSWORD")
    REDIS_SSL: bool = not TESTING_FLAG

    MONGODB_URL: str = "mongodb://mongodb:27017" if TESTING_FLAG else os.getenv("MONGODB_URL")
    MONGODB_NAME: str = "testdb" if TESTING_FLAG else os.getenv("MONGODB_NAME")

    CELERY_BROKER_URL: str = "redis://redis:6379/0" if TESTING_FLAG else os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0" if TESTING_FLAG else os.getenv("CELERY_RESULT_BACKEND")

    ENVIRONMENT: str = "development" if TESTING_FLAG else os.getenv("ENVIRONMENT")

    # Logging settings
    LOG_LEVEL: str = "INFO" if TESTING_FLAG else os.getenv("LOG_LEVEL", "INFO")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if self.REDIS_SSL:
            protocol = "rediss"
            password_part = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
            self.CELERY_BROKER_URL = f"{protocol}://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

        if self.REDIS_SSL:
            self.CELERY_RESULT_BACKEND = self.CELERY_BROKER_URL


settings = Settings()
