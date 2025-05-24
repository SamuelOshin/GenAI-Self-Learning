import logging
import anthropic
from typing import Dict, Any, Optional
from prompts.resume_analysis import MAIN_ANALYSIS_PROMPT, JOB_MATCH_PROMPT, FEEDBACK_PROMPT
from utils.parser import extract_resume_text, extract_resume_sections
import os
from dotenv import load_dotenv

logger = logging.getLogger("resume_reviewer")

class ResumeReviewService:
    def __init__(self, api_key: Optional[str] = None):
        # Try to load from environment if not provided
        if api_key is None:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("ANTHROPIC_API_KEY")
        self.api_key = api_key
        if not self.api_key:
            logger.warning("No API key provided. The agent will not work without a valid API key.")
        
        # Load model configuration from environment variables
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4000"))

    def call_llm(self, prompt: str, model: str = None, temperature: float = 0.2, messages: Optional[list] = None) -> str:
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            system_prompt = "You are a helpful, expert resume reviewer."
            
            # Use instance model if no model specified, otherwise use provided model
            model_to_use = model if model is not None else self.model
            
            if messages:
                # Anthropic expects a single system prompt and a list of messages
                response = client.messages.create(
                    model=model_to_use,
                    max_tokens=self.max_tokens,
                    system=system_prompt,
                    messages=messages
                )
                return response.content[0].text if hasattr(response, 'content') else response.completion
            else:
                messages = [{"role": "user", "content": prompt}]
                response = client.messages.create(
                    model=model_to_use,
                    max_tokens=self.max_tokens,
                    system=system_prompt,
                    messages=messages
                )
                return response.content[0].text if hasattr(response, 'content') else response.completion
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "[LLM Error: Unable to generate response.]"

    def analyze_resume(self, sections: Dict[str, str]) -> Dict[str, Any]:
        logger.info("Analyzing resume sections with LLM...")
        resume_content = "\n".join([f"{k.title()}: {v}" for k, v in sections.items()])
        prompt = MAIN_ANALYSIS_PROMPT.format(resume_content=resume_content)
        response = self.call_llm(prompt)
        return {"llm_analysis": response}

    def analyze_job_match(self, sections: Dict[str, str], job_description: str) -> Dict[str, Any]:
        logger.info("Analyzing job match with LLM...")
        resume_content = "\n".join([f"{k.title()}: {v}" for k, v in sections.items()])
        prompt = JOB_MATCH_PROMPT.format(resume_content=resume_content, job_description=job_description)
        response = self.call_llm(prompt)
        return {"llm_job_match": response}

    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        logger.info("Generating report with LLM feedback prompt...")
        prompt = FEEDBACK_PROMPT.format(analysis_results=analysis_results)
        response = self.call_llm(prompt)
        return response

    def review_resume_text(self, resume_text: str, job_title: Optional[str] = None, messages: Optional[list] = None) -> Dict[str, Any]:
        logger.info("Reviewing resume text with LLM (raw text + chat history support)...")
        # If chat history is provided, use it for prompt chaining
        if messages:
            # Always ensure the resume text is in the system prompt
            if not any(m["role"] == "system" for m in messages):
                system_prompt = f"You are a professional resume reviewer. Here is the candidate's resume:\n---\n{resume_text}\n---"
                if job_title:
                    system_prompt += f"\nThe candidate is targeting the job title: {job_title}."
                system_prompt += "\nProvide a tone assessment, strengths, weaknesses, suggestions for improvement, and optionally rewrite weak sections."
                messages.insert(0, {"role": "system", "content": system_prompt})
            response = self.call_llm("", messages=messages)
            return {"llm_analysis": response}
        else:
            # Fallback to single-shot prompt
            system_prompt = f"You are a professional resume reviewer. Here is the candidate's resume:\n---\n{resume_text}\n---"
            if job_title:
                system_prompt += f"\nThe candidate is targeting the job title: {job_title}."
            system_prompt += "\nProvide a tone assessment, strengths, weaknesses, suggestions for improvement, and optionally rewrite weak sections."
            response = self.call_llm(system_prompt)
            return {"llm_analysis": response}
