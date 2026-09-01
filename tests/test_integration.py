import pytest


@pytest.mark.asyncio
async def test_health_contract():

    from src.api.main import app


    assert app.title.startswith(
        "Smart Customer Support"
    )