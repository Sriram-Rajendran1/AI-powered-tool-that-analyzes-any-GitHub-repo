import os
import ast
import re

# Supported code file types
CODE_EXTENSIONS = (".py", ".js", ".ts", ".go", ".java", ".cpp", ".c", ".cs")


def build_folder_tree(root_path: str) -> dict:
    """
    Build nested folder tree structure.
    """
    def build_node(path: str) -> dict:
        name = os.path.basename(path) or path

        if os.path.isdir(path):
            children = []
            for entry in sorted(os.listdir(path)):
                full_path = os.path.join(path, entry)

                if entry in {".git", "__pycache__", ".venv", "venv"}:
                    continue

                children.append(build_node(full_path))

            return {"name": name, "type": "folder", "children": children}

        return {"name": name, "type": "file"}

    return build_node(root_path)


def folder_tree_to_text(tree: dict, indent: int = 0) -> str:
    prefix = "  " * indent
    lines = []

    if tree["type"] == "folder":
        lines.append(f"{prefix}{tree['name']}/")
        for child in tree["children"]:
            lines.append(folder_tree_to_text(child, indent + 1))
    else:
        lines.append(f"{prefix}{tree['name']}")

    return "\n".join(lines)


def detect_language_by_ext(ext: str) -> str:
    return {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".go": "go",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "csharp"
    }.get(ext.lower(), "code")


# ---------------- Dependency Parsers ----------------

def get_python_imports(code: str):
    imports = []
    try:
        tree = ast.parse(code)
    except:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)

    return imports


JS_IMPORT_RE = re.compile(
    r"(?:import\s+.*?\s+from\s+['\"](.*?)['\"]|require\(['\"](.*?)['\"]\))"
)


def get_js_imports(code: str):
    imports = []
    for m in JS_IMPORT_RE.finditer(code):
        mod = m.group(1) or m.group(2)
        if mod:
            imports.append(mod)
    return imports
