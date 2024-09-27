from models.graph import FlowGraph
from utils.utils import GraphUtils
import random


class Individual:
    def __init__(self, graph: FlowGraph):
        self.graph = graph
        self.code = GraphUtils.generate_initial_solution(self.graph)
        self.fitness = self.calc_fitness()

    def calc_fitness(self) -> float:
        return self.code.calculate_score()

    def mutate(self, mutation_prob: float) -> None:
        for index, flow_path in enumerate(self.code.flow_paths):
            demand_key = (flow_path.sink, index)
            if random.random() < mutation_prob:
                mutated_solution = GraphUtils.generate_neighbor(self.code, self.graph, demand_key=demand_key)
                self.code = mutated_solution
