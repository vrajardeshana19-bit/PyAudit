import os
import sys
import asyncio
import typer
from rich.console import Console
from rich.table import Table

from pyaudit.scanner.ast_analyzer import analyze_file
from pyaudit.scanner.secret_scanner import scan_file_for_secrets
from pyaudit.scanner.dep_checker import check_dependencies
from pyaudit.reporter.export import export_to_json, export_to_markdown
from pyaudit.remediator.fixer import fix_vulnerable_dependencies, apply_secret_gitignore_fix
from pyaudit.ai.explainer import explain_finding_with_ai

app = typer.Typer(help="PyAudit — Asynchronous Python Security & Secret Scanner")
console = Console()

@app.callback()
def main():
    """PyAudit CLI Tool"""
    pass

@app.command()
def scan(
    target_dir: str = typer.Argument(".", help="Directory path to scan"),
    output: str = typer.Option(None, "--output", "-o", help="Path to export report (.json or .md)"),
    strict: bool = typer.Option(False, "--strict", help="Exit with non-zero code if findings exist"),
    fix: bool = typer.Option(False, "--fix", help="Automatically attempt remediation for detected issues"),
    explain: bool = typer.Option(False, "--explain", help="Use AI to explain findings and suggest safe refactored code"),
    local: bool = typer.Option(False, "--local", help="Use local Ollama instance instead of Cloud LLM API for --explain")
):
    console.print(f"\n[bold blue]🔍 Starting PyAudit scan on:[bold blue] [yellow]{target_dir}[/yellow]\n")

    all_ast_findings = []
    all_secret_findings = []
    all_dep_findings = []

    for root, _, files in os.walk(target_dir):
        if "venv" in root or ".venv" in root or ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)

            # 1. AST Code Analysis (.py files)
            if file.endswith(".py"):
                all_ast_findings.extend(analyze_file(file_path))

            # 2. Secret & Credential Scanning
            all_secret_findings.extend(scan_file_for_secrets(file_path))

            # 3. Dependency CVE Scanning
            if "requirements" in file.lower() and file.endswith(".txt"):
                dep_results = asyncio.run(check_dependencies(file_path))
                all_dep_findings.extend(dep_results)

    combined_findings = all_ast_findings + all_secret_findings + all_dep_findings

    table = Table(title="PyAudit Security Findings")
    table.add_column("File", style="cyan")
    table.add_column("Line", style="magenta")
    table.add_column("Severity", style="bold red")
    table.add_column("Issue Description", style="white")
    table.add_column("MITRE ATT&CK", style="green")

    for item in combined_findings:
        table.add_row(
            item.file_path,
            str(item.line_number),
            item.severity,
            item.issue,
            item.mitre_id
        )

    console.print(table)
    console.print(f"\n[bold green]Scan complete.[bold green] Found [bold red]{len(combined_findings)}[/bold red] potential issue(s).\n")

    # AI Remediation Explainer Module (Cloud or Local Ollama)
    if explain and combined_findings:
        mode_str = "Local Ollama" if local else "Cloud AI"
        console.print(f"[bold magenta]🤖 Requesting AI Security Explanations ({mode_str})...[/bold magenta]\n")
        for item in combined_findings:
            asyncio.run(explain_finding_with_ai(item.file_path, item.line_number, item.issue, item.mitre_id, local=local))

    # Auto-Remediation Execution Engine
    if fix and combined_findings:
        console.print("[bold cyan]🛠️  Executing PyAudit Auto-Remediation Engine...[/bold cyan]\n")
        
        for root, _, files in os.walk(target_dir):
            for file in files:
                if "requirements" in file.lower() and file.endswith(".txt"):
                    req_path = os.path.join(root, file)
                    asyncio.run(fix_vulnerable_dependencies(req_path))

        for secret_finding in all_secret_findings:
            apply_secret_gitignore_fix(secret_finding.file_path)

        console.print("\n[bold green]✅ Auto-remediation actions completed successfully![/bold green]\n")

    if output:
        if output.endswith(".json"):
            export_to_json(combined_findings, output)
            console.print(f"[bold yellow]📄 Report exported to JSON:[bold yellow] [green]{output}[/green]\n")
        elif output.endswith(".md"):
            export_to_markdown(combined_findings, output)
            console.print(f"[bold yellow]📄 Report exported to Markdown:[bold yellow] [green]{output}[/green]\n")
        else:
            console.print("[bold red]❌ Unsupported extension. Use .json or .md[/bold red]\n")

    if strict and len(combined_findings) > 0:
        raise typer.Exit(code=1)

@app.command()
def install_hook():
    """Installs PyAudit as a Git pre-commit hook."""
    git_dir = os.path.join(".", ".git")
    if not os.path.exists(git_dir):
        console.print("[bold red]❌ Not a Git repository. Run 'git init' first.[/bold red]\n")
        return

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    hook_path = os.path.join(hooks_dir, "pre-commit")

    hook_script = """#!/bin/sh
echo "🔍 Running PyAudit pre-commit security gate..."
python -m pyaudit.cli scan . --strict
if [ $? -ne 0 ]; then
    echo "❌ [PyAudit] Security flaws or leaked keys detected! Commit aborted."
    exit 1
fi
"""
    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(hook_script)

    try:
        os.chmod(hook_path, 0o755)
    except Exception:
        pass

    console.print("[bold green]✅ PyAudit pre-commit gate successfully installed in .git/hooks/pre-commit![/bold green]\n")

if __name__ == "__main__":
    app()