import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from src.agents.orchestrator import (
    process_customer_query,
)

from src.models.schemas import (
    ChatRequest,
    ChatResponse,
    ErrorResponse,
    HealthResponse,
)

from src.services.database import (
    ping_database,
    check_mongodb_health,
)


router = APIRouter(
    prefix="/api"
)


@router.get("/keepalive")
async def keepalive():
    print("[KEEPALIVE] Endpoint called")
    return {
        "status": "ok",
        "service": "smart-customer-support",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        500: {"model": ErrorResponse},
        504: {"model": ErrorResponse},
    },
)
async def chat(
    request: ChatRequest,
):

    request_id = uuid.uuid4().hex[:8]
    t0 = time.perf_counter()

    print(f"[CHAT][{request_id}] Request received | query={request.query[:60]}...")

    try:
        result = await process_customer_query(
            query=request.query,
            thread_id=request.thread_id,
        )

        elapsed = time.perf_counter() - t0
        print(f"[CHAT][{request_id}] Completed in {elapsed:.2f}s")

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
            request_id=request_id,
        )

    except TimeoutError as exc:
        elapsed = time.perf_counter() - t0
        print(f"[CHAT][{request_id}] TIMEOUT after {elapsed:.2f}s: {exc}")
        raise HTTPException(
            status_code=504,
            detail={
                "error": "request_timeout",
                "message": "The support workflow took too long to complete.",
                "request_id": request_id,
            },
        )

    except Exception as exc:
        elapsed = time.perf_counter() - t0
        print(f"[CHAT][{request_id}] ERROR after {elapsed:.2f}s: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An internal error occurred while processing your request.",
                "request_id": request_id,
            },
        )


@router.get("/debug/ping")
async def debug_ping():
    return {"message": "backend reachable"}


@router.get("/debug/openai")
async def debug_openai():
    from src.config import get_settings

    settings = get_settings()
    if not settings.openai_api_key:
        return {"status": "error", "message": "OPENAI_API_KEY not configured"}

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=15,
        )
        t0 = time.perf_counter()
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": "Say hello in one word."}],
            max_tokens=10,
        )
        elapsed = time.perf_counter() - t0
        return {
            "status": "ok",
            "model": settings.openai_model,
            "latency_ms": round(elapsed * 1000, 1),
            "response_preview": response.choices[0].message.content[:50],
        }
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        return {
            "status": "error",
            "model": settings.openai_model,
            "latency_ms": round(elapsed * 1000, 1),
            "error": str(exc),
        }


@router.get("/debug/mongodb")
async def debug_mongodb():
    health = check_mongodb_health()
    return {
        "status": "ok" if health["status"] == "connected" else "error",
        "mongodb": health,
    }


@router.post("/debug/llm")
async def debug_llm(body: dict):
    from src.config import get_settings
    from openai import AsyncOpenAI

    query = body.get("query", "Say hello in one sentence.")
    settings = get_settings()

    if not settings.openai_api_key:
        return {"status": "error", "message": "OPENAI_API_KEY not configured"}

    try:
        client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=30,
        )
        t0 = time.perf_counter()
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Reply concisely."},
                {"role": "user", "content": query},
            ],
            temperature=0.2,
        )
        elapsed = time.perf_counter() - t0
        return {
            "status": "ok",
            "model": settings.openai_model,
            "latency_ms": round(elapsed * 1000, 1),
            "response": response.choices[0].message.content,
        }
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        return {
            "status": "error",
            "model": settings.openai_model,
            "latency_ms": round(elapsed * 1000, 1),
            "error": str(exc),
        }
