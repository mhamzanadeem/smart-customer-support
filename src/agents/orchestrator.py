import logging

from typing import (
    TypedDict,
    Literal,
)

from agents import (
    Agent,
    Runner,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from .worker_agents import (
    rag_agent,
    technical_agent,
    escalation_agent,
    learning_agent,
)

from ..tools.search_tool import (
    create_support_ticket,
)

from ..services.vector_store import (
    VectorStore,
)


log = logging.getLogger(__name__)

store = VectorStore()


class SupportState(TypedDict, total=False):

    query: str

    query_type: str

    retrieved: list[dict]

    answer: str

    escalated: bool

    ticket_id: str | None

    trace: list[str]

    learning_candidate: str

    attempts: int


async def run_agent(
    agent: Agent,
    prompt: str,
    max_turns: int = 6,
) -> str:

    result = await Runner.run(
        agent,
        prompt,
        max_turns=max_turns,
    )

    return str(
        result.final_output
    )


# ==========================================
# Classification
# ==========================================

def classify_query(
    state: SupportState,
):

    query = state["query"].lower()


    # FAQ patterns

    if any(
        x in query
        for x in [
            "refund",
            "cancel",
            "pricing",
            "password",
            "hours",
            "policy",
            "how do i",
        ]
    ):

        kind = "faq"


    # Technical patterns

    elif any(
        x in query
        for x in [
            "error",
            "api",
            "timeout",
            "integration",
            "bug",
            "500",
            "401",
            "429",
            "database",
        ]
    ):

        kind = "technical"


    # Escalation patterns

    elif any(
        x in query
        for x in [
            "legal",
            "security breach",
            "chargeback",
            "manager",
            "human",
            "complaint",
            "urgent",
        ]
    ):

        kind = "escalation"


    else:

        kind = "faq"


    return {

        "query_type": kind,

        "trace":
            state.get(
                "trace",
                [],
            )
            + [
                f"classified:{kind}"
            ],
    }


# ==========================================
# RAG node
# ==========================================

async def rag_node(
    state: SupportState,
):

    rows = await store.search(
        state["query"]
    )


    prompt = (

        f"Customer query:\n"
        f"{state['query']}\n\n"

        f"Retrieved internal evidence:\n"
        f"{rows}\n\n"

        "Answer using only the evidence. "
        "If evidence is weak, say that clearly."
    )


    answer = await run_agent(
        rag_agent,
        prompt,
    )


    return {

        "retrieved":
            rows,

        "answer":
            answer,

        "trace":
            state.get(
                "trace",
                [],
            )
            + [
                "rag_agent"
            ],
    }


# ==========================================
# Technical node
# ==========================================

async def technical_node(
    state: SupportState,
):

    rows = await store.search(
        state["query"]
    )


    prompt = (

        f"Customer query:\n"
        f"{state['query']}\n\n"

        f"Relevant internal evidence:\n"
        f"{rows}\n\n"

        "Solve the issue. "
        "Use tools for error-code diagnosis "
        "when useful. "

        "Give numbered troubleshooting steps "
        "and a clear stopping condition."
    )


    answer = await run_agent(
        technical_agent,
        prompt,
    )


    return {

        "retrieved":
            rows,

        "answer":
            answer,

        "attempts":
            state.get(
                "attempts",
                0,
            ) + 1,

        "trace":
            state.get(
                "trace",
                [],
            )
            + [
                "technical_agent"
            ],
    }


# ==========================================
# Escalation decision
# ==========================================

def needs_escalation(
    state: SupportState,
) -> Literal[
    "escalate",
    "finish",
]:

    answer = state.get(
        "answer",
        "",
    )


    if (
        state.get("query_type")
        == "escalation"
    ):

        return "escalate"


    if (
        state.get("attempts", 0)
        >= 2
    ):

        return "escalate"


    if (
        "unable to resolve"
        in answer.lower()
        or
        "human"
        in answer.lower()
    ):

        return "escalate"


    return "finish"


# ==========================================
# Escalation node
# ==========================================

async def escalation_node(
    state: SupportState,
):

    prompt = (

        "Prepare a human handoff for "
        "this customer issue:\n"

        f"{state['query']}\n\n"

        "Previous answer/evidence:\n"

        f"{state.get('answer', '')}\n"

        f"{state.get('retrieved', [])}"
    )


    package = await run_agent(
        escalation_agent,
        prompt,
    )


    ticket = create_support_ticket(
        package,
        state["query"],
    )


    return {

        "answer":
            (
                "I’m escalating this to a "
                "human support specialist.\n\n"

                + package

                + (
                    f"\n\nTicket: "
                    f"{ticket['ticket_id']}"
                )
            ),

        "escalated":
            True,

        "ticket_id":
            ticket["ticket_id"],

        "trace":
            state.get(
                "trace",
                [],
            )
            + [
                "escalation_agent",
                "human_review_simulation",
            ],
    }


# ==========================================
# Learning node
# ==========================================

async def learning_node(
    state: SupportState,
):

    if state.get("escalated"):

        return {

            "trace":
                state.get(
                    "trace",
                    [],
                )
                + [
                    "learning_skipped_escalated"
                ],
        }


    prompt = (

        f"Customer query:\n"
        f"{state['query']}\n\n"

        f"Final answer:\n"
        f"{state.get('answer', '')}\n\n"

        "Create a candidate support article "
        "only if the interaction contains "
        "reusable knowledge.\n\n"

        "Return TITLE on the first line and "
        "ARTICLE on subsequent lines."
    )


    candidate = await run_agent(
        learning_agent,
        prompt,
    )


    return {

        "learning_candidate":
            candidate,

        "trace":
            state.get(
                "trace",
                [],
            )
            + [
                "learning_agent"
            ],
    }


# ==========================================
# Build LangGraph
# ==========================================

def build_graph():

    builder = StateGraph(
        SupportState
    )


    builder.add_node(
        "classify_query",
        classify_query,
    )

    builder.add_node(
        "rag_agent",
        rag_node,
    )

    builder.add_node(
        "technical_agent",
        technical_node,
    )

    builder.add_node(
        "escalate",
        escalation_node,
    )

    builder.add_node(
        "update_kb",
        learning_node,
    )


    builder.add_edge(
        START,
        "classify_query",
    )


    builder.add_conditional_edges(

        "classify_query",

        lambda state:
            state["query_type"],

        {
            "faq":
                "rag_agent",

            "technical":
                "technical_agent",

            "escalation":
                "escalate",
        },
    )


    builder.add_edge(
        "rag_agent",
        "update_kb",
    )


    builder.add_conditional_edges(

        "technical_agent",

        needs_escalation,

        {
            "escalate":
                "escalate",

            "finish":
                "update_kb",
        },
    )


    builder.add_edge(
        "escalate",
        END,
    )


    builder.add_edge(
        "update_kb",
        END,
    )


    # --------------------------------------
    # Local development checkpoint
    # --------------------------------------

    return builder.compile(
        checkpointer=InMemorySaver()
    )


graph = build_graph()


# ==========================================
# Public workflow
# ==========================================

async def run_support(
    query: str,
    thread_id: str,
):

    result = await graph.ainvoke(

        {
            "query": query,

            "trace": [],

            "attempts": 0,

            "escalated": False,
        },

        {
            "configurable": {
                "thread_id":
                    thread_id
            }
        },

        config={
            "recursion_limit": 12
        },
    )


    return result