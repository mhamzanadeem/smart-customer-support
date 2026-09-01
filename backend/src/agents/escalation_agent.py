from agents import Agent, Runner


escalation_agent = Agent(
    name="Escalation Agent",
    instructions="""
You are a customer support escalation specialist.

Create a professional human escalation summary.

Include:

1. Customer issue
2. What was already attempted
3. Why human intervention is needed
4. Recommended next action

Never claim that a human has actually responded.
""",
)


async def create_escalation(
    query: str,
) -> str:

    result = await Runner.run(
        escalation_agent,
        query,
    )

    return result.final_output