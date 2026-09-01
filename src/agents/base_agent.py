from agents import Agent

from ..services.llm_service import (
    get_agent_model,
)


def make_agent(
    name: str,
    instructions: str,
    tools=None,
    handoffs=None,
) -> Agent:

    return Agent(

        name=name,

        instructions=instructions,

        model=get_agent_model(),

        tools=tools or [],

        handoffs=handoffs or [],
    )