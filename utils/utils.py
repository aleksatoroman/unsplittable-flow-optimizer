from typing import List

from models.flow_result import FlowResult
from models.graph import FlowGraph
import random


class GraphUtils:
    @staticmethod
    def find_random_path(graph: FlowGraph, source: int, destination: int) -> List[int]:
        def dfs(current_node: int, destination_dfs: int, visited: set, path: List[int]) -> List[int]:
            path.append(current_node)

            if current_node == destination_dfs:
                return path

            visited.add(current_node)

            neighbors = list(graph.get_graph().neighbors(current_node))
            random.shuffle(neighbors)

            for neighbor in neighbors:
                if neighbor not in visited:
                    result = dfs(neighbor, destination_dfs, visited, path)
                    if result:
                        return result

            path.pop()
            return []

        return dfs(source, destination, set(), [])

    @staticmethod
    def generate_neighbor(current_solution: FlowResult, graph: FlowGraph, demand_key=None) -> FlowResult:
        if demand_key is None:
            demands = list(current_solution.demands.values())
            demand = random.choice(demands)
        else:
            demand = current_solution.demands[demand_key]

        current_path = current_solution.paths[demand.sink]

        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            random_node_index = random.randint(0, len(current_path) - 2)
            start_node = current_path[random_node_index]

            random_node_index2 = random.randint(random_node_index + 1, len(current_path) - 1)
            end_node = current_path[random_node_index2]

            alternative_path = GraphUtils.find_random_path(graph, start_node, end_node)

            if alternative_path:
                modified_path = current_path[:random_node_index] + alternative_path + current_path[
                                                                                      random_node_index2 + 1:]
                if modified_path != current_path:
                    new_paths = current_solution.paths.copy()
                    new_paths[demand.sink] = modified_path

                    return FlowResult(new_paths, current_solution.demands, graph.get_edges_with_capacities())

            attempt += 1

        return current_solution

    @staticmethod
    def generate_initial_solution(graph: FlowGraph) -> FlowResult:
        paths = {}
        demands = graph.get_demands()

        for demand in demands:
            chosen_path = GraphUtils.find_random_path(graph, demand.source, demand.sink)
            paths[demand.sink] = chosen_path

        return FlowResult(paths, {demand.sink: demand for demand in demands}, graph.get_edges_with_capacities())
