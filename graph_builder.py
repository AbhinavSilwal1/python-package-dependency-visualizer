import networkx as nx


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