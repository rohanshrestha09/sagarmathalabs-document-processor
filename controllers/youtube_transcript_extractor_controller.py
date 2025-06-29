from dtos.youtube_transcript_extractor_dto import (
    YoutubeTranscriptExtractorRequestDto,
    YoutubeTranscriptExtractorResponseDto,
)
from services.youtube_transcript_extractor_service import (
    YoutubeTranscriptExtractorService,
)


class YoutubeTranscriptExtractorController:
    def __init__(self):
        self.youtube_transcript_extractor_service = YoutubeTranscriptExtractorService()

    async def extract_transcript(
        self, youtube_transcript_extractor_dto: YoutubeTranscriptExtractorRequestDto
    ) -> YoutubeTranscriptExtractorResponseDto:
        text = await self.youtube_transcript_extractor_service.extract_transcript(
            url=youtube_transcript_extractor_dto.url.encoded_string(),
            languages=youtube_transcript_extractor_dto.languages,
        )
        return YoutubeTranscriptExtractorResponseDto(text=text)
