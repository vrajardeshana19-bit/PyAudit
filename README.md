Here is the complete, single-block `README.md` text with a dedicated **👨‍💻 Built by Vraj Ardeshana** section highlighting your role, contributions, technical impact, and leadership:

```markdown
# 🛡️ PyAudit — DevSecOps Static Security & Secret Scanner

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![AI Engine](https://img.shields.io/badge/AI-Gemini%20%7C%20Ollama-magenta)
![Maintainer](https://img.shields.io/badge/Built%20By-Vraj%20Ardeshana-brightgreen)

**PyAudit** is an asynchronous Python security analysis tool designed to detect vulnerabilities, scan for leaked API secrets, audit dependency CVEs, and automatically fix security flaws. Powered by a hybrid AI engine (Google Gemini Cloud & local Ollama), PyAudit provides real-time vulnerability explanations, refactored safe code suggestions, and an interactive DevSecOps terminal assistant.

---

## 👨‍💻 Built by Vraj Ardeshana

**PyAudit** was designed, architected, and built by **Vraj Ardeshana** — Computer Science Engineering student (CMRIT, Bengaluru), Club Secretary & Promotion Head at RISE, and DevSecOps / Security Engineering builder.

### 🚀 Key Technical Contributions & What I Worked On:
- **Core Security Engine**: Implemented AST static analysis parsing (`ast.parse`) to detect dangerous execution sinks (`eval()`, `exec()`, `subprocess`) mapped directly to **MITRE ATT&CK IDs**.
- **Secret & Credential Detection**: Engineered high-entropy calculation algorithms and regex pattern matching to flag leaked AWS keys, API tokens, and private keys.
- **Asynchronous SCA Dependency Checker**: Built async PyPI API query modules (`httpx`, `asyncio`) to check project dependencies against known CVE databases.
- **Active Remediation Engine (`--fix`)**: Developed auto-remediation features that automatically patch `.gitignore` files to block secret exposure and upgrade vulnerable requirements packages.
- **Hybrid AI Engine (`--explain` / `chat`)**: Designed dual-execution AI integration using the official **Google GenAI SDK** for cloud analysis and direct **Ollama REST APIs** for 100% offline, privacy-first local LLM inference.
- **CLI & UX Polish**: Formatted terminal output with `Rich` library components, including syntax-highlighted Markdown panels, dynamic loading spinners, and quiet logging wrappers.

---

## ✨ Features

- **🔍 AST Static Analysis**: Parses Python Abstract Syntax Trees (`ast`) to catch dangerous execution sinks (`eval()`, `exec()`, `shell=True`, weak cryptography) tagged with **MITRE ATT&CK IDs**.
- **🔑 Secret & Credential Detection**: High-entropy analysis and pattern matching for leaked API keys, tokens, and private credentials.
- **📦 SCA & Dependency Audit**: Asynchronously queries vulnerability databases to flag outdated or compromised Python dependencies.
- **🛠️ Active Auto-Remediation (`--fix`)**: Upgrades vulnerable dependencies automatically and patches `.gitignore` to prevent secret leaks.
- **🤖 Hybrid AI Explainer (`--explain`)**: Contextual AI explanations and safe code refactoring snippets via **Google Gemini SDK (Cloud)** or **Ollama (Local Offline Mode)**.
- **💬 Interactive Terminal Assistant (`pyaudit chat`)**: Built-in DevSecOps AI chatbot with syntax highlighting and animated progress spinners.
- **⚡ Git Pre-commit Security Gate (`install-hook`)**: Automatically blocks vulnerable commits before code leaves your local environment.

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies in a virtual environment:

```bash
git clone [https://github.com/vrajardeshana19-bit/PyAudit.git](https://github.com/vrajardeshana19-bit/PyAudit.git)
cd PyAudit
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 2. Set Up API Key (Optional for Cloud AI)

To enable Cloud AI explanations using Google Gemini:

```bash
# On Linux/macOS
export GEMINI_API_KEY="your_google_ai_studio_api_key"

# On Windows (PowerShell)
$env:GEMINI_API_KEY="your_google_ai_studio_api_key"

```

> **Note**: For 100% offline analysis, run PyAudit with the `--local` flag to route requests through a locally running [Ollama](https://ollama.com/) instance (`llama3.2` or `qwen2.5-coder`).

---

## 🛠️ Usage & Commands

### 🔍 Scan a Directory

Perform security static analysis on your project:

```bash
python -m pyaudit.cli scan .

```

### 🤖 AI Security Explainer (Cloud or Local)

Request AI-driven vulnerability breakdowns and secure refactored code snippets:

```bash
# Cloud Mode (Google Gemini API)
python -m pyaudit.cli scan . --explain

# Local Mode (Offline via Ollama)
python -m pyaudit.cli scan . --explain --local

```

### 🛠️ Auto-Remediate Vulnerabilities

Automatically patch `.gitignore` and upgrade vulnerable requirements:

```bash
python -m pyaudit.cli scan . --fix

```

### 💬 Interactive Terminal Security Chatbot

Launch a conversational DevSecOps AI assistant right in your shell:

```bash
# Cloud Chat
python -m pyaudit.cli chat

# Local Offline Chat
python -m pyaudit.cli chat --local

```

### 📄 Export Security Reports

Export scan results to JSON or Markdown:

```bash
python -m pyaudit.cli scan . -o report.json
python -m pyaudit.cli scan . -o report.md

```

### 🔒 Install Git Pre-commit Security Hook

Enforce strict security checks before every Git commit:

```bash
python -m pyaudit.cli install-hook

```

---

## 🏗️ Architecture Overview

```text
PyAudit CLI Tool
├── Scanner Engine
│   ├── AST Analyzer (Dangerous calls, MITRE ATT&CK tagging)
│   ├── Secret Scanner (High entropy + Pattern matching)
│   └── SCA Dependency Checker (Async PyPI/CVE lookups)
├── Remediation Engine (--fix)
│   ├── Requirements version upgrader
│   └── .gitignore patcher
├── Hybrid AI Engine (--explain / chat)
│   ├── Cloud Mode (Google GenAI SDK)
│   └── Local Mode (Ollama REST API via httpx)
└── Integration & Reporting
    ├── Rich Terminal UI (Markdown panels & spinners)
    ├── JSON / Markdown Exporter
    └── Git Pre-commit Hook Installer

```

---

## 🛡️ Security & Privacy

PyAudit is built with **enterprise privacy constraints** in mind:

* Local scanning performs static AST parsing on your machine without transmitting code anywhere.
* Running `--local` ensures that all AI explanations and interactive chat sessions remain **100% offline** on your local machine using Ollama.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

```

```
