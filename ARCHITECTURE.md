# Architecture Documentation

Generated automatically by LLM Doc Generator

==================================================

As a Senior Software Architect, I have analyzed the provided Python codebase. Below is the architecture documentation, outlining its purpose, structure, interactions, and an onboarding guide for new engineers.

---

## Architecture Documentation: LLM-Powered Development Tools

### 1. Project Overview

This project provides a set of command-line utilities designed to leverage Large Language Models (LLMs), specifically Google's Gemini API, to enhance various aspects of software development. It comprises two primary tools:

1.  **Architecture Documentation Generator (`doc_generator.py`)**: This tool automates the creation of high-level architecture documentation for a given Python codebase. It intelligently scans a specified folder, aggregates all Python file contents, and then prompts an LLM to generate a structured `ARCHITECTURE.md` file, detailing the project's overview, file structure, key functions, data flow, and an onboarding guide.
2.  **Code Reviewer (`reviewer.py`)**: This utility offers a two-stage code review process for individual Python files. It first performs a fast, pattern-based static analysis to flag known defects (e.g., hardcoded secrets, SQL injection risks) using regular expressions. Subsequently, it engages an LLM for a deeper, more nuanced review, covering potential bugs, bad practices, security vulnerabilities, and suggestions for improvement, outputting a detailed `_review.txt` report.

The `sample.py` file serves as an example codebase, deliberately including common coding pitfalls, to effectively demonstrate the capabilities of the `reviewer.py` script and to be processed by `doc_generator.py`. The overall goal of this project is to streamline documentation and initial code quality assurance by integrating AI into the development workflow.

### 2. File Structure

The project is composed of three distinct Python files, each with a specialized role:

*   **`doc_generator.py`**:
    *   **Responsibility**: This is the core application for automated architecture documentation generation. It handles file system traversal, content aggregation of multiple Python files, crafting detailed prompts for the LLM, making API calls to Google Gemini, and persisting the generated documentation to a Markdown file.
    *   **Key Dependencies**: `google.genai`, `os`, `sys`, `glob`.

*   **`reviewer.py`**:
    *   **Responsibility**: This file is dedicated to providing automated code reviews. It encompasses both a rule-based static analysis engine (using regular expressions) for quick detection of known defect patterns and an LLM-driven deep review for comprehensive analysis of a single Python file. It formats and saves the review findings.
    *   **Key Dependencies**: `google.genai`, `os`, `sys`, `re`.

*   **`sample.py`**:
    *   **Responsibility**: This file acts as a demonstration or test case for the `reviewer.py` and `doc_generator.py` tools. It contains various Python constructs, some of which are intentionally written with common errors (e.g., hardcoded credentials, potential division-by-zero, resource leaks, SQL injection vulnerability) to showcase the defect detection and review capabilities of the other scripts.
    *   **Key Dependencies**: `os`, `json` (though `json` is imported, it's not used in the provided snippet).

### 3. Key Functions

Here are the most important functions across the codebase:

**In `doc_generator.py`:**

*   **`read_files(folder_path)`**:
    *   **Purpose**: To discover and read the content of all relevant Python files within a specified directory.
    *   **Explanation**: This function uses `glob` to recursively find all `.py` files, while crucially filtering out common development-related directories (e.g., `venv`, `node_modules`, `__pycache__`, `.git`) to avoid irrelevant or generated code. It returns a dictionary mapping file paths to their full string content, forming the raw input for the LLM.

*   **`generate_architecture_doc(folder_path)`**:
    *   **Purpose**: The primary orchestrator for the entire documentation generation process.
    *   **Explanation**: It first invokes `read_files` to collect the codebase. It then dynamically constructs a comprehensive prompt for the Gemini LLM, embedding all gathered file contents with clear delimiters. After sending this prompt to the `gemini-2.5-flash` model via the `genai.Client`, it prints the LLM's response and saves the complete, formatted documentation into an `ARCHITECTURE.md` file in the target folder.

**In `reviewer.py`:**

*   **`detect_patterns(code)`**:
    *   **Purpose**: To perform a fast, rule-based scan for predefined defect patterns within a given code string.
    *   **Explanation**: This function iterates through the `DEFECT_PATTERNS` list, which contains regular expressions for known issues like hardcoded secrets, insecure SQL query construction, unclosed file handles, and more. It uses `re.search` to find matches in the provided code, recording detailed findings including line number, issue, severity, and suggested fix, acting as the first line of defense in the review process.

*   **`review_code(file_path)`**:
    *   **Purpose**: The central function that coordinates the multi-stage code review for a single Python file.
    *   **Explanation**: It reads the target Python file, then initiates the `detect_patterns` function for a quick static analysis, printing its findings. Following this, it constructs an LLM-specific prompt, providing the entire code to the Gemini LLM for a deeper, more contextual review (covering bugs, bad practices, security, and overall quality). The LLM's response is then printed and combined with the pattern findings into a detailed `_review.txt` report saved alongside the original file.

### 4. How Files Connect

The files in this project are designed as standalone command-line tools but share fundamental commonalities in their operational model and dependencies. They do not directly import or call functions from one another but rather share an implicit connection through their purpose and reliance on external services.

*   **External LLM Dependency (Google Gemini API)**: Both `doc_generator.py` and `reviewer.py` are critically dependent on the `google.genai` library. They each initialize a `genai.Client` using an API key (fetched from the `GEMINI_API_KEY` environment variable). This shared dependency is the core mechanism by which both tools perform their intelligent operations, leveraging the computational and analytical power of LLMs.

*   **Environment Variable for Authentication**: Both scripts require the `GEMINI_API_KEY` environment variable to be correctly configured to authenticate with the Google Gemini API. This is a crucial shared setup step.

*   **Shared Target (`sample.py` as an Input)**: While not directly linked programmatically, `sample.py` serves as a common example or test input for both tools.
    *   You would typically run `python reviewer.py sample.py` to get a code review of `sample.py`.
    *   You would run `python doc_generator.py .` (if `sample.py` is in the current directory) to include `sample.py`'s content in the generated project documentation. This demonstrates their conceptual integration within a development workflow.

*   **Internal Connections**:
    *   `doc_generator.py`: The `generate_architecture_doc` function internally calls `read_files` to gather input before interacting with the LLM.
    *   `reviewer.py`: The `review_code` function internally calls `detect_patterns` and `print_pattern_report` as part of its multi-stage review process.

### 5. Data Flow

Here's a step-by-step breakdown of how data moves through the system for each primary tool:

**A. Data Flow for `doc_generator.py` (Architecture Documentation Generation)**

1.  **Command-Line Input**: The user executes the script: `python doc_generator.py <target_folder_path>`. The `<target_folder_path>` is passed as a string.
2.  **File System Scan & Read**:
    *   `generate_architecture_doc(<target_folder_path>)` is invoked.
    *   It calls `read_files(<target_folder_path>)`.
    *   `read_files` performs a recursive scan using `glob`, filtering out specified skip folders.
    *   For each identified Python file, its content is read into memory.
    *   **Data Output**: A dictionary `files_content` mapping absolute file paths (strings) to their full source code content (strings).
3.  **LLM Prompt Construction**:
    *   `generate_architecture_doc` iterates through `files_content`.
    *   It concatenates all file paths and their respective contents into a single, large Markdown-formatted string (`prompt`), clearly demarcating each file's contribution.
    *   **Data Output**: A single, extensive string `prompt` containing instructions and the entire aggregated codebase.
4.  **LLM API Call**:
    *   The `prompt` string is sent to the Google Gemini API (`client.models.generate_content`) using the `gemini-2.5-flash` model.
    *   Authentication is handled via the `GEMINI_API_KEY` environment variable.
    *   **Data Output**: A `response` object from the Gemini API, containing the generated architecture documentation as a string in its `response.text` attribute.
5.  **Documentation Saving**:
    *   The `response.text` content is extracted.
    *   A file path for `ARCHITECTURE.md` is constructed within the `<target_folder_path>`.
    *   The generated documentation (prefixed with a header) is written to this `ARCHITECTURE.md` file.
    *   **Data Output**: An `ARCHITECTURE.md` file is created/updated in the `target_folder_path` containing the AI-generated documentation.

**B. Data Flow for `reviewer.py` (Code Review)**

1.  **Command-Line Input**: The user executes the script: `python reviewer.py <python_file_path>`. The `<python_file_path>` is passed as a string.
2.  **File Read**:
    *   `review_code(<python_file_path>)` is invoked.
    *   The specified Python file is opened, and its entire content is read into a string.
    *   **Data Output**: A string `code` containing the full source code of the file to be reviewed.
3.  **Pattern Detection (First Pass)**:
    *   `review_code` calls `detect_patterns(code)`.
    *   `detect_patterns` applies regular expressions from `DEFECT_PATTERNS` against the `code` string, line by line.
    *   **Data Output**: A list `findings`, where each element is a dictionary detailing a detected issue (line number, code snippet, issue name, severity, suggestion).
4.  **Pattern Report Display**:
    *   `review_code` calls `print_pattern_report(findings)`.
    *   The `findings` are formatted and printed to the console.
    *   **Data Output**: Textual report of detected patterns displayed on the console.
5.  **LLM Prompt Construction**:
    *   `review_code` creates a string `prompt` for the LLM. This prompt includes specific instructions for a deep code review and embeds the `code` string.
    *   **Data Output**: A string `prompt` for the LLM deep review.
6.  **LLM API Call (Deep Review)**:
    *   The `prompt` string is sent to the Google Gemini API (`client.models.generate_content`) using the `gemini-2.5-flash` model.
    *   Authentication is handled via the `GEMINI_API_KEY` environment variable.
    *   **Data Output**: A `response` object from the Gemini API, containing the detailed code review text in `response.text`.
7.  **Review Report Saving**:
    *   The `response.text` content is extracted.
    *   A report file path (e.g., `my_file_review.txt` for `my_file.py`) is constructed.
    *   Both the `findings` from the pattern detection and the LLM's detailed review text are combined into this report file.
    *   **Data Output**: A `_review.txt` file (e.g., `sample_review.txt`) is created/updated next to the original Python file, containing the comprehensive code review.

### 6. Onboarding Guide (5 Steps for a New Engineer)

To effectively understand and contribute to this codebase, a new engineer should follow these steps:

1.  **Understand the Problem Space & Tool Objectives**:
    *   Begin by thoroughly reading the "Project Overview" and "File Structure" sections of this documentation. Grasp the core problem these tools solve (automated documentation and code review) and the distinct responsibilities of `doc_generator.py` and `reviewer.py`. Understand that `sample.py` is a testing artifact.
    *   **Self-Question**: *What specific pain points in software development do these tools address?*

2.  **Set Up the Development Environment & API Key**:
    *   **Prerequisites**: Ensure Python 3.8+ is installed.
    *   **Virtual Environment**: Create and activate a virtual environment: `python -m venv venv` then `source venv/bin/activate` (Linux/macOS) or `.\venv\Scripts\activate` (Windows PowerShell).
    *   **Install Dependencies**: Install the Google Generative AI library: `pip install google-generativeai`.
    *   **API Key**: Obtain a `GEMINI_API_KEY` from Google AI Studio. Set this as an environment variable (e.g., `export GEMINI_API_KEY="your_key"` or `set GEMINI_API_KEY=your_key`) before running any script, as both tools rely on it for LLM communication.
    *   **Self-Check**: *Can I successfully print the value of `os.environ.get('GEMINI_API_KEY')` in a Python interpreter within my activated environment?*

3.  **Explore and Execute `reviewer.py`**:
    *   **Static Analysis**: Examine `reviewer.py`, focusing on the `DEFECT_PATTERNS` list and the `detect_patterns` function. Understand how regular expressions (`re` module) are used for quick, deterministic defect detection.
    *   **LLM Integration**: Then, analyze the `review_code` function. Pay close attention to how the LLM prompt is constructed (the `prompt` string) and how the `genai.Client` is used to send code for deep analysis.
    *   **Hands-on**: Run the reviewer on the provided sample: `python reviewer.py sample.py`. Observe the console output, first for pattern findings, then for the LLM's comprehensive review. Review the generated `sample_review.txt` file.
    *   **Self-Question**: *How do the pattern-based findings differ from the LLM's deep review? What are the strengths of each approach?*

4.  **Explore and Execute `doc_generator.py`**:
    *   **File Aggregation**: Dive into `doc_generator.py`. Focus on the `read_files` function: understand how `glob` is used for recursive file discovery and how `SKIP_FOLDERS` prevent irrelevant files from being included.
    *   **Full Context Prompt**: Study the `generate_architecture_doc` function, specifically how it aggregates the content of multiple files into a single, potentially large, LLM prompt string. This demonstrates managing LLM context windows.
    *   **Hands-on**: Run the documentation generator for the current project directory (or a sub-directory containing Python files): `python doc_generator.py .`. Inspect the newly created `ARCHITECTURE.md` file to see the AI-generated project documentation.
    *   **Self-Question**: *What are the potential limitations of passing an entire codebase as a single prompt to an LLM, especially for large projects?*

5.  **Understand LLM Interaction and Prompt Engineering**:
    *   **Commonalities**: Note that both `doc_generator.py` and `reviewer.py` use the same `genai.Client` and `gemini-2.5-flash` model.
    *   **Prompt Engineering is Key**: Recognize that the quality and relevance of the LLM's output are directly proportional to the clarity, detail, and structure of the input prompts. Experiment with modifying the prompt strings in both `generate_architecture_doc` and `review_code` to see how it affects the generated output.
    *   **Consider LLM Behavior**: Think about how to structure prompts to elicit specific types of information (e.g., "list security issues," "provide a 5-step onboarding guide"). This skill is crucial for extending or refining these tools.
    *   **Self-Question**: *If I wanted the LLM to focus more on performance optimizations, how would I modify the prompt in `reviewer.py`?*