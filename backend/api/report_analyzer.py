"""
API Endpoints for Medical Report Analysis
"""

import logging
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from services.report_analyzer import report_analyzer

logger = logging.getLogger(__name__)

router = APIRouter()


class ReportAnalysisRequest(BaseModel):
    """Request model for report analysis"""

    report_text: str
    patient_id: Optional[str] = None


class ReportAnalysisResponse(BaseModel):
    """Response model for report analysis"""

    success: bool
    summary: Optional[str] = None
    key_findings: Optional[list] = None  # Added for AI analysis
    entities: Optional[dict] = None
    lab_values: Optional[list] = None
    abnormalities: Optional[list] = None
    explanation: Optional[str] = None
    severity: Optional[str] = None
    recommendations: Optional[list] = None
    error: Optional[str] = None


@router.post("/analyze/report", response_model=ReportAnalysisResponse)
async def analyze_report(request: ReportAnalysisRequest):
    """
    Analyze a medical report and return simplified insights

    - **report_text**: The text content of the medical report
    - **patient_id**: Optional patient identifier
    """
    try:
        logger.info(f"📄 Analyzing report (length: {len(request.report_text)} chars)")

        if not request.report_text or len(request.report_text) < 10:
            raise HTTPException(status_code=400, detail="Report text is too short")

        # Analyze the report
        result = report_analyzer.analyze_report(request.report_text)

        if not result["success"]:
            raise HTTPException(
                status_code=500, detail=result.get("error", "Analysis failed")
            )

        return ReportAnalysisResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in report analysis endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/report/file")
async def analyze_report_file(file: UploadFile = File(...)):
    """
    Analyze a medical report from uploaded file (PDF, Image, DOCX, or Text)

    - **file**: Medical report file (PDF, JPG, PNG, DOCX, TXT)

    This endpoint extracts text from the uploaded document and analyzes it
    """
    try:
        logger.info(f"📁 Analyzing uploaded file: {file.filename}")

        # Read file content
        content = await file.read()

        # Use document processor to extract text
        from services.document_processor import document_processor

        try:
            text = await document_processor.extract_text(content, file.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Could not extract meaningful text from the file. Please ensure the file contains readable text.",
            )

        logger.info(f"✅ Extracted {len(text)} characters from {file.filename}")

        # Analyze the report
        result = report_analyzer.analyze_report(text)

        if not result["success"]:
            raise HTTPException(
                status_code=500, detail=result.get("error", "Analysis failed")
            )

        return ReportAnalysisResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in file analysis endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/report/sample")
async def get_sample_analysis():
    """
    Get a sample report analysis for demo purposes
    """
    sample_report = """
    Blood Test Report
    
    Patient: Sample Patient
    Date: November 18, 2025
    
    Test Results:
    Glucose: 145 mg/dL (Normal: 70-100 mg/dL)
    Hemoglobin: 13.5 g/dL (Normal: 13-17 g/dL)
    Cholesterol: 210 mg/dL (Normal: <200 mg/dL)
    WBC: 7.2 K/uL (Normal: 4-11 K/uL)
    
    Diagnosis: Type 2 Diabetes Mellitus, Hyperlipidemia
    Medications: Metformin 500mg twice daily, Atorvastatin 20mg once daily
    """

    result = report_analyzer.analyze_report(sample_report)
    return ReportAnalysisResponse(**result)
