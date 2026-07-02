import typer
from pathlib import Path
from graph_builder import build_graph
from analyzer import (
    build_dependency_graph,
    find_internal_dependencies,
    calculate_statistics
)


app = typer.Typer()


# Python Package Dependency Visualizer
@app.callback()
def callback():
    pass


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

    graph = build_graph(dependency_graph)

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

    print("\nGraph Summary")
    print("-" * 15)
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")


if __name__ == "__main__":
    app()