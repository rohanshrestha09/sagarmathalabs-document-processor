import io
import aiohttp
from fastapi import UploadFile


async def upload_file(url: str) -> UploadFile:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"Failed to download file from URL: {url}")

            content = await response.read()
            file_stream = io.BytesIO(content)

            filename = url.split("/")[-1]
            if not filename:
                filename = "downloaded_file"

            return UploadFile(
                file=file_stream,
                filename=filename,
                headers=response.headers,
            )
