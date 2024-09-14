import networkx as nx

class FlowGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_edge(self, u, v, capacity):
        """Add a directed edge with capacity to the graph."""
        self.graph.add_edge(u, v, capacity=capacity)

    def get_capacity(self, u, v):
        """Get the capacity of the edge between nodes u and v."""
        return self.graph[u][v]['capacity']

    def update_capacity(self, u, v, flow):
        """Update the capacity of an edge after flow is routed through it."""
        self.graph[u][v]['capacity'] -= flow

    def get_graph(self):
        """Return the underlying networkx graph object."""
        return self.graph
