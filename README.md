# RoleColorAI - Resume Intelligence System

An AI-powered resume intelligence system that analyzes and rewrites resumes through a **team-role lens** rather than generic job titles.

## 🎯 Overview

People naturally contribute to teams in different ways. RoleColorAI identifies these contribution styles:

| RoleColor | Description | Key Traits |
|-----------|-------------|------------|
| 🔵 **Builder** | Drive innovation, vision, and strategy | Architect, innovate, scale, transform |
| 🟢 **Enabler** | Connect people, execute plans, bridge gaps | Collaborate, mentor, coordinate, facilitate |
| 🟠 **Thriver** | Perform under pressure, adapt quickly | Deadline-driven, ownership, fast-paced, deliver |
| 🟣 **Supportee** | Ensure reliability, consistency, stability | Maintain, document, reliable, compliance |

## ✨ Features

1. **Multi-Format Resume Upload** - Upload PDF or Word documents (.docx, .doc) for automatic text extraction
2. **RoleColor Keyword Framework** - Weighted keyword mapping for each RoleColor trait
3. **Resume Scoring** - Analyze resumes and generate normalized score distributions
4. **AI Summary Rewriting** - Generate role-optimized summaries using OpenAI
5. **LaTeX/Overleaf Generation** - Create professional LaTeX resumes
6. **E2B Sandbox Compilation** - Compile LaTeX to PDF in the cloud
7. **Interactive Chat Assistant** - Get help refining your resume through AI chat

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- E2B API key (optional, for PDF compilation)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/rolecolorai.git
cd rolecolorai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional, for advanced NLP)
python -m spacy download en_core_web_sm
```

### Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
E2B_API_KEY=your_e2b_api_key_here
```

### Running the Application

```bash
# Run the Streamlit web app
streamlit run app.py
```

Or use the Jupyter notebook:

```bash
jupyter notebook rolecolor_demo.ipynb
```

## 📁 Project Structure

```
rolecolorai/
├── app.py                    # Main Streamlit application
├── rolecolor_framework.py    # Keyword definitions and mappings
├── resume_scorer.py          # Scoring algorithm
├── resume_rewriter.py        # OpenAI-powered summary rewriting
├── latex_generator.py        # LaTeX code generation
├── e2b_runner.py            # E2B sandbox integration
├── chat_assistant.py        # AI chat functionality
├── rolecolor_demo.ipynb     # Jupyter notebook demo
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not committed)
├── .gitignore              # Git ignore rules
├── sample_resumes/         # Sample resume files
│   ├── sample_resume_1.txt
│   ├── sample_resume_2.txt
│   └── sample_resume_3.txt
└── README.md               # This file
```

## 🔧 How It Works

### Part 1: RoleColor Keyword Framework

The framework defines weighted keywords for each RoleColor:

```python
ROLECOLOR_KEYWORDS = {
    "Builder": {
        "strategy": 1.5, "vision": 1.5, "architect": 1.4,
        "innovate": 1.5, "scalable": 1.3, "transform": 1.4, ...
    },
    "Enabler": {
        "collaborate": 1.5, "coordinate": 1.4, "mentor": 1.5,
        "cross-functional": 1.5, "facilitate": 1.5, ...
    },
    # ... etc
}
```

**Keyword Selection Rationale:**
- **Builder**: Strategic/visionary language (vision, roadmap, architecture)
- **Enabler**: Collaborative/bridging language (coordinate, mentor, stakeholder)
- **Thriver**: Speed/ownership language (deadline, fast-paced, ownership)
- **Supportee**: Reliability/process language (maintain, document, compliance)

### Part 2: Resume Scoring

The scoring algorithm:

1. Preprocesses text (lowercase, normalize whitespace)
2. Finds keyword matches using word boundary regex
3. Applies weights with diminishing returns for repeated keywords
4. Normalizes scores to sum to 1.0

```python
from resume_scorer import score_resume

result = score_resume(resume_text)
print(result['scores'])
# Output: {'Builder': 0.45, 'Enabler': 0.30, 'Thriver': 0.15, 'Supportee': 0.10}
```

### Part 3: Summary Rewriting

Uses OpenAI to generate role-aligned summaries:

```python
from resume_rewriter import rewrite_summary

summary = rewrite_summary(
    resume_text=resume_text,
    dominant_role="Builder",
    scores=scores
)
```

## 📊 Sample Output

**Input Resume:**
> Software engineer with 2 years of experience in backend development and APIs.

**RoleColor Scores:**
```
Builder:   [████████████████████░░░░░░░░░░░░░░░░░░░░] 45%
Enabler:   [████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30%
Thriver:   [██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 15%
Supportee: [████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 10%
```

**Rewritten Summary (Builder-leaning):**
> Strategic backend engineer with a strong focus on system architecture, scalable APIs, and long-term product thinking. Proven ability to design solutions that support growth and innovation. Experienced in building robust systems that form the foundation for product development.

## 🔌 API Usage

### Scoring a Resume

```python
from resume_scorer import score_resume

result = score_resume("""
    Software engineer with experience in building scalable systems...
""")

print(f"Dominant Role: {result['dominant_role']}")
print(f"Scores: {result['scores']}")
```

### Generating LaTeX

```python
from latex_generator import generate_latex_from_resume

latex_code = generate_latex_from_resume(
    resume_text=resume_text,
    rewritten_summary=summary,
    dominant_role="Builder",
    scores=scores
)
```

### Using the Chat Assistant

```python
from chat_assistant import ChatAssistant

assistant = ChatAssistant()
assistant.set_context(scores=scores, summary=summary)
response = assistant.chat("How can I improve my resume?")
```

## 🎨 Streamlit App Features

The web application provides:

1. **Resume Input Tab** - Paste or upload resume text
2. **Analysis Tab** - View score distributions and matched keywords
3. **Summary Tab** - Generate and refine AI summaries
4. **LaTeX Tab** - Generate, edit, and compile LaTeX code
5. **Chat Sidebar** - Interactive AI assistant

## ⚙️ Configuration Options

| Environment Variable | Description | Required |
|---------------------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for summary generation | Yes |
| `E2B_API_KEY` | E2B API key for LaTeX compilation | No |

## 📝 Assumptions

1. Resume text is in English
2. Keywords are case-insensitive
3. Repeated keywords have diminishing returns in scoring
4. The dominant RoleColor is used for summary generation by default
5. LaTeX generation assumes standard resume structure

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

---

Built with ❤️ for the RoleColorAI take-home assignment.
