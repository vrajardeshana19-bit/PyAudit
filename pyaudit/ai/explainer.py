import os
from google import genai
from rich.console import Console
from rich.panel import Panel

console = Console()

async def explain_finding_with_ai(file_path: str, line_number: int, issue: str, mitre_id: str):
    """Uses the official Google GenAI SDK to generate security explanations and fix recommendations."""
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

    try:
        client = genai.Client(api_key=api_key)
        
        # Retry up to 3 times on 503 server spikes
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )
                break
            except Exception as e:
                if "503" in str(e) and attempt < 2:
                    import asyncio
                    await asyncio.sleep(2)
                    continue
                raise e
        if response and response.text:
            panel = Panel(
                response.text,
                title=f"[bold green]🤖 PyAudit AI Security Insights — {file_path}:{line_number}[/bold green]",
                border_style="magenta",
                expand=False
            )
            console.print(panel)
        else:
            console.print("[bold red]❌ Empty response received from Gemini API.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]❌ AI Explanation Engine Error: {e}[/bold red]")