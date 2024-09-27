from typing import List, Tuple
from models.flow_result import FlowResult, FlowPath
from models.graph import FlowGraph
import random


class GraphUtils:
    @staticmethod
    def find_random_path(graph: FlowGraph, source: int, destination: int, exclude_paths: set = None,
                         cycle_nodes: set = None) -> List[int]:

        def dfs(current_node: int, destination_dfs: int, visited: set, path: List[int]) -> List[int]:
            path.append(current_node)

            if current_node == destination_dfs:
                if exclude_paths is None or tuple(path) not in exclude_paths:
                    return path
                else:
                    path.pop()
                    return []

            visited.add(current_node)

            neighbors = list(graph.get_graph().neighbors(current_node))
            random.shuffle(neighbors)

            for neighbor in neighbors:
                if neighbor not in visited and (cycle_nodes is None or neighbor not in cycle_nodes):
                    result = dfs(neighbor, destination_dfs, visited, path)
                    if result:
                        return result

            path.pop()
            return []

        return dfs(source, destination, set(), [])

    @staticmethod
    def generate_neighbor(current_solution: FlowResult, graph: FlowGraph,
                          demand_key: Tuple[int, int] | None = None) -> FlowResult:
        flow_paths = current_solution.flow_paths

        if demand_key is not None:
            sink, index = demand_key
            demand_to_modify = flow_paths[index]
        else:
            demand_to_modify = random.choice(flow_paths)

        current_path = demand_to_modify.path

        if len(current_path) == 2:
            random_node_index = 0
            random_node_index2 = 1
            start_node, end_node = current_path[0], current_path[1]
        else:
            random_node_index = random.randint(0, len(current_path) - 2)
            start_node = current_path[random_node_index]
            random_node_index2 = random.randint(random_node_index + 1, len(current_path) - 1)
            end_node = current_path[random_node_index2]

        spliced_portion = tuple(current_path[random_node_index:random_node_index2 + 1])

        cycle_nodes = set(current_path[:random_node_index] + current_path[random_node_index2 + 1:])

        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            alternative_path = GraphUtils.find_random_path(
                graph,
                start_node,
                end_node,
                exclude_paths={spliced_portion},
                cycle_nodes=cycle_nodes
            )

            if len(alternative_path) == 0:
                random_node_index = random.randint(0, len(current_path) - 2)
                start_node = current_path[random_node_index]
                random_node_index2 = random.randint(random_node_index + 1, len(current_path) - 1)
                end_node = current_path[random_node_index2]
                spliced_portion = tuple(current_path[random_node_index:random_node_index2 + 1])
                cycle_nodes = set(current_path[:random_node_index] + current_path[random_node_index2 + 1:])
                attempt += 1
                continue

            if not set(alternative_path).intersection(cycle_nodes):
                modified_path = current_path[:random_node_index] + alternative_path + current_path[
                                                                                      random_node_index2 + 1:]

                new_flow_paths = [
                    FlowPath(source=fp.source, sink=fp.sink,
                             path=fp.path if fp != demand_to_modify else modified_path, flow=fp.flow)
                    for fp in flow_paths
                ]
                return FlowResult(flow_paths=new_flow_paths, edges=graph.get_edges_with_capacities())

            attempt += 1

        return current_solution

    @staticmethod
    def reroute_entire_demand(current_solution: FlowResult, graph: FlowGraph,
                              demand_key: Tuple[int, int]) -> FlowResult:
        flow_paths = current_solution.flow_paths
        sink, index = demand_key
        demand_to_modify = flow_paths[index]

        exclude_paths = {tuple(demand_to_modify.path)}

        new_path = GraphUtils.find_random_path(graph, demand_to_modify.source, demand_to_modify.sink,
                                               exclude_paths=exclude_paths)

        if len(new_path) == 0:
            return current_solution

        new_flow_paths = [
            FlowPath(
                source=fp.source,
                sink=fp.sink,
                path=fp.path if fp != demand_to_modify else new_path,
                flow=fp.flow
            )
            for fp in flow_paths
        ]
        return FlowResult(flow_paths=new_flow_paths, edges=graph.get_edges_with_capacities())

    @staticmethod
    def generate_initial_solution(graph: FlowGraph) -> FlowResult:
        flow_paths = []
        demands = graph.get_demands()

        for demand in demands:
            chosen_path = GraphUtils.find_random_path(graph, demand.source, demand.sink)
            flow_paths.append(FlowPath(source=demand.source, sink=demand.sink, path=chosen_path, flow=demand.flow))

        return FlowResult(flow_paths=flow_paths, edges=graph.get_edges_with_capacities())
