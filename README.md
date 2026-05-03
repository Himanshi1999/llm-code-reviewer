# LLM Code Reviewer

An AI-powered code review tool that automatically detects defect patterns 
and generates architecture documentation using Gemini API.

## Features
- Detects known defect patterns (SQL injection, hardcoded secrets, resource leaks)
- LLM-powered deep code review with improvement suggestions
- Generates architecture documentation for entire codebases
- Reviews single files or entire project folders

## Setup

1. Clone the repo

2. Create virtual environment

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install google-genai

4. Set your Gemini API key

set GEMINI_API_KEY=your_key_here

## Usage

Review a single file:
python reviewer.py sample.py

Review entire folder:
python reviewer.py --folder .

Generate architecture docs:
python doc_generator.py .

## Tech Stack
- Python
- Google Gemini API (swappable with Claude/OpenAI)
- Regex pattern matching
- File I/O