from typing import Optional
from fastapi import File, Form, HTTPException, UploadFile
from pydantic import BaseModel, model_validator


class TextExtractorRequestDto(BaseModel):
    url: Optional[str]
    file: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        url: Optional[str] = Form(None, description="The URL"),
        file: Optional[UploadFile] = File(None, description="The file"),
    ) -> "TextExtractorRequestDto":
        return cls(url=url, file=file)

    @model_validator(mode="after")
    def validate_file_or_url(self) -> "TextExtractorRequestDto":
        if not self.file and not self.url:
            raise HTTPException(
                status_code=400, detail="Either 'file' or 'url' must be provided."
            )
        return self


class TextExtractorResponseDto(BaseModel):
    text: str
    chunks: list[str]
