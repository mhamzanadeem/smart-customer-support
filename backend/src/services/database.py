import time
from functools import lru_cache

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from src.config import get_settings


@lru_cache
def get_client() -> MongoClient:
    settings = get_settings()

    return MongoClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=settings.mongo_timeout * 1000,
        connectTimeoutMS=settings.mongo_timeout * 1000,
        socketTimeoutMS=settings.mongo_timeout * 1000,
    )


def get_database():
    settings = get_settings()
    return get_client()[settings.mongodb_database]


def get_collection(name: str):
    return get_database()[name]


def ping_database() -> bool:
    try:
        get_client().admin.command("ping")
        return True
    except Exception:
        return False


def check_mongodb_health() -> dict:
    try:
        t0 = time.perf_counter()
        client = get_client()
        client.admin.command("ping")
        elapsed = time.perf_counter() - t0
        return {
            "status": "connected",
            "latency_ms": round(elapsed * 1000, 1),
        }
    except ConnectionFailure as exc:
        return {
            "status": "connection_failed",
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
        }
