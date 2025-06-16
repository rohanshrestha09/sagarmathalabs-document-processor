from http import HTTPStatus
from math import ceil
from fastapi import Request, Response
from fastapi.exceptions import HTTPException


async def rate_limit_callback(request: Request, response: Response, pexpire: int):
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status_code=HTTPStatus.TOO_MANY_REQUESTS,
        detail=f"Too many requests. Please try again after {expire} seconds.",
        headers={"Retry-After": str(expire)},
    )
