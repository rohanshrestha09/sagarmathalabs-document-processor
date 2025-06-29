from pydantic import BaseModel, HttpUrl, Field


class YoutubeTranscriptExtractorRequestDto(BaseModel):
    url: HttpUrl
    languages: list[str] = Field(default=["en"])


class YoutubeTranscriptExtractorResponseDto(BaseModel):
    text: str
