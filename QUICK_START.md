# GenAI Pinnacle+ Quick Start Guide

This guide will help you quickly set up and run the different projects in this learning path.

## 📋 Prerequisites

Before starting, make sure you have:

1. **Python 3.9+** installed on your system
2. **Git** for version control
3. A **code editor** like VS Code
4. **API keys** for services like OpenAI, Hugging Face, etc.

## 🚀 Setup Instructions

### 1. Clone the repository (if using version control)

```bash
git clone <your-repo-url>
cd genai-pinnacleplus
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root by copying the template:

```bash
cp .env.template .env
# Now edit .env and add your API keys
```

## 🧩 Running the Projects

### Week 1: Prompt Engineering

1. **Prompt Playground**:
   Open the notebook in Jupyter or VS Code:
   ```bash
   jupyter notebook week_01_prompt_engineering/prompt_playground.ipynb
   ```

2. **Resume Reviewer Agent**:
   ```bash
   cd week_01_prompt_engineering/resume_reviewer_agent
   pip install -r requirements.txt
   python app.py path/to/resume.pdf --job path/to/job_description.txt
   ```

### Week 2: Python & ML

1. **NumPy & Pandas Notebook**:
   ```bash
   jupyter notebook week_02_python_ml/numpy_pandas.ipynb
   ```

2. **Titanic Project**:
   ```bash
   cd week_02_python_ml/mini_project_titanic
   python model.py
   ```

### Week 4: LangChain

```bash
cd week_04_langchain
jupyter notebook langchain_basics.ipynb
```

### Week 5: RAG Systems

```bash
cd week_05_rag
jupyter notebook rag_basics.ipynb
```

### Week 6: AI Agents

```bash
cd week_06_agents
jupyter notebook react_agents.ipynb
```

### Week 8: Deployment

1. **FastAPI App**:
   ```bash
   cd week_08_deployment
   uvicorn fastapi_app:app --reload
   ```

2. **Streamlit App**:
   ```bash
   cd week_08_deployment
   streamlit run streamlit_app.py
   ```

## 📚 Resources

- [GenAI Pinnacle+ Curriculum PDF](./GenAI_Pinnacle_Plus_Projects.pdf)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [OpenAI Documentation](https://platform.openai.com/docs/)
- [Hugging Face Documentation](https://huggingface.co/docs)

## 🔍 Troubleshooting

- **API Key Issues**: Make sure you have correctly set up your .env file
- **Package Errors**: Check that you have installed all requirements with `pip install -r requirements.txt`
- **Runtime Errors**: Ensure you're running the code within the virtual environment

For more help, check the README files in each project directory.
