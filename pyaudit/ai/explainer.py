import os
import logging
import httpx
from google import genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Mute SDK notices and warnings
logging.getLogger("google_genai").setLevel(logging.ERROR)

console = Console()

async def explain_finding_with_ai(
    file_path: str, line_number: int, issue: str, mitre_id: str, local: bool = False
):
    """Generates security explanations using Cloud Gemini SDK or Local Ollama LLM."""
    
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

    # --- LOCAL MODE (Ollama) ---
    if local:
        ollama_url = "http://localhost:11434/api/generate"
        payload = {"model": "llama3.2", "prompt": prompt, "stream": False}
        try:
            with console.status(f"[bold cyan]Asking Local LLM for remediation on {file_path}:{line_number}...[/bold cyan]", spinner="dots"):
                async with httpx.AsyncClient() as client:
                    response = await client.post(ollama_url, json=payload, timeout=30.0)
                    if response.status_code == 200:
                        data = response.json()
                        explanation = data.get("response", "")
                        console.print(Panel(
                            Markdown(explanation),
                            title=f"[bold cyan]🦙 PyAudit Local AI Insights (Ollama) — {file_path}:{line_number}[/bold cyan]",
                            border_style="cyan",
                            expand=False
                        ))
                    else:
                        console.print(f"[bold red]❌ Ollama request failed ({response.status_code}).[/bold red]")
        except Exception as e:
            console.print(f"[bold red]❌ Local Ollama Error: {e}[/bold red]")
        return

    # --- CLOUD MODE (Google GenAI SDK) ---
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]⚠️ GEMINI_API_KEY environment variable not found. Skipping AI explanation.[/bold red]")
        return

    try:
        client = genai.Client(api_key=api_key)
        with console.status(f"[bold magenta]Analyzing finding on {file_path}:{line_number} with Gemini AI...[/bold magenta]", spinner="dots"):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

        if response and response.text:
            console.print(Panel(
                Markdown(response.text),
                title=f"[bold green]🤖 PyAudit AI Security Insights (Cloud) — {file_path}:{line_number}[/bold green]",
                border_style="magenta",
                expand=False
            ))
        else:
            console.print("[bold red]❌ Empty response received from Gemini API.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]❌ AI Explanation Engine Error: {e}[/bold red]")