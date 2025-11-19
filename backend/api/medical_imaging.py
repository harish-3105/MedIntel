"""
Medical Imaging Analysis API
Endpoints for analyzing X-rays, CT scans, and other medical images
"""

import logging
from typing import Dict

from fastapi import APIRouter, File, HTTPException, UploadFile
from services.medical_imaging import medical_imaging_analyzer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze/image")
async def analyze_medical_image(
    file: UploadFile = File(...),
    image_type: str = "xray",
) -> Dict:
    """
    Analyze a medical image (X-ray, CT scan, etc.)

    Args:
        file: Image file (JPEG, PNG)
        image_type: Type of image (xray, ct, mri)

    Returns:
        Analysis results with findings, confidence, and recommendations
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image file (JPEG, PNG).",
            )

        # Read image content
        image_content = await file.read()

        if len(image_content) == 0:
            raise HTTPException(
                status_code=400, detail="Empty file uploaded. Please try again."
            )

        logger.info(
            f"📸 Analyzing {image_type} image: {file.filename} ({len(image_content)} bytes)"
        )

        # Analyze the image
        analysis = await medical_imaging_analyzer.analyze_medical_image(
            image_content, image_type
        )

        logger.info(
            f"✅ Analysis complete: {len(analysis.get('findings', []))} findings"
        )

        return {
            "success": True,
            "filename": file.filename,
            "image_type": image_type,
            "analysis": analysis,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Medical image analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze medical image: {str(e)}",
        )
