"""
LaTeX/Overleaf Resume Generator Module

This module generates professional LaTeX code for resumes
that can be compiled in Overleaf or any LaTeX environment.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_openai_client() -> OpenAI:
    """Initialize and return OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)


# Professional LaTeX resume template
LATEX_TEMPLATE = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{xcolor}

% Page margins
\geometry{left=0.75in, right=0.75in, top=0.75in, bottom=0.75in}

% Colors for RoleColor accents
\definecolor{BuilderColor}{RGB}{59, 130, 246}
\definecolor{EnablerColor}{RGB}{34, 197, 94}
\definecolor{ThriverColor}{RGB}{249, 115, 22}
\definecolor{SupporteeColor}{RGB}{139, 92, 246}

% Section formatting
\titleformat{\section}{\large\bfseries\color{<<ROLE_COLOR>>}}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{12pt}{6pt}

% Remove page numbers
\pagenumbering{gobble}

% Custom commands
\newcommand{\resumeitem}[1]{\item #1}
\newcommand{\rolecolorbadge}[1]{\textcolor{<<ROLE_COLOR>>}{\textbf{[#1]}}}

\begin{document}

% Header
\begin{center}
    {\LARGE\bfseries <<NAME>>}\\[4pt]
    <<CONTACT_INFO>>
\end{center}

% Professional Summary with RoleColor Badge
\section{Professional Summary \rolecolorbadge{<<DOMINANT_ROLE>>}}
<<SUMMARY>>

% Experience
\section{Experience}
<<EXPERIENCE>>

% Skills
\section{Skills}
<<SKILLS>>

% Education
\section{Education}
<<EDUCATION>>

\end{document}
"""


def get_color_for_role(role: str) -> str:
    """Get the LaTeX color name for a RoleColor."""
    colors = {
        "Builder": "BuilderColor",
        "Enabler": "EnablerColor",
        "Thriver": "ThriverColor",
        "Supportee": "SupporteeColor"
    }
    return colors.get(role, "BuilderColor")


def generate_latex_from_resume(
    resume_text: str,
    rewritten_summary: str,
    dominant_role: str,
    scores: Dict[str, float],
    model: str = "gpt-4o-mini"
) -> str:
    """
    Generate complete LaTeX code from resume text.
    
    Args:
        resume_text: Original resume text
        rewritten_summary: The rewritten RoleColor summary
        dominant_role: Dominant RoleColor
        scores: Score distribution
        model: OpenAI model to use
    
    Returns:
        Complete LaTeX code ready for Overleaf
    """
    client = get_openai_client()
    
    # First, extract structured information from resume
    extraction_prompt = f"""Extract the following information from this resume and return as structured text.
If information is not available, provide reasonable placeholder text.

RESUME:
{resume_text}

Return in this EXACT format (use the exact headers):
NAME: [Full name]
CONTACT: [Email | Phone | Location - on one line]
EXPERIENCE: [List each job with bullet points, format: Company - Title (Dates), then bullet points for achievements]
SKILLS: [Comma-separated list of skills]
EDUCATION: [Degree, Institution, Year]

Be concise but complete. Use LaTeX-safe characters (escape special chars like & % $ # _ {{ }})."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a resume parser. Extract information accurately and format for LaTeX."},
                {"role": "user", "content": extraction_prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        extracted = response.choices[0].message.content.strip()
        
        # Parse extracted content
        sections = {}
        current_section = None
        current_content = []
        
        for line in extracted.split('\n'):
            line = line.strip()
            if line.startswith('NAME:'):
                sections['name'] = line.replace('NAME:', '').strip()
            elif line.startswith('CONTACT:'):
                sections['contact'] = line.replace('CONTACT:', '').strip()
            elif line.startswith('EXPERIENCE:'):
                current_section = 'experience'
                content = line.replace('EXPERIENCE:', '').strip()
                if content:
                    current_content.append(content)
            elif line.startswith('SKILLS:'):
                if current_section == 'experience':
                    sections['experience'] = '\n'.join(current_content)
                    current_content = []
                current_section = 'skills'
                content = line.replace('SKILLS:', '').strip()
                if content:
                    current_content.append(content)
            elif line.startswith('EDUCATION:'):
                if current_section == 'skills':
                    sections['skills'] = '\n'.join(current_content)
                    current_content = []
                current_section = 'education'
                content = line.replace('EDUCATION:', '').strip()
                if content:
                    current_content.append(content)
            elif line and current_section:
                current_content.append(line)
        
        # Capture last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        # Generate LaTeX
        latex = LATEX_TEMPLATE
        role_color = get_color_for_role(dominant_role)
        
        latex = latex.replace('<<ROLE_COLOR>>', role_color)
        latex = latex.replace('<<NAME>>', sections.get('name', 'Your Name'))
        latex = latex.replace('<<CONTACT_INFO>>', sections.get('contact', 'email@example.com | (555) 123-4567'))
        latex = latex.replace('<<DOMINANT_ROLE>>', dominant_role)
        latex = latex.replace('<<SUMMARY>>', rewritten_summary)
        
        # Format experience
        exp_text = sections.get('experience', '')
        if exp_text:
            # Convert to LaTeX itemize
            exp_lines = exp_text.split('\n')
            formatted_exp = []
            in_itemize = False
            for line in exp_lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    if not in_itemize:
                        formatted_exp.append(r'\begin{itemize}[leftmargin=*]')
                        in_itemize = True
                    formatted_exp.append(r'\item ' + line.lstrip('-•').strip())
                elif line:
                    if in_itemize:
                        formatted_exp.append(r'\end{itemize}')
                        in_itemize = False
                    formatted_exp.append(r'\textbf{' + line + '}\\\\')
            if in_itemize:
                formatted_exp.append(r'\end{itemize}')
            latex = latex.replace('<<EXPERIENCE>>', '\n'.join(formatted_exp))
        else:
            latex = latex.replace('<<EXPERIENCE>>', 'Experience details here')
        
        # Format skills
        skills_text = sections.get('skills', 'Skills here')
        latex = latex.replace('<<SKILLS>>', skills_text)
        
        # Format education
        edu_text = sections.get('education', 'Education details here')
        latex = latex.replace('<<EDUCATION>>', edu_text)
        
        return latex
        
    except Exception as e:
        return f"% Error generating LaTeX: {str(e)}\n{LATEX_TEMPLATE}"


def generate_simple_latex(
    name: str,
    contact: str,
    summary: str,
    dominant_role: str
) -> str:
    """Generate a simple LaTeX template with just the summary."""
    role_color = get_color_for_role(dominant_role)
    
    latex = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{xcolor}

\geometry{left=0.75in, right=0.75in, top=0.75in, bottom=0.75in}

\definecolor{RoleColor}{RGB}{<<RGB>>}

\titleformat{\section}{\large\bfseries\color{RoleColor}}{}{0em}{}[\titlerule]
\pagenumbering{gobble}

\begin{document}

\begin{center}
    {\LARGE\bfseries <<NAME>>}\\[4pt]
    <<CONTACT>>
\end{center}

\section{Professional Summary}
\textcolor{RoleColor}{\textbf{[<<ROLE>>]}} <<SUMMARY>>

\section{Experience}
% Add your experience here

\section{Skills}
% Add your skills here

\section{Education}
% Add your education here

\end{document}
"""
    
    rgb_values = {
        "Builder": "59, 130, 246",
        "Enabler": "34, 197, 94",
        "Thriver": "249, 115, 22",
        "Supportee": "139, 92, 246"
    }
    
    latex = latex.replace('<<RGB>>', rgb_values.get(dominant_role, "59, 130, 246"))
    latex = latex.replace('<<NAME>>', name)
    latex = latex.replace('<<CONTACT>>', contact)
    latex = latex.replace('<<ROLE>>', dominant_role)
    latex = latex.replace('<<SUMMARY>>', summary)
    
    return latex


def validate_latex_syntax(latex_code: str) -> tuple[bool, list[str]]:
    """
    Perform basic syntax validation on LaTeX code.
    
    Args:
        latex_code: LaTeX code to validate
    
    Returns:
        Tuple of (is_valid, list of issues found)
    """
    issues = []
    
    # Check for basic document structure
    if r'\documentclass' not in latex_code:
        issues.append("Missing \\documentclass declaration")
    
    if r'\begin{document}' not in latex_code:
        issues.append("Missing \\begin{document}")
    
    if r'\end{document}' not in latex_code:
        issues.append("Missing \\end{document}")
    
    # Check for balanced braces (basic check)
    open_braces = latex_code.count('{')
    close_braces = latex_code.count('}')
    if open_braces != close_braces:
        issues.append(f"Unbalanced braces: {open_braces} opening vs {close_braces} closing")
    
    # Check for balanced begin/end environments
    import re
    begins = re.findall(r'\\begin\{(\w+)\}', latex_code)
    ends = re.findall(r'\\end\{(\w+)\}', latex_code)
    
    begin_counts = {}
    for env in begins:
        begin_counts[env] = begin_counts.get(env, 0) + 1
    
    end_counts = {}
    for env in ends:
        end_counts[env] = end_counts.get(env, 0) + 1
    
    for env in set(list(begin_counts.keys()) + list(end_counts.keys())):
        b_count = begin_counts.get(env, 0)
        e_count = end_counts.get(env, 0)
        if b_count != e_count:
            issues.append(f"Unbalanced environment '{env}': {b_count} begins vs {e_count} ends")
    
    return (len(issues) == 0, issues)


def edit_latex_with_ai(
    current_latex: str,
    user_request: str,
    model: str = "gpt-4o-mini"
) -> str:
    """
    Edit LaTeX code based on user's chat request.
    
    Args:
        current_latex: Current LaTeX code
        user_request: User's modification request
        model: OpenAI model to use
    
    Returns:
        Modified LaTeX code
    """
    client = get_openai_client()
    
    system_prompt = """You are a LaTeX expert. You help modify resume LaTeX code based on user requests.

RULES:
1. Return ONLY the complete modified LaTeX code
2. Maintain proper LaTeX syntax
3. Keep the document compilable
4. Preserve the overall structure unless asked to change it
5. Do not add explanations, just return the LaTeX code"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Current LaTeX:\n```latex\n{current_latex}\n```\n\nUser request: {user_request}\n\nReturn the modified LaTeX:"}
            ],
            temperature=0.3,
            max_tokens=2500
        )
        result = response.choices[0].message.content.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if result.startswith('```'):
            lines = result.split('\n')
            result = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])
        
        return result
    except Exception as e:
        return f"% Error editing LaTeX: {str(e)}\n{current_latex}"


if __name__ == "__main__":
    # Test simple LaTeX generation
    latex = generate_simple_latex(
        name="John Doe",
        contact="john@example.com | (555) 123-4567 | New York, NY",
        summary="Strategic software engineer with a focus on building scalable systems...",
        dominant_role="Builder"
    )
    print(latex)
