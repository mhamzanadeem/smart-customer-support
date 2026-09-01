from agents import Agent


def create_base_agent(
    name: str,
    instructions: str,
    tools: list | None = None,
    handoffs: list | None = None,
) -> Agent:

    return Agent(
        name=name,
        instructions=instructions,
        tools=tools or [],
        handoffs=handoffs or [],
    )