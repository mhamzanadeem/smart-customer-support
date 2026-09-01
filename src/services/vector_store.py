import logging

from supabase import (
    create_client,
    Client,
)

from .config import get_settings
from .llm_service import (
    get_embeddings_client,
)


log = logging.getLogger(__name__)


class VectorStore:

    def __init__(self):

        settings = get_settings()

        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key,
        )

        self.embedding_client = (
            get_embeddings_client()
        )


    async def embed(
        self,
        text: str,
    ) -> list[float]:

        settings = get_settings()

        response = (
            await self.embedding_client
            .embeddings
            .create(
                model=settings.embedding_model,
                input=text,
            )
        )

        return response.data[0].embedding


    async def search(
        self,
        query: str,
        top_k: int | None = None,
    ):

        settings = get_settings()

        embedding = await self.embed(query)

        result = self.client.rpc(
            "match_documents",
            {
                "query_embedding": embedding,

                "match_threshold":
                    settings.similarity_threshold,

                "match_count":
                    top_k or settings.top_k,
            },
        ).execute()

        return result.data or []


    async def upsert_document(
        self,
        title: str,
        content: str,
        source: str = "manual",
    ):

        embedding = await self.embed(
            content
        )

        result = (
            self.client
            .table("documents")
            .insert(
                {
                    "title": title,
                    "content": content,
                    "source": source,
                    "embedding": embedding,
                }
            )
            .execute()
        )

        return result.data