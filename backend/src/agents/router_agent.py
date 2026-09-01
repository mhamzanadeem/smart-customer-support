import time

from agents import Agent, Runner

from src.config import get_settings


router_agent = Agent(
    name="Query Router",
    instructions="""
Classify the customer request into exactly one category.

Allowed categories:

FAQ
TECHNICAL
ESCALATION

FAQ:
Company policies, general questions,
shipping, refunds, account information.

TECHNICAL:
Errors, failed payments, broken features,
orders, technical troubleshooting.

ESCALATION:
Legal complaints, angry customers,
security incidents, unresolved complex issues,
requests requiring a human.

Return ONLY the category.
""",
)


async def classify_query(
    query: str,
) -> str:

    _log(f"Classifying query: {query[:50]}...")
    t0 = time.perf_counter()

    try:
        result = await Runner.run(
            router_agent,
            query,
        )
        elapsed = time.perf_counter() - t0
        category = result.final_output.strip().upper()
        _log(f"Classification done: {category} ({elapsed:.2f}s)")

        if category not in {
            "FAQ",
            "TECHNICAL",
            "ESCALATION",
        }:
            _log(f"Unexpected category '{category}', defaulting to ESCALATION")
            return "ESCALATION"

        return category
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        _log(f"Classification FAILED ({elapsed:.2f}s): {exc}")
        raise


def _log(msg: str):
    print(f"[ROUTER] {msg}")
