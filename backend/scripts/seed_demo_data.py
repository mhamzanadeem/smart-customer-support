from datetime import datetime, timezone

from src.services.database import (
    get_collection,
)


customers = [
    {
        "customer_id": "CUST-1001",
        "name": "Demo Customer",
        "email": "customer@example.com",
        "plan": "premium",
    },
    {
        "customer_id": "CUST-1002",
        "name": "Test Customer",
        "email": "test@example.com",
        "plan": "basic",
    },
]


orders = [
    {
        "order_id": "ORD-10001",
        "customer_id": "CUST-1001",
        "status": "delayed",
        "total": 129.99,
        "estimated_delivery": "2026-09-05",
    },
    {
        "order_id": "ORD-10002",
        "customer_id": "CUST-1002",
        "status": "delivered",
        "total": 59.99,
        "estimated_delivery": "2026-08-29",
    },
]


def seed():

    db = get_collection("customers").database

    db.customers.delete_many({})
    db.orders.delete_many({})

    db.customers.insert_many(
        customers
    )

    db.orders.insert_many(
        orders
    )

    print(
        "Demo customers and orders inserted."
    )


if __name__ == "__main__":
    seed()