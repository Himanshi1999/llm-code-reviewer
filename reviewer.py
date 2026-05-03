from google import genai
import os
import sys
import re
import glob

# Setup client
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# Known defect patterns to flag automatically
DEFECT_PATTERNS = [
    {
        "name": "Hardcoded Password",
        "pattern": r'password\s*=\s*["\'].*["\']',
        "severity": "CRITICAL",
        "suggestion": "Use environment variables instead"
    },
    {
        "name": "Hardcoded API Key",
        "pattern": r'api_key\s*=\s*["\'].*["\']',
        "severity": "CRITICAL",
        "suggestion": "Use environment variables instead"
    },
    {
        "name": "SQL Injection Risk",
        "pattern": r'SELECT.*\+.*|INSERT.*\+.*|DELETE.*\+.*',
        "severity": "CRITICAL",
        "suggestion": "Use parameterized queries"
    },
    {
        "name": "File Not Closed",
        "pattern": r'open\(.*\)(?!.*with)',
        "severity": "HIGH",
        "suggestion": "Use 'with open()' to auto close files"
    },
    {
        "name": "Division Without Zero Check",
        "pattern": r'\/(?!\/)',
        "severity": "MEDIUM",
        "suggestion": "Check for zero before dividing"
    },
    {
        "name": "Empty Exception Handler",
        "pattern": r'except:\s*pass',
        "severity": "HIGH",
        "suggestion": "Always handle exceptions explicitly"
    },
    {
        "name": "Print Used for Debugging",
        "pattern": r'\bprint\b',
        "severity": "LOW",
        "suggestion": "Use logging module instead of print"
    },
    {
    "name": "Missing Return Statement",
    "pattern": r'def .*:(?!.*return)',
    "severity": "MEDIUM",
    "suggestion": "Ensure functions return expected values"
    },
]

def detect_patterns(code):
    """First pass — flag known defect patterns before LLM review"""
    findings = []
    lines = code.split('\n')

    for pattern_info in DEFECT_PATTERNS:
        for line_num, line in enumerate(lines, 1):
            if re.search(pattern_info["pattern"], line, re.IGNORECASE):
                findings.append({
                    "line": line_num,
                    "code": line.strip(),
                    "issue": pattern_info["name"],
                    "severity": pattern_info["severity"],
                    "suggestion": pattern_info["suggestion"]
                })

    return findings

def print_pattern_report(findings):
    """Print defect pattern findings"""
    if not findings:
        print("✅ No known defect patterns found\n")
        return

    print(f"⚠️  Found {len(findings)} defect pattern(s):\n")
    for f in findings:
        print(f"  [{f['severity']}] Line {f['line']}: {f['issue']}")
        print(f"  Code    : {f['code']}")
        print(f"  Fix     : {f['suggestion']}")
        print()

def review_code(file_path):
    # Read the Python file
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()

    print(f"\n📝 Reviewing: {file_path}\n")
    print("=" * 50)

    # Step 1 — Pattern detection (fast, no API call)
    print("🔍 STEP 1: Scanning for known defect patterns...\n")
    findings = detect_patterns(code)
    print_pattern_report(findings)

    # Step 2 — LLM deep review
    print("🤖 STEP 2: Running LLM deep review...\n")
    print("=" * 50)

    prompt = f"""
    You are an expert Python code reviewer.
    Review the following code and provide:
    1. Bugs or errors found
    2. Bad practices
    3. Security issues
    4. Suggestions to improve
    5. Overall quality score out of 10

    Code to review:
    {code}
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    print(response.text)

    # Step 3 — Save full report
    report_path = file_path.replace('.py', '_review.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=== DEFECT PATTERN SCAN ===\n\n")
        for finding in findings:
            f.write(f"[{finding['severity']}] Line {finding['line']}: {finding['issue']}\n")
            f.write(f"Code: {finding['code']}\n")
            f.write(f"Fix: {finding['suggestion']}\n\n")
        f.write("\n=== LLM DEEP REVIEW ===\n\n")
        f.write(response.text)

    print(f"\n✅ Report saved to: {report_path}")

def review_folder(folder_path):
    """Review all Python files in a folder"""
    
    # Same skip list as doc generator
    SKIP_FOLDERS = [
        'venv', 'node_modules', '__pycache__',
        '.git', '.idea', 'dist', 'build', 'env'
    ]

    py_files = [
        f for f in glob.glob(f"{folder_path}/**/*.py", recursive=True)
        if not any(skip in f.split(os.sep) for skip in SKIP_FOLDERS)
    ]

    if not py_files:
        print(f"No Python files found in {folder_path}")
        return

    print(f"\n📁 Found {len(py_files)} file(s) to review:\n")
    for f in py_files:
        print(f"  - {f}")

    print("\n" + "=" * 50)

    # Review each file one by one
    total_findings = 0
    for file_path in py_files:
        review_code(file_path)
        total_findings += 1
        print("\n" + "=" * 50 + "\n")

    print(f"✅ Done! Reviewed {total_findings} file(s)")
    print(f"📄 Individual reports saved next to each file")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Review one file   : python reviewer.py sample.py")
        print("  Review folder     : python reviewer.py --folder .")
    elif sys.argv[1] == "--folder":
        if len(sys.argv) < 3:
            print("Please provide folder path: python reviewer.py --folder <path>")
        else:
            review_folder(sys.argv[2])
    else:
        review_code(sys.argv[1])