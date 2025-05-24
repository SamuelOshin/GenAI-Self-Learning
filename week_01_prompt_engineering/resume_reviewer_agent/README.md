# Resume Reviewer Agent 📝

An AI-powered resume reviewer that provides comprehensive feedback, suggestions, and rewrite recommendations. Built with Streamlit for an interactive web interface and FastAPI for robust backend processing.

## ✨ Features

### Core Functionality
- **Multi-format Support**: Upload PDF, DOCX, or TXT resume files
- **Intelligent Parsing**: Extract text content from various document formats
- **AI-Powered Analysis**: Comprehensive resume review using Anthropic's Claude models
- **ATS Optimization**: Feedback tailored for Applicant Tracking Systems
- **Interactive Chat**: Follow-up questions and personalized advice
- **Rewrite Suggestions**: Specific section improvements and rewrites

### What Gets Analyzed
- Resume structure and formatting
- Content clarity and impact
- Keyword optimization for ATS
- Professional summary effectiveness
- Work experience descriptions
- Skills presentation
- Common resume mistakes
- Job-specific customization recommendations

## 🚀 How to Use

### Prerequisites
- Python 3.8 or higher
- Anthropic API key

### Installation

1. **Clone or download the project**
   ```powershell
   cd "c:\Users\PC\Documents\AI Learning Path&Project\week_01_prompt_engineering\resume_reviewer_agent"
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
    **Create a virtual environment**
      ```powershell
      python -m venv venv
      .\venv\Scripts\activate
      ```

      If you're using macOS or Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
3. **Set up environment variables**
   Copy the example environment file and configure it:
   ```powershell
   cp .env.example .env
   ```
   
   Edit the `.env` file with your settings:
   ```
   # Required: Your Anthropic API key
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   
   # Optional: Model configuration (defaults shown)
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ANTHROPIC_MAX_TOKENS=4000
   ```

### Exporting Feedback as DOCX

You can now export your AI-generated resume feedback as a professionally formatted DOCX file directly from the Streamlit interface:

- After uploading your resume and receiving feedback, click the **"📄 Export Feedback as DOCX"** button.
- The exported document includes only the AI's responses, with clear section headings and bullet points for easy reading and direct use.
- Headings and bullet points are automatically detected and formatted for a clean, professional look.

**Example workflow:**
1. Upload your resume (PDF, DOCX, or TXT)
2. Click **Get Initial Review**
3. (Optional) Chat with the AI for follow-up questions or rewrite suggestions
4. Click **📄 Export Feedback as DOCX** to download your feedback report

The exported file is ready for sharing or further editing in Microsoft Word or Google Docs.

### Running the Application

#### Option 1: Streamlit Web Interface (Recommended)
```powershell
streamlit run streamlit_app.py
```
- Open your browser to `http://localhost:8501`
- Upload your resume (PDF, DOCX, or TXT)
- Optionally enter a target job title
- Get instant AI feedback and chat for follow-ups

#### Option 2: FastAPI Backend + Frontend
```powershell
# Terminal 1 - Start the API server
python main.py

# Terminal 2 - Start the Streamlit frontend
streamlit run streamlit_app.py
```

### Usage Steps
1. **Upload Resume**: Drag and drop or select your resume file
2. **Add Job Title** (Optional): Enter the target position for tailored feedback
3. **Get Initial Review**: Click to receive comprehensive analysis
4. **Interactive Chat**: Ask follow-up questions or request specific rewrites
5. **Export Feedback**: Download your feedback as a text file

## ⚙️ Configuration

### Environment Variables

The application supports the following configuration options through environment variables:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `ANTHROPIC_API_KEY` | **Required.** Your Anthropic API key | - | `sk-ant-api03-...` |
| `ANTHROPIC_MODEL` | Claude model to use | `claude-3-5-sonnet-20241022` | `claude-3-haiku-20240307` |
| `ANTHROPIC_MAX_TOKENS` | Maximum tokens per response | `4000` | `2000` |

### Available Models

- **claude-3-5-sonnet-20241022**: Best performance, highest cost
- **claude-3-sonnet-20240229**: Good balance of quality and cost  
- **claude-3-haiku-20240307**: Fastest and most cost-effective

### Token Limits

- Higher `ANTHROPIC_MAX_TOKENS` = longer, more detailed responses but higher cost
- Lower values = more concise responses, faster, cheaper
- Recommended: 2000-4000 for resume reviews

## 🛠 Implementation Details

### Technology Stack
- **Frontend**: Streamlit (Interactive web UI)
- **Backend**: FastAPI (RESTful API)
- **AI Model**: Anthropic Claude (via API)
- **Document Processing**: PyPDF2, python-docx
- **Prompt Engineering**: Custom prompts for resume analysis

### Key Components

#### Document Processing
- **PDF Extraction**: PyPDF2 for reliable text extraction
- **DOCX Processing**: python-docx for Microsoft Word documents
- **Error Handling**: Graceful handling of encoding and format issues

#### AI Analysis Pipeline
- **Resume Parsing**: Extract and structure resume content
- **Contextual Analysis**: Compare against job requirements
- **Feedback Generation**: Structured, actionable recommendations
- **Interactive Chat**: Streaming responses for real-time interaction

#### Prompt Engineering Techniques
- **Few-shot Learning**: Examples of good resume feedback
- **Chain of Thought**: Step-by-step analysis process
- **Role Playing**: AI acts as professional resume reviewer
- **Structured Output**: Consistent feedback format

## 📁 Project Structure

```
resume_reviewer_agent/
│
├── streamlit_app.py        # Main Streamlit web interface
├── app.py                  # Core application logic
├── main.py                 # FastAPI server entry point
├── requirements.txt        # Project dependencies
├── README.md              # This documentation
│
├── api/                   # FastAPI backend
│   ├── routes.py          # API endpoints
│   ├── schema.py          # Data models
│   └── service.py         # Business logic
│
├── prompts/               # AI prompt templates
│   ├── resume_analysis.py # Resume analysis prompts
│   └── feedback.py        # Feedback generation prompts
│
└── utils/                 # Utility functions
    ├── parser.py          # Resume parsing functions
    ├── output.py          # Output formatting
    └── route_schema.py    # API schemas
```

## 🔧 Advanced Features

### Chat Interface
- Ask specific questions about your resume
- Request section rewrites (e.g., "Rewrite my professional summary")
- Get ATS optimization tips
- Receive industry-specific advice

### Export Options
- Download complete feedback as text file
- Copy-paste ready section rewrites
- Structured improvement recommendations

## 🎯 Prompt Engineering Showcase

This project demonstrates several prompt engineering techniques:

1. **System Prompting**: Setting the AI's role as a professional resume reviewer
2. **Context Injection**: Including resume text and job descriptions in prompts
3. **Output Formatting**: Structured feedback with specific sections
4. **Iterative Refinement**: Follow-up prompts for deeper analysis
5. **Task Chaining**: Breaking down resume review into multiple focused tasks

## 🐛 Troubleshooting

### Common Issues

**UnicodeDecodeError when uploading DOCX**
- Ensure you have `python-docx` installed
- The app now handles this gracefully with proper error messages

**API Connection Issues**
- Check your Anthropic API key in `.env` file
- Ensure you have internet connectivity
- Verify API quota and billing

**File Upload Problems**
- Supported formats: PDF, DOCX, TXT
- Maximum file size depends on Streamlit settings
- Try converting complex PDFs to simpler formats

## 📈 Future Enhancements

- [ ] Multiple LLM provider support (OpenAI GPT, Llama)
- [ ] Resume template suggestions
- [ ] Industry-specific optimization
- [ ] Batch processing for multiple resumes
- [ ] Integration with job boards for real-time matching
- [ ] Resume scoring and benchmarking

## Future Enhancements

- Add support for more file formats
- Implement industry-specific feedback
- Create a web interface with Streamlit
- Add visualization of resume strengths/weaknesses
