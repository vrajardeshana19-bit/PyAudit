import json
from typing import List, Any

def export_to_json(findings: List[Any], output_path: str):
    """Exports scan findings to a JSON file."""
    report_data = []
    for item in findings:
        if hasattr(item, "model_dump"):
            report_data.append(item.model_dump())
        elif hasattr(item, "__dict__"):
            report_data.append(item.__dict__)
        else:
            report_data.append(dict(item))
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

def export_to_markdown(findings: List[Any], output_path: str):
    """Exports scan findings to a Markdown report."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# PyAudit Security Scan Report\n\n")
        f.write(f"**Total Findings:** {len(findings)}\n\n")
        f.write("| File | Line | Severity | Issue Description | MITRE ATT&CK |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        for item in findings:
            f.write(f"| `{item.file_path}` | {item.line_number} | {item.severity} | {item.issue} | `{item.mitre_id}` |\n")