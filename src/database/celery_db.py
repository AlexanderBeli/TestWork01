"""Database connection for Celery."""

from pymongo import MongoClient

from config import settings

client = MongoClient(
    settings.MONGODB_URL, maxPoolSize=100, minPoolSize=10, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000
)

db = client[settings.MONGODB_NAME]

collection_name = db["quotes"]
