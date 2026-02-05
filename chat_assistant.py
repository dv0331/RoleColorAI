"""
Chat Assistant Module

This module provides AI chat functionality for:
1. Answering questions about the RoleColor analysis
2. Helping refine resume summaries
3. Assisting with LaTeX modifications
4. General resume advice
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_openai_client() -> OpenAI:
    """Initialize and return OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)


class ChatAssistant:
    """AI Chat Assistant for RoleColorAI."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = get_openai_client()
        self.model = model
        self.conversation_history: List[Dict] = []
        self.context = {}
        
        self.system_prompt = """You are an AI assistant for RoleColorAI, a resume intelligence system.

Your capabilities:
1. Explain RoleColor analysis results
2. Help refine resume summaries to better reflect specific RoleColors
3. Assist with LaTeX resume modifications
4. Provide general resume writing advice
5. Answer questions about the four RoleColors:
   - Builder: Innovation, vision, strategy, architecture
   - Enabler: Collaboration, coordination, mentoring, bridging gaps
   - Thriver: Fast-paced delivery, adaptability, ownership, deadline-driven
   - Supportee: Reliability, consistency, documentation, maintenance

When helping with resume modifications:
- Be specific and actionable
- Maintain professional tone
- Focus on the dominant RoleColor when relevant
- Suggest concrete changes

When helping with LaTeX:
- Provide exact LaTeX code when needed
- Explain modifications clearly
- Ensure code is syntactically correct

Always be helpful, concise, and focused on improving the user's resume."""

    def set_context(
        self,
        resume_text: Optional[str] = None,
        scores: Optional[Dict] = None,
        summary: Optional[str] = None,
        latex_code: Optional[str] = None
    ):
        """Set the current context for more relevant responses."""
        if resume_text:
            self.context['resume'] = resume_text
        if scores:
            self.context['scores'] = scores
        if summary:
            self.context['summary'] = summary
        if latex_code:
            self.context['latex'] = latex_code

    def _build_context_message(self) -> str:
        """Build a context message from current context."""
        parts = []
        
        if self.context.get('scores'):
            scores_text = ", ".join(
                f"{role}: {score:.0%}" 
                for role, score in sorted(
                    self.context['scores'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
            )
            parts.append(f"Current RoleColor scores: {scores_text}")
            dominant = max(self.context['scores'], key=self.context['scores'].get)
            parts.append(f"Dominant RoleColor: {dominant}")
        
        if self.context.get('summary'):
            parts.append(f"Current summary: {self.context['summary'][:200]}...")
        
        if self.context.get('resume'):
            parts.append(f"Resume length: {len(self.context['resume'])} characters")
        
        if self.context.get('latex'):
            parts.append("LaTeX code is available for modification")
        
        if parts:
            return "\n[Context]\n" + "\n".join(parts) + "\n"
        return ""

    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response.
        
        Args:
            user_message: The user's message
            
        Returns:
            Assistant's response
        """
        # Build messages for API call
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add context if available
        context_msg = self._build_context_message()
        if context_msg:
            messages.append({"role": "system", "content": context_msg})
        
        # Add conversation history (last 10 exchanges)
        messages.extend(self.conversation_history[-20:])
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def get_summary_suggestion(self, feedback: str) -> str:
        """Get a suggestion for improving the summary based on feedback."""
        if not self.context.get('summary'):
            return "Please generate a summary first before asking for improvements."
        
        prompt = f"""The user wants to improve their resume summary.
        
Current summary:
{self.context.get('summary')}

User feedback: {feedback}

Provide a specific, improved version of the summary that addresses the feedback while maintaining the RoleColor tone."""

        return self.chat(prompt)

    def get_latex_modification(self, request: str) -> str:
        """Get LaTeX code modification based on request."""
        if not self.context.get('latex'):
            return "No LaTeX code is currently loaded. Please generate LaTeX first."
        
        prompt = f"""The user wants to modify their LaTeX resume code.

Request: {request}

Provide the specific LaTeX code changes needed. If it's a small change, show just the modified section. If it's a larger change, provide the complete modified code block."""

        return self.chat(prompt)

    def explain_scores(self) -> str:
        """Explain the current RoleColor scores."""
        if not self.context.get('scores'):
            return "No RoleColor analysis has been performed yet. Please analyze a resume first."
        
        prompt = """Explain the current RoleColor score distribution in 2-3 sentences. 
What does this tell us about the candidate's natural team contribution style? 
What are the implications for their resume?"""
        
        return self.chat(prompt)

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def clear_context(self):
        """Clear all context."""
        self.context = {}
        self.conversation_history = []


def create_assistant() -> ChatAssistant:
    """Factory function to create a new ChatAssistant."""
    return ChatAssistant()


if __name__ == "__main__":
    # Test the chat assistant
    assistant = ChatAssistant()
    
    # Set some context
    assistant.set_context(
        scores={"Builder": 0.45, "Enabler": 0.25, "Thriver": 0.20, "Supportee": 0.10},
        summary="Strategic software engineer focused on building scalable systems..."
    )
    
    # Test chat
    response = assistant.chat("What does my RoleColor score tell you about me?")
    print("Assistant:", response)
