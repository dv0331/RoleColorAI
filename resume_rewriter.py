"""
Resume Summary Rewriter Module

This module uses OpenAI's API to rewrite resume summaries
based on the dominant RoleColor identified in the scoring.

Approach:
1. Take the original resume text and RoleColor scores
2. Generate a rewritten summary emphasizing the dominant RoleColor traits
3. Use specific prompts tailored to each RoleColor
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from rolecolor_framework import get_rolecolor_descriptions

# Load environment variables
load_dotenv()


def get_openai_client() -> OpenAI:
    """Initialize and return OpenAI client.
    
    Supports both Streamlit Cloud secrets and local .env files.
    """
    api_key = None
    
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            api_key = st.secrets['OPENAI_API_KEY']
    except Exception:
        pass
    
    # Fall back to environment variable
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Set it in .env file or Streamlit secrets.")
    return OpenAI(api_key=api_key)


def get_rolecolor_prompt(role: str) -> str:
    """Get the writing style prompt for each RoleColor."""
    prompts = {
        "Builder": """
Write in a visionary, strategic tone. Emphasize:
- Innovation and creation of new systems/solutions
- Strategic thinking and long-term vision
- Architecture and scalable design
- Leadership in driving change and growth
Use words like: architect, innovate, strategic, vision, scalable, transform, pioneer, build
""",
        "Enabler": """
Write in a collaborative, supportive tone. Emphasize:
- Team collaboration and cross-functional work
- Communication and stakeholder management
- Mentoring and empowering others
- Bridging gaps and facilitating alignment
Use words like: collaborate, facilitate, mentor, coordinate, cross-functional, stakeholder, enable, align
""",
        "Thriver": """
Write in a dynamic, results-driven tone. Emphasize:
- Ability to deliver under pressure
- Adaptability and quick pivots
- Strong ownership and accountability
- Meeting and exceeding deadlines
Use words like: deliver, adapt, ownership, fast-paced, deadline, achieve, proactive, dynamic
""",
        "Supportee": """
Write in a reliable, methodical tone. Emphasize:
- Consistency and dependability
- Process documentation and standards
- Quality assurance and compliance
- System maintenance and stability
Use words like: reliable, consistent, maintain, document, quality, compliance, systematic, thorough
"""
    }
    return prompts.get(role, prompts["Builder"])


def rewrite_summary(
    resume_text: str,
    dominant_role: str,
    scores: Dict[str, float],
    original_summary: Optional[str] = None,
    model: str = "gpt-4o-mini"
) -> str:
    """
    Rewrite the resume summary based on the dominant RoleColor.
    
    Args:
        resume_text: Full resume text
        dominant_role: The dominant RoleColor from scoring
        scores: Score distribution
        original_summary: Optional original summary to enhance
        model: OpenAI model to use
    
    Returns:
        Rewritten summary (4-6 lines)
    """
    client = get_openai_client()
    
    role_descriptions = get_rolecolor_descriptions()
    style_prompt = get_rolecolor_prompt(dominant_role)
    
    # Build the prompt
    system_prompt = f"""You are an expert resume writer specializing in highlighting 
team contribution styles. You help candidates present their experience through 
the lens of their natural team role.

The candidate's dominant RoleColor is: {dominant_role}
RoleColor Description: {role_descriptions[dominant_role]}

Score Distribution:
{chr(10).join(f"- {role}: {score:.0%}" for role, score in sorted(scores.items(), key=lambda x: x[1], reverse=True))}

Writing Style Guidelines:
{style_prompt}

IMPORTANT RULES:
1. Write exactly 4-6 lines (sentences)
2. Be specific and concrete, not generic
3. Highlight achievements and impact
4. Use active voice and strong action verbs
5. Maintain professional tone
6. Do NOT use buzzwords without substance
7. Keep the technical/domain context from the original
"""

    user_prompt = f"""Based on the following resume, write a compelling professional summary 
that emphasizes the candidate's {dominant_role} traits.

RESUME:
{resume_text}

{f"ORIGINAL SUMMARY TO ENHANCE: {original_summary}" if original_summary else ""}

Write the new summary (4-6 lines):"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def enhance_with_chat(
    resume_text: str,
    current_summary: str,
    user_feedback: str,
    dominant_role: str,
    model: str = "gpt-4o-mini"
) -> str:
    """
    Enhance the summary based on user feedback through chat.
    
    Args:
        resume_text: Original resume text
        current_summary: Current generated summary
        user_feedback: User's feedback or request
        dominant_role: The dominant RoleColor
        model: OpenAI model to use
    
    Returns:
        Updated summary based on feedback
    """
    client = get_openai_client()
    
    system_prompt = f"""You are an expert resume writer. You're helping refine a resume summary.
The candidate's dominant RoleColor is: {dominant_role}

Current Summary:
{current_summary}

Original Resume:
{resume_text}

RULES:
1. Apply the user's feedback while maintaining the {dominant_role} tone
2. Keep the summary to 4-6 lines
3. Maintain professional quality
4. Be specific and concrete
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please update the summary based on this feedback: {user_feedback}"}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error updating summary: {str(e)}"


if __name__ == "__main__":
    # Test the rewriter
    sample_resume = """
    Software Engineer with 2 years of experience in backend development and APIs.
    Worked on Python and Node.js projects. Built REST APIs and worked with databases.
    """
    
    sample_scores = {
        "Builder": 0.45,
        "Enabler": 0.25,
        "Thriver": 0.20,
        "Supportee": 0.10
    }
    
    print("Original Resume:")
    print(sample_resume)
    print("\n" + "=" * 50)
    print("Rewritten Summary (Builder-focused):")
    print("=" * 50)
    
    summary = rewrite_summary(
        resume_text=sample_resume,
        dominant_role="Builder",
        scores=sample_scores
    )
    print(summary)
