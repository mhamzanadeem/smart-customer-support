from datetime import datetime, timezone

from src.config import get_settings
from src.api.routes import router
from src.services.logging_config import setup_logging
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

from fastapi import FastAPI, Request
from fastapi.responses import Response

settings = get_settings()

setup_logging()


app = FastAPI(
    title="Smart Customer Support API",
    version="1.0.0",
)


@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "*")

    if request.method == "OPTIONS":
        return Response(
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "86400",
            },
        )

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


app.include_router(router)


@app.get("/")
async def root():

    return {
        "name": "Smart Customer Support",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    from src.services.database import ping_database
    return {
        "status": "ok",
        "service": "smart-customer-support",
        "database": ping_database(),
    }
