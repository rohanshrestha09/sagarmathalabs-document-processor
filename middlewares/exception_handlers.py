from http import HTTPStatus
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


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

    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST, content={"detail": formatted_errors}
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": [{"message": exc.detail}]},
    )


async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"detail": [{"message": str(exc.args[0])}]},
    )


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"detail": [{"message": str(exc)}]},
    )
