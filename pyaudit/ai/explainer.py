import os
import httpx
from rich.console import Console
from rich.panel import Panel

console = Console()

async def explain_finding_with_ai(file_path: str, line_number: int, issue: str, mitre_id: str):
    """Calls Gemini REST API to explain the security finding and provide a safe code fix."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]⚠️ GEMINI_API_KEY environment variable not found. Skipping AI explanation.[/bold red]")
        return

    # Extract target line context from source file
    code_snippet = ""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if 0 <= line_number - 1 < len(lines):
                    code_snippet = lines[line_number - 1].strip()
    except Exception:
        pass

    prompt = f"""
    You are an expert DevSecOps security advisor.
    A Python security scanner flagged an issue in code:
    File: {file_path}
    Line {line_number}: {code_snippet}
    Issue: {issue}
    MITRE ATT&CK ID: {mitre_id}

    Please provide:
    1. A concise, 2-sentence explanation of why this code is dangerous.
    2. A secure refactored code example replacing the vulnerable code.
    Keep the output clean and markdown-formatted.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                explanation = data["candidates"][0]["content"]["parts"][0]["text"]
                
                panel = Panel(
                    explanation,
                    title=f"[bold green]🤖 PyAudit AI Security Insights — {file_path}:{line_number}[/bold green]",
                    border_style="magenta",
                    expand=False
                )
                console.print(panel)
            else:
                console.print(f"[bold red]❌ AI API request failed ({response.status_code}): {response.text}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]❌ Error generating AI explanation: {e}[/bold red]")