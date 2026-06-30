import ast
from pathlib import Path


# Extract import statements from a Python file using AST
def extract_imports(file_path: Path) -> set[str]:
    imports = set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))

        for node in ast.walk(tree):

            # Handle: import x
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)

            # Handle: from x import y and relative imports
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                if node.level > 0:
                    module = "." * node.level + module

                imports.add(module)

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return imports