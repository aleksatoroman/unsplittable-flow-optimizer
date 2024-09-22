import argparse
import os
import time
from typing import List
from algorithms.brute_force import BruteForce
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.simulated_annealing import SimulatedAnnealing
from models.log_level import LogLevel
from models.runner import Runner
from utils.graph_parser import parse_graph_with_demands
from utils.graph_generator import GraphGeneratorManager
from itertools import product
from glob import glob


def run_algorithms_in_folder(root_folder: str, algorithm_names: List[str]) -> None:
    txt_files = glob(os.path.join(root_folder, "*.txt"))

    sa_param_grid = {
        'initial_temp': [1000, 5000],
        'cooling_rate': [0.99, 0.95],
        'num_iterations': [1000, 2000]
    }

    ga_param_grid = {
        'population_size': [100, 200],
        'num_generations': [200, 500],
        'tournament_size': [5, 7],
        'elitism_size': [10, 20],
        'mutation_prob': [0.1, 0.2]
    }

    sa_combinations = [dict(zip(sa_param_grid, v)) for v in product(*sa_param_grid.values())]
    ga_combinations = [dict(zip(ga_param_grid, v)) for v in product(*ga_param_grid.values())]

    algorithms = []
    if "brute-force" in algorithm_names:
        algorithms.append((BruteForce, [{}]))
    if "genetic" in algorithm_names:
        algorithms.append((GeneticAlgorithm, ga_combinations))
    if "simulated-annealing" in algorithm_names:
        algorithms.append((SimulatedAnnealing, sa_combinations))

    timestamp = time.strftime("%Y-%m-%d_%H_%M_%S")
    for txt_file in txt_files:
        try:
            graph = parse_graph_with_demands(txt_file)
        except Exception as e:
            print(f"Error parsing file {txt_file}: {str(e)}. Skipping.")
            continue

        example_name = os.path.splitext(os.path.basename(txt_file))[0]

        report_dir = os.path.join(root_folder, 'reports', timestamp, example_name)
        os.makedirs(report_dir, exist_ok=True)

        for algorithm_class, param_combinations in algorithms:
            for params in param_combinations:
                print(f"Running {algorithm_class.__name__} on {example_name} with params: {params}")
                runner = Runner(algorithm_class, graph, params, report_dir)
                runner.run(LogLevel.INFO)
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
    parser.add_argument("--algorithms", type=str, required=False, help="Algorithms to as run as comma separated list (brute-force, genetic, simulated-annealing)")
    parser.add_argument("--examples", type=str, required=False, help="Root folder of examples to run algorithms on")

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
        if args.algorithms:
            algorithms = args.algorithms.split(",")
            algorithms = [algorithm.strip() for algorithm in algorithms]
            if not all(algorithm in ["brute-force", "genetic", "simulated-annealing"] for algorithm in algorithms):
                return
        else:
            algorithms = ["brute-force", "genetic", "simulated-annealing"]

        if args.examples:
            root_path = args.examples
        else:
            root_path = "./resources/examples/"
        run_algorithms_in_folder(root_path, algorithms)


if __name__ == "__main__":
    main()
