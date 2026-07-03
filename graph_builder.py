import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import graphviz
from pathlib import Path


# Build a directed graph from dependency data
def build_graph(dependency_graph: dict[str, set[str]]) -> nx.DiGraph:

    graph = nx.DiGraph()

    for file, imports in dependency_graph.items():

        # Add file node
        graph.add_node(file)

        # Add dependency edges
        for imp in imports:
            graph.add_edge(file, imp)

    return graph


# Export graph to Graphviz DOT format
def export_dot(graph, output_file: str) -> None:
    write_dot(graph, output_file)


# Render graph as a PNG image
def export_png(graph, output_file: Path) -> None:

    dot = nx.nx_pydot.to_pydot(graph)

    graphviz.Source(dot.to_string()).render(
        filename=str(output_file.with_suffix("")),
        format="png",
        cleanup=True
    )