from dataclasses import dataclass


@dataclass
class AppContext:
    customer_id: str = "anonymous"
    channel: str = "web"