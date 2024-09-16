from algorithms.brute_force import BruteForce
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.simulated_annealing import SimulatedAnnealing
from models.log_level import LogLevel
from models.runner import Runner
from utils.graph_parser import parse_graph_with_demands
from utils.graph_visualizer import visualize_flow_graph


def main() -> None:
    file_path: str = "./resources/2.txt"
    graph = parse_graph_with_demands(file_path)

    visualize_flow_graph(graph, layout='circular', seed=42)

    initial_temp = 1000
    cooling_rate = 0.99
    num_iterations = 1000

    algorithms = [BruteForce(),
                  SimulatedAnnealing(initial_temp=initial_temp,
                                     cooling_rate=cooling_rate,
                                     num_iterations=num_iterations),
                  GeneticAlgorithm(population_size=100,
                                   num_generations=100,
                                   tournament_size=7,
                                   elitism_size=10,
                                   mutation_prob=0.05)]

    for algorithm in algorithms:
        runner = Runner(algorithm, graph)
        runner.run()
        print('*' * 50)

if __name__ == "__main__":
    main()
