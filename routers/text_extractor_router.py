from fastapi import APIRouter, Depends

from controllers.text_extractor_controller import TextExtractorController
from dtos.text_extractor_dto import TextExtractorRequestDto, TextExtractorResponseDto

text_extractor_router = APIRouter(prefix="/api/text-extractor")

text_extractor_controller = TextExtractorController()


@text_extractor_router.post("/extract")
async def extract_text(
    text_extractor_dto: TextExtractorRequestDto = Depends(
        TextExtractorRequestDto.as_form
    ),
) -> TextExtractorResponseDto:
    return await text_extractor_controller.extract_text(text_extractor_dto)
