import asyncio

from services.queue_service import QueueService
from services.text_extractor_service import TextExtractorService
from constants.queue_constant import QueueTopics
from utils import file_util

queue_service = QueueService()

text_extractor_service = TextExtractorService()


@queue_service.add_subscriber(QueueTopics.PROCESS_DOCUMENT)
async def process_document(data: dict):
    try:
        if not data.get("url"):
            raise ValueError("URL is required")

        file = await file_util.upload_file(data.get("url"))
        chunks, text = await text_extractor_service.extract_text(file)
        await queue_service.publish(
            QueueTopics.DOCUMENT_PROCESSED,
            {
                **data,
                "chunks": chunks,
                "text": text,
            },
        )
    except Exception as e:
        queue_service.publish(
            QueueTopics.DOCUMENT_PROCESSED,
            {
                **data,
                "error": str(e),
            },
        )


if __name__ == "__main__":
    asyncio.run(queue_service.subscribe())
