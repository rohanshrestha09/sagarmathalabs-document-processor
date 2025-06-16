from http import HTTPStatus
from fastapi import Request
from fastapi.responses import JSONResponse

from configs.app_config import AppConfig


async def auth_middleware(request: Request, call_next):
    response = await call_next(request)

    if request.method == "OPTIONS":
        return JSONResponse(status_code=200)

    if any(
        path in request.url.path
        for path in ["/docs", "/redoc", "/openapi.json", "/scalar"]
    ):
        return response

    api_key = request.headers.get("X-API-KEY")

    if not api_key or api_key not in AppConfig.get_valid_api_keys():
        return JSONResponse(
            content={
                "detail": [{"message": "Unauthorized - Invalid or missing API key"}]
            },
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    return response
