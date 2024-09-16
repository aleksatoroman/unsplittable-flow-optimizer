import math
import random
from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult

from utils.utils import GraphUtils


class SimulatedAnnealing(BaseFlowAlgorithm):
    def __init__(self, initial_temp: float, cooling_rate: float, num_iterations: int):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations

    def solve(self, graph: FlowGraph) -> FlowResult | None:
        current_solution = GraphUtils.generate_initial_solution(graph)
        best_solution = current_solution
        current_temp = self.initial_temp

        for iteration in range(self.num_iterations):
            new_solution = GraphUtils.generate_neighbor(current_solution, graph)

            if not new_solution.is_feasible():
                continue

            new_obj = new_solution.calculate_max_flow_to_capacity_ratio()
            current_obj = current_solution.calculate_max_flow_to_capacity_ratio()

            if new_obj < current_obj or random.random() < SimulatedAnnealing.acceptance_probability(current_obj,
                                                                                                    new_obj,
                                                                                                    current_temp):
                current_solution = new_solution

                if new_obj < best_solution.calculate_max_flow_to_capacity_ratio():
                    best_solution = new_solution

            current_temp *= self.cooling_rate

            if current_temp < 1e-3:
                break

        return best_solution

    @staticmethod
    def acceptance_probability(current_obj: float, new_obj: float, temp: float) -> float:
        return math.exp((current_obj - new_obj) / temp) if new_obj > current_obj else 1.0
