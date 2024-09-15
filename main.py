from utils.graph_parser import parse_graph_with_demands
from utils.graph_visualizer import visualize_flow_graph
from algorithms.brute_force import BruteForceFlow

def main() -> None:
    file_path: str = "./resources/4.txt"

    graph = parse_graph_with_demands(file_path)

    visualize_flow_graph(graph, layout='circular', seed=42)

    bf_solver = BruteForceFlow()
    result = bf_solver.solve(graph)

    if result:
        print("Valid paths found for all demands:")
        for i, (path, demand) in enumerate(zip(result.paths.values(), graph.get_demands()), start=1):
            print(f"Path for Demand {i} (Sink: {demand.sink}, Demand: {demand.flow}): {path}")

        result.validate()
    else:
        print("No valid solution found")


if __name__ == "__main__":
    main()
