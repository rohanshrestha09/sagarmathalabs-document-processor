from fastapi import APIRouter, Depends

from configs.app_config import AppConfig
from controllers.youtube_transcript_extractor_controller import (
    YoutubeTranscriptExtractorController,
)
from dtos.youtube_transcript_extractor_dto import (
    YoutubeTranscriptExtractorRequestDto,
    YoutubeTranscriptExtractorResponseDto,
)
from fastapi_limiter.depends import RateLimiter


youtube_transcript_extractor_router = APIRouter(
    prefix="/api/youtube-transcript-extractor"
)

youtube_transcript_extractor_controller = YoutubeTranscriptExtractorController()


@youtube_transcript_extractor_router.post(
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
async def extract_transcript(
    youtube_transcript_extractor_dto: YoutubeTranscriptExtractorRequestDto,
) -> YoutubeTranscriptExtractorResponseDto:
    return await youtube_transcript_extractor_controller.extract_transcript(
        youtube_transcript_extractor_dto
    )
