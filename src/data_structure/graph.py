from collections import defaultdict
from typing import Dict, Set

class Graph:
    """
    Defines a graph for describing elements which has relation of connection with
    other elements (Like IfcWall)
    """
    def __init__(self):
        self.graph = defaultdict(set)

    def add_edge(self, from_node: str, to_node: str):
        self.graph[from_node].add(to_node)
        self.graph[to_node].add(from_node)

    def get_connections(self) -> Dict[str, Set[str]]:
        return self.graph

    def __str__(self):
        result = ""
        for node, edges in self.graph.items():
            result += f"{node}: {', '.join(edges)}\n"
        return result
