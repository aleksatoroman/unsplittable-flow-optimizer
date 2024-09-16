import networkx as nx
from itertools import product
from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult


class BruteForce(BaseFlowAlgorithm):
    def solve(self, graph: FlowGraph) -> FlowResult | None:
        all_paths = []
        demands = graph.get_demands()

        for demand in demands:
            paths = list(nx.all_simple_paths(graph.get_graph(), source=demand.source, target=demand.sink))
            all_paths.append(paths)

        print('Number of paths for each demand:', [len(paths) for paths in all_paths])

        best_combination = None
        min_max_ratio = float('inf')

        count = 0
        count_feasible = 0
        for path_combination in product(*all_paths):
            count += 1
            paths = {d.sink: p for d, p in zip(demands, path_combination)}
            result = FlowResult(paths=paths, demands={d.sink: d for d in demands}, edges=graph.get_edges_with_capacities())

            if result.is_feasible():
                count_feasible += 1
                max_ratio = result.calculate_max_flow_to_capacity_ratio()

                if max_ratio < min_max_ratio:
                    min_max_ratio = max_ratio
                    best_combination = result

        print('Total combinations:', count)
        print('Feasible combinations:', count_feasible)
        if best_combination:
            return best_combination
        return None
