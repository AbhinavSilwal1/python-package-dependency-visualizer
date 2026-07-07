import typer
from pathlib import Path
import json
from html import escape
from analyzer import (
    collect_python_files,
    build_dependency_graph,
    find_internal_dependencies,
    calculate_statistics,
    find_cycles,
    build_internal_dependency_graph,
    analyze_orphan_and_leaf_modules,
    rank_modules
)
from graph_builder import (
    build_graph,
    export_dot,
    export_png,
    export_svg
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

    python_files = collect_python_files(project_path)

    print(f"Found {len(python_files)} Python files:")

    dependency_graph = build_dependency_graph(python_files, project_path)
    graph = build_graph(dependency_graph)
    cycles = find_cycles(graph)
    orphans, leaf_nodes = analyze_orphan_and_leaf_modules(dependency_graph)
    most_imported, most_dependent = rank_modules(dependency_graph)
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

    print("\nCircular Dependencies")
    print("-" * 21)
    if cycles:
        for cycle in cycles:
            print(" -> ".join(cycle + [cycle[0]]))
    else:
        print("None")

    print("\nOrphan Modules")
    print("-" * 14)
    if orphans:
        for o in sorted(orphans):
            print(f"- {o}")
    else:
        print("None")

    print("\nLeaf Modules")
    print("-" * 12)
    if leaf_nodes:
        for l in sorted(leaf_nodes):
            print(f"- {l}")
    else:
        print("None")

    print("\nDependency Rankings")
    print("-" * 19)
    
    print("Most Imported Modules")
    for index, (file, count) in enumerate(most_imported, start=1):
        print(f"{index}. {file} ({count})")

    print("\nMost Dependent Modules")
    for index, (file, count) in enumerate(most_dependent, start=1):
        print(f"{index}. {file} ({count})")


# Export dependency graph as a dot or png file
@app.command()
def export(
    path: str = typer.Argument("."),
    output: str = typer.Argument("dependency_graph.dot"),
    internal_only: bool = typer.Option(
        False,
        "--internal-only",
        help="Export only internal project dependencies."
    )
):
    project_path = Path(path)
    output_path = Path(output).expanduser()

    # Create output directory if it doesn't exist
    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    if not project_path.exists():
        print("Path does not exist.")
        raise typer.Exit()

    python_files = collect_python_files(project_path)

    dependency_graph = build_dependency_graph(python_files, project_path)
    internal_dependencies = find_internal_dependencies(dependency_graph)

    if internal_only:
        dependency_graph = build_internal_dependency_graph(internal_dependencies)

    graph = build_graph(dependency_graph)
    cycles = find_cycles(graph)

    if output_path.suffix == ".dot":
        export_dot(graph, output_path)
    elif output_path.suffix == ".png":
        export_png(graph, output_path, cycles)
    elif output_path.suffix == ".svg":
        export_svg(graph, output_path, cycles)
    else:
        print("Unsupported output format. Please use .dot, .png, or .svg.")
        raise typer.Exit()

    print("\nGraph Summary")
    print("-" * 15)
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")
    print(f"Output file: {output_path}")
    print(f"\nDependency graph exported to {output_path}")


# Export dependency analysis as a JSON report
@app.command()
def report(
    path: str = typer.Argument("."),
    output: str = typer.Argument("dependency_report.json")
):
    project_path = Path(path)
    output_path = Path(output).expanduser()

    if output_path.parent != Path("."):
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    if not project_path.exists():
        print("Path does not exist.")
        raise typer.Exit()

    python_files = collect_python_files(project_path)

    dependency_graph = build_dependency_graph(python_files, project_path)
    internal_dependencies = find_internal_dependencies(dependency_graph)
    statistics = calculate_statistics(dependency_graph, internal_dependencies)
    graph = build_graph(dependency_graph)
    cycles = find_cycles(graph)
    orphans, leaf_nodes = analyze_orphan_and_leaf_modules(dependency_graph)
    most_imported, most_dependent = rank_modules(dependency_graph)

    report = {
        "project_summary": {
            "python_files": statistics["total_files"],
            "total_imports": statistics["total_imports"],
            "internal_dependencies": statistics["total_internal"],
            "average_imports": statistics["average_imports"]
        },

        "dependency_graph": {
            file: sorted(imports)
            for file, imports in dependency_graph.items()
        },

        "internal_dependencies": {
            file: sorted(imports)
            for file, imports in internal_dependencies.items()
        },

        "circular_dependencies": cycles,

        "orphan_modules": sorted(orphans),

        "leaf_modules": sorted(leaf_nodes),

        "most_imported_modules": [
            {
                "module": file,
                "count": count
            }
            for file, count in most_imported
        ],

        "most_dependent_modules": [
            {
                "module": file,
                "count": count
            }
            for file, count in most_dependent
        ]
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4
        )

    print(f"\nJSON report exported to {output_path}")


# Export dependency analysis as an HTML report
@app.command()
def html_report(
    path: str = typer.Argument("."),
    output: str = typer.Argument("dependency_report.html")
):
    project_path = Path(path)
    output_path = Path(output).expanduser()

    if output_path.parent != Path("."):
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    if not project_path.exists():
        print("Path does not exist.")
        raise typer.Exit()

    python_files = collect_python_files(project_path)

    dependency_graph = build_dependency_graph(python_files, project_path)
    internal_dependencies = find_internal_dependencies(dependency_graph)
    statistics = calculate_statistics(dependency_graph, internal_dependencies)
    graph = build_graph(dependency_graph)
    cycles = find_cycles(graph)
    orphans, leaf_nodes = analyze_orphan_and_leaf_modules(dependency_graph)
    most_imported, most_dependent = rank_modules(dependency_graph)

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

    <meta charset="UTF-8">

    <title>Dependency Report</title>

    <style>

    body {{
        font-family: Arial, sans-serif;
        margin: 40px;
        background: #f4f4f4;
    }}

    h1 {{
        color: #222;
    }}

    section {{
        background: white;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 8px;
    }}

    table {{
        border-collapse: collapse;
        width: 100%;
    }}

    th, td {{
        border: 1px solid #ddd;
        padding: 8px;
    }}

    th {{
        background: #4CAF50;
        color: white;
    }}

    code {{
        background: #efefef;
        padding: 2px 4px;
    }}

    </style>

    </head>

    <body>

    <h1>Python Package Dependency Report</h1>

    <section>

    <h2>Project Summary</h2>

    <ul>
    <li>Python files: {statistics["total_files"]}</li>
    <li>Total imports: {statistics["total_imports"]}</li>
    <li>Internal dependencies: {statistics["total_internal"]}</li>
    <li>Average imports per file: {statistics["average_imports"]:.1f}</li>
    </ul>

    </section>
    """

    html += """
    <section>

    <h2>Dependencies</h2>

    <table>

    <tr>
    <th>Module</th>
    <th>Imports</th>
    </tr>
    """

    for file, imports in dependency_graph.items():

        html += f"""
    <tr>

    <td>{escape(file)}</td>

    <td>{", ".join(sorted(imports))}</td>

    </tr>
    """
    
    html += """
    </table>

    </section>
    """

    html += """
    <section>

    <h2>Circular Dependencies</h2>

    <ul>
    """

    if cycles:
        for cycle in cycles:
            html += f"<li>{' → '.join(cycle + [cycle[0]])}</li>"

    else:
        html += "<li>None</li>"

    html += """
    </ul>

    </section>
    """

    html += """
    <section>

    <h2>Orphan Modules</h2>

    <ul>
    """

    if orphans:
        for module in sorted(orphans):
            html += f"<li>{escape(module)}</li>"

    else:
        html += "<li>None</li>"

    html += """
    </ul>

    </section>
    """

    html += """
    <section>

    <h2>Leaf Modules</h2>

    <ul>
    """

    if leaf_nodes:
        for module in sorted(leaf_nodes):
            html += f"<li>{escape(module)}</li>"

    else:
        html += "<li>None</li>"

    html += """
    </ul>

    </section>
    """

    html += """
    <section>

    <h2>Most Imported Modules</h2>

    <table>

    <tr>
    <th>Rank</th>
    <th>Module</th>
    <th>Imports</th>
    </tr>
    """

    for index, (module, count) in enumerate(most_imported, start=1):
        html += f"""
    <tr>
    <td>{index}</td>
    <td>{escape(module)}</td>
    <td>{count}</td>
    </tr>
    """

    html += """
    </table>

    </section>
    """

    html += """
    <section>

    <h2>Most Dependent Modules</h2>

    <table>

    <tr>
    <th>Rank</th>
    <th>Module</th>
    <th>Dependencies</th>
    </tr>
    """

    for index, (module, count) in enumerate(most_dependent, start=1):
        html += f"""
    <tr>
    <td>{index}</td>
    <td>{escape(module)}</td>
    <td>{count}</td>
    </tr>
    """

    html += """
    </table>

    </section>
    """
    
    html += """
    </body>

    </html>
    """

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"\nHTML report exported to {output_path}")


if __name__ == "__main__":
    app()