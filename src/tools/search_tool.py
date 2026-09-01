import uuid


def create_support_ticket(
    summary: str,
    customer_context: str = "",
) -> dict:
    """
    Simulate creation of a human-support ticket.
    """

    return {

        "ticket_id":
            f"SUP-{uuid.uuid4().hex[:8].upper()}",

        "status":
            "pending_human_review",

        "summary":
            summary,

        "customer_context":
            customer_context,
    }