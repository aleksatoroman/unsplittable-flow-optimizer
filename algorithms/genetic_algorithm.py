from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.flow_result import FlowResult, FlowPath
import random
from time import perf_counter
from models.individual import Individual


class GeneticAlgorithm(BaseFlowAlgorithm):

    def __init__(self, params: dict):
        super().__init__(params)
        self.population_size = params.get('population_size', 100)
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
        start_time = perf_counter()
        population = [Individual(graph) for _ in range(self.population_size)]
        new_population = population.copy()

        iterations_since_last_improvement = 0
        best_fitness = max(ind.fitness for ind in population)

        while perf_counter() - start_time < self.max_time and iterations_since_last_improvement < self.no_improvement_threshold:
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

            current_best_fitness = max(ind.fitness for ind in population)
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                iterations_since_last_improvement = 0
            else:
                iterations_since_last_improvement += 1

        max_individual = max(population, key=lambda x: x.fitness)

        if perf_counter() - start_time >= self.max_time:
            max_individual.code.stopping_reason = 'Max time reached'
        else:
            max_individual.code.stopping_reason = 'No improvement threshold reached'

        return max_individual.code
