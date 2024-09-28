import random
from time import perf_counter
from copy import deepcopy

from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult
from utils.utils import GraphUtils


class VNSAlgorithm(BaseFlowAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)
        self.k_min = params.get('k_min', 1)
        self.k_max = params.get('k_max', 5)
        self.move_prob = params.get('move_prob', 0.1)
        self.reroute_entire_path_prob = params.get('reroute_entire_path_prob', 0.5)

    def solve(self, graph: FlowGraph) -> FlowResult | None:
        start_time = perf_counter()

        solution = GraphUtils.generate_initial_solution(graph)
        current_score = solution.calculate_score()

        iterations_since_last_improvement = 0

        while perf_counter() - start_time < self.max_time or iterations_since_last_improvement < self.no_improvement_threshold:
            for k in range(self.k_min, self.k_max):
                new_solution = self.shaking(solution, graph, k)
                new_score = new_solution.calculate_score()

                new_solution, new_score = self.local_search(new_solution, new_score, graph)

                if new_score > current_score or (new_score == current_score and random.random() < self.move_prob):
                    current_score = new_score
                    solution = deepcopy(new_solution)
                    iterations_since_last_improvement = 0
                else:
                    iterations_since_last_improvement += 1

        if iterations_since_last_improvement >= self.no_improvement_threshold:
            solution.stopping_reason = 'No improvement threshold reached'
        else:
            solution.stopping_reason = 'Max time reached'

        return solution

    def shaking(self, solution: FlowResult, graph: FlowGraph, k: int) -> FlowResult:
        num_demands_to_modify = min(k, len(solution.flow_paths))
        return self.multi_path_modification(solution, graph, num_demands_to_modify, self.reroute_entire_path_prob)

    @staticmethod
    def local_search(solution: FlowResult, score: float, graph: FlowGraph) -> (FlowResult, float):
        new_solution = deepcopy(solution)
        current_score = score
        improved = True

        while improved:
            improved = False
            demand_order = list(range(len(new_solution.flow_paths)))
            random.shuffle(demand_order)

            for i in demand_order:
                modified_solution = GraphUtils.generate_neighbor(new_solution, graph, demand_key=(new_solution.flow_paths[i].sink, i))
                new_score = modified_solution.calculate_score()

                if new_score > current_score:
                    new_solution = deepcopy(modified_solution)
                    current_score = new_score
                    improved = True
                    break

        return new_solution, current_score

    @staticmethod
    def multi_path_modification(current_solution: FlowResult, graph: FlowGraph, num_demands_to_modify: int,
                                reroute_entire_path_prob: float = 0.5) -> FlowResult:
        flow_paths = current_solution.flow_paths
        demands_to_modify = random.sample(list(enumerate(flow_paths)), num_demands_to_modify)

        new_solution = deepcopy(current_solution)

        for index, flow_path in demands_to_modify:
            demand_key = (flow_path.sink, index)

            if random.random() < reroute_entire_path_prob:
                new_solution = GraphUtils.reroute_entire_demand(new_solution, graph, demand_key=demand_key)
            else:
                new_solution = GraphUtils.generate_neighbor(new_solution, graph, demand_key=demand_key)

        return new_solution
