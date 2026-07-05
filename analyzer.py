from pathlib import Path
from parser import extract_imports


# Collect Python source files from a project
def collect_python_files(project_path: Path) -> list[Path]:
    python_files = []

    for file in project_path.rglob("*.py"):
        if ".venv" in file.parts or "__pycache__" in file.parts:
            continue

        python_files.append(file)

    return python_files


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
    project_modules = {Path(file).stem for file in dependency_graph}

    for file, imports in dependency_graph.items():
        internal_dependencies[file] = {
            module
            for module in imports
            if module.split(".")[0] in project_modules
        }

    return internal_dependencies


# Calculate dependency statistics
def calculate_statistics(dependency_graph: dict[str, set[str]], internal_dependencies: dict[str, set[str]]) -> dict[str, float]:
    total_files = len(dependency_graph)
    total_imports = sum(len(i) for i in dependency_graph.values())
    total_internal = sum(len(i) for i in internal_dependencies.values())

    average_imports = (
        total_imports / total_files
        if total_files > 0 else 0
    )

    return {
        "total_files": total_files,
        "total_imports": total_imports,
        "total_internal": total_internal,
        "average_imports": average_imports
    }


# Find circular dependencies in the graph
def find_cycles(graph) -> list[list[str]]:
    import networkx as nx

    return list(nx.simple_cycles(graph))