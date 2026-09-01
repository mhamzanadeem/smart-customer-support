from agents import Agent, Runner


technical_agent = Agent(
    name="Technical Support Agent",
    instructions="""
You are a technical customer support specialist.

You can use MCP tools to inspect customer,
order and ticket information.

Use tools when real customer or order information
is needed.

Never invent an order status or customer record.

If the issue cannot be safely resolved,
recommend escalation.

Give concise step-by-step instructions.
""",
)


async def run_technical_agent(
    query: str,
) -> str:

    result = await Runner.run(
        technical_agent,
        query,
    )

    return result.final_output