import argparse
import os
from algorithms.brute_force import BruteForce
from algorithms.genetic_algorithm import GeneticAlgorithm
from models.runner import Runner
from utils.graph_parser import parse_graph_with_demands
from utils.graph_visualizer import visualize_flow_graph
from models.graph_generator import GraphGeneratorManager


def run_algorithms(file_path: str) -> None:
    graph = parse_graph_with_demands(file_path)

    visualize_flow_graph(graph, layout='circular', seed=42)

    initial_temp = 1000
    cooling_rate = 0.99
    num_iterations = 1000

    algorithms = [
        # BruteForce(),
        # SimulatedAnnealing(initial_temp=initial_temp,
        #                    cooling_rate=cooling_rate,
        #                    num_iterations=num_iterations),
        GeneticAlgorithm(population_size=200,
                         num_generations=350,
                         tournament_size=7,
                         elitism_size=20,
                         mutation_prob=0.1)
    ]

    for algorithm in algorithms:
        runner = Runner(algorithm, graph)
        runner.run()
        print('*' * 50)


def generate_graphs(output_dir: str) -> None:
    manager = GraphGeneratorManager(output_dir=output_dir)

    for i in range(1, 4):
        manager.generate_small_graph()
        manager.generate_medium_graph(demand_type='balanced')
        manager.generate_medium_graph(demand_type='large')
        manager.generate_large_graph(demand_type='balanced')
        manager.generate_large_graph(demand_type='large')


def main() -> None:
    parser = argparse.ArgumentParser(description="Flow Graph Generator and Algorithm Runner")
    parser.add_argument("--action", type=str, choices=["generate", "run"], required=True, help="Action to perform (generate or run)")

    args = parser.parse_args()

    generated_graphs_path = "./resources/generated"

    if args.action == "generate":
        if not os.path.exists(generated_graphs_path):
            os.makedirs(generated_graphs_path)
        else:
            files = os.listdir(generated_graphs_path)
            for file in files:
                os.remove(os.path.join(generated_graphs_path, file))
        generate_graphs(output_dir=generated_graphs_path)

    elif args.action == "run":
        file_path = "./resources/generated/medium_graph_balanced_65726bcf.txt"
        run_algorithms(file_path=file_path)


if __name__ == "__main__":
    main()
