import time

from src.services.vector_store import (
    MongoVectorStore,
)


class RAGRetriever:

    def __init__(self):
        self.store = MongoVectorStore()

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        return await self.store.search(
            query=query,
            limit=top_k,
        )

    async def format_context(
        self,
        query: str,
    ) -> str:

        documents = await self.retrieve(
            query
        )

        if not documents:
            return (
                "No relevant company documentation "
                "was found."
            )

        sections = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            sections.append(
                f"""
SOURCE {index}
Title: {document.get("title")}
Source: {document.get("source")}
Similarity: {document.get("score", 0):.3f}

{document.get("content")}
"""
            )

        return "\n".join(sections)
