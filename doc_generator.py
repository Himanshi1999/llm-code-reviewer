from google import genai
import os
import sys
import glob

# Setup client
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

def read_files(folder_path):
    """Read all Python files from a folder"""
    files_content = {}
    
    # Folders to skip
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
        return {}
    
    print(f"Found {len(py_files)} Python file(s):\n")
    
    for file_path in py_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            files_content[file_path] = content
            print(f"  ✅ {file_path}")
    
    return files_content

def generate_architecture_doc(folder_path):
    """Generate architecture documentation for a codebase"""
    
    print(f"\n📁 Reading files from: {folder_path}\n")
    print("=" * 50)
    
    # Step 1 - Read all files
    files_content = read_files(folder_path)
    
    if not files_content:
        return
    
    # Step 2 - Build prompt with all files
    files_text = ""
    for file_path, content in files_content.items():
        files_text += f"\n\n### File: {file_path}\n```python\n{content}\n```"
    
    prompt = f"""
    You are a senior software architect.
    Analyze the following Python codebase and generate clear architecture documentation.
    
    Include:
    1. Project Overview — what does this project do in simple terms
    2. File Structure — what each file is responsible for
    3. Key Functions — list and explain the most important functions
    4. How Files Connect — how do the files interact with each other
    5. Data Flow — how data moves through the system step by step
    6. Onboarding Guide — 5 steps a new engineer should follow to understand this codebase
    
    Codebase:
    {files_text}
    """
    
    print(f"\n🤖 Generating architecture documentation...\n")
    print("=" * 50)
    
    # Step 3 - Call Gemini
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    print(response.text)
    
    # Step 4 - Save documentation
    doc_path = os.path.join(folder_path, "ARCHITECTURE.md")
    with open(doc_path, 'w') as f:
        f.write("# Architecture Documentation\n\n")
        f.write(f"Generated automatically by LLM Doc Generator\n\n")
        f.write("=" * 50 + "\n\n")
        f.write(response.text)
    
    print(f"\n✅ Architecture doc saved to: {doc_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python doc_generator.py <folder_path>")
        print("Example: python doc_generator.py .")
    else:
        generate_architecture_doc(sys.argv[1])