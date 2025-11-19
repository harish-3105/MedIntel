"""
OCR and Document Processing Service
Handles extraction of text from images, PDFs, and documents
"""

import logging

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from services.document_processor import document_processor

logger = logging.getLogger(__name__)

router = APIRouter()


class DocumentExtractionResponse(BaseModel):
    """Response model for document text extraction"""

    success: bool
    text: str
    filename: str
    page_count: int = 1
    extraction_method: str
    error: str = None


@router.post("/ocr/extract", response_model=DocumentExtractionResponse)
async def extract_document_text(file: UploadFile = File(...)):
    """
    Extract text from uploaded document (PDF, Image, DOCX, etc.)

    - **file**: Document file (PDF, JPG, PNG, DOCX, TXT)

    Returns extracted text that can be used for medical report analysis
    """
    try:
        logger.info(f"📄 Processing document: {file.filename}")

        # Read file content
        content = await file.read()

        # Extract text using document processor
        extracted_text = await document_processor.extract_text(content, file.filename)

        if not extracted_text or len(extracted_text.strip()) < 10:
            return DocumentExtractionResponse(
                success=False,
                text="",
                filename=file.filename,
                extraction_method="none",
                error="Could not extract meaningful text from document. File may be empty or corrupted.",
            )

        # Determine extraction method
        ext = file.filename.lower().split(".")[-1]
        method_map = {
            "pdf": "PDF text extraction",
            "jpg": "OCR (Image)",
            "jpeg": "OCR (Image)",
            "png": "OCR (Image)",
            "bmp": "OCR (Image)",
            "tiff": "OCR (Image)",
            "docx": "DOCX text extraction",
            "doc": "DOC text extraction",
            "txt": "Plain text",
        }

        extraction_method = method_map.get(ext, "Unknown")

        logger.info(
            f"✅ Successfully extracted {len(extracted_text)} characters from {file.filename}"
        )

        return DocumentExtractionResponse(
            success=True,
            text=extracted_text,
            filename=file.filename,
            extraction_method=extraction_method,
        )

    except ValueError as e:
        logger.error(f"❌ Unsupported file format: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"❌ Processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error in document processing: {e}")
        raise HTTPException(
            status_code=500, detail=f"Document processing failed: {str(e)}"
        )


@router.post("/ocr/prescription")
async def read_prescription(file: UploadFile = File(...)):
    """
    Extract text from prescription image (OCR)
    Legacy endpoint - redirects to /ocr/extract

    - **file**: Image file of prescription
    """
    return await extract_document_text(file)
