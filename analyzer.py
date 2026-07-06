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


# Build a dependency graph containing only internal dependencies
def build_internal_dependency_graph(internal_dependencies: dict[str, set[str]]) -> dict[str, set[str]]:
    return {
        file: set(dependencies)
        for file, dependencies in internal_dependencies.items()
    }


# Find orphan and leaf modules
def analyze_orphan_and_leaf_modules(dependency_graph: dict[str, set[str]]) -> tuple[set[str], set[str]]:
    project_modules = {Path(file).stem: file for file in dependency_graph}
    incoming = {file: set() for file in dependency_graph}

    for file, imports in dependency_graph.items():
        for module in imports:
            if module in project_modules:
                target_file = project_modules[module]
                incoming[target_file].add(file)

    orphans = {file for file, dependencies in incoming.items() if not dependencies}

    leaf_modules = set()

    for file, imports in dependency_graph.items():
        internal_imports = {
            module
            for module in imports
            if module in project_modules
        }

        if not internal_imports:
            leaf_modules.add(file)

    return orphans, leaf_modules


# Rank modules by incoming and outgoing dependencies
def rank_modules(dependency_graph: dict[str, set[str]]) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:

    project_modules = {Path(file).stem: file for file in dependency_graph}
    incoming = {file: 0 for file in dependency_graph}

    outgoing = {}

    for file, imports in dependency_graph.items():

        internal_imports = {project_modules[module] for module in imports if module in project_modules}

        outgoing[file] = len(internal_imports)

        for dependency in internal_imports:
            incoming[dependency] += 1

    most_imported = sorted(incoming.items(), key=lambda item: item[1], reverse=True)
    most_dependent = sorted(outgoing.items(), key=lambda item: item[1], reverse=True)

    return most_imported, most_dependent