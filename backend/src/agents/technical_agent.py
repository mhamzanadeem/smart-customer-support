import time

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

    _log(f"Running technical agent for: {query[:50]}...")
    t0 = time.perf_counter()

    try:
        result = await Runner.run(
            technical_agent,
            query,
        )
        elapsed = time.perf_counter() - t0
        _log(f"Technical agent done ({elapsed:.2f}s)")
        return result.final_output
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        _log(f"Technical agent FAILED ({elapsed:.2f}s): {exc}")
        raise


def _log(msg: str):
    print(f"[TECHNICAL] {msg}")
