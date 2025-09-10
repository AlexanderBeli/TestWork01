"""Database models."""

from datetime import datetime

from pydantic import BaseModel


class Quote(BaseModel):
    author: str
    quote: str
    tags: list[str]
    time_added: datetime
