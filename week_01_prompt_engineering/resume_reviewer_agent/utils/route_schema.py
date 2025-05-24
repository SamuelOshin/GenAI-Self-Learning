"""
Routing and schema utilities for Resume Reviewer Agent (FastAPI-ready example)
"""

from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, Form

# Pydantic schema for resume review request
class ResumeReviewRequest(BaseModel):
    resume_path: str
    job_description: Optional[str] = None

class ResumeReviewResponse(BaseModel):
    analysis_results: dict
    report: str

# FastAPI router for resume review endpoints
def get_resume_router(service):
    router = APIRouter()

    @router.post("/review", response_model=ResumeReviewResponse)
    async def review_resume(
        resume_path: str = Form(...),
        job_description: Optional[str] = Form(None)
    ):
        analysis_results = service.review_resume(resume_path, job_description)
        report = service.generate_report(analysis_results)
        return ResumeReviewResponse(analysis_results=analysis_results, report=report)

    # Example for file upload (if needed)
    @router.post("/review-upload", response_model=ResumeReviewResponse)
    async def review_resume_upload(
        resume: UploadFile = File(...),
        job_description: Optional[str] = Form(None)
    ):
        # Save file temporarily, then pass path to service
        temp_path = f"/tmp/{resume.filename}"
        with open(temp_path, "wb") as f:
            f.write(await resume.read())
        analysis_results = service.review_resume(temp_path, job_description)
        report = service.generate_report(analysis_results)
        return ResumeReviewResponse(analysis_results=analysis_results, report=report)

    return router
