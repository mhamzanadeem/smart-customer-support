from typing import TypedDict


class SupportState(TypedDict, total=False):

    query: str

    thread_id: str

    category: str

    retrieved_context: str

    sources: list[str]

    draft_answer: str

    answer: str

    agent: str

    escalated: bool

    retry_count: int

    needs_more_retrieval: bool

    error: str