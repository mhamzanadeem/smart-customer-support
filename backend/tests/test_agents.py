import pytest
from unittest.mock import patch, AsyncMock

from src.graph.nodes import (
    classify_node,
    rag_node,
    technical_node,
    escalation_node,
    learning_node,
    should_retry_rag,
    route_category,
)


def make_state(**overrides):
    state = {
        "query": "test query",
        "thread_id": "test-123",
        "retry_count": 0,
        "sources": [],
        "escalated": False,
    }
    state.update(overrides)
    return state


@pytest.mark.asyncio
@patch("src.graph.nodes.classify_query", new_callable=AsyncMock, return_value="FAQ")
async def test_classify_node(mock_classify):
    state = make_state()
    result = await classify_node(state)
    assert result["category"] == "FAQ"


@pytest.mark.asyncio
@patch("src.graph.nodes.classify_query", new_callable=AsyncMock, return_value="TECHNICAL")
async def test_classify_node_technical(mock_classify):
    state = make_state()
    result = await classify_node(state)
    assert result["category"] == "TECHNICAL"


@pytest.mark.asyncio
@patch("src.graph.nodes.classify_query", new_callable=AsyncMock, side_effect=Exception("LLM timeout"))
async def test_classify_node_error(mock_classify):
    state = make_state()
    result = await classify_node(state)
    assert result["category"] == "ESCALATION"


@pytest.mark.asyncio
@patch("src.graph.nodes.run_rag_agent", new_callable=AsyncMock, return_value=("answer", [{"title": "t", "source": "s", "content": "c"}]))
async def test_rag_node(mock_rag):
    state = make_state()
    result = await rag_node(state)
    assert result["agent"] == "rag_agent"
    assert result["retry_count"] == 1
    assert result["needs_more_retrieval"] is False


@pytest.mark.asyncio
@patch("src.graph.nodes.run_rag_agent", new_callable=AsyncMock, return_value=("answer", []))
async def test_rag_node_no_sources(mock_rag):
    state = make_state()
    result = await rag_node(state)
    assert result["needs_more_retrieval"] is True
    assert result["retry_count"] == 1


@pytest.mark.asyncio
@patch("src.graph.nodes.run_rag_agent", new_callable=AsyncMock, side_effect=Exception("MongoDB timeout"))
async def test_rag_node_error(mock_rag):
    state = make_state()
    result = await rag_node(state)
    assert result["needs_more_retrieval"] is False
    assert result["retry_count"] == 1
    assert "error" in result["answer"].lower() or "apologize" in result["answer"].lower()


def test_should_retry_rag_no_sources():
    state = make_state(needs_more_retrieval=True, retry_count=0)
    assert should_retry_rag(state) == "retry"


def test_should_retry_rag_already_retried():
    state = make_state(needs_more_retrieval=True, retry_count=1)
    assert should_retry_rag(state) == "continue"


def test_should_retry_rag_has_sources():
    state = make_state(needs_more_retrieval=False, retry_count=0)
    assert should_retry_rag(state) == "continue"


def test_route_category_faq():
    state = make_state(category="FAQ")
    assert route_category(state) == "rag"


def test_route_category_technical():
    state = make_state(category="TECHNICAL")
    assert route_category(state) == "technical"


def test_route_category_escalation():
    state = make_state(category="ESCALATION")
    assert route_category(state) == "escalation"


def test_route_category_unknown():
    state = make_state(category="UNKNOWN")
    assert route_category(state) == "escalation"
