from utils.graph_parser import parse_graph_with_demands
from utils.graph_visualizer import visualize_flow_graph
from algorithms.brute_force import BruteForceFlow

def main() -> None:
    file_path: str = "./resources/1.txt"

    graph = parse_graph_with_demands(file_path)

    visualize_flow_graph(graph)

    bf_solver = BruteForceFlow()
    result = bf_solver.solve(graph, graph.get_demands())

    if result:
        print("Valid paths found for all demands:")
        for i, path in enumerate(result):
            print(f"Path for Demand {i + 1}: {path}")
    else:
        print("No valid solution found")


if __name__ == "__main__":
    main()
