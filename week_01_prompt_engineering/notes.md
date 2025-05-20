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
