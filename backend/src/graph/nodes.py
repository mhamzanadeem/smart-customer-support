import time

from src.agents.escalation_agent import (
    create_escalation,
)

from src.agents.learning_agent import (
    record_interaction,
)

from src.agents.rag_agent import (
    run_rag_agent,
)

from src.agents.router_agent import (
    classify_query,
)

from src.agents.technical_agent import (
    run_technical_agent,
)

from src.graph.state import SupportState


def _log(rid: str, msg: str):
    print(f"[GRAPH][{rid}] {msg}")


async def classify_node(
    state: SupportState,
) -> SupportState:

    rid = state.get("thread_id", "???")
    _log(rid, "ENTER classify")
    t0 = time.perf_counter()

    try:
        category = await classify_query(
            state["query"]
        )
        elapsed = time.perf_counter() - t0
        _log(rid, f"EXIT classify -> {category} ({elapsed:.2f}s)")

        return {
            **state,
            "category": category,
        }
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        _log(rid, f"ERROR classify ({elapsed:.2f}s): {exc}")
        return {
            **state,
            "category": "ESCALATION",
        }


async def rag_node(
    state: SupportState,
) -> SupportState:

    rid = state.get("thread_id", "???")
    retry = state.get("retry_count", 0)
    _log(rid, f"ENTER rag (attempt {retry + 1})")
    t0 = time.perf_counter()

    try:
        answer, sources = await run_rag_agent(
            state["query"]
        )
        elapsed = time.perf_counter() - t0
        _log(rid, f"EXIT rag -> sources={len(sources)} ({elapsed:.2f}s)")

        return {
            **state,
            "answer": answer,
            "agent": "rag_agent",
            "sources": sources,
            "needs_more_retrieval": (
                len(sources) == 0
            ),
            "retry_count": retry + 1,
        }
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        _log(rid, f"ERROR rag ({elapsed:.2f}s): {exc}")
        return {
            **state,
            "answer": (
                "I apologize, but I encountered an error "
                "while searching our knowledge base. "
                "Please try again or contact support."
            ),
            "agent": "rag_agent",
            "sources": [],
            "needs_more_retrieval": False,
            "retry_count": retry + 1,
        }


async def technical_node(
    state: SupportState,
) -> SupportState:

    rid = state.get("thread_id", "???")
    _log(rid, "ENTER technical")
    t0 = time.perf_counter()

    try:
        answer = await run_technical_agent(
            state["query"]
        )
        elapsed = time.perf_counter() - t0
        _log(rid, f"EXIT technical ({elapsed:.2f}s)")

        return {
            **state,
            "answer": answer,
            "agent": "technical_agent",
        }
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        _log(rid, f"ERROR technical ({elapsed:.2f}s): {exc}")
        return {
            **state,
            "answer": (
                "I apologize, but I encountered a technical "
                "issue while processing your request. "
                "Please try again later."
            ),
            "agent": "technical_agent",
        }


async def escalation_node(
    state: SupportState,
) -> SupportState:

    rid = state.get("thread_id", "???")
    _log(rid, "ENTER escalation")
    t0 = time.perf_counter()

    try:
        summary = await create_escalation(
            state["query"]
        )
        elapsed = time.perf_counter() - t0
        _log(rid, f"EXIT escalation ({elapsed:.2f}s)")

        return {
            **state,
            "answer": (
                "This issue requires human support.\n\n"
                + summary
            ),
            "agent": "escalation_agent",
            "escalated": True,
        }
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        _log(rid, f"ERROR escalation ({elapsed:.2f}s): {exc}")
        return {
            **state,
            "answer": (
                "This issue requires human support. "
                "Our team will contact you shortly."
            ),
            "agent": "escalation_agent",
            "escalated": True,
        }


def learning_node(
    state: SupportState,
) -> SupportState:

    rid = state.get("thread_id", "???")
    _log(rid, "ENTER learning")

    try:
        record_interaction(
            thread_id=state["thread_id"],
            query=state["query"],
            answer=state.get("answer", ""),
            category=state.get("category", "UNKNOWN"),
            agent=state.get("agent", "unknown"),
        )
        _log(rid, "EXIT learning")
    except Exception as exc:
        _log(rid, f"ERROR learning (non-fatal): {exc}")

    return state


def should_retry_rag(
    state: SupportState,
) -> str:

    retry_count = state.get(
        "retry_count",
        0,
    )

    rid = state.get("thread_id", "???")

    if (
        state.get(
            "needs_more_retrieval",
            False,
        )
        and retry_count < 1
    ):
        _log(rid, f"route = retry (attempt {retry_count + 1})")
        return "retry"

    _log(rid, "route = continue")
    return "continue"


def route_category(
    state: SupportState,
) -> str:

    category = state["category"]
    rid = state.get("thread_id", "???")

    if category == "FAQ":
        _log(rid, "route = FAQ -> rag")
        return "rag"

    if category == "TECHNICAL":
        _log(rid, "route = TECHNICAL -> technical")
        return "technical"

    _log(rid, "route = ESCALATION -> escalation")
    return "escalation"
