"""
Resume RoleColor Scoring Module

This module provides functionality to score resumes across the four RoleColors
using keyword presence and weighted scoring.

Scoring Algorithm:
1. Normalize and tokenize the resume text
2. For each RoleColor, check keyword presence
3. Apply weights to found keywords
4. Normalize scores to get a distribution (sum = 1.0)
"""

import re
from collections import defaultdict
from typing import Dict, List, Tuple
from rolecolor_framework import ROLECOLOR_KEYWORDS


def preprocess_text(text: str) -> str:
    """
    Preprocess resume text for analysis.
    
    Steps:
    1. Convert to lowercase
    2. Normalize whitespace
    3. Keep hyphens for compound words (e.g., cross-functional)
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def find_keyword_matches(text: str, keywords: Dict[str, float]) -> List[Tuple[str, float, int]]:
    """
    Find all keyword matches in text.
    
    Returns list of (keyword, weight, count) tuples.
    """
    matches = []
    text_lower = text.lower()
    
    for keyword, weight in keywords.items():
        # Use word boundary matching for more accurate results
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        count = len(re.findall(pattern, text_lower))
        if count > 0:
            matches.append((keyword, weight, count))
    
    return matches


def calculate_role_score(text: str, keywords: Dict[str, float]) -> Tuple[float, List[Tuple[str, float, int]]]:
    """
    Calculate score for a single RoleColor.
    
    Returns:
        Tuple of (total_score, list of matches)
    """
    matches = find_keyword_matches(text, keywords)
    
    # Calculate weighted score
    # Score = sum of (weight * count) for each matched keyword
    # Apply diminishing returns for repeated keywords
    total_score = 0.0
    for keyword, weight, count in matches:
        # First occurrence gets full weight, subsequent get diminishing
        score = weight * (1 + 0.3 * (min(count, 5) - 1))  # Cap at 5 occurrences
        total_score += score
    
    return total_score, matches


def score_resume(resume_text: str) -> Dict[str, any]:
    """
    Score a resume across all four RoleColors.
    
    Returns:
        Dictionary containing:
        - scores: Normalized score distribution
        - raw_scores: Raw (unnormalized) scores
        - matches: Keyword matches for each RoleColor
        - dominant_role: The RoleColor with highest score
    """
    preprocessed = preprocess_text(resume_text)
    
    raw_scores = {}
    all_matches = {}
    
    # Calculate scores for each RoleColor
    for role, keywords in ROLECOLOR_KEYWORDS.items():
        score, matches = calculate_role_score(preprocessed, keywords)
        raw_scores[role] = score
        all_matches[role] = matches
    
    # Normalize scores to sum to 1.0
    total = sum(raw_scores.values())
    
    if total == 0:
        # No keywords found, return equal distribution
        normalized_scores = {role: 0.25 for role in ROLECOLOR_KEYWORDS.keys()}
    else:
        normalized_scores = {role: score / total for role, score in raw_scores.items()}
    
    # Find dominant role
    dominant_role = max(normalized_scores, key=normalized_scores.get)
    
    return {
        "scores": normalized_scores,
        "raw_scores": raw_scores,
        "matches": all_matches,
        "dominant_role": dominant_role,
        "total_keywords_matched": sum(len(m) for m in all_matches.values())
    }


def format_score_output(result: Dict) -> str:
    """Format scoring results for display."""
    output = []
    output.append("=" * 50)
    output.append("ROLECOLOR SCORE DISTRIBUTION")
    output.append("=" * 50)
    
    # Sort by score descending
    sorted_scores = sorted(result["scores"].items(), key=lambda x: x[1], reverse=True)
    
    for role, score in sorted_scores:
        bar_length = int(score * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        output.append(f"{role:10} [{bar}] {score:.2%}")
    
    output.append("")
    output.append(f"Dominant RoleColor: {result['dominant_role']}")
    output.append(f"Total keywords matched: {result['total_keywords_matched']}")
    
    output.append("")
    output.append("-" * 50)
    output.append("KEYWORD MATCHES BY ROLECOLOR")
    output.append("-" * 50)
    
    for role, matches in result["matches"].items():
        if matches:
            output.append(f"\n{role}:")
            sorted_matches = sorted(matches, key=lambda x: x[1] * x[2], reverse=True)[:5]
            for keyword, weight, count in sorted_matches:
                output.append(f"  • {keyword} (×{count}, weight: {weight})")
    
    return "\n".join(output)


def get_score_summary(result: Dict) -> str:
    """Get a brief score summary."""
    lines = []
    for role, score in sorted(result["scores"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"{role}: {score:.2f}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample resume
    sample_resume = """
    Senior Software Engineer with 5 years of experience in building scalable 
    backend systems and APIs. Led a team of 4 engineers to architect and develop 
    a microservices platform that handles 10M+ daily transactions.
    
    Key achievements:
    - Designed and implemented a real-time data processing pipeline using Kafka
    - Collaborated with cross-functional teams to deliver features on tight deadlines
    - Mentored junior developers and established coding standards
    - Maintained 99.9% uptime for production systems through proactive monitoring
    - Spearheaded the migration to cloud infrastructure, reducing costs by 40%
    
    Skills: Python, Go, AWS, Kubernetes, PostgreSQL, Redis
    """
    
    result = score_resume(sample_resume)
    print(format_score_output(result))
