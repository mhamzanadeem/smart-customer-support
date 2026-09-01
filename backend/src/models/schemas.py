from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=5000,
    )

    thread_id: str = "default"


class ChatResponse(BaseModel):
    answer: str

    category: str

    agent: str

    sources: list[str] = []

    escalated: bool = False

    thread_id: str

    request_id: str = ""


class HealthResponse(BaseModel):
    status: str

    database: bool

    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: str = ""


class Ticket(BaseModel):
    ticket_id: str

    customer_id: str

    issue: str

    status: str

    created_at: datetime | None = None
