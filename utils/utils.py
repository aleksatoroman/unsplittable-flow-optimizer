from typing import List, Tuple
from models.flow_result import FlowResult, FlowPath
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
    def generate_neighbor(current_solution: FlowResult, graph: FlowGraph, demand_key: Tuple[int, int] | None = None) -> FlowResult:
        flow_paths = current_solution.flow_paths

        if demand_key is not None:
            sink, index = demand_key
            demand_to_modify = flow_paths[index]
        else:
            demand_to_modify = random.choice(flow_paths)

        current_path = demand_to_modify.path

        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            random_node_index = random.randint(0, len(current_path) - 2)
            start_node = current_path[random_node_index]
            random_node_index2 = random.randint(random_node_index + 1, len(current_path) - 1)
            end_node = current_path[random_node_index2]

            alternative_path = GraphUtils.find_random_path(graph, start_node, end_node)

            if alternative_path:
                modified_path = current_path[:random_node_index] + alternative_path + current_path[random_node_index2 + 1:]

                if modified_path != current_path:
                    new_flow_paths = [
                        FlowPath(source=fp.source, sink=fp.sink, path=fp.path if fp != demand_to_modify else modified_path, flow=fp.flow)
                        for fp in flow_paths
                    ]
                    return FlowResult(flow_paths=new_flow_paths, edges=graph.get_edges_with_capacities())

            attempt += 1

        return current_solution

    @staticmethod
    def generate_initial_solution(graph: FlowGraph) -> FlowResult:
        flow_paths = []
        demands = graph.get_demands()

        for demand in demands:
            chosen_path = GraphUtils.find_random_path(graph, demand.source, demand.sink)
            flow_paths.append(FlowPath(source=demand.source, sink=demand.sink, path=chosen_path, flow=demand.flow))

        return FlowResult(flow_paths=flow_paths, edges=graph.get_edges_with_capacities())
