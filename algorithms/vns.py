import random
from time import perf_counter
from copy import deepcopy

from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult, FlowPath
from utils.utils import GraphUtils


class VNSAlgorithm(BaseFlowAlgorithm):
    def __init__(self, params: dict):
        super().__init__(params)
        self.time_limit = params.get('time_limit', 300)
        self.k_min = params.get('k_min', 1)
        self.k_max = params.get('k_max', 5)
        self.move_prob = params.get('move_prob', 0.1)
        self.num_iterations = params.get('num_iterations', 1000)

    def solve(self, graph: FlowGraph) -> FlowResult | None:
        start_time = perf_counter()

        solution = GraphUtils.generate_initial_solution(graph)
        value = solution.calculate_max_flow_to_capacity_ratio()

        for _ in range(self.num_iterations):
            for k in range(self.k_min, self.k_max):
                new_solution = self.shaking(solution, graph, k)
                new_value = new_solution.calculate_max_flow_to_capacity_ratio()

                new_solution, new_value = self.local_search(new_solution, new_value, graph)

                if new_value < value or (new_value == value and random.random() < self.move_prob):
                    value = new_value
                    solution = deepcopy(new_solution)

        return solution

    def shaking(self, solution: FlowResult, graph: FlowGraph, k: int) -> FlowResult:
        num_demands_to_modify = min(k, len(solution.flow_paths))
        return self.multi_path_modification(solution, graph, num_demands_to_modify)

    @staticmethod
    def local_search(solution: FlowResult, value: float, graph: FlowGraph) -> (FlowResult, float):
        new_solution = deepcopy(solution)
        current_value = value
        improved = True

        while improved:
            improved = False
            demand_order = list(range(len(new_solution.flow_paths)))
            random.shuffle(demand_order)

            for i in demand_order:
                modified_solution = GraphUtils.generate_neighbor(new_solution, graph,
                                                           demand_key=(new_solution.flow_paths[i].sink, i))
                new_value = modified_solution.calculate_max_flow_to_capacity_ratio()

                if new_value < current_value:
                    new_solution = deepcopy(modified_solution)
                    current_value = new_value
                    improved = True
                    break

        return new_solution, current_value



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
