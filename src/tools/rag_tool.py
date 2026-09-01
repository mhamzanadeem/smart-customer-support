from agents import function_tool

from ..services.vector_store import (
    VectorStore,
)


_store = VectorStore()


@function_tool
async def semantic_search(
    query: str,
) -> str:
    """
    Search internal customer-support
    documentation and return relevant passages.
    """

    rows = await _store.search(query)

    if not rows:

        return (
            "No relevant internal "
            "documentation was found."
        )


    chunks = []


    for index, row in enumerate(
        rows,
        1,
    ):

        chunks.append(
            f"[Source {index}] "
            f"{row.get('title', 'Untitled')} "
            f"(similarity="
            f"{row.get('similarity', 0):.3f})\n"
            f"{row.get('content', '')}"
        )


    return "\n\n".join(chunks)