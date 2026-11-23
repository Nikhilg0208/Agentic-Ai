from app.config import settings
import redis
from pymongo import MongoClient
from qdrant_client import QdrantClient

def get_redis_client() -> redis.Redis:
    """Returns a Redis client instance."""
    return redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_mongo_client() -> MongoClient:
    """Returns a MongoDB client instance."""
    return MongoClient(settings.MONGODB_URL)

def get_qdrant_client() -> QdrantClient:
    """Returns a Qdrant client instance."""
    return QdrantClient(url=settings.QDRANT_URL, check_compatibility=False)
