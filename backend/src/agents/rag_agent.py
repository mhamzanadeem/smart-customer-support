import time

from agents import Agent, Runner

from src.rag.retriever import RAGRetriever


retriever = RAGRetriever()


rag_agent = Agent(
    name="RAG Support Agent",
    instructions="""
You are the company's knowledge-base support specialist.

Answer customer questions using ONLY the supplied
company documentation context.

Never invent company policies.

If the documentation does not contain enough information,
clearly say that the information is insufficient and
recommend escalation.

Keep answers concise, professional and actionable.
""",
)


async def run_rag_agent(
    query: str,
) -> tuple[str, list[str]]:

    rid = query[:20] if query else "???"

    try:
        _log(rid, "Retrieving context from RAG store")
        t0 = time.perf_counter()
        context = await retriever.retrieve(query)
        elapsed = time.perf_counter() - t0
        _log(rid, f"RAG retrieval done: {len(context)} docs ({elapsed:.2f}s)")
    except Exception as exc:
        _log(rid, f"RAG retrieval failed: {exc}")
        return (
            "I apologize, but I encountered an error "
            "while searching our knowledge base.",
            [],
        )

    if not context:
        _log(rid, "No context found, returning fallback")
        return (
            "I could not find enough information "
            "in the company knowledge base to answer "
            "your question confidently.",
            [],
        )

    formatted = "\n\n".join(
        [
            (
                f"Title: {item['title']}\n"
                f"Source: {item['source']}\n"
                f"Content: {item['content']}"
            )
            for item in context
        ]
    )

    prompt = f"""
Customer question:

{query}

Company knowledge base:

{formatted}

Answer the customer using the knowledge base.
"""

    try:
        _log(rid, "Running RAG agent LLM call")
        t0 = time.perf_counter()
        result = await Runner.run(
            rag_agent,
            prompt,
        )
        elapsed = time.perf_counter() - t0
        _log(rid, f"RAG LLM done ({elapsed:.2f}s)")
    except Exception as exc:
        _log(rid, f"RAG LLM failed: {exc}")
        return (
            "I apologize, but I encountered an error "
            "while generating the response.",
            [],
        )

    sources = [
        item["source"]
        for item in context
    ]

    return result.final_output, sources


def _log(rid: str, msg: str):
    print(f"[RAG][{rid}] {msg}")
