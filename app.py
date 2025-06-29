from dotenv import load_dotenv
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from scalar_fastapi import get_scalar_api_reference
from middlewares.auth_middleware import auth_middleware
from middlewares.exception_handlers import validation_exception_handler
from middlewares.exception_handlers import http_exception_handler
from middlewares.exception_handlers import value_error_handler
from middlewares.exception_handlers import exception_handler
from middlewares.rate_limit_middleware import rate_limit_callback
from routers.text_extractor_router import text_extractor_router
from routers.youtube_transcript_extractor_router import (
    youtube_transcript_extractor_router,
)
from configs.app_config import AppConfig

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connection = redis.from_url(
        AppConfig.get_redis_connection_string(),
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_connection, http_callback=rate_limit_callback)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=AppConfig.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.middleware("http")(auth_middleware)


app.exception_handler(RequestValidationError)(validation_exception_handler)

app.exception_handler(HTTPException)(http_exception_handler)

app.exception_handler(ValueError)(value_error_handler)

app.exception_handler(Exception)(exception_handler)


app.include_router(text_extractor_router)

app.include_router(youtube_transcript_extractor_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
