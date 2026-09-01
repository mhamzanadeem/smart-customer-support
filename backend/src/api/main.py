from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.api.routes import router


settings = get_settings()


app = FastAPI(
    title="Smart Customer Support API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
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