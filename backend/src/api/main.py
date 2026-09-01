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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

setup_logging()


app = FastAPI(
    title="Smart Customer Support API",
    version="1.0.0",
)


cors_origins = settings.cors_origin_list
print(f"[CORS] Configured origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
