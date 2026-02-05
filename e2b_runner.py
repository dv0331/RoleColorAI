"""
E2B Sandbox Runner Module

This module provides functionality to compile LaTeX code
using the E2B sandbox environment.

Updated for E2B SDK v2.x
"""

import os
import base64
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


def get_e2b_api_key() -> str:
    """Get E2B API key from environment."""
    api_key = os.getenv("E2B_API_KEY")
    if not api_key:
        raise ValueError("E2B_API_KEY not found in environment variables")
    return api_key


def compile_latex_in_sandbox(latex_code: str, filename: str = "resume") -> Dict:
    """
    Compile LaTeX code in E2B sandbox and return the PDF.
    
    Args:
        latex_code: The LaTeX source code
        filename: Base filename (without extension)
    
    Returns:
        Dictionary with:
        - success: bool
        - pdf_data: base64 encoded PDF (if successful)
        - log: compilation log
        - error: error message (if failed)
    """
    try:
        from e2b import Sandbox
    except ImportError:
        return {
            "success": False,
            "error": "E2B package not installed. Run: pip install e2b",
            "log": "",
            "pdf_data": None
        }
    
    # Validate API key format
    try:
        api_key = get_e2b_api_key()
        if not api_key.startswith("e2b_"):
            return {
                "success": False,
                "error": f"E2B API key appears invalid. Keys should start with 'e2b_'. Got: {api_key[:10]}...",
                "log": "",
                "pdf_data": None
            }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "log": "",
            "pdf_data": None
        }
    
    sandbox = None
    
    try:
        # Create sandbox using E2B SDK v2.x class method
        # Sandbox.create() is the recommended way in v2.x
        print(f"[E2B Debug] Creating sandbox with API key: {api_key[:10]}...")
        sandbox = Sandbox.create(api_key=api_key, timeout=300)
        print(f"[E2B Debug] Sandbox created successfully")
        
        # Write LaTeX file
        tex_path = f"/home/user/{filename}.tex"
        sandbox.files.write(tex_path, latex_code)
        
        # Install LaTeX (texlive-latex-base for basic, texlive-full for complete)
        # Using a minimal install for speed
        # Note: sudo is required in E2B sandbox for package installation
        install_result = sandbox.commands.run(
            "sudo apt-get update && sudo apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-latex-extra",
            timeout=180
        )
        
        if install_result.exit_code != 0:
            return {
                "success": False,
                "error": f"Failed to install LaTeX: {install_result.stderr}",
                "log": install_result.stdout
            }
        
        # Compile LaTeX to PDF
        compile_cmd = f"cd /home/user && pdflatex -interaction=nonstopmode {filename}.tex"
        compile_result = sandbox.commands.run(compile_cmd, timeout=60)
        
        # Check for PDF
        pdf_path = f"/home/user/{filename}.pdf"
        
        try:
            pdf_content = sandbox.files.read(pdf_path, format="bytes")
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            return {
                "success": True,
                "pdf_data": pdf_base64,
                "log": compile_result.stdout,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"PDF not generated. LaTeX errors: {compile_result.stderr}",
                "log": compile_result.stdout
            }
            
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        original_error = f"[{error_type}] {error_msg}"  # Keep original with type for debugging
        
        print(f"[E2B Debug] Exception caught: {original_error}")
        
        # Check exception type and message for more specific errors
        error_lower = error_msg.lower()
        
        # Provide more helpful error messages for common issues
        if "WebSocket" in error_msg or "connection" in error_lower:
            error_msg = f"Connection error: {original_error}. This may be a temporary E2B service issue. Please try again."
        elif any(x in error_lower for x in ["api_key", "unauthorized", "authentication", "invalid key"]) or "401" in error_msg:
            error_msg = f"API key error: Please verify your E2B_API_KEY is correct and active."
        elif "403" in error_msg or "forbidden" in error_lower:
            error_msg = f"Access forbidden. Your API key may not have access to this template or feature."
        elif "404" in error_msg or "not found" in error_lower:
            error_msg = f"Resource not found. The template may not be available."
        elif "timeout" in error_lower:
            error_msg = f"Operation timed out. E2B service may be slow or unavailable."
        elif "template" in error_lower:
            error_msg = f"Template error: {original_error}"
        elif "quota" in error_lower or "limit" in error_lower or "rate" in error_lower:
            error_msg = f"Rate limit or quota exceeded. Please wait and try again."
        else:
            error_msg = f"E2B Error: {original_error}"
        
        return {
            "success": False,
            "error": error_msg,
            "log": "",
            "pdf_data": None
        }
    finally:
        # Always clean up the sandbox
        if sandbox:
            try:
                sandbox.kill()
            except:
                pass


def compile_latex_simple(latex_code: str) -> Tuple[bool, str, str]:
    """
    Simplified LaTeX compilation that returns status, message, and log.
    
    Returns:
        Tuple of (success, message, log)
    """
    result = compile_latex_in_sandbox(latex_code)
    
    if result["success"]:
        return True, "PDF compiled successfully!", result["log"]
    else:
        return False, result["error"], result["log"]


def validate_latex_syntax(latex_code: str) -> Dict:
    """
    Validate LaTeX syntax without full compilation.
    Basic checks for common errors.
    
    Returns:
        Dictionary with validation results
    """
    errors = []
    warnings = []
    
    # Check for document class
    if r'\documentclass' not in latex_code:
        errors.append("Missing \\documentclass declaration")
    
    # Check for begin/end document
    if r'\begin{document}' not in latex_code:
        errors.append("Missing \\begin{document}")
    if r'\end{document}' not in latex_code:
        errors.append("Missing \\end{document}")
    
    # Check for balanced braces (simple check)
    open_braces = latex_code.count('{')
    close_braces = latex_code.count('}')
    if open_braces != close_braces:
        errors.append(f"Unbalanced braces: {open_braces} opening, {close_braces} closing")
    
    # Check for balanced begin/end environments
    import re
    begins = re.findall(r'\\begin\{(\w+)\}', latex_code)
    ends = re.findall(r'\\end\{(\w+)\}', latex_code)
    
    begin_counts = {}
    end_counts = {}
    for env in begins:
        begin_counts[env] = begin_counts.get(env, 0) + 1
    for env in ends:
        end_counts[env] = end_counts.get(env, 0) + 1
    
    for env in set(list(begin_counts.keys()) + list(end_counts.keys())):
        b = begin_counts.get(env, 0)
        e = end_counts.get(env, 0)
        if b != e:
            errors.append(f"Unbalanced environment '{env}': {b} begins, {e} ends")
    
    # Check for common mistakes
    if r'\\' in latex_code and r'\\\\' not in latex_code:
        warnings.append("Check line breaks - use \\\\ for line breaks in LaTeX")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def get_compilation_status_message(result: Dict) -> str:
    """Format compilation result for display."""
    if result["success"]:
        return "✅ LaTeX compiled successfully! PDF is ready for download."
    else:
        return f"❌ Compilation failed: {result['error']}\n\nLog:\n{result['log'][:500]}"


if __name__ == "__main__":
    # Test validation
    test_latex = r"""
\documentclass{article}
\begin{document}
Hello World!
\end{document}
"""
    
    validation = validate_latex_syntax(test_latex)
    print("Validation result:", validation)
