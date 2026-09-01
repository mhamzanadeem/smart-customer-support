from src.graph.workflow import (
    build_workflow,
)


workflow = build_workflow()


async def process_customer_query(
    query: str,
    thread_id: str,
) -> dict:

    initial_state = {
        "query": query,
        "thread_id": thread_id,
        "retry_count": 0,
        "sources": [],
        "escalated": False,
    }

    result = await workflow.ainvoke(
        initial_state
    )

    return result