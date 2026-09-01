from fastapi import APIRouter, HTTPException

from src.agents.orchestrator import (
    process_customer_query,
)

from src.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
)

from src.services.database import (
    ping_database,
)


router = APIRouter(
    prefix="/api"
)


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    return HealthResponse(
        status="ok",
        database=ping_database(),
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    try:

        result = await process_customer_query(
            query=request.query,
            thread_id=request.thread_id,
        )

        return ChatResponse(
            answer=result.get(
                "answer",
                "No answer generated.",
            ),
            category=result.get(
                "category",
                "UNKNOWN",
            ),
            agent=result.get(
                "agent",
                "unknown",
            ),
            sources=result.get(
                "sources",
                [],
            ),
            escalated=result.get(
                "escalated",
                False,
            ),
            thread_id=request.thread_id,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )