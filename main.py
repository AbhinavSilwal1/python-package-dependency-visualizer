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

            # Handle: from x import y and relative imports
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                if node.level > 0:
                    module = "." * node.level + module

                imports.add(module)

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


# Find internal project dependencies
def find_internal_dependencies(dependency_graph: dict[str, set[str]]) -> dict[str, set[str]]:
    internal_dependencies = {}

    project_modules = {
        Path(file).stem
        for file in dependency_graph
    }

    for file, imports in dependency_graph.items():
        internal_dependencies[file] = {
            module
            for module in imports
            if module.split(".")[0] in project_modules
        }

    return internal_dependencies


# Calculate dependency statistics
def calculate_statistics(
    dependency_graph: dict[str, set[str]],
    internal_dependencies: dict[str, set[str]]
) -> dict[str, float]:

    total_files = len(dependency_graph)

    total_imports = sum(
        len(imports)
        for imports in dependency_graph.values()
    )

    total_internal = sum(
        len(imports)
        for imports in internal_dependencies.values()
    )

    average_imports = (
        total_imports / total_files
        if total_files > 0
        else 0
    )

    return {
        "total_files": total_files,
        "total_imports": total_imports,
        "total_internal": total_internal,
        "average_imports": average_imports
    }


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

    internal_dependencies = find_internal_dependencies(dependency_graph)
    statistics = calculate_statistics(dependency_graph,internal_dependencies)

    for file, imports in dependency_graph.items():
        print(f"\n{file}")

        if imports:
            print("  Imports:")
            for imp in sorted(imports):
                print(f"    - {imp}")
        
        else:
            print("  No imports found")

        print("  Internal Dependencies:")

        internal = internal_dependencies[file]

        if internal:
            for dependency in sorted(internal):
                print(f"    - {dependency}")

        else:
            print("    None")

    print("\nProject Summary")
    print("-" * 15)

    print(f"Python files: {statistics['total_files']}")
    print(f"Total imports: {statistics['total_imports']}")
    print(f"Internal dependencies: {statistics['total_internal']}")
    print(f"Average imports per file: {statistics['average_imports']:.1f}")


if __name__ == "__main__":
    app()