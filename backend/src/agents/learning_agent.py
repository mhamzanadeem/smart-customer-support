from datetime import datetime, timezone

from src.services.database import (
    get_collection,
)


def record_interaction(
    thread_id: str,
    query: str,
    answer: str,
    category: str,
    agent: str,
):

    collection = get_collection(
        "conversations"
    )

    collection.insert_one(
        {
            "thread_id": thread_id,
            "query": query,
            "answer": answer,
            "category": category,
            "agent": agent,
            "created_at": datetime.now(
                timezone.utc
            ),
        }
    )