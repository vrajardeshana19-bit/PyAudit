# 🛡️ PyAudit — DevSecOps Static Security & Secret Scanner

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![AI Engine](https://img.shields.io/badge/AI-Gemini%20%7C%20Ollama-magenta)
![Security](https://img.shields.io/badge/Security-DevSecOps-red)
![Maintainer](https://img.shields.io/badge/Built%20By-Vraj%20Ardeshana-brightgreen)

**PyAudit** is an asynchronous Python-based DevSecOps security analysis tool designed to identify common security vulnerabilities, detect leaked secrets, audit dependencies, provide AI-powered security explanations, and assist with automated remediation.

It combines **AST-based static analysis, secret detection, dependency security analysis, automated remediation, Git security hooks, and a hybrid AI engine** supporting both cloud-based Google Gemini and local Ollama models.

---

## 🚀 Why PyAudit?

Modern applications can accidentally introduce security vulnerabilities through:

* Dangerous Python functions
* Hardcoded API keys and credentials
* Vulnerable dependencies
* Weak cryptographic practices
* Unsafe subprocess execution
* Secrets accidentally committed to Git
* Misconfigured project files

PyAudit provides a lightweight security layer that developers can run directly from their terminal before code reaches production.

### Core Workflow

```text
Developer Project
       │
       ▼
   PyAudit CLI
       │
       ├── AST Static Analysis
       │
       ├── Secret Detection
       │
       ├── Dependency Audit
       │
       ├── Security Risk Analysis
       │
       ├── AI Explanation
       │
       └── Automated Remediation
              │
              ▼
       Secure Developer Workflow
```

---


## ✨ Features

### 🔍 AST Static Security Analysis

PyAudit parses Python source code using Python's built-in `ast` module to identify potentially dangerous patterns without executing the analyzed code.

It can detect patterns such as:

* `eval()`
* `exec()`
* Unsafe `subprocess` usage
* `shell=True`
* Weak cryptographic algorithms
* Other potentially dangerous execution patterns

Detected vulnerabilities can be mapped to relevant **MITRE ATT&CK techniques**.

---

### 🔑 Secret & Credential Detection

PyAudit scans source files for accidentally exposed credentials and secrets.

Detection combines:

* Regex pattern matching
* Secret-specific patterns
* Entropy analysis
* API token detection
* Private key detection
* Cloud credential detection

Examples include:

* AWS-style access keys
* API tokens
* Authentication credentials
* Private keys
* High-entropy strings

The goal is to catch secrets before they are committed to a repository.

---

### 📦 Software Composition Analysis

PyAudit can inspect Python project dependencies and perform asynchronous security checks.

The dependency analysis can identify:

* Outdated packages
* Potentially vulnerable dependencies
* Package version issues
* Dependencies requiring security updates

Asynchronous requests using `asyncio` and `httpx` allow dependency checks to be performed efficiently.

---

### 🛠️ Automated Remediation

PyAudit includes an active remediation mode through:

```bash
--fix
```

Depending on the detected issue, PyAudit can assist with actions such as:

* Updating vulnerable dependency versions
* Adding secret-related patterns to `.gitignore`
* Reducing the chance of accidentally committing credentials

Always review automatically generated changes before committing them to production repositories.

---

### 🤖 Hybrid AI Security Engine

PyAudit supports two AI execution modes.

#### ☁️ Cloud Mode

Uses Google's Gemini API to provide:

* Vulnerability explanations
* Security recommendations
* Safer code suggestions
* Context-aware remediation guidance

#### 💻 Local Mode

Uses Ollama to run supported local LLMs directly on the developer's machine.

This allows AI-assisted analysis without sending source code to a cloud AI service.

Example:

```bash
python -m pyaudit.cli scan . --explain --local
```

---

### 💬 Interactive DevSecOps Assistant

PyAudit includes an interactive terminal assistant:

```bash
python -m pyaudit.cli chat
```

It provides a conversational interface for discussing security findings and development-security questions directly from the terminal.

For local/offline AI:

```bash
python -m pyaudit.cli chat --local
```

---

### ⚡ Git Pre-Commit Security Gate

PyAudit can install a Git pre-commit hook that performs security checks before code is committed.

Install it using:

```bash
python -m pyaudit.cli install-hook
```

This creates an additional security checkpoint in the development workflow.

---

## 👨‍💻 Built By

**Vraj Ardeshana**

Computer Science Engineering student and technology builder focused on **DevSecOps, cybersecurity, AI-powered developer tools, and software engineering**.

### Key Technical Contributions

* Designed the core AST-based security analysis engine.
* Implemented detection of dangerous Python execution patterns.
* Integrated security findings with MITRE ATT&CK references.
* Developed secret detection using pattern matching and entropy analysis.
* Implemented asynchronous dependency analysis.
* Developed automated remediation functionality.
* Integrated Google Gemini for cloud-based AI security analysis.
* Integrated Ollama for local AI inference.
* Built the interactive DevSecOps terminal assistant.
* Implemented Rich-based terminal output and security reporting.
* Developed Git pre-commit security integration.

---

# 🚀 Quick Start

## 1. Clone the Repository

```bash
git clone https://github.com/vrajardeshana19-bit/PyAudit.git
cd PyAudit
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 AI Configuration

AI functionality is optional.

## Google Gemini

To use cloud-based AI explanations, configure your Gemini API key.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_google_ai_studio_api_key"
```

### Linux / macOS

```bash
export GEMINI_API_KEY="your_google_ai_studio_api_key"
```

Do not commit your API key to GitHub.

For production development, use environment variables or a secure secret-management solution.

---

# 💻 Local AI with Ollama

PyAudit can use Ollama for local AI inference.

Install and configure Ollama separately, then download a compatible model.

For example:

```bash
ollama pull llama3.2
```

or:

```bash
ollama pull qwen2.5-coder
```

Then run PyAudit in local mode:

```bash
python -m pyaudit.cli scan . --explain --local
```

Local mode is designed to keep AI analysis on the developer's machine.

---

# 🛠️ Usage

## 🔍 Scan a Project

Run a security scan against the current directory:

```bash
python -m pyaudit.cli scan .
```

---

## 🤖 Scan with AI Explanations

### Cloud AI

```bash
python -m pyaudit.cli scan . --explain
```

### Local AI

```bash
python -m pyaudit.cli scan . --explain --local
```

---

## 🛠️ Automatically Remediate Findings

```bash
python -m pyaudit.cli scan . --fix
```

Review all automatically modified files before committing changes.

---

## 💬 Start the Security Assistant

### Cloud Mode

```bash
python -m pyaudit.cli chat
```

### Local Mode

```bash
python -m pyaudit.cli chat --local
```

---

## 📄 Export Scan Results

### JSON

```bash
python -m pyaudit.cli scan . -o report.json
```

### Markdown

```bash
python -m pyaudit.cli scan . -o report.md
```

---

## 🔒 Install the Git Security Hook

```bash
python -m pyaudit.cli install-hook
```

After installation, PyAudit can perform security checks as part of the Git commit workflow.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      PyAudit CLI     │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
        │ AST Analyzer  │   │ Secret Scanner│   │ Dependency    │
        │               │   │               │   │ Analyzer      │
        └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
                │                   │                   │
                └───────────────────┼───────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Security Findings    │
                         └──────────┬───────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
           ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
           │ AI Engine   │  │ Remediation  │  │ Reporting    │
           │             │  │ Engine       │  │              │
           └──────┬──────┘  └──────┬───────┘  └──────┬───────┘
                  │                │                 │
          ┌───────┴───────┐        │        ┌────────┴────────┐
          │               │        │        │                 │
          ▼               ▼        ▼        ▼                 ▼
       Gemini          Ollama   --fix     JSON            Markdown
```

---

# 📂 Project Structure

```text
PyAudit/
│
├── pyaudit/
│   ├── __init__.py
│   ├── cli.py
│   │
│   ├── scanner/
│   │   ├── ast_analyzer.py
│   │   ├── secret_scanner.py
│   │   └── dependency_checker.py
│   │
│   ├── ai/
│   │   ├── gemini.py
│   │   └── ollama.py
│   │
│   ├── remediation/
│   │   └── fixer.py
│   │
│   └── reporting/
│       ├── json_report.py
│       └── markdown_report.py
│
├── tests/
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

> The exact project structure may evolve as PyAudit develops.

---

# 🛡️ Security & Privacy

PyAudit follows a privacy-focused approach to security analysis.

### Local Static Analysis

AST parsing and local security checks are performed on the developer's machine.

Source code is not required to be uploaded to a remote server for basic static analysis.

### Local AI Mode

When using:

```bash
--local
```

AI requests are routed through a locally running Ollama instance rather than a cloud AI provider.

This is useful when working with:

* Proprietary source code
* Internal projects
* Sensitive development environments
* Code that should remain on the local machine

### API Keys

Never commit API keys or credentials to GitHub.

Use environment variables for sensitive configuration.

---

# ⚠️ Important Notes

PyAudit is a developer security tool and should be treated as an additional security layer rather than a replacement for a complete security program.

Static analysis can produce:

* False positives
* False negatives
* Findings requiring manual review

Security findings should therefore be validated before taking production actions.

---

# 🧪 Example Workflow

A typical developer workflow can look like this:

```text
1. Write Code
      │
      ▼
2. Run PyAudit
      │
      ▼
3. Detect Vulnerabilities
      │
      ▼
4. Review Findings
      │
      ├── Safe ───────────────► Continue
      │
      └── Vulnerable
                │
                ▼
        AI Security Explanation
                │
                ▼
        Automated Remediation
                │
                ▼
        Developer Review
                │
                ▼
        Git Pre-Commit Check
                │
                ▼
             Commit
```

---

# 🎯 Project Goals

PyAudit aims to make security analysis more accessible to developers by bringing essential DevSecOps capabilities directly into the development workflow.

Future development areas may include:

* Expanded vulnerability rules
* More secret detection patterns
* Improved dependency intelligence
* Additional programming language support
* SARIF report generation
* CI/CD integrations
* GitHub Actions integration
* Improved vulnerability prioritization
* Security dashboards
* Additional local LLM support

---

# 🤝 Contributing

Contributions, bug reports, feature requests, and security improvements are welcome.

### Basic contribution workflow


```bash
git clone https://github.com/vrajardeshana19-bit/PyAudit.git
cd PyAudit

git checkout -b feature/your-feature

# Make your changes

git add .
git commit -m "Add: your feature"

git push origin feature/your-feature
```

Then open a Pull Request on GitHub.

---

# 📜 License

PyAudit is distributed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for more information.

---

# ⭐ Support the Project

If you find PyAudit useful:

* ⭐ Star the repository
* 🐛 Report bugs
* 💡 Suggest improvements
* 🔧 Contribute features
* 📢 Share the project with other developers

---

## 🛡️ PyAudit

**Security scanning for developers, built for the DevSecOps workflow.**

Built with ❤️ by **Vraj Ardeshana**
