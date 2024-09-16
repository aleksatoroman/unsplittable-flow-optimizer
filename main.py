from algorithms.brute_force import BruteForce
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.simulated_annealing import SimulatedAnnealing
from utils.graph_parser import parse_graph_with_demands
from utils.graph_visualizer import visualize_flow_graph


def main() -> None:
    file_path: str = "./resources/1.txt"

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
        result = algorithm.solve(graph)
        if result:
            print(f"Valid paths found for all demands using {algorithm.__class__.__name__}:")
            for i, (path, demand) in enumerate(zip(result.paths.values(), graph.get_demands()), start=1):
                print(f"Path for Demand {i} (Sink: {demand.sink}, Demand: {demand.flow}): {path}")

            result.validate()
            print('*' * 50)
        else:
            print(f"No valid solution found using {algorithm.__class__.__name__}")


if __name__ == "__main__":
    main()
