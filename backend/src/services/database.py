from functools import lru_cache

from pymongo import MongoClient

from src.config import get_settings


@lru_cache
def get_client() -> MongoClient:
    settings = get_settings()

    return MongoClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=10000,
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