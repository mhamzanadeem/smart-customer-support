from .base_agent import make_agent

from ..tools.rag_tool import (
    semantic_search,
)

from ..tools.analysis_tool import (
    diagnose_error,
)

from ..tools.search_tool import (
    create_support_ticket,
)


# ==========================================
# RAG Agent
# ==========================================

rag_agent = make_agent(

    "RAG Agent",

    """
Answer customer questions using internal
documentation.

Use semantic_search first.

Do not invent policy or product facts.

Cite the source title in plain text
when available.

If evidence is insufficient, say so and
recommend escalation when appropriate.
""",

    tools=[
        semantic_search
    ],
)


# ==========================================
# Technical Agent
# ==========================================

technical_agent = make_agent(

    "Technical Agent",

    """
Solve technical customer issues.

Use diagnose_error for recognizable
error codes.

Reason from evidence.

Give safe troubleshooting steps.

Never claim a production system was changed
unless a tool actually performed that action.
""",

    tools=[
        diagnose_error
    ],
)


# ==========================================
# Escalation Agent
# ==========================================

escalation_agent = make_agent(

    "Escalation Agent",

    """
Handle issues that require a human.

Summarize:

- the problem
- evidence
- attempted steps
- requested outcome

Produce a concise escalation package.

The orchestrator will create the
simulated ticket.
""",
)


# ==========================================
# Learning Agent
# ==========================================

learning_agent = make_agent(

    "Learning Agent",

    """
Turn a solved support interaction into
a reusable knowledge candidate.

Return a concise title and a clean
support article body.

Never include secrets, personal data,
or speculative facts.
""",
)