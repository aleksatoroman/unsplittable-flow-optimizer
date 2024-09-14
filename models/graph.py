import networkx as nx
from typing import List

from models.demand import Demand


class FlowGraph:
    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.demands: List[Demand] = []  # List of Demand instances

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        self.graph.add_edge(u, v, capacity=capacity)

    def add_demand(self, demand: Demand) -> None:
        self.demands.append(demand)

    def get_demands(self) -> List[Demand]:
        return self.demands

    def get_capacity(self, u: int, v: int) -> int:
        return self.graph[u][v]['capacity']

    def update_capacity(self, u: int, v: int, flow: int) -> None:
        self.graph[u][v]['capacity'] -= flow

    def get_graph(self) -> nx.DiGraph:
        return self.graph
