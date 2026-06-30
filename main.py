import typer
from pathlib import Path
import ast


app = typer.Typer()


def extract_imports(file_path: Path) -> set[str]:
    # Extract import statements from a Python file using AST

    imports = set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))

        for node in ast.walk(tree):
            # Handle: import x
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)

            # Handle: from x import y
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return imports


@app.command()
def hello():
    # Temporary test command to verify CLI works.
    print("Python Package Dependency Visualizer is running 🚀")


@app.command()
def version():
    # Show version of the tool.
    print("v0.1.0")


@app.command()
def scan(path: str = typer.Argument(".")):
    # Scan project and extract imports

    project_path = Path(path)

    print(f"Scanning project: {project_path.resolve()}\n")

    if not project_path.exists():
        print("Path does not exist.")
        raise typer.Exit()

    python_files = []

    for file in project_path.rglob("*.py"):
        if ".venv" in file.parts or "__pycache__" in file.parts:
            continue

        python_files.append(file)

    print(f"Found {len(python_files)} Python files:\n")

    for file in python_files:
        print(f"\n{file.relative_to(project_path)}")

        imports = extract_imports(file)

        if imports:
            print("  Imports:")
            for imp in sorted(imports):
                print(f"    - {imp}")
        else:
            print("  No imports found")


if __name__ == "__main__":
    app()