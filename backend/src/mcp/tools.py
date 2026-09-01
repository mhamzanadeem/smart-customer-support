from datetime import datetime, timezone
from bson import ObjectId

from src.services.database import (
    get_collection,
)


def get_customer(
    customer_id: str,
) -> dict:

    customer = get_collection(
        "customers"
    ).find_one(
        {
            "customer_id": customer_id
        },
        {
            "_id": 0
        },
    )

    if not customer:
        return {
            "found": False,
            "message": "Customer not found.",
        }

    return customer


def get_order(
    order_id: str,
) -> dict:

    order = get_collection(
        "orders"
    ).find_one(
        {
            "order_id": order_id
        },
        {
            "_id": 0
        },
    )

    if not order:
        return {
            "found": False,
            "message": "Order not found.",
        }

    return order


def create_ticket(
    customer_id: str,
    issue: str,
) -> dict:

    collection = get_collection(
        "support_tickets"
    )

    ticket_id = (
        f"TICKET-{ObjectId()}"
    )

    ticket = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "issue": issue,
        "status": "open",
        "created_at": datetime.now(
            timezone.utc
        ),
    }

    collection.insert_one(ticket)

    return {
        "success": True,
        "ticket_id": ticket_id,
        "status": "open",
    }


def get_ticket(
    ticket_id: str,
) -> dict:

    ticket = get_collection(
        "support_tickets"
    ).find_one(
        {
            "ticket_id": ticket_id
        },
        {
            "_id": 0
        },
    )

    if not ticket:
        return {
            "found": False,
            "message": "Ticket not found.",
        }

    return ticket