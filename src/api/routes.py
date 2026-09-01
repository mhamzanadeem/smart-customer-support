from fastapi import (
    APIRouter,
    HTTPException,
)

from ..models.schemas import (
    ChatRequest,
    ChatResponse,
    Source,
)

from ..agents.orchestrator import (
    run_support,
)


router = APIRouter()


@router.get("/health")
async def health():

    return {
        "status": "ok"
    }


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    req: ChatRequest,
):

    try:

        result = await run_support(
            req.query,
            req.thread_id,
        )


        sources = [

            Source(

                title=row.get(
                    "title",
                    "Untitled",
                ),

                content=row.get(
                    "content",
                    "",
                ),

                similarity=row.get(
                    "similarity"
                ),
            )

            for row
            in result.get(
                "retrieved",
                [],
            )
        ]


        return ChatResponse(

            answer=result.get(
                "answer",
                "No answer generated.",
            ),

            query_type=result.get(
                "query_type",
                "faq",
            ),

            sources=sources,

            escalated=bool(
                result.get(
                    "escalated",
                    False,
                )
            ),

            ticket_id=result.get(
                "ticket_id"
            ),

            thread_id=req.thread_id,

            trace=result.get(
                "trace",
                [],
            ),
        )


    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=(
                "Agent workflow failed: "
                f"{exc}"
            ),

        ) from exc