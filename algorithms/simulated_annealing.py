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

            new_fitness = new_solution.calculate_score()
            current_fitness = current_solution.calculate_score()
            best_fitness = best_solution.calculate_score()

            if new_fitness > current_fitness or random.random() < SimulatedAnnealing.acceptance_probability(current_fitness, new_fitness, current_temp):
                current_solution = new_solution

            if new_fitness > best_fitness:
                best_solution = new_solution

            current_temp *= self.cooling_rate

            if current_temp < 1e-3:
                break

        return best_solution

    @staticmethod
    def acceptance_probability(current_fitness: float, new_fitness: float, temp: float) -> float:
        return math.exp((new_fitness - current_fitness) / temp) if new_fitness < current_fitness else 1.0
