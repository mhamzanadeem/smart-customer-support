from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from src.graph.nodes import (
    classify_node,
    escalation_node,
    learning_node,
    rag_node,
    route_category,
    should_retry_rag,
    technical_node,
)

from src.graph.state import SupportState


def build_workflow():

    graph = StateGraph(
        SupportState
    )

    graph.add_node(
        "classify",
        classify_node,
    )

    graph.add_node(
        "rag",
        rag_node,
    )

    graph.add_node(
        "technical",
        technical_node,
    )

    graph.add_node(
        "escalation",
        escalation_node,
    )

    graph.add_node(
        "learning",
        learning_node,
    )

    graph.add_edge(
        START,
        "classify",
    )

    graph.add_conditional_edges(
        "classify",
        route_category,
        {
            "rag": "rag",
            "technical": "technical",
            "escalation": "escalation",
        },
    )

    graph.add_conditional_edges(
        "rag",
        should_retry_rag,
        {
            "retry": "rag",
            "continue": "learning",
        },
    )

    graph.add_edge(
        "technical",
        "learning",
    )

    graph.add_edge(
        "escalation",
        "learning",
    )

    graph.add_edge(
        "learning",
        END,
    )

    return graph.compile()