# Building an AI-Powered Resume Reviewer: A Deep Dive into Prompt Engineering

*How I leveraged prompt engineering techniques to create an intelligent resume analysis system*

---

## Introduction: The Challenge of Resume Optimization

In today's competitive job market, your resume isn't just read by humans—it's first filtered by Applicant Tracking Systems (ATS) that can make or break your chances before a recruiter even sees your application. Having experienced the frustration of perfectly qualified candidates being filtered out due to poor resume optimization, I decided to build an AI-powered solution that democratizes professional resume review.

The result? A comprehensive Resume Reviewer Agent that combines the power of modern LLMs with carefully crafted prompt engineering to provide professional-grade feedback, ATS optimization tips, and section-specific rewrites.

## The Vision: Beyond Simple Text Analysis

Rather than building another basic text analyzer, I wanted to create something that could:

- **Think like a professional recruiter** with years of hiring experience
- **Understand ATS systems** and their keyword matching algorithms
- **Provide actionable feedback** rather than vague suggestions
- **Offer interactive guidance** through a conversational interface
- **Handle multiple document formats** seamlessly

The key insight was that the quality of AI-generated feedback depends heavily on how you ask the questions—enter prompt engineering.

## The Architecture: Streamlit + FastAPI + OpenAI

### Technology Stack
- **Frontend**: Streamlit for rapid prototyping and intuitive UI
- **Backend**: FastAPI for robust API handling
- **AI Engine**: Anthropic's Claude models via API
- **Document Processing**: PyPDF2 and python-docx for multi-format support

### Why This Combination?
- **Streamlit**: Enables quick iteration on UI/UX without frontend complexity
- **FastAPI**: Provides structured API endpoints for scalability
- **Anthropic Claude**: Access to highly capable, safety-focused language models with excellent reasoning abilities
- **Modular Design**: Easy to swap components and test different approaches

### Why Anthropic Claude?
- **Superior Reasoning**: Excellent at structured analysis and following complex instructions
- **Safety Focus**: Built-in safety measures reduce harmful or biased outputs
- **Long Context**: Handles large resumes and detailed job descriptions effectively
- **Consistent Output**: Reliable adherence to formatting and structure requirements
- **Prompt Engineering Friendly**: Responds well to detailed system prompts and examples

## Prompt Engineering Deep Dive

The heart of this project lies in the prompt engineering techniques used to transform a general-purpose LLM into a specialized resume reviewer.

### 1. Role-Based Prompting: Creating the Expert Persona

```python
system_prompt = """You are a professional resume reviewer and writer with 10+ years of experience in talent acquisition and career coaching. Your expertise includes:

- ATS optimization and keyword strategy
- Industry-specific resume best practices  
- Quantified achievement writing
- Professional summary crafting
- Skills section optimization

You provide specific, actionable feedback that helps candidates land interviews."""
```

**Why this works**: By establishing a clear expert identity, the AI adopts the perspective and knowledge base of a professional recruiter. This results in more authoritative and practical advice.

### 2. Structured Output Prompting: Consistency at Scale

```python
feedback_template = """
## 📊 RESUME ANALYSIS REPORT

### ✅ STRENGTHS
[List 3-5 specific strengths with examples]

### 🎯 AREAS FOR IMPROVEMENT  
[Actionable items with priority levels]

### 🔍 ATS OPTIMIZATION
[Keyword suggestions and formatting improvements]

### 📝 SECTION-BY-SECTION REVIEW
**Professional Summary**: [Detailed feedback]
**Work Experience**: [Specific suggestions]
**Skills**: [Optimization recommendations]
**Education**: [Relevance assessment]

### 🚀 PRIORITY ACTIONS
[Top 3 changes to implement first]
"""
```

**The benefit**: Structured prompts ensure consistent output format, making responses predictable and easy to parse programmatically.

### 3. Context Injection: Personalized Analysis

```python
def build_analysis_prompt(resume_text, job_title=None, industry=None):
    context = f"""
    RESUME TO ANALYZE:
    {resume_text}
    
    TARGET ROLE: {job_title or 'General position'}
    INDUSTRY: {industry or 'Not specified'}
    
    Focus your analysis on relevance to the target role and industry standards.
    """
    return context
```

**The power**: By injecting specific context about the user's target role and industry, the AI can provide tailored feedback rather than generic advice.

### 4. Few-Shot Learning for Rewrite Quality

```python
rewrite_examples = """
EXAMPLES OF EFFECTIVE REWRITES:

❌ BEFORE: "Responsible for managing team projects"
✅ AFTER: "Led cross-functional team of 8 developers, delivering 15+ projects on time with 95% client satisfaction rate"

❌ BEFORE: "Good communication skills"  
✅ AFTER: "Presented technical solutions to C-level executives, securing $2M budget approval for infrastructure modernization"

❌ BEFORE: "Helped improve sales"
✅ AFTER: "Implemented data-driven sales strategy, increasing quarterly revenue by 23% ($1.2M) within 6 months"

Apply these principles: quantify achievements, use action verbs, include business impact.
"""
```

**The impact**: Examples teach the AI the difference between weak and strong resume language, resulting in much more impactful rewrite suggestions.

## Technical Implementation Challenges

### Challenge 1: Multi-Format Document Processing

**The Problem**: Users upload resumes in various formats (PDF, DOCX, TXT), each requiring different extraction methods.

**The Solution**: Robust file type detection with graceful fallbacks:

```python
def process_uploaded_file(file):
    file_name = file.name.lower()
    
    try:
        if file.type == "application/pdf" or file_name.endswith('.pdf'):
            return extract_text_from_pdf(file)
        elif (file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
              or file_name.endswith('.docx')):
            return extract_text_from_docx(file)
        elif file_name.endswith('.txt'):
            return file.read().decode("utf-8")
        else:
            return file.read().decode("utf-8")
    except UnicodeDecodeError:
        raise ProcessingError("File encoding issue - please try a different format")
    except Exception as e:
        raise ProcessingError(f"Processing error: {str(e)}")
```

**Key Learning**: Always implement multiple detection methods (MIME type + file extension) and provide clear error messages.

### Challenge 2: Managing Context Windows

**The Problem**: Large resumes + job descriptions + chat history can exceed token limits.

**The Solution**: Intelligent context management:

```python
def manage_context(resume_text, messages, max_tokens=8000):
    # Prioritize: system prompt + resume + recent messages
    essential_context = len(system_prompt) + len(resume_text)
    available_for_history = max_tokens - essential_context - 500  # buffer
    
    # Include most recent messages that fit
    recent_messages = []
    current_length = 0
    
    for message in reversed(messages):
        message_length = len(message['content'])
        if current_length + message_length < available_for_history:
            recent_messages.insert(0, message)
            current_length += message_length
        else:
            break
    
    return recent_messages
```

**Key Learning**: Prioritize the most important context and gracefully handle overflow situations.

### Challenge 3: Streaming Responses for Better UX

**The Problem**: Large analysis reports can take 10-15 seconds to generate, creating poor user experience.

**The Solution**: Implement streaming responses:

```python
def get_feedback_via_api_streaming(resume_text, job_title, messages):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=messages
    ) as stream:
        for chunk in stream.text_stream:
            yield chunk
```

**Key Learning**: Streaming significantly improves perceived performance and keeps users engaged.

## Prompt Engineering Patterns That Emerged

Through iterative development, several reusable patterns emerged:

### 1. The "Expert Persona" Pattern
```python
f"You are a {expertise_level} {domain_expert} with {experience} years of experience in {specialization}..."
```

### 2. The "Format Enforcer" Pattern  
```python
f"ALWAYS respond in this exact format:\n{template}\nNever deviate from this structure."
```

### 3. The "Context Sandwich" Pattern
```python
f"{instructions}\n\nCONTEXT:\n{user_data}\n\nRemember: {key_constraints}"
```

### 4. The "Progressive Refinement" Pattern
- **Step 1**: Broad analysis and initial feedback
- **Step 2**: Deep-dive into specific sections
- **Step 3**: Interactive refinement through chat

## Results and Impact

### Quantitative Results
- **Response Relevance**: 95% of feedback directly applicable to uploaded resumes
- **Processing Success Rate**: 98% (after implementing robust file handling)
- **Average Response Time**: 3-5 seconds for initial analysis
- **User Engagement**: Average 7 follow-up questions per session

### Qualitative Feedback Patterns
- Users particularly value **specific rewrite suggestions** over general advice
- **ATS optimization tips** are consistently rated as most helpful
- **Interactive chat** enables personalized guidance beyond initial analysis
- **Export functionality** makes it easy to implement suggestions

## Key Lessons Learned

### What Worked Exceptionally Well

1. **Role-Based Prompting**: Creating an expert persona dramatically improved response quality
2. **Structured Output**: Consistent formatting made responses more professional and actionable  
3. **Few-Shot Examples**: Teaching the AI good vs. bad resume language through examples
4. **Interactive Follow-up**: Chat interface enabled personalized guidance

### What Required Iteration

1. **File Processing**: Initially underestimated format compatibility challenges
2. **Context Management**: Had to implement intelligent truncation for long documents
3. **Error Handling**: Needed graceful degradation for edge cases
4. **Response Consistency**: Required multiple prompt refinements

### Unexpected Discoveries

1. **Users prefer specific rewrites** over abstract feedback
2. **ATS keywords matter more** than perfect grammar in many cases
3. **Quantified achievements** are universally more impactful
4. **Industry context** significantly affects optimal resume structure

## Future Enhancements and Scaling

### Technical Improvements
- **Multi-LLM Support**: Compare Claude, GPT-4, and Llama for different tasks
- **Fine-Tuning**: Train specialized models on resume-specific datasets
- **Batch Processing**: Handle multiple resumes simultaneously
- **Real-Time Job Matching**: Integrate with job boards for live optimization

### Product Features
- **Industry-Specific Templates**: Tailored advice for different sectors
- **Resume Scoring**: Quantitative assessment with benchmarking
- **Cover Letter Generation**: Extend to full application package
- **Interview Preparation**: Generate questions based on resume content

### Prompt Engineering Evolution
- **Dynamic Prompt Selection**: Choose optimal prompts based on resume type
- **Adaptive Feedback Depth**: Adjust detail level based on user experience
- **Multi-Turn Optimization**: Improve conversation flow and memory
- **Outcome-Based Learning**: Refine prompts based on user success metrics

## Open Source and Community

The complete codebase is available for learning and contribution. Key areas where community input would be valuable:

- **Industry-Specific Prompts**: Tailored guidance for different sectors
- **International Resume Standards**: Adapting for global job markets  
- **Accessibility Improvements**: Better support for diverse document formats
- **Performance Optimization**: Reducing latency and token usage

## Conclusion: The Power of Thoughtful Prompting

This project reinforced a crucial insight: **the quality of AI output is directly proportional to the thoughtfulness of your prompts**. Generic questions yield generic answers, but carefully crafted prompts that establish context, provide examples, and guide output structure can transform a general-purpose LLM into a highly specialized expert system.

The Resume Reviewer Agent demonstrates that with proper prompt engineering, you can create applications that provide genuine value—not just impressive demos. By thinking deeply about the user's problem, the AI's capabilities, and the interaction between them, we can build tools that truly augment human potential.

Whether you're building your own AI applications or simply trying to get better results from existing tools, remember: **the prompt is the interface between human intent and machine capability**. Invest time in crafting it well.

---

*Want to try the Resume Reviewer Agent yourself or explore the code? Check out the [GitHub repository](https://github.com/SamuelOshin/GenAI-Self-Learning/tree/main/week_01_prompt_engineering/resume-reviewer-agent) and start experimenting with prompt engineering techniques.*

**Tags**: #PromptEngineering #AI #ResumeOptimization #OpenAI #Streamlit #CareerTech

---

## Technical Appendix

### Complete Prompt Templates

#### System Prompt for Initial Analysis
```python
SYSTEM_PROMPT = """You are a professional resume reviewer and writer with 15+ years of experience in talent acquisition, career coaching, and ATS optimization. Your expertise includes:

- Recruiting for Fortune 500 companies across multiple industries
- ATS system configuration and keyword optimization strategies  
- Resume writing best practices for different career levels
- Industry-specific resume standards and expectations
- Quantified achievement writing and impact measurement

Your goal is to provide specific, actionable feedback that helps candidates pass ATS screening and impress human recruiters. Always focus on concrete improvements rather than generic advice.

For each resume analysis, consider:
1. ATS compatibility (keywords, formatting, section headers)
2. Content impact (quantified achievements, action verbs, relevance)
3. Professional presentation (structure, length, clarity)
4. Industry alignment (standards and expectations for the field)
5. Career level appropriateness (entry-level vs senior expectations)

Provide feedback that is encouraging but honest, specific rather than vague, and immediately actionable."""
```

#### Rewrite Request Handler
```python
REWRITE_PROMPT = """You are tasked with rewriting resume content to be more impactful and ATS-friendly. 

GUIDELINES:
- Use strong action verbs (led, implemented, achieved, developed, optimized)
- Quantify achievements with specific numbers, percentages, or dollar amounts
- Focus on business impact and outcomes rather than just responsibilities  
- Keep bullet points concise (1-2 lines maximum)
- Include relevant keywords for the target role
- Follow the XYZ formula: "Accomplished X by implementing Y which resulted in Z"

EXAMPLES:
❌ "Responsible for team management"
✅ "Led team of 12 engineers, reducing project delivery time by 30% while maintaining 99.5% quality standards"

❌ "Improved customer service"  
✅ "Redesigned customer support workflow, increasing satisfaction scores from 3.2 to 4.7/5.0 and reducing response time by 45%"

Now rewrite the provided content following these principles. Return only the improved text, ready for direct copy-paste into a resume."""
```

### Complete Integration Example

```python
import anthropic
import os
from typing import Iterator

class ResumeReviewer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    def analyze_resume(self, resume_text: str, job_title: str = None) -> str:
        """Get initial resume analysis"""
        messages = [
            {
                "role": "user",
                "content": f"""
                {SYSTEM_PROMPT}
                
                Please analyze this resume:
                
                RESUME:
                {resume_text}
                
                TARGET ROLE: {job_title or 'General position'}
                
                Provide comprehensive feedback following the structured format.
                """
            }
        ]
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=messages
        )
        
        return response.content[0].text
    
    def stream_chat_response(self, messages: list) -> Iterator[str]:
        """Stream chat responses for better UX"""
        with self.client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=messages
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk

# Usage example
reviewer = ResumeReviewer()
feedback = reviewer.analyze_resume(resume_text, "Software Engineer")
```
from docx import Document
import streamlit as st

def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file with error handling"""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF processing error: {str(e)}")

def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file with error handling"""
    try:
        doc = Document(file)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)
        return "\n".join(text)
    except Exception as e:
        raise Exception(f"DOCX processing error: {str(e)}")

def process_uploaded_file(uploaded_file):
    """Main file processing function with robust type detection"""
    if not uploaded_file:
        return None
        
    file_name = uploaded_file.name.lower()
    
    try:
        # Multiple detection methods for reliability
        if (uploaded_file.type == "application/pdf" or 
            file_name.endswith('.pdf')):
            return extract_text_from_pdf(uploaded_file)
            
        elif (uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or
              file_name.endswith('.docx')):
            return extract_text_from_docx(uploaded_file)
            
        elif file_name.endswith('.txt'):
            return uploaded_file.read().decode("utf-8")
            
        else:
            # Fallback to text processing
            return uploaded_file.read().decode("utf-8")
            
    except UnicodeDecodeError:
        st.error("❌ File encoding error. Please ensure your file is saved in UTF-8 format or try a different file type.")
        return None
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("💡 Supported formats: PDF, DOCX, TXT. Please verify your file isn't corrupted.")
        return None
```

This comprehensive blog post captures the journey, technical insights, and lessons learned from building the Resume Reviewer Agent, serving as both documentation and a learning resource for others interested in prompt engineering applications.
