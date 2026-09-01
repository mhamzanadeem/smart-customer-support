from agents import Agent, Runner


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

    result = await Runner.run(
        router_agent,
        query,
    )

    category = result.final_output.strip().upper()

    if category not in {
        "FAQ",
        "TECHNICAL",
        "ESCALATION",
    }:
        return "ESCALATION"

    return category