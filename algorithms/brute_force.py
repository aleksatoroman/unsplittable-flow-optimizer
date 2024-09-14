import networkx as nx
from itertools import product
from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.demand import Demand


class BruteForceFlow(BaseFlowAlgorithm):
    def solve(self, graph: FlowGraph, demands: list[Demand]) -> list[list[int]] | None:
        all_paths = []

        for demand in demands:
            paths = list(nx.all_simple_paths(graph.get_graph(), source=demand.source, target=demand.sink))
            all_paths.append(paths)

        for path_combination in product(*all_paths):
            if self.is_valid_combination(graph, path_combination, demands):
                return path_combination

        return None

    def is_valid_combination(self, graph: FlowGraph, path_combination: list[list[int]], demands: list[Demand]) -> bool:
        edge_flow = {}

        for path, demand in zip(path_combination, demands):
            for u, v in zip(path[:-1], path[1:]):
                if (u, v) not in edge_flow:
                    edge_flow[(u, v)] = 0
                edge_flow[(u, v)] += demand.flow

        for (u, v), flow in edge_flow.items():
            if flow > graph.get_capacity(u, v):
                return False

        return True
