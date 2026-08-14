import ast
from pydantic import BaseModel

class Finding(BaseModel):
    file_path: str
    line_number: int
    issue: str
    severity: str
    mitre_id: str

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.findings = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
            self.findings.append(
                Finding(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue=f"Use of unsafe function '{node.func.id}' detected.",
                    severity="HIGH",
                    mitre_id="T1059.006"
                )
            )
        for keyword in node.keywords:
            if keyword.arg == "verify" and isinstance(keyword.value, ast.Constant) and keyword.value.value is False:
                self.findings.append(
                    Finding(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        issue="Disabled SSL certificate verification (verify=False).",
                        severity="HIGH",
                        mitre_id="T1557"
                    )
                )
        self.generic_visit(node)

def analyze_file(file_path: str) -> list[Finding]:
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
            visitor = SecurityVisitor(file_path)
            visitor.visit(tree)
            return visitor.findings
        except SyntaxError:
            return []