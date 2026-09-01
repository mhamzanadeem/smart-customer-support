from typing import Literal

from pydantic import BaseModel, Field


QueryType = Literal[
    "faq",
    "technical",
    "escalation",
]


class ChatRequest(BaseModel):
    query: str = Field(
        min_length=2,
        max_length=4000,
    )

    thread_id: str = Field(
        default="demo-thread",
        min_length=1,
        max_length=200,
    )


class Source(BaseModel):
    title: str
    content: str
    similarity: float | None = None


class ChatResponse(BaseModel):
    answer: str

    query_type: QueryType

    sources: list[Source] = []

    escalated: bool = False

    ticket_id: str | None = None

    thread_id: str

    trace: list[str] = []