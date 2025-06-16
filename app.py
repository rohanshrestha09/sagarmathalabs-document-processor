import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.text_extractor_router import text_extractor_router
from scalar_fastapi import get_scalar_api_reference
from configs.app_config import AppConfig

load_dotenv()


if not os.getenv("ALLOWED_ORIGINS"):
    raise ValueError("ALLOWED_ORIGINS is not set")

app = FastAPI(debug=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS").split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def check_api_key(request: Request, call_next):
    response = await call_next(request)

    if request.method == "OPTIONS":
        return JSONResponse(status_code=200)

    if any(
        path in request.url.path
        for path in ["/docs", "/redoc", "/openapi.json", "/scalar"]
    ):
        return response

    api_key = request.headers.get("X-API-KEY")

    if not api_key or api_key not in AppConfig.VALID_API_KEYS:
        return JSONResponse(
            content={
                "detail": [{"message": "Unauthorized - Invalid or missing API key"}]
            },
            status_code=401,
        )

    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    formatted_errors = [
        {
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "type": err["type"],
        }
        for err in errors
    ]

    return JSONResponse(status_code=400, content={"detail": formatted_errors})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": [{"message": exc.detail}]},
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=500,
        content={"detail": [{"message": str(exc.args[0])}]},
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": [{"message": str(exc)}]})


app.include_router(text_extractor_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
