import typer
from pathlib import Path
import ast


app = typer.Typer()


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

            # Handle: from x import y
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return imports


# Build a dependency graph from Python files
def build_dependency_graph(python_files: list[Path], project_path: Path) -> dict[str, set[str]]:
    dependency_graph = {}

    for file in python_files:
        relative_path = str(file.relative_to(project_path))
        dependency_graph[relative_path] = extract_imports(file)

    return dependency_graph


# Temporary test command to verify CLI works
@app.command()
def hello():
    print("Python Package Dependency Visualizer is running 🚀")


# Show version of the tool
@app.command()
def version():
    print("v0.1.0")


# Scan project and extract imports
@app.command()
def scan(path: str = typer.Argument(".")):
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

    dependency_graph = build_dependency_graph(
        python_files,
        project_path
    )

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