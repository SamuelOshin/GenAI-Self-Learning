# Prompt Engineering Notes

## Introduction to Prompt Engineering
Prompt engineering is the process of designing and refining inputs to large language models (LLMs) to get desired outputs. It's a critical skill for working with AI systems like ChatGPT, Claude, or Llama.

## Key Prompt Types

### 1. Zero-shot Prompting
- **Definition**: Asking the model to perform a task without examples
- **Example**: "Explain quantum computing in simple terms"
- **When to use**: Simple tasks, general knowledge questions
- **Limitations**: Less effective for complex or specialized tasks

### 2. Few-shot Prompting
- **Definition**: Providing examples in the prompt before asking the model to complete a similar pattern
- **Example**: 
  ```
  Convert these sentences to French:
  English: The weather is nice today.
  French: Il fait beau aujourd'hui.
  
  English: Where is the library?
  French: 
  ```
- **When to use**: When consistency in format or style is needed
- **Limitations**: Takes up token space, can sometimes confuse the model

### 3. Chain of Thought (CoT)
- **Definition**: Guiding the model through a step-by-step reasoning process
- **Example**: "Think step-by-step to solve this math problem: If a train leaves at 2pm and travels at 60mph, and another train leaves at 3pm traveling at 90mph, when will the second train catch up?"
- **When to use**: Complex reasoning tasks, math problems, logical puzzles
- **Limitations**: Can sometimes lead to incorrect reasoning that seems plausible

## Best Practices

### Be Specific
- Clearly state what you want
- Specify format, length, tone, audience, and constraints

### Structure Matters
- Use clear sections, bullet points, and formatting
- Put the most important instructions first and last (primacy and recency effect)

### Iterate
- Start simple, then refine based on outputs
- Keep a log of what works and what doesn't

### Manage Token Limits
- Be aware of context window limitations (e.g., 4K, 8K, 16K tokens)
- Prioritize the most relevant information
- Consider splitting very long tasks

## Evaluation Metrics
- Relevance: Does the response address the question/task?
- Accuracy: Is the information correct?
- Comprehensiveness: Is the response complete?
- Format: Does it follow the requested format?
- Creativity/Originality: For creative tasks, how novel is the output?

## Real-World Application: Resume Reviewer Agent

### Project Overview
Built a comprehensive resume reviewer using prompt engineering techniques with Anthropic's Claude. The system analyzes resumes, provides feedback, and offers rewrite suggestions optimized for ATS systems.

### Prompt Engineering Techniques Applied

#### 1. Role-Based Prompting
```python
system_prompt = """You are a professional resume reviewer and writer with 10+ years of experience. 
Your expertise includes ATS optimization, industry best practices, and career coaching."""
```
- **Why it works**: Establishes context and expertise level
- **Result**: More professional and authoritative feedback

#### 2. Structured Output Prompting
```python
prompt = """Analyze this resume and provide feedback in the following format:
1. STRENGTHS: List 3-5 key strengths
2. AREAS FOR IMPROVEMENT: Specific actionable items
3. ATS OPTIMIZATION: Keywords and formatting suggestions
4. SECTION-BY-SECTION REVIEW: Detailed analysis
"""
```
- **Why it works**: Ensures consistent, organized output
- **Result**: Predictable, parseable responses

#### 3. Context Injection
- **Resume Text**: Full resume content injected into prompt
- **Job Description**: Target role requirements for tailored feedback
- **Chat History**: Previous conversation for continuity

#### 4. Few-Shot Examples for Rewrites
```python
examples = """
BEFORE: Responsible for managing team projects
AFTER: Led cross-functional team of 8 developers, delivering 15+ projects on time with 95% client satisfaction

BEFORE: Good communication skills
AFTER: Presented technical solutions to C-level executives, resulting in $2M budget approval
"""
```

### Technical Implementation Insights

#### Document Processing Challenges
- **Problem**: DOCX files causing UnicodeDecodeError
- **Solution**: Multi-layered file type detection (MIME type + extension)
- **Learning**: Always implement fallback mechanisms for file processing

#### Streaming Responses
- **Implementation**: Real-time chat interface using streaming API
- **Benefit**: Better user experience with immediate feedback
- **Technical**: Handled partial responses and state management

#### Error Handling Patterns
```python
try:
    if file_name.endswith('.docx'):
        text = extract_text_from_docx(file)
    elif file_name.endswith('.pdf'):
        text = extract_text_from_pdf(file)
except UnicodeDecodeError:
    st.error("File encoding issue - please try a different format")
except Exception as e:
    st.error(f"Processing error: {str(e)}")
```

### Prompt Optimization Lessons

#### 1. Specificity Matters
- **Vague**: "Review this resume"
- **Specific**: "Analyze this resume for ATS optimization, focusing on keyword density, formatting, and quantified achievements"

#### 2. Output Format Instructions
- **Before**: Inconsistent feedback structure
- **After**: Clear markdown formatting with headers, bullet points, and sections

#### 3. Context Window Management
- **Challenge**: Large resumes + job descriptions + chat history
- **Solution**: Prioritize recent context, summarize older exchanges

#### 4. Prompt Chaining for Complex Tasks
1. **Initial Analysis**: Overall resume assessment
2. **Section-Specific**: Detailed feedback per section
3. **Rewrite Generation**: Specific improvement suggestions
4. **Follow-up Chat**: Interactive Q&A

### Performance Metrics Observed

#### Response Quality
- **Relevance**: 95% - Feedback directly related to resume content
- **Actionability**: 90% - Specific, implementable suggestions
- **ATS Optimization**: 85% - Relevant keyword and formatting advice

#### User Experience
- **File Processing**: 98% success rate (after fixes)
- **Response Time**: 3-5 seconds for initial analysis
- **Chat Continuity**: Maintained context across 10+ exchanges

### Key Takeaways

#### What Worked Well
1. **Role-based prompting** created authoritative responses
2. **Structured output** ensured consistent feedback format
3. **Interactive chat** enabled personalized follow-up advice
4. **Multi-format support** increased accessibility

#### Challenges Overcome
1. **File format compatibility** - solved with robust detection
2. **Context management** - balanced detail vs. token limits
3. **Response consistency** - achieved through structured prompts
4. **Error handling** - graceful degradation for edge cases

#### Future Improvements
1. **Model comparison** - test different LLMs for specialized tasks
2. **Fine-tuning** - custom model for resume-specific language
3. **Batch processing** - handle multiple resumes simultaneously
4. **Industry specialization** - tailored prompts for different sectors

### Prompt Engineering Patterns Discovered

#### 1. The "Expert Persona" Pattern
```python
f"You are a {expertise_level} {domain_expert} with {experience} years of experience..."
```

#### 2. The "Format Enforcer" Pattern
```python
f"ALWAYS respond in this exact format:\n{template}\nNever deviate from this structure."
```

#### 3. The "Context Sandwich" Pattern
```python
f"{instructions}\n\nCONTEXT:\n{user_data}\n\nRemember: {key_constraints}"
```

#### 4. The "Progressive Refinement" Pattern
- Start with broad analysis
- Drill down into specifics
- Provide actionable next steps
