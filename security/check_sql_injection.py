import os
import sys
import re

findings = []


def scan_for_sql_issues():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app_path = os.path.join(project_root, "app")

    dangerous_patterns = [
        r"execute\(.+\+.+\)",  # string concatenation in SQL
        r"f\"SELECT .*{.*}\"",  # f-string SQL
        r"SELECT .* \+ .*",  # SQL string concatenation
    ]

    for root, _, files in os.walk(app_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                    for pattern in dangerous_patterns:
                        if re.search(pattern, content):
                            findings.append(
                                {
                                    "file": filepath,
                                    "issue": "Possible SQL Injection",
                                    "severity": "HIGH",
                                }
                            )


if __name__ == "__main__":
    print("Running SQL Injection Pattern Check...\n")
    scan_for_sql_issues()

    if findings:
        for f in findings:
            print(f"[{f['severity']}] {f['issue']} in {f['file']}")
        sys.exit(1)
    else:
        print("Security Check PASSED ✅")
        sys.exit(0)
