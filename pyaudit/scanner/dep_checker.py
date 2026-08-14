import httpx
from pydantic import BaseModel

class DepFinding(BaseModel):
    file_path: str
    line_number: int
    issue: str
    severity: str
    mitre_id: str

async def check_dependencies(req_file_path: str) -> list[DepFinding]:
    """Scans requirements.txt against the OSV.dev REST API for known CVE vulnerabilities."""
    findings = []
    try:
        async with httpx.AsyncClient() as client:
            with open(req_file_path, "r", encoding="utf-8") as f:
                for line_idx, line in enumerate(f, start=1):
                    clean_line = line.strip()
                    # Parse standard package==version lines
                    if clean_line and not clean_line.startswith("#") and "==" in clean_line:
                        parts = clean_line.split("==")
                        package = parts[0].strip()
                        version = parts[1].strip()
                        payload = {"package": {"name": package, "ecosystem": "PyPI"}, "version": version}
                        
                        try:
                            response = await client.post("https://api.osv.dev/v1/query", json=payload, timeout=5.0)
                            if response.status_code == 200:
                                res_data = response.json()
                                if "vulns" in res_data:
                                    vuln_count = len(res_data["vulns"])
                                    findings.append(
                                        DepFinding(
                                            file_path=req_file_path,
                                            line_number=line_idx,
                                            issue=f"Vulnerable dependency: {package}=={version} ({vuln_count} known CVEs)",
                                            severity="HIGH",
                                            mitre_id="T1195.002"
                                        )
                                    )
                        except Exception:
                            continue
    except Exception:
        pass
    return findings