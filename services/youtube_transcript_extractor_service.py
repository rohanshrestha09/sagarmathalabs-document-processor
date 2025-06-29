from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat


class YoutubeTranscriptExtractorService:
    async def extract_transcript(self, url: str, languages: list[str]) -> str:
        if not url or "youtube.com" not in url:
            raise ValueError(f"Invalid URL: {url}")

        loader = YoutubeLoader.from_youtube_url(
            url,
            language=languages,
            transcript_format=TranscriptFormat.LINES,
        )
        docs = await loader.aload()
        return "\n".join([doc.page_content for doc in docs])
