import re
import math
from pydantic import BaseModel

class SecretFinding(BaseModel):
    file_path: str
    line_number: int
    issue: str
    severity: str
    mitre_id: str

SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Personal Access Token": r"ghp_[a-zA-Z0-9]{36}",
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{48}",
    "Generic Private Key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
}

def calculate_shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    entropy = 0.0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        entropy -= p_x * math.log2(p_x)
    return entropy

def scan_file_for_secrets(file_path: str) -> list[SecretFinding]:
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f, start=1):
                clean_line = line.strip()

                for secret_type, pattern in SECRET_PATTERNS.items():
                    if re.search(pattern, clean_line):
                        findings.append(
                            SecretFinding(
                                file_path=file_path,
                                line_number=line_idx,
                                issue=f"Exposed secret detected: {secret_type}",
                                severity="HIGH",
                                mitre_id="T1552.001"
                            )
                        )

                words = clean_line.split()
                for word in words:
                    if len(word) > 20 and calculate_shannon_entropy(word) > 4.5:
                        findings.append(
                            SecretFinding(
                                file_path=file_path,
                                line_number=line_idx,
                                issue="High-entropy string detected (possible secret/token)",
                                severity="MEDIUM",
                                mitre_id="T1552.001"
                            )
                        )
    except Exception:
        pass
    return findings