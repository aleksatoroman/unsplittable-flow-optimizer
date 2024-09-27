from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult, FlowPath
import random
from models.individual import Individual


class GeneticAlgorithm(BaseFlowAlgorithm):

    def __init__(self, params: dict):
        super().__init__(params)
        self.population_size = params.get('population_size', 100)
        self.num_generations = params.get('num_generations', 500)
        self.tournament_size = params.get('tournament_size', 5)
        self.elitism_size = params.get('elitism_size', 5)
        self.mutation_prob = params.get('mutation_prob', 0.01)

    @staticmethod
    def selection(population, tournament_size) -> Individual:
        chosen = random.sample(population, tournament_size)
        return max(chosen, key=lambda x: x.fitness)

    @staticmethod
    def crossover(parent1: Individual, parent2: Individual, child1: Individual, child2: Individual) -> None:
        for i, flow_path in enumerate(parent1.code.flow_paths):
            if random.random() < 0.5:
                child1.code.flow_paths[i] = FlowPath(
                    source=parent1.code.flow_paths[i].source,
                    sink=parent1.code.flow_paths[i].sink,
                    path=parent1.code.flow_paths[i].path,
                    flow=parent1.code.flow_paths[i].flow
                )
                child2.code.flow_paths[i] = FlowPath(
                    source=parent2.code.flow_paths[i].source,
                    sink=parent2.code.flow_paths[i].sink,
                    path=parent2.code.flow_paths[i].path,
                    flow=parent2.code.flow_paths[i].flow
                )
            else:
                child1.code.flow_paths[i] = FlowPath(
                    source=parent2.code.flow_paths[i].source,
                    sink=parent2.code.flow_paths[i].sink,
                    path=parent2.code.flow_paths[i].path,
                    flow=parent2.code.flow_paths[i].flow
                )
                child2.code.flow_paths[i] = FlowPath(
                    source=parent1.code.flow_paths[i].source,
                    sink=parent1.code.flow_paths[i].sink,
                    path=parent1.code.flow_paths[i].path,
                    flow=parent1.code.flow_paths[i].flow
                )

    def solve(self, graph) -> FlowResult | None:
        population = [Individual(graph) for _ in range(self.population_size)]
        new_population = population.copy()

        for i in range(self.num_generations):
            population.sort(key=lambda x: x.fitness, reverse=True)

            new_population[:self.elitism_size] = population[:self.elitism_size]

            for j in range(self.elitism_size, self.population_size, 2):
                parent1 = GeneticAlgorithm.selection(population, self.tournament_size)
                parent2 = GeneticAlgorithm.selection(population, self.tournament_size)

                if j + 1 >= self.population_size:
                    new_population[j].mutate(self.mutation_prob)
                    new_population[j].fitness = new_population[j].calc_fitness()
                else:
                    GeneticAlgorithm.crossover(parent1, parent2, child1=new_population[j], child2=new_population[j + 1])
                    new_population[j].mutate(self.mutation_prob)
                    new_population[j + 1].mutate(self.mutation_prob)

                    new_population[j].fitness = new_population[j].calc_fitness()
                    new_population[j + 1].fitness = new_population[j + 1].calc_fitness()

        max_individual = max(population, key=lambda x: x.fitness)
        return max_individual.code

