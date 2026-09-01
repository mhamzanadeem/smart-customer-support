import time

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

    _log(f"Creating escalation for: {query[:50]}...")
    t0 = time.perf_counter()

    try:
        result = await Runner.run(
            escalation_agent,
            query,
        )
        elapsed = time.perf_counter() - t0
        _log(f"Escalation done ({elapsed:.2f}s)")
        return result.final_output
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        _log(f"Escalation FAILED ({elapsed:.2f}s): {exc}")
        raise


def _log(msg: str):
    print(f"[ESCALATION] {msg}")
