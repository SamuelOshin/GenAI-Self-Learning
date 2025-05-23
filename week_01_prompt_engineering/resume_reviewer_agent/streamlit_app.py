"""
Streamlit UI for Resume Reviewer Agent
"""

import os
import streamlit as st
import anthropic
import requests
from utils.parser import extract_resume_text, extract_resume_sections, extract_keywords
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment variables
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
ANTHROPIC_MAX_TOKENS = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4000"))

API_URL = "http://localhost:8000/api/review"

# --- Helper Functions ---
def extract_text_from_pdf(file) -> str:
    import PyPDF2
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file) -> str:
    from docx import Document
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def create_feedback_docx(messages, job_title="General Review"):
    """Create a formatted DOCX document with AI feedback only, with improved heading/bullet detection"""
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    import io
    from datetime import datetime
    
    doc = Document()
    # Set document margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    # Add title
    title = doc.add_heading('Resume Review Feedback Report', 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # Add subtitle with job title and date
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    if job_title and job_title.strip():
        subtitle.add_run(f"Target Position: {job_title}\n").bold = True
    subtitle.add_run(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    # Add separator line
    doc.add_paragraph("_" * 60).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    doc.add_paragraph()  # Empty line
    # Filter AI responses only (exclude system messages)
    ai_responses = [msg for msg in messages if msg["role"] == "assistant"]
    for i, msg in enumerate(ai_responses, 1):
        # Add section heading
        if i == 1:
            doc.add_heading('📋 Initial Resume Analysis', level=1)
        else:
            doc.add_heading(f'💬 Follow-up Response {i-1}', level=1)
        content = msg["content"].strip()
        # Split content by double newlines to identify sections
        sections = [s for s in content.split('\n\n') if s.strip()]
        for section in sections:
            lines = [line.strip() for line in section.split('\n') if line.strip()]
            # If only one line and not a bullet, treat as heading
            if len(lines) == 1:
                line = lines[0]
                if (not line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')) 
                    and not line.endswith(':') 
                    and not line.isupper()):
                    doc.add_heading(line, level=2)
                    continue
            # If all lines are bullets, treat as bullet list
            if all(l.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')) for l in lines):
                for line in lines:
                    clean_line = line.lstrip('•-*123456789. ').strip()
                    if clean_line:
                        doc.add_paragraph(clean_line, style='List Bullet')
                continue
            # If first line is a heading, treat as heading + paragraph
            if lines and (lines[0].endswith(':') or lines[0].isupper()):
                doc.add_heading(lines[0].replace(':','').strip(), level=2)
                if len(lines) > 1:
                    doc.add_paragraph(' '.join(lines[1:]))
                continue
            # Otherwise, treat as paragraph
            doc.add_paragraph(' '.join(lines))
        # Add spacing between major sections
        if i < len(ai_responses):
            doc.add_paragraph()
            doc.add_paragraph("─" * 40).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            doc.add_paragraph()
    # Add footer
    doc.add_page_break()
    footer_para = doc.add_paragraph()
    footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    footer_run = footer_para.add_run("Generated by Resume Reviewer Agent")
    footer_run.italic = True
    footer_run.font.size = Pt(10)
    # Save to bytes buffer
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def get_feedback_via_api(resume_text, job_title=None, messages=None):
    response = requests.post(
        API_URL,
        json={"resume_path": "", "job_description": job_title or "", "resume_text": resume_text, "messages": messages or []}
    )
    if response.status_code == 200:
        data = response.json()
        return data["report"], []
    else:
        return f"[API Error: {response.status_code}] {response.text}", []

def reset_session():
    for key in ["resume_text", "job_title", "messages", "initial_feedback"]:
        if key in st.session_state:
            del st.session_state[key]

# --- Streamlit UI ---
st.set_page_config(page_title="Resume Reviewer Agent", page_icon="📝", layout="wide")
st.title("📝 Resume Reviewer Agent")
st.markdown("""
Upload your resume, get instant AI-powered feedback, and chat for personalized advice!
""")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

with st.sidebar:
    st.header("Options")
    if st.button("Start Over", use_container_width=True):
        reset_session()
        st.rerun()
    st.markdown("---")
    st.info("Your data is processed securely and not stored.")

# --- File Upload ---
resume_file = st.file_uploader("Upload your resume (.pdf, .txt, or .docx)", type=["pdf", "txt", "docx"])
if resume_file:
    file_name = resume_file.name.lower()
    
    try:
        if resume_file.type == "application/pdf" or file_name.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_file)
        elif (resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
              or file_name.endswith('.docx')):
            resume_text = extract_text_from_docx(resume_file)
        elif file_name.endswith('.txt'):
            resume_text = resume_file.read().decode("utf-8")
        else:
            # Fallback for other text files
            resume_text = resume_file.read().decode("utf-8")
        
        st.session_state["resume_text"] = resume_text
        st.subheader("📄 Resume Preview")
        st.text_area("Extracted Resume Text", resume_text, height=200)
        
    except UnicodeDecodeError:
        st.error("❌ Error reading file. Please make sure you've uploaded a valid PDF, DOCX, or TXT file.")
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("💡 Make sure you have the required libraries installed: `pip install python-docx PyPDF2`")

    job_title = st.text_input("Target Job Title (optional)", value=st.session_state.get("job_title", ""))
    st.session_state["job_title"] = job_title

    if "initial_feedback" not in st.session_state and st.button("Get Initial Review", use_container_width=True):
        with st.spinner("Analyzing your resume..."):
            feedback, history = get_feedback_via_api(resume_text, job_title)
            st.session_state["initial_feedback"] = feedback
            st.session_state["messages"] = [
                {"role": "system", "content": f"Resume: {resume_text}\nJob Title: {job_title}"},
                {"role": "assistant", "content": feedback}
            ]

if "initial_feedback" in st.session_state:
    st.subheader("🧠 Initial Review")
    st.chat_message("assistant").write(st.session_state["initial_feedback"])

    # --- Chat Interface ---
    st.subheader("💬 Ask Follow-up Questions")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask a follow-up about your resume or request a rewrite suggestion (e.g., 'Rewrite my professional summary to be more impactful and ATS-friendly')...")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            enhanced_messages = st.session_state["messages"][:]
            enhanced_messages.insert(0, {
                "role": "system",
                "content": (
                    "You are a professional resume reviewer and writer. "
                    "For each section or feedback, provide specific, ATS-compliant rewrite suggestions. "
                    "If the user requests, rewrite the section in a way that is concise, impactful, and tailored for applicant tracking systems (ATS). "
                    "Use bullet points, quantify achievements, and use action verbs. "
                    "If the user asks for a rewrite, return only the improved text for direct copy-paste into the CV."
                )
            })
            # Streaming response
            response_placeholder = st.empty()
            streamed_text = ""
            from app import get_feedback_via_api_streaming
            try:
                for partial in get_feedback_via_api_streaming(
                    st.session_state["resume_text"],
                    st.session_state.get("job_title"),
                    enhanced_messages
                ):
                    streamed_text += partial  
                    response_placeholder.markdown(streamed_text)
                st.session_state["messages"].append({"role": "assistant", "content": streamed_text})
                st.chat_message("assistant").write(streamed_text)
            except Exception as e:
                st.error(f"❌ Streaming failed: {str(e)}. Please check your Anthropic API key and network connection.")

    # --- Export Feedback ---
    st.markdown("---")
    if st.button("📄 Export Feedback as DOCX", use_container_width=True):
        try:
            # Use the sophisticated helper function to create formatted DOCX
            docx_data = create_feedback_docx(
                st.session_state["messages"], 
                st.session_state.get("job_title", "General Review")
            )
            
            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_feedback_{timestamp}.docx"
            
            st.download_button(
                label="💾 Download Feedback Report",
                data=docx_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            
            st.success("✅ Document ready for download! Click the button above to save your formatted feedback report.")
            
        except Exception as e:
            st.error(f"❌ Error creating document: {str(e)}")
            st.info("💡 Make sure you have python-docx installed: `pip install python-docx`")
