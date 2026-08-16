import os
import httpx
from rich.console import Console

console = Console()

async def get_latest_pypi_version(package_name: str) -> str | None:
    """Queries PyPI REST API to fetch the latest release version for a package."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5.0)
            if response.status_code == 200:
                return response.json()["info"]["version"]
    except Exception:
        pass
    return None

async def fix_vulnerable_dependencies(req_file_path: str) -> int:
    """Updates vulnerable dependencies in requirements.txt to their latest PyPI versions."""
    fixed_count = 0
    if not os.path.exists(req_file_path):
        return fixed_count

    with open(req_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        clean_line = line.strip()
        if clean_line and not clean_line.startswith("#") and "==" in clean_line:
            package, current_version = clean_line.split("==")[0].strip(), clean_line.split("==")[1].strip()
            latest_version = await get_latest_pypi_version(package)
            if latest_version and latest_version != current_version:
                new_lines.append(f"{package}=={latest_version}\n")
                console.print(f"[bold green]🔧 Auto-upgraded {package}: [red]{current_version}[/red] ➔ [green]{latest_version}[/green][/bold green]")
                fixed_count += 1
                continue
        new_lines.append(line)

    if fixed_count > 0:
        with open(req_file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return fixed_count

def apply_secret_gitignore_fix(file_path: str) -> bool:
    """Appends files containing exposed hardcoded secrets to .gitignore."""
    gitignore_path = ".gitignore"
    clean_path = os.path.normpath(file_path).replace("\\", "/")
    
    existing_entries = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            existing_entries = [line.strip() for line in f.readlines()]

    if clean_path not in existing_entries:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write(f"\n# Auto-ignored by PyAudit Remediation Engine\n{clean_path}\n")
        console.print(f"[bold yellow]🛡️ Added {clean_path} to .gitignore to prevent secret leaks.[/bold yellow]")
        return True
    return False