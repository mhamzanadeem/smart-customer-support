from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from ..services.logging_config import (
    configure_logging,
)

from .routes import router


configure_logging()


app = FastAPI(

    title=(
        "Smart Customer Support "
        "& Knowledge Management"
    ),

    version="1.0.0",

    description=(
        "RAG + LangGraph + "
        "OpenAI Agents SDK capstone."
    ),
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(
    router,
    prefix="/api",
)


@app.get("/")
async def root():

    return {

        "name":
            "smart-customer-support",

        "docs":
            "/docs",
    }