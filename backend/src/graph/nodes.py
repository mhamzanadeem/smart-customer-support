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


async def classify_node(
    state: SupportState,
) -> SupportState:

    category = await classify_query(
        state["query"]
    )

    return {
        **state,
        "category": category,
    }


async def rag_node(
    state: SupportState,
) -> SupportState:

    answer, sources = await run_rag_agent(
        state["query"]
    )

    return {
        **state,
        "answer": answer,
        "agent": "rag_agent",
        "sources": sources,
        "needs_more_retrieval": (
            len(sources) == 0
        ),
    }


async def technical_node(
    state: SupportState,
) -> SupportState:

    answer = await run_technical_agent(
        state["query"]
    )

    return {
        **state,
        "answer": answer,
        "agent": "technical_agent",
    }


async def escalation_node(
    state: SupportState,
) -> SupportState:

    summary = await create_escalation(
        state["query"]
    )

    return {
        **state,
        "answer": (
            "This issue requires human support.\n\n"
            + summary
        ),
        "agent": "escalation_agent",
        "escalated": True,
    }


def learning_node(
    state: SupportState,
) -> SupportState:

    record_interaction(
        thread_id=state["thread_id"],
        query=state["query"],
        answer=state["answer"],
        category=state["category"],
        agent=state["agent"],
    )

    return state


def should_retry_rag(
    state: SupportState,
) -> str:

    retry_count = state.get(
        "retry_count",
        0,
    )

    if (
        state.get(
            "needs_more_retrieval",
            False,
        )
        and retry_count < 1
    ):
        return "retry"

    return "continue"


def route_category(
    state: SupportState,
) -> str:

    category = state["category"]

    if category == "FAQ":
        return "rag"

    if category == "TECHNICAL":
        return "technical"

    return "escalation"