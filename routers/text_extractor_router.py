from fastapi import APIRouter, Depends

from configs.app_config import AppConfig
from controllers.text_extractor_controller import TextExtractorController
from dtos.text_extractor_dto import TextExtractorRequestDto, TextExtractorResponseDto
from fastapi_limiter.depends import RateLimiter


text_extractor_router = APIRouter(prefix="/api/text-extractor")

text_extractor_controller = TextExtractorController()


@text_extractor_router.post(
    "/extract",
    dependencies=[
        Depends(
            RateLimiter(
                times=AppConfig.get_request_limit(),
                seconds=AppConfig.get_request_time_window(),
            )
        )
    ],
)
async def extract_text(
    text_extractor_dto: TextExtractorRequestDto = Depends(
        TextExtractorRequestDto.as_form
    ),
) -> TextExtractorResponseDto:
    return await text_extractor_controller.extract_text(text_extractor_dto)
