import time

from models.flow_result import FlowResult
from models.graph import FlowGraph
from models.log_level import LogLevel
from utils.reports import write_report_to_csv


class Runner:
    def __init__(self, algorithm_class, graph: FlowGraph, params: dict, csv_file: str | None):
        self.algorithm = algorithm_class(params)
        self.graph = graph
        self.params = params
        self.csv_file = csv_file

    def run(self, log_level: LogLevel = LogLevel.INFO) -> FlowResult | None:
        print(f"Running {self.algorithm.__class__.__name__} with params {self.params}...")

        start_time = time.time()
        result = self.algorithm.solve(self.graph)
        end_time = time.time()

        elapsed_time = end_time - start_time

        print(f"Algorithm {self.algorithm.__class__.__name__} finished. Time taken: {elapsed_time:.4f} seconds")

        if result:
            result.info(log_level)
        else:
            print(f"No solution found using {self.algorithm.__class__.__name__}")

        if self.csv_file is not None:
            write_report_to_csv(self.csv_file, self.algorithm.__class__.__name__, self.params, elapsed_time, result)

        return result
