import os
import sys


def scan_for_debug():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app_path = os.path.join(project_root, "app")

    vulnerable = False

    for root, _, files in os.walk(app_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                    if "debug=True" in content.replace(" ", ""):
                        print(f"[HIGH] Debug mode enabled in {filepath}")
                        vulnerable = True

    return vulnerable


if __name__ == "__main__":
    print("Running Debug Mode Security Check...\n")

    if scan_for_debug():
        print("\nSecurity Check FAILED ❌")
        sys.exit(1)
    else:
        print("Security Check PASSED ✅")
        sys.exit(0)
