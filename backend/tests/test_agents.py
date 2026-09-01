import pytest

from src.agents.router_agent import (
    classify_query,
)


@pytest.mark.asyncio
async def test_router_returns_valid_category():

    result = await classify_query(
        "What is your refund policy?"
    )

    assert result in {
        "FAQ",
        "TECHNICAL",
        "ESCALATION",
    }