import time

from algorithms.base_algorithm import BaseFlowAlgorithm
from models.graph import FlowGraph
from models.log_level import LogLevel


class Runner:
    def __init__(self, algorithm: BaseFlowAlgorithm, graph: FlowGraph):
        self.algorithm = algorithm
        self.graph = graph

    def run(self):
        print(f"Running {self.algorithm.__class__.__name__}...")

        start_time = time.time()

        result = self.algorithm.solve(self.graph)

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Algorithm {self.algorithm.__class__.__name__} finished. Time taken: {elapsed_time:.4f} seconds")

        if result:
            result.info(LogLevel.INFO)
        else:
            print(f"No solution found using {self.algorithm.__class__.__name__}")

        return result
