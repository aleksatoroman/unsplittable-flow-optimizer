from models.flow_result import FlowResult
from models.graph import FlowGraph
from utils.utils import GraphUtils
import random


class Individual:
    def __init__(self, graph: FlowGraph):
        self.graph = graph
        self.code = GraphUtils.generate_initial_solution(self.graph)
        self.fitness = self.calc_fitness()

    def calc_fitness(self) -> float:
        total_penalty = 0
        feasible = True

        edge_flows = self.code.calculate_edge_flows()
        capacities = self.graph.get_edges_with_capacities()

        for edge, flow in edge_flows.items():
            capacity = capacities[edge]
            if flow > capacity:
                overflow = flow - capacity
                total_penalty += overflow
                feasible = False

        if feasible:
            max_flow_to_capacity_ratio = self.code.calculate_max_flow_to_capacity_ratio()
            return 1 - max_flow_to_capacity_ratio
        else:
            return -(1 + total_penalty)

    def mutate(self, mutation_prob: float) -> None:
        for demand_key in self.code.paths.keys():
            if random.random() < mutation_prob:
                mutated_solution = GraphUtils.generate_neighbor(self.code, self.graph, demand_key)
                self.code = mutated_solution
