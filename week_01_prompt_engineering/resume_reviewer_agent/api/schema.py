from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class ResumeReviewRequest(BaseModel):
    resume_path: str
    job_description: Optional[str] = None

class ResumeReviewResponse(BaseModel):
    analysis_results: Dict[str, Any]
    report: str

class ResumeReviewChatRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None
