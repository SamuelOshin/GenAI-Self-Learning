"""
Resume Reviewer Agent

This is the main application file for the Resume Reviewer Agent.
"""

import os
import argparse
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging
import anthropic
import requests

# Import utilities
from utils.parser import extract_resume_text, extract_resume_sections, extract_keywords
from api.service import ResumeReviewService

# Configure logging at the top-level of the module
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

# Load environment variables
load_dotenv()

# Configuration from environment variables
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
ANTHROPIC_MAX_TOKENS = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4000"))

API_URL = "http://localhost:8000/api/review"

class ResumeReviewer:
    """Main class for the Resume Reviewer Agent."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Resume Reviewer Agent.
        
        Args:
            api_key: Optional API key for the LLM service. If not provided, will try to get from environment.        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        # Use a module-level logger for consistency
        self.logger = logging.getLogger(__name__)
        self.service = ResumeReviewService(api_key=self.api_key)
        if not self.api_key:
            self.logger.warning("No API key provided. The agent will not work without a valid API key.")

    def review_resume(self, resume_path: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """Review a resume and generate feedback.
        
        Args:
            resume_path: Path to the resume file (PDF or DOCX)
            job_description: Optional job description to compare against
            
        Returns:
            Dictionary containing analysis results
        """
        self.logger.info(f"Reviewing resume: {resume_path}")
        resume_text = extract_resume_text(resume_path)
        sections = extract_resume_sections(resume_text)
        analysis_results = self.service.analyze_resume(sections)
        if job_description:
            job_match = self.service.analyze_job_match(sections, job_description)
            analysis_results["job_match"] = job_match
        return analysis_results

    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a markdown report from analysis results using LLM feedback prompt."""
        self.logger.info("Generating report from analysis results...")
        return self.service.generate_report(analysis_results)

# --- Helper Functions ---
# (Streamlit UI and related helpers have been moved to streamlit_app.py)

def extract_text_from_pdf(file) -> str:
    import PyPDF2
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def get_feedback_via_api(resume_text, job_title=None, messages=None):
    """
    Get resume feedback using Anthropic Claude (non-streaming version).
    """
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Prepare system prompt
        system_prompt = """You are a professional resume reviewer and writer with 15+ years of experience. 
        Provide specific, actionable feedback that helps candidates pass ATS screening and impress recruiters."""
        
        if job_title:
            system_prompt += f"\n\nTarget role: {job_title}"
        
        system_prompt += f"\n\nResume to review:\n{resume_text}"
        
        # Prepare messages
        if messages:
            conversation = messages.copy()
        else:
            conversation = [{
                "role": "user", 
                "content": "Please provide a comprehensive resume analysis with specific improvement suggestions."
            }]
          # Get response
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=ANTHROPIC_MAX_TOKENS,
            system=system_prompt,
            messages=conversation
        )
        
        return response.content[0].text, []
        
    except Exception as e:
        return f"[Error] Unable to connect to AI service: {str(e)}", []

def get_feedback_via_api_streaming(resume_text, job_title=None, messages=None):
    """
    Stream responses directly from Anthropic Claude for better user experience.
    """
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Prepare the conversation
        if messages:
            conversation = messages.copy()
        else:
            conversation = []
        
        # Add system context if not already present
        system_prompt = """You are a professional resume reviewer and writer with 15+ years of experience. \
        Provide specific, actionable feedback that helps candidates pass ATS screening and impress recruiters.\
        Focus on concrete improvements rather than generic advice."""
        
        if job_title:
            system_prompt += f"\n\nThe candidate is targeting: {job_title}"
        
        system_prompt += f"\n\nResume to review:\n{resume_text}"
        
        # If no messages, this is the initial analysis
        if not messages:
            conversation.append({
                "role": "user", 
                "content": "Please provide a comprehensive resume analysis with specific improvement suggestions."
            })
        with client.messages.stream(
            model=ANTHROPIC_MODEL,
            max_tokens=ANTHROPIC_MAX_TOKENS,
            system=system_prompt,
            messages=conversation
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk 
    except Exception as e:
        yield f"[Error] Unable to connect to AI service: {str(e)}"

def main():
    """Main function for running the Resume Reviewer Agent from command line."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Resume Reviewer Agent')
    parser.add_argument('resume_path', help='Path to the resume file (PDF or DOCX)')
    parser.add_argument('--job', '-j', help='Path to a job description file')
    parser.add_argument('--output', '-o', help='Path to save the output markdown report')
    args = parser.parse_args()
    
    # Check if resume file exists
    if not os.path.isfile(args.resume_path):
        print(f"Error: Resume file not found at {args.resume_path}")
        return
    
    # Initialize the resume reviewer
    reviewer = ResumeReviewer()
    
    # Read job description if provided
    job_description = None
    if args.job and os.path.isfile(args.job):
        with open(args.job, 'r') as f:
            job_description = f.read()
    
    # Review the resume
    analysis_results = reviewer.review_resume(args.resume_path, job_description)
    
    # Generate the report
    report = reviewer.generate_report(analysis_results)
    
    # Save or print the report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    import sys
    # Prevent CLI main() from running under Streamlit
    if not (
        "streamlit" in sys.argv[0].lower() or
        os.environ.get("STREAMLIT_RUN_CONTEXT")
    ):
        main()
