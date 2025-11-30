import os

from fs_service import (
    CODE_EXTENSIONS,
    build_folder_tree,
    folder_tree_to_text,
    detect_language_by_ext,
    get_python_imports,
    get_js_imports
)

from llm_service import (
    explain_code,
    security_scan,
    generate_tests,
    generate_architecture_diagram
)


def analyze_repo_dir(repo_path: str, repo_name: str) -> dict:
    folder_tree = build_folder_tree(repo_path)
    folder_tree_text = folder_tree_to_text(folder_tree)

    summaries = {}
    security = {}
    tests = {}
    dependencies = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".venv", "venv"}]

        for file in files:
            path = os.path.join(root, file)
            rel = os.path.relpath(path, repo_path).replace("\\", "/")
            _, ext = os.path.splitext(file)

            if ext.lower() not in CODE_EXTENSIONS:
                continue

            try:
                code = open(path, "r", encoding="utf8", errors="ignore").read()
            except:
                continue

            lang = detect_language_by_ext(ext)

            summaries[rel] = explain_code(code, rel)
            security[rel] = security_scan(code, rel, lang)
            tests[rel] = generate_tests(code, rel, lang)

            # Dependencies
            if ext == ".py":
                imports = get_python_imports(code)
            elif ext in (".js", ".ts"):
                imports = get_js_imports(code)
            else:
                imports = []

            for imp in imports:
                dependencies.append({"source": rel, "target": imp})

    architecture = generate_architecture_diagram(repo_name, folder_tree_text)

    return {
        "repo_name": repo_name,
        "folder_tree": folder_tree,
        "folder_tree_text": folder_tree_text,
        "file_summaries": summaries,
        "security_reports": security,
        "test_cases": tests,
        "dependency_graph": dependencies,
        "architecture": architecture
    }
