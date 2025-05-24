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
            for partial in get_feedback_via_api_streaming(
                st.session_state["resume_text"],
                st.session_state.get("job_title"),
                enhanced_messages
            ):
                streamed_text = partial
                response_placeholder.markdown(streamed_text)
            st.session_state["messages"].append({"role": "assistant", "content": streamed_text})
            st.chat_message("assistant").write(streamed_text)

    # --- Export Feedback ---
    st.markdown("---")
    if st.button("Export Feedback as .txt", use_container_width=True):
        feedback_text = "\n\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state["messages"]
        ])
        st.download_button(
            label="Download Feedback",
            data=feedback_text,
            file_name="resume_feedback.txt",
            mime="text/plain"
        )
