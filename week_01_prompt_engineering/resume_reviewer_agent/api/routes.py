from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from typing import Optional, List, Dict, Any
from .schema import ResumeReviewRequest, ResumeReviewResponse
from .service import ResumeReviewService
import os
import tempfile
from pydantic import BaseModel

router = APIRouter()
service = ResumeReviewService()

class ResumeReviewChatRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None

@router.post("/review", response_model=ResumeReviewResponse)
def review_resume(request: ResumeReviewChatRequest):
    try:
        # Use resume_text directly if provided, else fallback to file path logic
        resume_text = request.resume_text
        job_title = request.job_description
        messages = request.messages or []
        # If chat history is provided, use it for context (prompt chaining)
        # For now, just use the latest user message as a follow-up
        # You can expand this logic to use the full chat history in your prompt templates
        analysis_results = service.review_resume_text(resume_text, job_title, messages)
        report = service.generate_report(analysis_results)
        return ResumeReviewResponse(analysis_results=analysis_results, report=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/review-upload", response_model=ResumeReviewResponse)
def review_resume_upload(resume: UploadFile = File(...), job_description: Optional[str] = Form(None)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume.filename)[-1]) as tmp:
            tmp.write(resume.file.read())
            tmp_path = tmp.name
        analysis_results = service.review_resume(tmp_path, job_description)
        report = service.generate_report(analysis_results)
        os.remove(tmp_path)
        return ResumeReviewResponse(analysis_results=analysis_results, report=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
