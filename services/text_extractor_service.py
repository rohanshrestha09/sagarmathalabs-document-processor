import io
import os
import tempfile
import asyncio
from fastapi import UploadFile
from fpdf import FPDF
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.chunking import HybridChunker


class TextExtractorService:
    def __init__(self):
        self.document_converter = DocumentConverter(
            allowed_formats=[
                InputFormat.HTML,
                InputFormat.PDF,
                InputFormat.CSV,
                InputFormat.DOCX,
                InputFormat.XLSX,
                InputFormat.IMAGE,
                InputFormat.MD,
                InputFormat.PPTX,
            ],
        )

        self.allowed_mimetypes = {
            "text/html": InputFormat.HTML,
            "application/pdf": InputFormat.PDF,
            "text/csv": InputFormat.CSV,
            "image/jpeg": InputFormat.IMAGE,
            "image/png": InputFormat.IMAGE,
            "image/webp": InputFormat.IMAGE,
            "text/markdown": InputFormat.MD,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": InputFormat.DOCX,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": InputFormat.XLSX,
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": InputFormat.PPTX,
        }

    def _text_to_pdf(self, text: str) -> bytes:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=text)
        return pdf.output(dest="S").encode("latin-1")

    def _validate_file_type(self, file: UploadFile) -> None:
        mimetype = file.content_type
        if mimetype not in self.allowed_mimetypes:
            raise ValueError(
                f"Unsupported file type: {mimetype}. "
                f"Allowed types are: {', '.join(str(format.value) for format in set(self.allowed_mimetypes.values()))}"
            )

    def _convert_if_text_file(self, file: UploadFile) -> bytes:
        if not file.content_type.startswith("text/plain"):
            return file

        text_content = file.file.read().decode("latin-1")
        pdf_content = io.BytesIO(self._text_to_pdf(text_content))
        filename = file.filename.replace(".txt", ".pdf")
        return UploadFile(
            file=pdf_content,
            filename=filename,
            headers={
                "content-type": "application/pdf",
            },
        )

    async def extract_text(self, file: UploadFile) -> tuple[list[str], str]:
        file = self._convert_if_text_file(file)

        self._validate_file_type(file)

        with tempfile.NamedTemporaryFile(
            suffix=os.path.splitext(file.filename)[1]
        ) as tmp:
            file_path = tmp.name
            with open(file_path, "wb") as f:
                f.write(file.file.read())

            doc = await asyncio.to_thread(self.document_converter.convert, file_path)

            chunker = HybridChunker()
            chunk_iter = chunker.chunk(dl_doc=doc.document)

            chunked_text = []
            for chunk in chunk_iter:
                chunked_text.append(chunker.contextualize(chunk))

            return chunked_text, doc.document.export_to_markdown()
