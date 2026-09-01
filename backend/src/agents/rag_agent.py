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

    context = await retriever.retrieve(
        query
    )

    if not context:

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

    result = await Runner.run(
        rag_agent,
        prompt,
    )

    sources = [
        item["source"]
        for item in context
    ]

    return result.final_output, sources