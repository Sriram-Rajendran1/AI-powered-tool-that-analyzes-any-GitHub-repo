import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Initialize client
client = OpenAI()

MODEL_NAME = "gpt-4o-mini"



def llm(prompt: str, max_tokens: int = 2000) -> str:
    """
    Call OpenAI responses API and return plain text.
    """
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        max_output_tokens=max_tokens
    )
    return response.output_text or ""


def explain_code(code: str, filepath: str) -> str:
    prompt = f"""
You are a senior software engineer.

Explain this file step-by-step.

File path: {filepath}

Code:
{code}

Return the output in this structure:

Summary:
- short summary (2–3 lines)

Step-by-step Explanation:
- point 1
- point 2
- point 3

Key Functions or Classes:
- name : short explanation

Role in Project:
- explain how this file connects to the project
"""
    return llm(prompt)


def security_scan(code: str, filepath: str, language: str) -> str:
    prompt = f"""
You are a professional application security auditor.

Scan this {language} code file for vulnerabilities.

File: {filepath}

Code:
{code}

Return the output in this structure:

Security Issues:

Issue:
- Type:
- Severity:
- Description:
- Fix Recommendation:
"""
    return llm(prompt)


def generate_tests(code: str, filepath: str, language: str) -> str:
    prompt = f"""
You are a QA engineer.

Generate unit + integration tests for this {language} file.

File: {filepath}

Code:
{code}

Return the output in this structure:

Test Strategy:
- bullet points

Unit Tests:
- code examples (pytest / Jest / JUnit etc)

Integration Tests:
- code or explanation (if relevant)
"""
    return llm(prompt)


def generate_architecture_diagram(repo_name: str, folder_tree_text: str) -> str:
    prompt = f"""
You are a senior system architect.

Analyze this project and generate:

1. Architecture Overview
2. Mermaid Diagram

Repository Name:
{repo_name}

Folder Structure:
{folder_tree_text}

Return the output in this structure:

Architecture Overview:
- text explanation

Mermaid Diagram:
flowchart TD
  A[Component] --> B[Component]
"""
    return llm(prompt, max_tokens=2500)
