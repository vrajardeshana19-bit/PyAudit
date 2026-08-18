import os
import logging
import httpx
from google import genai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Mute SDK notices and warnings
logging.getLogger("google_genai").setLevel(logging.ERROR)

console = Console()

def start_interactive_chat(local: bool = False):
    """Starts an interactive DevSecOps AI Chat session in the terminal."""
    mode_title = "🦙 Local Ollama (Offline)" if local else "🤖 Google Gemini (Cloud)"
    
    console.print(Panel(
        f"[bold cyan]Welcome to PyAudit AI Security Assistant![/bold cyan]\n"
        f"Powered by: [bold yellow]{mode_title}[/bold yellow]\n\n"
        f"• Ask about code refactoring, vulnerability fixes, or MITRE tactics.\n"
        f"• Type [bold red]'exit'[/bold red] or [bold red]'quit'[/bold red] to close session.",
        title="[bold magenta]🔒 PyAudit DevSecOps Terminal Shell[/bold magenta]",
        border_style="bright_blue",
        expand=False
    ))

    api_key = os.getenv("GEMINI_API_KEY") if not local else None
    if not local and not api_key:
        console.print("[bold red]⚠️ GEMINI_API_KEY environment variable not found. Set your key or run with --local for Ollama.[/bold red]")
        return

    client = genai.Client(api_key=api_key) if not local else None

    while True:
        user_input = Prompt.ask("\n[bold green]pyaudit-ai>[/bold green]")
        if user_input.strip().lower() in ["exit", "quit"]:
            console.print("\n[bold yellow]Ending AI session. Stay secure! 🔒[/bold yellow]\n")
            break

        if not user_input.strip():
            continue

        system_context = (
            "You are PyAudit AI, an expert DevSecOps and Python security advisor. "
            "Help the user understand vulnerabilities, refactoring fixes, and MITRE concepts concisely.\n\n"
            f"User Question: {user_input}"
        )

        # LOCAL MODE (Ollama)
        if local:
            try:
                with console.status("[bold cyan]Analyzing query with local LLM...[/bold cyan]", spinner="dots"):
                    response = httpx.post(
                        "http://localhost:11434/api/generate",
                        json={"model": "llama3.2", "prompt": system_context, "stream": False},
                        timeout=30.0
                    )
                if response.status_code == 200:
                    ans = response.json().get("response", "")
                    console.print(Panel(Markdown(ans), title="🦙 PyAudit AI (Local)", border_style="cyan"))
                else:
                    console.print("[bold red]❌ Failed to reach local Ollama instance on http://localhost:11434[/bold red]")
            except Exception as e:
                console.print(f"[bold red]❌ Ollama Error: {e}[/bold red]")

        # CLOUD MODE (Google GenAI SDK)
        else:
            try:
                with console.status("[bold magenta]Consulting Gemini DevSecOps Brain...[/bold magenta]", spinner="dots"):
                    res = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=system_context
                    )
                if res and res.text:
                    console.print(Panel(Markdown(res.text), title="🤖 PyAudit AI (Cloud)", border_style="magenta"))
                else:
                    console.print("[bold red]❌ Empty response from Gemini API.[/bold red]")
            except Exception as e:
                console.print(f"[bold red]❌ Gemini AI Error: {e}[/bold red]")