import time
from datetime import datetime, timezone

from src.config import get_settings
from src.rag.embeddings import EmbeddingService
from src.services.database import get_collection


class MongoVectorStore:

    def __init__(self):
        self.settings = get_settings()
        self.collection = get_collection(
            "knowledge_documents"
        )
        self.embeddings = EmbeddingService()

    async def add_document(
        self,
        title: str,
        content: str,
        source: str,
    ):

        embedding = await self.embeddings.embed(
            content
        )

        document = {
            "title": title,
            "content": content,
            "source": source,
            "embedding": embedding,
            "created_at": datetime.now(
                timezone.utc
            ),
        }

        result = self.collection.insert_one(
            document
        )

        return str(result.inserted_id)

    async def search(
        self,
        query: str,
        limit: int | None = None,
    ) -> list[dict]:

        _log(f"Starting embedding for vector search")
        t0 = time.perf_counter()
        embedding = await self.embeddings.embed(query)
        elapsed = time.perf_counter() - t0
        _log(f"Embedding done ({elapsed:.2f}s)")

        limit = limit or self.settings.rag_top_k

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "knowledge_vector_index",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": max(
                        limit * 10,
                        50,
                    ),
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "title": 1,
                    "content": 1,
                    "source": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    },
                }
            },
        ]

        _log(f"Starting MongoDB vector search (limit={limit})")
        t1 = time.perf_counter()

        try:
            results = list(
                self.collection.aggregate(
                    pipeline
                )
            )
            elapsed = time.perf_counter() - t1
            _log(f"MongoDB search done: {len(results)} raw results ({elapsed:.2f}s)")
        except Exception as exc:
            elapsed = time.perf_counter() - t1
            _log(f"MongoDB search FAILED ({elapsed:.2f}s): {exc}")
            raise

        filtered = [
            result
            for result in results
            if result.get("score", 0)
            >= self.settings.rag_similarity_threshold
        ]

        _log(f"After threshold filter: {len(filtered)} docs (threshold={self.settings.rag_similarity_threshold})")

        return filtered


def _log(msg: str):
    print(f"[VECTOR_STORE] {msg}")
