# 🛡️ PyAudit

> A lightweight, asynchronous Python security tool that scans source code for static vulnerabilities, hardcoded credentials, and maps findings to the **MITRE ATT&CK** matrix.

## 🚀 Key Features

* **AST Static Code Analysis**: Parses Python code trees to catch high-risk functions (`eval`, `exec`, `verify=False`).
* **Secret & Entropy Scanner**: Detects exposed API keys (AWS, OpenAI, GitHub PATs) using pattern matching and Shannon Entropy calculations.
* **MITRE ATT&CK Mapping**: Automatically maps security flaws to standard MITRE IDs.
* **Terminal UI**: Clean, formatted tables rendered with `rich` and `typer`.
* **Export Engines**: Supports generating structured reports in `.json` and `.md` formats.

## 📦 Installation

```bash
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/pyaudit.git
cd pyaudit
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
