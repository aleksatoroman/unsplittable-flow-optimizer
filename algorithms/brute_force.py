import networkx as nx
from itertools import product
from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.demand import Demand
from models.flow_result import FlowResult


class BruteForceFlow(BaseFlowAlgorithm):
    def solve(self, graph: FlowGraph) -> FlowResult | None:
        all_paths = []
        demands = graph.get_demands()

        for demand in demands:
            paths = list(nx.all_simple_paths(graph.get_graph(), source=demand.source, target=demand.sink))
            all_paths.append(paths)

        best_combination = None
        min_max_ratio = float('inf')

        for path_combination in product(*all_paths):
            edge_flow = self.calculate_edge_flow(path_combination, demands)

            if self.is_valid_combination(edge_flow, graph):
                max_ratio = self.calculate_max_flow_to_capacity_ratio(edge_flow, graph)

                if max_ratio < min_max_ratio:
                    min_max_ratio = max_ratio
                    best_combination = path_combination

        if best_combination:
            edges = graph.get_edges_with_capacities()
            print(f"Best flow-to-capacity ratio: {min_max_ratio}")
            return FlowResult(paths={d.sink: p for d, p in zip(demands, best_combination)},
                              demands={d.sink: d for d in demands},
                              edges=edges)

        return None

    def calculate_edge_flow(self, path_combination: list[list[int]], demands: list[Demand]) -> dict:
        edge_flow = {}
        for path, demand in zip(path_combination, demands):
            for u, v in zip(path[:-1], path[1:]):
                if (u, v) not in edge_flow:
                    edge_flow[(u, v)] = 0
                edge_flow[(u, v)] += demand.flow
        return edge_flow

    def is_valid_combination(self, edge_flow: dict, graph: FlowGraph) -> bool:
        for (u, v), flow in edge_flow.items():
            if flow > graph.get_capacity(u, v):
                return False
        return True

    def calculate_max_flow_to_capacity_ratio(self, edge_flow: dict, graph: FlowGraph) -> float:
        max_ratio = 0
        for (u, v), flow in edge_flow.items():
            capacity = graph.get_capacity(u, v)
            ratio = flow / capacity
            max_ratio = max(max_ratio, ratio)
        return max_ratio
