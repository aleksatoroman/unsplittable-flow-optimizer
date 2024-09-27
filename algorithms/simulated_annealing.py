import math
import random
from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult
from utils.utils import GraphUtils


class SimulatedAnnealing(BaseFlowAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)
        self.initial_temp = params.get('initial_temp', 100.0)
        self.cooling_rate = params.get('cooling_rate', 0.95)
        self.num_iterations = params.get('num_iterations', 1000)

    def solve(self, graph: FlowGraph) -> FlowResult | None:
        current_solution = GraphUtils.generate_initial_solution(graph)
        best_solution = current_solution
        current_temp = self.initial_temp

        for iteration in range(self.num_iterations):
            new_solution = GraphUtils.generate_neighbor(current_solution, graph)

            new_overflow = new_solution.calculate_overflow() if not new_solution.is_feasible() else 0
            current_overflow = current_solution.calculate_overflow() if not current_solution.is_feasible() else 0
            best_overflow = best_solution.calculate_overflow() if not best_solution.is_feasible() else 0

            new_obj = new_solution.calculate_max_flow_to_capacity_ratio()
            current_obj = current_solution.calculate_max_flow_to_capacity_ratio()
            best_obj = best_solution.calculate_max_flow_to_capacity_ratio()

            if not new_solution.is_feasible():
                if new_overflow < current_overflow:
                    current_solution = new_solution
                if new_overflow < best_overflow:
                    best_solution = new_solution
            else:
                if new_obj < current_obj or random.random() < SimulatedAnnealing.acceptance_probability(current_obj, new_obj, current_temp):
                    current_solution = new_solution

                if new_obj < best_obj or (not best_solution.is_feasible() and new_solution.is_feasible()):
                    best_solution = new_solution

            current_temp *= self.cooling_rate

            if current_temp < 1e-3:
                break

        return best_solution

    @staticmethod
    def acceptance_probability(current_obj: float, new_obj: float, temp: float) -> float:
        return math.exp((current_obj - new_obj) / temp) if new_obj > current_obj else 1.0
