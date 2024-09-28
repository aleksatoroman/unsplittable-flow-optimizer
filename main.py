import argparse
import itertools
import os
import time
from typing import List

from algorithms.base_algorithm import BaseFlowAlgorithm
from algorithms.brute_force import BruteForce
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.vns import VNSAlgorithm
from models.graph import FlowGraph
from models.log_level import LogLevel
from models.runner import Runner
from utils.graph_parser import parse_graph_with_demands
from utils.graph_generator import GraphGeneratorManager
from itertools import product
from glob import glob

from utils.graph_visualizer import visualize_flow_graph
from utils.statistics import Statistics


def get_algorithms(algorithm_names: List[str]):
    algorithms = []
    if "brute-force" in algorithm_names:
        algorithms.append(BruteForce)
    if "genetic" in algorithm_names:
        algorithms.append(GeneticAlgorithm)
    if "simulated-annealing" in algorithm_names:
        algorithms.append(SimulatedAnnealing)
    if "vns" in algorithm_names:
        algorithms.append(VNSAlgorithm)
    return algorithms


def run_algorithms_in_folder(root_folder: str, algorithm_names: List[str]) -> None:
    txt_files = glob(os.path.join(root_folder, "*.txt"))

    sa_param_grid = {
        'initial_temp': [3000, 5000],
        'cooling_rate': [0.99, 0.95]
    }

    ga_param_grid = {
        'population_size': [100, 200, 400],
        'num_generations': [300, 500],
        'tournament_size': [5, 10],
        'mutation_prob': [0.05, 0.1, 0.15, 0.2]
    }

    ga_combinations = []

    for pop_size in ga_param_grid['population_size']:
        if pop_size == 100:
            elitism_size = 5
        elif pop_size == 200:
            elitism_size = 10
        else:
            elitism_size = 20

        for combo in itertools.product(
                [pop_size],
                ga_param_grid['num_generations'],
                ga_param_grid['tournament_size'],
                ga_param_grid['mutation_prob']
        ):
            ga_combinations.append({
                'population_size': combo[0],
                'num_generations': combo[1],
                'tournament_size': combo[2],
                'elitism_size': elitism_size,
                'mutation_prob': combo[3]
            })

    vns_param_grid = {
        'k_min': [0, 1, 2],
        'k_max': [3, 5],
        'move_prob': [0.1, 0.2],
        'reroute_entire_path_prob': [0.3, 0.5]
    }

    sa_combinations = [dict(zip(sa_param_grid, v)) for v in product(*sa_param_grid.values())]
    ga_combinations = [dict(zip(ga_param_grid, v)) for v in product(*ga_param_grid.values())]
    vns_combinations = [dict(zip(vns_param_grid, v)) for v in product(*vns_param_grid.values())]

    algorithms = []
    if "brute-force" in algorithm_names:
        algorithms.append((BruteForce, [{}]))
    if "genetic" in algorithm_names:
        algorithms.append((GeneticAlgorithm, ga_combinations))
    if "simulated-annealing" in algorithm_names:
        algorithms.append((SimulatedAnnealing, sa_combinations))
    if "vns" in algorithm_names:
        algorithms.append((VNSAlgorithm, vns_combinations))

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
            stopping_criteria = get_stopping_criteria(algorithm_class.__name__, graph)

            for params in param_combinations:
                params.update(stopping_criteria)

                print(f"Running {algorithm_class.__name__} on {example_name} with params: {params}")
                runner = Runner(algorithm_class, graph, params, report_dir)
                runner.run(LogLevel.INFO)
                print('*' * 50)


def get_stopping_criteria(algorithm: str, graph: FlowGraph) -> dict:
    num_nodes = len(graph.get_graph().nodes)
    num_edges = len(graph.get_graph().edges)

    if num_nodes <= 10 and num_edges <= 20:
        graph_size = 'small'
    elif num_nodes <= 25 and num_edges <= 50:
        graph_size = 'medium'
    else:
        graph_size = 'large'

    if algorithm == 'SimulatedAnnealing':
        if graph_size == 'small':
            max_time = 20
            no_improvement_threshold = 50
        elif graph_size == 'medium':
            max_time = 60
            no_improvement_threshold = 150
        else:
            max_time = 80
            no_improvement_threshold = 250

    elif algorithm == 'GeneticAlgorithm':
        if graph_size == 'small':
            max_time = 20
            no_improvement_threshold = 40
        elif graph_size == 'medium':
            max_time = 60
            no_improvement_threshold = 100
        else:
            max_time = 80
            no_improvement_threshold = 150

    elif algorithm == 'VNSAlgorithm':
        if graph_size == 'small':
            max_time = 20
            no_improvement_threshold = 50
        elif graph_size == 'medium':
            max_time = 60
            no_improvement_threshold = 150
        else:
            max_time = 80
            no_improvement_threshold = 250
    elif algorithm == 'BruteForce':
        # This is not used for BruteForce
        return {
            'max_time': float('inf'),
            'no_improvement_threshold': 0
        }

    else:
        raise ValueError(f"Algorithm {algorithm} is not recognized")

    return {
        'max_time': max_time,
        'no_improvement_threshold': no_improvement_threshold
    }


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

    parser.add_argument("--action", type=str, choices=["generate", "run", "run-single", "analyze"], required=True, help="Action to perform (generate or run, run-single, analyze)")
    parser.add_argument("--algorithms", type=str, required=False, help="Algorithms to as run as comma separated list (brute-force, genetic, simulated-annealing, vns)")
    parser.add_argument("--examples", type=str, required=False, help="Root folder of examples to run algorithms on")
    parser.add_argument("--reports", type=str, required=False, help="Folder path to CSV report files for analysis")
    parser.add_argument("--example", type=str, required=False, help="File path of example to run single algorithm on")

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
    elif args.action == "run-single":
        if not args.example:
            print("You must provide an example file path using --example, using default path")
            file_path = "./resources/examples/2b.txt"
        else:
            file_path = args.example

        graph = parse_graph_with_demands(file_path)

        visualize_flow_graph(graph, 'circular')

        if args.algorithms:
            algorithm_names = args.algorithms.split(",")
            algorithm_names = [algorithm.strip() for algorithm in algorithm_names]
            if not all(algorithm in ["brute-force", "genetic", "simulated-annealing", "vns"] for algorithm in algorithm_names):
                return
        else:
            algorithm_names = ["brute-force", "genetic", "simulated-annealing", "vns"]

        algorithms = get_algorithms(algorithm_names)
        for algorithm_class in algorithms:
            print(f"Running {algorithm_class.__name__} on {file_path} with default params")
            runner = Runner(algorithm_class, graph, {}, None)
            runner.run(LogLevel.INFO)
            print('*' * 50)

    elif args.action == "run":
        if args.algorithms:
            algorithms = args.algorithms.split(",")
            algorithms = [algorithm.strip() for algorithm in algorithms]
            if not all(algorithm in ["brute-force", "genetic", "simulated-annealing", "vns"] for algorithm in algorithms):
                return
        else:
            algorithms = ["brute-force", "genetic", "simulated-annealing", "vns"]

        if args.examples:
            root_path = args.examples
        else:
            root_path = "./resources/examples/"
        run_algorithms_in_folder(root_path, algorithms)

    elif args.action == "analyze":
        if not args.reports:
            print("You must provide a path to the reports folder using --reports, using default path")
            reports = "./resources/generated/reports/2024-09-28_11_13_07"
        else:
            reports = args.reports

        stats = Statistics(reports)
        stats.run_best_of_best_analysis()


if __name__ == "__main__":
    main()
