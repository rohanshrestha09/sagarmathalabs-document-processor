from dtos.text_extractor_dto import TextExtractorRequestDto, TextExtractorResponseDto
from services.text_extractor_service import TextExtractorService
from utils import file_util


class TextExtractorController:
    def __init__(self):
        self.text_extractor_service = TextExtractorService()

    async def extract_text(
        self, text_extractor_dto: TextExtractorRequestDto
    ) -> TextExtractorResponseDto:
        file = (
            text_extractor_dto.file
            if text_extractor_dto.file
            else await file_util.upload_file(text_extractor_dto.url)
        )

        chunks, text = await self.text_extractor_service.extract_text(file)
        return TextExtractorResponseDto(text=text, chunks=chunks)
