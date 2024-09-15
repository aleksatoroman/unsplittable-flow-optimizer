import math
from collections import deque
from typing import List
import networkx as nx
import random
from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult
from typing import List


class SimulatedAnnealing(BaseFlowAlgorithm):
    def __init__(self, initial_temp: float, cooling_rate: float, num_iterations: int):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations

    def solve(self, graph: FlowGraph) -> FlowResult | None:
        current_solution = self.generate_initial_solution(graph)
        best_solution = current_solution
        current_temp = self.initial_temp

        for iteration in range(self.num_iterations):
            new_solution = self.generate_neighbor(current_solution, graph)

            if not new_solution.is_feasible():
                continue

            new_obj = new_solution.calculate_max_flow_to_capacity_ratio()
            current_obj = current_solution.calculate_max_flow_to_capacity_ratio()

            if new_obj < current_obj or random.random() < self.acceptance_probability(current_obj, new_obj,
                                                                                      current_temp):
                current_solution = new_solution

                if new_obj < best_solution.calculate_max_flow_to_capacity_ratio():
                    best_solution = new_solution

            current_temp *= self.cooling_rate

            if current_temp < 1e-3:
                break

        return best_solution

    def acceptance_probability(self, current_obj: float, new_obj: float, temp: float) -> float:
        return math.exp((current_obj - new_obj) / temp) if new_obj > current_obj else 1.0

    def generate_initial_solution(self, graph: FlowGraph) -> FlowResult:
        paths = {}
        demands = graph.get_demands()

        for demand in demands:
            chosen_path = self.find_random_path(graph, demand.source, demand.sink)
            paths[demand.sink] = chosen_path

        return FlowResult(paths, {demand.sink: demand for demand in demands}, graph.get_edges_with_capacities())

    def generate_neighbor(self, current_solution: FlowResult, graph: FlowGraph) -> FlowResult:
        demands = list(current_solution.demands.values())
        demand = random.choice(demands)
        current_path = current_solution.paths[demand.sink]

        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            random_node_index = random.randint(0, len(current_path) - 2)
            start_node = current_path[random_node_index]

            random_node_index2 = random.randint(random_node_index + 1, len(current_path) - 1)
            end_node = current_path[random_node_index2]

            alternative_path = self.find_random_path(graph, start_node, end_node)

            if alternative_path:
                modified_path = current_path[:random_node_index] + alternative_path + current_path[
                                                                                      random_node_index2 + 1:]
                if modified_path != current_path:
                    new_paths = current_solution.paths.copy()
                    new_paths[demand.sink] = modified_path

                    return FlowResult(new_paths, current_solution.demands, graph.get_edges_with_capacities())

            attempt += 1

        return current_solution

    def find_random_path(self, graph: FlowGraph, source: int, destination: int) -> List[int]:
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
