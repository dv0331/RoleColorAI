"""
RoleColorAI - Main Streamlit Application

A resume intelligence system that analyzes and rewrites resumes
through a team-role lens (Builder, Enabler, Thriver, Supportee).

Features:
- RoleColor scoring and analysis
- AI-powered summary rewriting
- LaTeX/Overleaf code generation
- E2B sandbox for LaTeX compilation
- Interactive chat assistant
- PDF and Word document upload support
"""

import streamlit as st
import base64
from io import BytesIO

# Document parsing imports
import PyPDF2
from docx import Document

# Import modules
from rolecolor_framework import ROLECOLOR_KEYWORDS, get_rolecolor_descriptions
from resume_scorer import score_resume, format_score_output, get_score_summary
from resume_rewriter import rewrite_summary, enhance_with_chat
from latex_generator import generate_latex_from_resume, generate_simple_latex, edit_latex_with_ai, validate_latex_syntax
from e2b_runner import compile_latex_in_sandbox, validate_latex_syntax as validate_latex
from chat_assistant import ChatAssistant

# Page configuration
st.set_page_config(
    page_title="RoleColorAI - Resume Intelligence",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .rolecolor-builder { color: #3B82F6; font-weight: bold; }
    .rolecolor-enabler { color: #22C55E; font-weight: bold; }
    .rolecolor-thriver { color: #F97316; font-weight: bold; }
    .rolecolor-supportee { color: #8B5CF6; font-weight: bold; }
    
    .score-bar {
        height: 24px;
        border-radius: 4px;
        margin: 4px 0;
    }
    
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
    }
    
    .chat-message {
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    
    .user-message {
        background-color: #E3F2FD;
    }
    
    .assistant-message {
        background-color: #F5F5F5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'scores' not in st.session_state:
    st.session_state.scores = None
if 'rewritten_summary' not in st.session_state:
    st.session_state.rewritten_summary = ""
if 'latex_code' not in st.session_state:
    st.session_state.latex_code = ""
if 'chat_assistant' not in st.session_state:
    st.session_state.chat_assistant = ChatAssistant()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_parts = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""


def extract_text_from_docx(docx_file) -> str:
    """Extract text from a Word document (.docx)."""
    try:
        doc = Document(docx_file)
        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        # Also extract from tables
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    text_parts.append(row_text)
        return "\n".join(text_parts)
    except Exception as e:
        st.error(f"Error reading Word document: {str(e)}")
        return ""


def display_rolecolor_scores(scores: dict, matches: dict):
    """Display RoleColor scores with visual bars."""
    colors = {
        "Builder": "#3B82F6",
        "Enabler": "#22C55E", 
        "Thriver": "#F97316",
        "Supportee": "#8B5CF6"
    }
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    for role, score in sorted_scores:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{role}**")
            st.progress(score, text=f"{score:.1%}")
        with col2:
            keywords = matches.get(role, [])
            if keywords:
                top_kw = [kw[0] for kw in sorted(keywords, key=lambda x: x[1]*x[2], reverse=True)[:3]]
                st.caption(", ".join(top_kw))


def main():
    # Sidebar - Chat Assistant
    with st.sidebar:
        st.header("💬 AI Chat Assistant")
        st.markdown("Ask questions about your analysis or get help refining your resume.")
        
        # Chat input
        chat_input = st.text_input("Your message:", key="chat_input", placeholder="Ask me anything...")
        
        col1, col2 = st.columns(2)
        with col1:
            send_button = st.button("Send", use_container_width=True)
        with col2:
            clear_button = st.button("Clear Chat", use_container_width=True)
        
        if clear_button:
            st.session_state.chat_history = []
            st.session_state.chat_assistant.clear_history()
            st.rerun()
        
        if send_button and chat_input:
            # Update assistant context
            st.session_state.chat_assistant.set_context(
                resume_text=st.session_state.resume_text,
                scores=st.session_state.scores['scores'] if st.session_state.scores else None,
                summary=st.session_state.rewritten_summary,
                latex_code=st.session_state.latex_code
            )
            
            # Get response
            response = st.session_state.chat_assistant.chat(chat_input)
            
            # Add to history
            st.session_state.chat_history.append({"role": "user", "content": chat_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            st.rerun()
        
        # Display chat history
        st.markdown("---")
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**AI:** {msg['content']}")
                st.markdown("")
        
        # Quick actions
        st.markdown("---")
        st.subheader("Quick Actions")
        
        if st.button("📊 Explain My Scores", use_container_width=True):
            if st.session_state.scores:
                st.session_state.chat_assistant.set_context(
                    scores=st.session_state.scores['scores']
                )
                response = st.session_state.chat_assistant.explain_scores()
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
            else:
                st.warning("Analyze a resume first!")
        
        if st.button("✨ Improve Summary", use_container_width=True):
            if st.session_state.rewritten_summary:
                st.session_state.chat_assistant.set_context(
                    summary=st.session_state.rewritten_summary,
                    scores=st.session_state.scores['scores'] if st.session_state.scores else None
                )
                response = st.session_state.chat_assistant.chat(
                    "Suggest improvements for my current resume summary"
                )
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
            else:
                st.warning("Generate a summary first!")

    # Main content
    st.title("🎨 RoleColorAI")
    st.markdown("*Transform your resume through the lens of team contribution styles*")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Resume Input", 
        "📊 RoleColor Analysis", 
        "✍️ Summary Rewrite",
        "📄 LaTeX/Overleaf"
    ])
    
    # Tab 1: Resume Input
    with tab1:
        st.header("Enter Your Resume")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # File upload section
            st.subheader("📁 Upload Resume File")
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF or Word)",
                type=["pdf", "docx", "doc"],
                help="Supported formats: PDF (.pdf), Word (.docx)"
            )
            
            if uploaded_file is not None:
                file_type = uploaded_file.name.split(".")[-1].lower()
                
                with st.spinner(f"Extracting text from {uploaded_file.name}..."):
                    if file_type == "pdf":
                        extracted_text = extract_text_from_pdf(uploaded_file)
                    elif file_type in ["docx", "doc"]:
                        extracted_text = extract_text_from_docx(uploaded_file)
                    else:
                        extracted_text = ""
                        st.error("Unsupported file format")
                
                if extracted_text:
                    st.success(f"✅ Successfully extracted text from **{uploaded_file.name}**")
                    st.session_state.resume_text = extracted_text
                    st.info(f"📄 Extracted {len(extracted_text)} characters from your resume")
            
            st.markdown("---")
            st.subheader("📝 Or Paste Text Directly")
            
            resume_input = st.text_area(
                "Paste your resume text here:",
                height=350,
                value=st.session_state.resume_text,
                placeholder="Paste your resume content here...\n\nExample:\nSoftware Engineer with 5 years of experience..."
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📤 Load Sample Resume", use_container_width=True):
                    sample = """Senior Software Engineer with 5 years of experience in building scalable 
backend systems and APIs. Led a team of 4 engineers to architect and develop 
a microservices platform that handles 10M+ daily transactions.

EXPERIENCE

Tech Company Inc. - Senior Software Engineer (2021-Present)
- Designed and implemented a real-time data processing pipeline using Kafka and Spark
- Collaborated with cross-functional teams including product, design, and data science
- Mentored 3 junior developers and established coding standards and best practices
- Spearheaded the migration to cloud infrastructure, reducing costs by 40%

Startup Co. - Software Engineer (2019-2021)
- Built REST APIs serving 1M+ daily requests with 99.9% uptime
- Maintained comprehensive documentation for all system components
- Worked in fast-paced agile environment, consistently meeting tight deadlines
- Proactively identified and resolved production issues

SKILLS
Python, Go, AWS, Kubernetes, PostgreSQL, Redis, Kafka, Docker

EDUCATION
B.S. Computer Science, State University, 2019"""
                    st.session_state.resume_text = sample
                    st.rerun()
            
            with col_btn2:
                if st.button("🗑️ Clear Text", use_container_width=True):
                    st.session_state.resume_text = ""
                    st.rerun()
        
        with col2:
            st.subheader("RoleColor Guide")
            
            descriptions = get_rolecolor_descriptions()
            
            with st.expander("🔵 Builder", expanded=False):
                st.markdown(descriptions["Builder"])
            
            with st.expander("🟢 Enabler", expanded=False):
                st.markdown(descriptions["Enabler"])
            
            with st.expander("🟠 Thriver", expanded=False):
                st.markdown(descriptions["Thriver"])
            
            with st.expander("🟣 Supportee", expanded=False):
                st.markdown(descriptions["Supportee"])
        
        if resume_input:
            st.session_state.resume_text = resume_input
            
            if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
                with st.spinner("Analyzing resume..."):
                    st.session_state.scores = score_resume(resume_input)
                st.success("Analysis complete! Go to the RoleColor Analysis tab.")

    # Tab 2: RoleColor Analysis
    with tab2:
        st.header("RoleColor Analysis Results")
        
        if st.session_state.scores:
            scores = st.session_state.scores
            
            # Dominant RoleColor highlight
            dominant = scores['dominant_role']
            role_colors = {
                "Builder": "🔵", "Enabler": "🟢", 
                "Thriver": "🟠", "Supportee": "🟣"
            }
            
            st.markdown(f"### {role_colors[dominant]} Dominant RoleColor: **{dominant}**")
            st.markdown(get_rolecolor_descriptions()[dominant])
            
            st.markdown("---")
            
            # Score distribution
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Score Distribution")
                display_rolecolor_scores(scores['scores'], scores['matches'])
            
            with col2:
                st.subheader("Summary")
                st.metric("Keywords Matched", scores['total_keywords_matched'])
                
                # Top keywords overall
                all_keywords = []
                for role, matches in scores['matches'].items():
                    for kw, weight, count in matches:
                        all_keywords.append((kw, role, weight * count))
                
                all_keywords.sort(key=lambda x: x[2], reverse=True)
                
                st.markdown("**Top Keywords Found:**")
                for kw, role, _ in all_keywords[:8]:
                    st.markdown(f"• {kw} ({role})")
            
            # Raw scores expander
            with st.expander("📈 Detailed Scoring Data"):
                st.json({
                    "normalized_scores": {k: round(v, 4) for k, v in scores['scores'].items()},
                    "raw_scores": {k: round(v, 2) for k, v in scores['raw_scores'].items()},
                    "keyword_counts": {k: len(v) for k, v in scores['matches'].items()}
                })
        else:
            st.info("👈 Enter a resume in the Resume Input tab and click Analyze")

    # Tab 3: Summary Rewrite
    with tab3:
        st.header("AI-Powered Summary Rewrite")
        
        if st.session_state.scores:
            dominant = st.session_state.scores['dominant_role']
            
            st.markdown(f"Generating summary optimized for **{dominant}** traits.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✨ Generate Summary", type="primary", use_container_width=True):
                    with st.spinner("AI is writing your summary..."):
                        summary = rewrite_summary(
                            resume_text=st.session_state.resume_text,
                            dominant_role=dominant,
                            scores=st.session_state.scores['scores']
                        )
                        st.session_state.rewritten_summary = summary
            
            with col2:
                target_role = st.selectbox(
                    "Or target a specific RoleColor:",
                    ["Auto (Dominant)", "Builder", "Enabler", "Thriver", "Supportee"]
                )
                
                if target_role != "Auto (Dominant)" and st.button("Generate for Selected"):
                    with st.spinner("AI is writing your summary..."):
                        summary = rewrite_summary(
                            resume_text=st.session_state.resume_text,
                            dominant_role=target_role,
                            scores=st.session_state.scores['scores']
                        )
                        st.session_state.rewritten_summary = summary
            
            if st.session_state.rewritten_summary:
                st.markdown("---")
                st.subheader("Generated Summary")
                
                # Editable summary
                edited_summary = st.text_area(
                    "Edit your summary:",
                    value=st.session_state.rewritten_summary,
                    height=200
                )
                
                if edited_summary != st.session_state.rewritten_summary:
                    st.session_state.rewritten_summary = edited_summary
                
                # Refinement through chat
                st.markdown("---")
                st.subheader("Refine with AI")
                
                refinement = st.text_input(
                    "What would you like to change?",
                    placeholder="e.g., Make it more technical, Add leadership focus, Shorter..."
                )
                
                if refinement and st.button("Apply Changes"):
                    with st.spinner("Refining..."):
                        new_summary = enhance_with_chat(
                            resume_text=st.session_state.resume_text,
                            current_summary=st.session_state.rewritten_summary,
                            user_feedback=refinement,
                            dominant_role=dominant
                        )
                        st.session_state.rewritten_summary = new_summary
                        st.rerun()
        else:
            st.info("👈 Analyze a resume first to generate a summary")

    # Tab 4: LaTeX/Overleaf
    with tab4:
        st.header("LaTeX Resume Generator")
        
        if st.session_state.scores and st.session_state.rewritten_summary:
            dominant = st.session_state.scores['dominant_role']
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Generate LaTeX")
                
                generation_type = st.radio(
                    "Generation mode:",
                    ["Full Resume", "Summary Only"],
                    horizontal=True
                )
                
                if st.button("📄 Generate LaTeX Code", type="primary", use_container_width=True):
                    with st.spinner("Generating LaTeX..."):
                        if generation_type == "Full Resume":
                            latex = generate_latex_from_resume(
                                resume_text=st.session_state.resume_text,
                                rewritten_summary=st.session_state.rewritten_summary,
                                dominant_role=dominant,
                                scores=st.session_state.scores['scores']
                            )
                        else:
                            latex = generate_simple_latex(
                                name="Your Name",
                                contact="email@example.com | (555) 123-4567",
                                summary=st.session_state.rewritten_summary,
                                dominant_role=dominant
                            )
                        st.session_state.latex_code = latex
                
                # Validate syntax
                if st.session_state.latex_code:
                    validation = validate_latex(st.session_state.latex_code)
                    if validation['valid']:
                        st.success("✅ LaTeX syntax is valid")
                    else:
                        for error in validation['errors']:
                            st.error(f"❌ {error}")
                        for warning in validation['warnings']:
                            st.warning(f"⚠️ {warning}")
            
            with col2:
                st.subheader("E2B Compilation")
                st.markdown("Compile your LaTeX to PDF using E2B sandbox.")
                
                if st.session_state.latex_code:
                    if st.button("🚀 Compile to PDF", use_container_width=True):
                        with st.spinner("Compiling LaTeX in E2B sandbox... (this may take a minute)"):
                            result = compile_latex_in_sandbox(st.session_state.latex_code)
                            
                            if result['success']:
                                st.success("✅ PDF compiled successfully!")
                                
                                # Create download button
                                pdf_bytes = base64.b64decode(result['pdf_data'])
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=pdf_bytes,
                                    file_name="resume.pdf",
                                    mime="application/pdf"
                                )
                            else:
                                st.error(f"❌ Compilation failed: {result['error']}")
                                if result['log']:
                                    with st.expander("View compilation log"):
                                        st.code(result['log'])
                else:
                    st.info("Generate LaTeX code first")
            
            # LaTeX Editor
            st.markdown("---")
            st.subheader("LaTeX Editor")
            
            if st.session_state.latex_code:
                # AI modification input
                latex_modification = st.text_input(
                    "Ask AI to modify the LaTeX:",
                    placeholder="e.g., Add a projects section, Change the color scheme, Make margins wider..."
                )
                
                if latex_modification and st.button("Apply AI Modification"):
                    with st.spinner("Modifying LaTeX..."):
                        new_latex = edit_latex_with_ai(
                            st.session_state.latex_code,
                            latex_modification
                        )
                        st.session_state.latex_code = new_latex
                        st.rerun()
                
                # Code editor
                edited_latex = st.text_area(
                    "Edit LaTeX code directly:",
                    value=st.session_state.latex_code,
                    height=400
                )
                
                if edited_latex != st.session_state.latex_code:
                    st.session_state.latex_code = edited_latex
                
                # Download LaTeX source
                st.download_button(
                    label="📥 Download .tex file",
                    data=st.session_state.latex_code,
                    file_name="resume.tex",
                    mime="text/plain"
                )
                
                # Copy to clipboard instruction
                st.info("💡 **Tip:** Copy the LaTeX code above and paste it into [Overleaf](https://www.overleaf.com/) for online editing and compilation.")
        else:
            st.info("👈 Complete the analysis and generate a summary first")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            RoleColorAI - Resume Intelligence System<br>
            Analyzing team contribution styles through AI
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
