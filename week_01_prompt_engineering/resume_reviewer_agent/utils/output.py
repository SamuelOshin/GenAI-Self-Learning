"""
Output Utilities

This module provides utilities for formatting and presenting feedback output.
"""

from typing import Dict, Any, List, Tuple

def format_overall_score(score: int) -> str:
    """
    Format an overall resume score with a visual indicator.
    
    Args:
        score: Resume score from 0-100
        
    Returns:
        Formatted score string with visual indicator
    """
    if score >= 90:
        return f"📈 {score}/100 - Excellent!"
    elif score >= 80:
        return f"👍 {score}/100 - Very Good"
    elif score >= 70:
        return f"👌 {score}/100 - Good"
    elif score >= 60:
        return f"🔍 {score}/100 - Needs Some Improvements"
    else:
        return f"⚠️ {score}/100 - Needs Significant Improvements"

def format_section_feedback(section_name: str, assessment: str, issues: List[str], suggestions: List[str]) -> str:
    """
    Format feedback for a specific resume section.
    
    Args:
        section_name: Name of the section (e.g., "Work Experience")
        assessment: Assessment level (e.g., "Strong", "Needs Improvement")
        issues: List of identified issues
        suggestions: List of improvement suggestions
        
    Returns:
        Formatted section feedback
    """
    # Determine emoji based on assessment
    emoji = "✅" if assessment == "Strong" else "⚠️" if assessment == "Needs Improvement" else "📝"
    
    # Build the feedback string
    feedback = f"## {emoji} {section_name}: {assessment}\n\n"
    
    if issues:
        feedback += "**Issues:**\n"
        for issue in issues:
            feedback += f"- {issue}\n"
        feedback += "\n"
    
    if suggestions:
        feedback += "**Suggestions:**\n"
        for suggestion in suggestions:
            feedback += f"- {suggestion}\n"
        feedback += "\n"
    
    return feedback

def format_job_match_analysis(match_percentage: int, missing_skills: List[str], 
                            emphasis_points: List[str], suggested_keywords: List[str]) -> str:
    """
    Format the job match analysis results.
    
    Args:
        match_percentage: Estimated match percentage (0-100%)
        missing_skills: Skills/requirements missing from the resume
        emphasis_points: Points that should be emphasized more
        suggested_keywords: Keywords that should be incorporated
        
    Returns:
        Formatted job match analysis
    """
    # Determine emoji based on match percentage
    if match_percentage >= 80:
        match_emoji = "🎯"
    elif match_percentage >= 60:
        match_emoji = "👍"
    else:
        match_emoji = "⚠️"
    
    # Build the analysis string
    analysis = f"# Job Match Analysis\n\n"
    analysis += f"{match_emoji} **Match Score:** {match_percentage}%\n\n"
    
    if missing_skills:
        analysis += "## Missing Skills/Requirements\n"
        for skill in missing_skills:
            analysis += f"- {skill}\n"
        analysis += "\n"
    
    if emphasis_points:
        analysis += "## Emphasize These Points\n"
        for point in emphasis_points:
            analysis += f"- {point}\n"
        analysis += "\n"
    
    if suggested_keywords:
        analysis += "## Suggested Keywords to Include\n"
        for keyword in suggested_keywords:
            analysis += f"- {keyword}\n"
        analysis += "\n"
    
    return analysis

def generate_markdown_report(analysis_results: Dict[str, Any]) -> str:
    """
    Generate a complete markdown report from analysis results.
    
    Args:
        analysis_results: Dictionary containing all analysis results
        
    Returns:
        Complete markdown report
    """
    report = "# Resume Analysis Report\n\n"
    
    # Add overall score
    report += f"## Overall Assessment\n\n"
    report += format_overall_score(analysis_results.get("overall_score", 0))
    report += "\n\n"
    
    # Add section feedback
    for section in ["structure", "summary", "experience", "education", "skills"]:
        if section in analysis_results:
            data = analysis_results[section]
            report += format_section_feedback(
                data.get("name", section.title()),
                data.get("assessment", ""),
                data.get("issues", []),
                data.get("suggestions", [])
            )
    
    # Add job match analysis if available
    if "job_match" in analysis_results:
        report += format_job_match_analysis(
            analysis_results["job_match"].get("match_percentage", 0),
            analysis_results["job_match"].get("missing_skills", []),
            analysis_results["job_match"].get("emphasis_points", []),
            analysis_results["job_match"].get("suggested_keywords", [])
        )
    
    # Add next steps
    if "next_steps" in analysis_results:
        report += "## Next Steps\n\n"
        for i, step in enumerate(analysis_results["next_steps"], 1):
            report += f"{i}. {step}\n"
    
    return report
