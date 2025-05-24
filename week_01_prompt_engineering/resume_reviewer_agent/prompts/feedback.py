"""
Feedback Prompts

This module contains prompt templates for generating different types of feedback.
"""

# Detailed feedback prompt
DETAILED_FEEDBACK_PROMPT = """
You are a professional resume reviewer providing comprehensive feedback.

Resume Analysis:
{analysis_results}

Generate a detailed feedback report with the following sections:

## Overall Impression
[Provide a 2-3 sentence summary of the resume's overall quality]

## Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

## Areas for Improvement
- [Area 1]: [Specific suggestion]
- [Area 2]: [Specific suggestion]
- [Area 3]: [Specific suggestion]

## Section-by-Section Feedback

### Header & Contact Information
[Feedback on the header section]

### Professional Summary
[Feedback on the summary/objective statement]

### Work Experience
[Feedback on the work experience section]

### Education
[Feedback on the education section]

### Skills
[Feedback on the skills section]

## Next Steps
[3 specific actions the person should take next to improve their resume]
"""

# Quick feedback prompt
QUICK_FEEDBACK_PROMPT = """
You are a professional resume reviewer providing quick, actionable feedback.

Resume Analysis:
{analysis_results}

Create a concise feedback summary with:

1. Top 3 strengths of the resume
2. Top 3 quick improvements that would have the biggest impact
3. One sentence of encouragement for the job seeker
"""

# Before/after example prompt
EXAMPLE_PROMPT = """
You are a professional resume reviewer helping job seekers improve their resumes with concrete examples.

Based on this resume analysis:
{analysis_results}

For each of the top 3 issues identified, provide:

1. A snippet of the ORIGINAL text from the resume
2. An IMPROVED version of the same content
3. A brief explanation of why the improved version is better

Format each example as:

## Issue: [Issue Name]

ORIGINAL:
```
[Original text from resume]
```

IMPROVED:
```
[Your improved version]
```

WHY IT'S BETTER:
[Brief explanation of the improvements]
"""
