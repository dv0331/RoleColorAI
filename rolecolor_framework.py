"""
RoleColor Keyword Framework

This module defines the keyword mappings for each RoleColor trait.
The four RoleColors represent different ways people contribute to teams:

- Builder: Drive innovation, vision, and strategy
- Enabler: Connect people, execute plans, and bridge gaps  
- Thriver: Perform under pressure and adapt quickly
- Supportee: Ensure reliability, consistency, and stability

Keyword Selection Rationale:
----------------------------
1. BUILDER keywords focus on:
   - Strategic thinking (strategy, vision, roadmap)
   - Innovation and creation (innovate, architect, design)
   - Leadership and direction (lead, pioneer, transform)
   - Long-term thinking (scalable, future-proof, growth)

2. ENABLER keywords focus on:
   - Collaboration (collaborate, coordinate, facilitate)
   - Communication (communicate, mentor, stakeholder)
   - Cross-functional work (cross-functional, bridge, integrate)
   - Team support (support, enable, empower)

3. THRIVER keywords focus on:
   - Speed and urgency (fast-paced, deadline, agile)
   - Adaptability (adapt, pivot, flexible)
   - Ownership (ownership, accountability, initiative)
   - Pressure handling (high-pressure, urgent, challenging)

4. SUPPORTEE keywords focus on:
   - Reliability (reliable, consistent, stable)
   - Maintenance (maintain, monitor, ensure)
   - Documentation (document, process, procedure)
   - Quality assurance (quality, accuracy, compliance)
"""

# RoleColor keyword definitions with weights
# Higher weights indicate stronger signal for that RoleColor

ROLECOLOR_KEYWORDS = {
    "Builder": {
        # Strategic keywords
        "strategy": 1.5,
        "strategic": 1.5,
        "vision": 1.5,
        "visionary": 1.5,
        "roadmap": 1.3,
        "architecture": 1.4,
        "architect": 1.4,
        
        # Innovation keywords
        "innovate": 1.5,
        "innovation": 1.5,
        "innovative": 1.4,
        "create": 1.0,
        "created": 1.0,
        "design": 1.2,
        "designed": 1.2,
        "develop": 1.0,
        "developed": 1.0,
        "build": 1.2,
        "built": 1.2,
        
        # Leadership keywords
        "lead": 1.3,
        "led": 1.3,
        "pioneer": 1.5,
        "pioneered": 1.5,
        "transform": 1.4,
        "transformed": 1.4,
        "spearhead": 1.4,
        "spearheaded": 1.4,
        
        # Growth keywords
        "scalable": 1.3,
        "scale": 1.2,
        "scaled": 1.2,
        "growth": 1.3,
        "expand": 1.2,
        "expanded": 1.2,
        "future-proof": 1.3,
        
        # Technical leadership
        "system": 1.0,
        "platform": 1.1,
        "framework": 1.2,
        "foundation": 1.2,
        "initiative": 1.2,
    },
    
    "Enabler": {
        # Collaboration keywords
        "collaborate": 1.5,
        "collaborated": 1.5,
        "collaboration": 1.5,
        "collaborative": 1.4,
        "coordinate": 1.4,
        "coordinated": 1.4,
        "coordination": 1.4,
        "facilitate": 1.5,
        "facilitated": 1.5,
        
        # Communication keywords
        "communicate": 1.3,
        "communicated": 1.3,
        "communication": 1.3,
        "present": 1.1,
        "presented": 1.1,
        "stakeholder": 1.4,
        "stakeholders": 1.4,
        
        # Cross-functional keywords
        "cross-functional": 1.5,
        "cross functional": 1.5,
        "bridge": 1.3,
        "bridged": 1.3,
        "integrate": 1.2,
        "integrated": 1.2,
        "integration": 1.2,
        
        # Team support keywords
        "support": 1.2,
        "supported": 1.2,
        "enable": 1.4,
        "enabled": 1.4,
        "empower": 1.4,
        "empowered": 1.4,
        "mentor": 1.5,
        "mentored": 1.5,
        "mentoring": 1.5,
        "coach": 1.4,
        "coached": 1.4,
        
        # Relationship keywords
        "partner": 1.3,
        "partnered": 1.3,
        "partnership": 1.3,
        "align": 1.2,
        "aligned": 1.2,
        "alignment": 1.2,
        "team": 1.0,
        "teams": 1.0,
    },
    
    "Thriver": {
        # Speed keywords
        "fast-paced": 1.5,
        "fast paced": 1.5,
        "rapid": 1.3,
        "rapidly": 1.3,
        "quick": 1.2,
        "quickly": 1.2,
        "accelerate": 1.3,
        "accelerated": 1.3,
        
        # Deadline keywords
        "deadline": 1.4,
        "deadlines": 1.4,
        "on-time": 1.3,
        "on time": 1.3,
        "timely": 1.2,
        
        # Agility keywords
        "agile": 1.4,
        "adapt": 1.4,
        "adapted": 1.4,
        "adaptable": 1.4,
        "pivot": 1.4,
        "pivoted": 1.4,
        "flexible": 1.3,
        "flexibility": 1.3,
        "dynamic": 1.3,
        
        # Ownership keywords
        "ownership": 1.5,
        "own": 1.2,
        "owned": 1.2,
        "accountability": 1.4,
        "accountable": 1.4,
        "initiative": 1.3,
        "proactive": 1.4,
        "proactively": 1.4,
        
        # Pressure keywords
        "high-pressure": 1.5,
        "high pressure": 1.5,
        "pressure": 1.3,
        "urgent": 1.4,
        "urgency": 1.4,
        "challenging": 1.2,
        "challenge": 1.2,
        "challenges": 1.2,
        
        # Results keywords
        "deliver": 1.3,
        "delivered": 1.3,
        "achieve": 1.3,
        "achieved": 1.3,
        "accomplish": 1.3,
        "accomplished": 1.3,
        "exceed": 1.4,
        "exceeded": 1.4,
    },
    
    "Supportee": {
        # Reliability keywords
        "reliable": 1.5,
        "reliability": 1.5,
        "consistent": 1.4,
        "consistency": 1.4,
        "stable": 1.3,
        "stability": 1.3,
        "dependable": 1.5,
        "steady": 1.3,
        
        # Maintenance keywords
        "maintain": 1.4,
        "maintained": 1.4,
        "maintenance": 1.4,
        "monitor": 1.3,
        "monitored": 1.3,
        "monitoring": 1.3,
        "ensure": 1.3,
        "ensured": 1.3,
        "upkeep": 1.3,
        
        # Documentation keywords
        "document": 1.4,
        "documented": 1.4,
        "documentation": 1.5,
        "process": 1.2,
        "processes": 1.2,
        "procedure": 1.4,
        "procedures": 1.4,
        "standard": 1.3,
        "standards": 1.3,
        
        # Quality keywords
        "quality": 1.4,
        "accuracy": 1.4,
        "accurate": 1.4,
        "compliance": 1.5,
        "compliant": 1.5,
        "audit": 1.4,
        "audited": 1.4,
        
        # Support keywords
        "troubleshoot": 1.3,
        "troubleshooting": 1.3,
        "resolve": 1.2,
        "resolved": 1.2,
        "fix": 1.1,
        "fixed": 1.1,
        "debug": 1.2,
        "debugged": 1.2,
        
        # Operations keywords
        "operational": 1.3,
        "operations": 1.2,
        "routine": 1.2,
        "systematic": 1.3,
        "methodical": 1.4,
        "thorough": 1.3,
    }
}


def get_all_keywords():
    """Return all keywords grouped by RoleColor."""
    return ROLECOLOR_KEYWORDS


def get_keywords_for_role(role: str) -> dict:
    """Get keywords for a specific RoleColor."""
    if role not in ROLECOLOR_KEYWORDS:
        raise ValueError(f"Unknown RoleColor: {role}. Must be one of: {list(ROLECOLOR_KEYWORDS.keys())}")
    return ROLECOLOR_KEYWORDS[role]


def get_rolecolor_descriptions() -> dict:
    """Return descriptions for each RoleColor."""
    return {
        "Builder": "Builders drive innovation, vision, and strategy. They create new systems, architect solutions, and think long-term about growth and scalability.",
        "Enabler": "Enablers connect people, execute plans, and bridge gaps. They facilitate collaboration, mentor others, and ensure smooth communication across teams.",
        "Thriver": "Thrivers perform under pressure and adapt quickly. They thrive in fast-paced environments, take ownership, and deliver results against tight deadlines.",
        "Supportee": "Supportees ensure reliability, consistency, and stability. They maintain systems, document processes, and provide the dependable foundation teams need."
    }


if __name__ == "__main__":
    # Print keyword summary
    print("RoleColor Keyword Framework")
    print("=" * 50)
    
    for role, keywords in ROLECOLOR_KEYWORDS.items():
        print(f"\n{role} ({len(keywords)} keywords):")
        print("-" * 30)
        # Show top 10 by weight
        sorted_kw = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        for kw, weight in sorted_kw:
            print(f"  {kw}: {weight}")
