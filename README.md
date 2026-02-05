# RoleColorAI - Resume Intelligence System

An AI-powered resume intelligence system that analyzes and rewrites resumes through a **team-role lens** rather than generic job titles.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rolecolorai.streamlit.app)

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
5. **LaTeX/Overleaf Generation** - Create professional LaTeX resumes with RoleColor styling
6. **Job Tailoring** - Generate resumes tailored to specific job descriptions
7. **E2B Sandbox Compilation** - Compile LaTeX to PDF in the cloud
8. **Local PDF Compilation** - Compile LaTeX locally (requires pdflatex)
9. **Word Document Export** - Export resumes as .docx files
10. **Interactive Chat Assistant** - Get help refining your resume through AI chat

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (required)
- E2B API key (optional, for cloud PDF compilation)

### Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/dv0331/RoleColorAI.git
cd RoleColorAI
```

#### Step 2: Create a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Download spaCy Model (Optional)

This is optional but recommended for advanced NLP features:

```bash
python -m spacy download en_core_web_sm
```

### Configuration

#### Step 5: Set Up Environment Variables

1. Copy the example environment file:

   **Windows (PowerShell):**
   ```powershell
   Copy-Item .env.example .env
   ```

   **macOS/Linux:**
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API keys:

   ```env
   OPENAI_API_KEY=sk-your-actual-openai-api-key
   E2B_API_KEY=e2b_your-actual-e2b-api-key
   ```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🔑 Getting API Keys

### OpenAI API Key (Required)

The OpenAI API key is required for AI-powered features like summary rewriting, job tailoring, and the chat assistant.

**How to get your OpenAI API key:**

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up for an account or log in
3. Navigate to **API Keys** in the left sidebar (or go directly to https://platform.openai.com/api-keys)
4. Click **"Create new secret key"**
5. Give it a name (e.g., "RoleColorAI")
6. Copy the key immediately (it starts with `sk-`)
7. Paste it in your `.env` file

**Important Notes:**
- OpenAI API is a paid service (pay-as-you-go)
- New accounts typically get free credits to start
- The app uses `gpt-4o-mini` which is cost-effective (~$0.15 per 1M input tokens)

### E2B API Key (Optional but Recommended)

The E2B (Code Interpreter) API key enables cloud-based LaTeX compilation to PDF without installing LaTeX locally.

**How to get your E2B API key:**

1. Go to [E2B.dev](https://e2b.dev/)
2. Click **"Get Started"** or **"Sign Up"**
3. Create an account (GitHub login is available for quick signup)
4. Once logged in, go to **Dashboard**
5. Navigate to **API Keys** section
6. Click **"Create API Key"**
7. Copy the key (it starts with `e2b_`)
8. Paste it in your `.env` file

**Important Notes:**
- E2B offers a **free tier** with generous limits for personal projects
- Free tier includes: Sandbox compute time sufficient for many compilations
- If you don't have an E2B key, you can still use **local compilation** (requires `pdflatex` installed)

### Alternative: Local LaTeX Compilation

If you prefer not to use E2B, you can install LaTeX locally:

**Windows:**
- Install [MiKTeX](https://miktex.org/download)

**macOS:**
- Install [MacTeX](https://www.tug.org/mactex/)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install texlive-full
```

---

## 📁 Project Structure

```
RoleColorAI/
├── app.py                    # Main Streamlit application
├── rolecolor_framework.py    # Keyword definitions and mappings
├── resume_scorer.py          # Scoring algorithm
├── resume_rewriter.py        # OpenAI-powered summary rewriting
├── latex_generator.py        # LaTeX code generation + job tailoring
├── e2b_runner.py             # E2B sandbox integration
├── chat_assistant.py         # AI chat functionality
├── rolecolor_demo.ipynb      # Jupyter notebook demo
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment configuration
├── .env                      # Your environment variables (not committed)
├── .gitignore                # Git ignore rules
├── sample_resumes/           # Sample resume files
│   ├── sample_resume_1.txt
│   ├── sample_resume_2.txt
│   └── sample_resume_3.txt
└── README.md                 # This file
```

---

## 🎨 Application Tabs

### 1. 📝 Resume Input
- Paste resume text directly
- Upload PDF documents
- Upload Word documents (.docx)
- Load sample resumes for testing

### 2. 📊 RoleColor Analysis
- View score distributions for all four RoleColors
- See matched keywords for each category
- Visual progress bars showing trait percentages

### 3. ✍️ Summary Rewrite
- Generate AI-powered summaries aligned with your dominant RoleColor
- Target a specific RoleColor if desired
- Preview before and after comparison

### 4. 📄 LaTeX/Overleaf
- Generate professional LaTeX resume code
- Download as .tex file
- Compile to PDF (locally or via E2B cloud)
- Export as Word document
- Edit LaTeX with AI assistance

### 5. 🎯 Job Tailoring (NEW!)
- Paste a job description
- AI generates a tailored resume highlighting relevant experience
- Automatic keyword optimization for ATS systems
- Download as LaTeX, PDF, or Word

---

## 🔧 How It Works

### RoleColor Keyword Framework

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

### Resume Scoring Algorithm

1. Preprocesses text (lowercase, normalize whitespace)
2. Finds keyword matches using word boundary regex
3. Applies weights with diminishing returns for repeated keywords
4. Normalizes scores to sum to 1.0

### Job Tailoring

The job tailoring feature uses OpenAI to:
1. Analyze the target job description
2. Identify key requirements and keywords
3. Rewrite your resume emphasizing relevant experience
4. Maintain truthfulness while optimizing for ATS systems

---

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
> Strategic backend engineer with a strong focus on system architecture, scalable APIs, and long-term product thinking. Proven ability to design solutions that support growth and innovation.

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push your code to GitHub (already done!)
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `dv0331/RoleColorAI`
6. Set the main file path: `app.py`
7. Click "Advanced settings" and add your secrets:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   E2B_API_KEY = "e2b_your-key-here"
   ```
8. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set OPENAI_API_KEY=sk-your-key
railway variables set E2B_API_KEY=e2b_your-key

# Deploy
railway up
```

### Deploy with Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t rolecolorai .
docker run -p 8501:8501 --env-file .env rolecolorai
```

---

## ⚙️ Configuration Options

| Environment Variable | Description | Required |
|---------------------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Yes |
| `E2B_API_KEY` | E2B API key for cloud LaTeX compilation | No |

---

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you've created a `.env` file (copy from `.env.example`)
- Ensure the key is correct and starts with `sk-`
- Restart the Streamlit app after adding the key

### "E2B compilation failed"
- Check that your E2B API key is correct and starts with `e2b_`
- Try the "Local Compilation" option instead
- E2B free tier has usage limits; wait and retry if you hit limits

### "Port 8501 is already in use"
- Another Streamlit app is running
- Kill it with: `taskkill /F /IM python.exe` (Windows) or `pkill -f streamlit` (macOS/Linux)

### PDF not generating locally
- Install LaTeX: MiKTeX (Windows), MacTeX (macOS), or texlive (Linux)
- Make sure `pdflatex` is in your system PATH

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🔗 Links

- **GitHub Repository**: https://github.com/dv0331/RoleColorAI
- **Live Demo**: [Coming Soon - Deploy to Streamlit Cloud]
- **OpenAI Platform**: https://platform.openai.com/
- **E2B.dev**: https://e2b.dev/

---

Built with ❤️ using Streamlit, OpenAI, and E2B
