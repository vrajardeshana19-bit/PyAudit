import os
import typer
from rich.console import Console
from rich.table import Table

from pyaudit.scanner.ast_analyzer import analyze_file
from pyaudit.scanner.secret_scanner import scan_file_for_secrets
from pyaudit.reporter.export import export_to_json, export_to_markdown

app = typer.Typer(help="PyAudit — Lightweight Python Security & Secret Scanner")
console = Console()

@app.callback()
def main():
    """PyAudit CLI Tool"""
    pass

@app.command()
def scan(
    target_dir: str = typer.Argument(".", help="Directory path to scan"),
    output: str = typer.Option(None, "--output", "-o", help="Path to export report (.json or .md)")
):
    console.print(f"\n[bold blue]🔍 Starting PyAudit scan on:[bold blue] [yellow]{target_dir}[/yellow]\n")

    all_ast_findings = []
    all_secret_findings = []

    for root, _, files in os.walk(target_dir):
        if "venv" in root or ".venv" in root or ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith(".py"):
                all_ast_findings.extend(analyze_file(file_path))

            all_secret_findings.extend(scan_file_for_secrets(file_path))

    combined_findings = all_ast_findings + all_secret_findings

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

    if output:
        if output.endswith(".json"):
            export_to_json(combined_findings, output)
            console.print(f"[bold yellow]📄 Report exported to JSON:[bold yellow] [green]{output}[/green]\n")
        elif output.endswith(".md"):
            export_to_markdown(combined_findings, output)
            console.print(f"[bold yellow]📄 Report exported to Markdown:[bold yellow] [green]{output}[/green]\n")
        else:
            console.print("[bold red]❌ Unsupported extension. Use .json or .md[/bold red]\n")

if __name__ == "__main__":
    app()