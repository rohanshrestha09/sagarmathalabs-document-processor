from fastapi import APIRouter, Depends

from controllers.text_extractor_controller import TextExtractorController
from dtos.text_extractor_dto import TextExtractorRequestDto, TextExtractorResponseDto
from utils.rate_limiter import RateLimiter

text_extractor_router = APIRouter(prefix="/api/text-extractor")

text_extractor_controller = TextExtractorController()


@text_extractor_router.post(
    "/extract", dependencies=[Depends(RateLimiter(requests_limit=100, time_window=60))]
)
async def extract_text(
    text_extractor_dto: TextExtractorRequestDto = Depends(
        TextExtractorRequestDto.as_form
    ),
) -> TextExtractorResponseDto:
    return await text_extractor_controller.extract_text(text_extractor_dto)
