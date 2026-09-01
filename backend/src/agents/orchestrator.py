import time
import uuid

from src.graph.workflow import (
    build_workflow,
)


workflow = build_workflow()

_MAX_WORKFLOW_SECONDS = 60


async def process_customer_query(
    query: str,
    thread_id: str,
) -> dict:

    request_id = uuid.uuid4().hex[:8]

    if not thread_id or thread_id == "default":
        thread_id = request_id

    print(f"[ORCHESTRATOR][{request_id}] Request received | query={query[:60]}... | thread_id={thread_id}")

    initial_state = {
        "query": query,
        "thread_id": request_id,
        "retry_count": 0,
        "sources": [],
        "escalated": False,
    }

    t0 = time.perf_counter()

    try:
        result = await workflow.ainvoke(
            initial_state
        )
        elapsed = time.perf_counter() - t0
        print(f"[ORCHESTRATOR][{request_id}] Workflow completed in {elapsed:.2f}s")
        return result
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        print(f"[ORCHESTRATOR][{request_id}] Workflow FAILED after {elapsed:.2f}s: {exc}")
        raise
