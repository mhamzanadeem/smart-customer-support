from mcp.server.fastmcp import FastMCP

from src.mcp.tools import (
    create_ticket,
    get_customer,
    get_order,
    get_ticket,
)


mcp = FastMCP(
    "Customer Support Tools"
)


@mcp.tool()
def customer_lookup(
    customer_id: str,
) -> dict:
    """
    Look up a customer by customer ID.
    """

    return get_customer(
        customer_id
    )


@mcp.tool()
def order_lookup(
    order_id: str,
) -> dict:
    """
    Look up an order by order ID.
    """

    return get_order(
        order_id
    )


@mcp.tool()
def support_ticket_create(
    customer_id: str,
    issue: str,
) -> dict:
    """
    Create a support ticket.
    """

    return create_ticket(
        customer_id,
        issue,
    )


@mcp.tool()
def support_ticket_lookup(
    ticket_id: str,
) -> dict:
    """
    Look up a support ticket.
    """

    return get_ticket(
        ticket_id
    )


if __name__ == "__main__":
    mcp.run()