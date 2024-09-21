from typing import List, Dict, Tuple
from models.log_level import LogLevel


class FlowPath:
    def __init__(self, source: int, sink: int, path: List[int], flow: int):
        self.source = source
        self.sink = sink
        self.path = path
        self.flow = flow

    def __repr__(self):
        return f"FlowPath(Source: {self.source}, Sink: {self.sink}, Flow: {self.flow}, Path: {self.path})"


class FlowResult:
    def __init__(self, flow_paths: List[FlowPath], edges: Dict[Tuple[int, int], int]):
        self.flow_paths = flow_paths
        self.edges = edges

    def calculate_edge_flows(self) -> Dict[Tuple[int, int], int]:
        edge_flows = {edge: 0 for edge in self.edges}

        for flow_path in self.flow_paths:
            path = flow_path.path
            flow = flow_path.flow

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge = (u, v)
                if edge in edge_flows:
                    edge_flows[edge] += flow

        return edge_flows

    def is_feasible(self) -> bool:
        edge_flows = self.calculate_edge_flows()

        for edge, flow in edge_flows.items():
            capacity = self.edges[edge]
            if flow > capacity:
                return False

        return True

    def calculate_max_flow_to_capacity_ratio(self) -> float:

        edge_flows = self.calculate_edge_flows()

        max_flow_to_capacity_ratio = 0
        penalty = 0

        for edge, flow in edge_flows.items():
            capacity = self.edges[edge]
            flow_to_capacity_ratio = flow / capacity

            if flow > capacity:
                penalty += (flow - capacity)

            max_flow_to_capacity_ratio = max(max_flow_to_capacity_ratio, flow_to_capacity_ratio)

        return max_flow_to_capacity_ratio + penalty

    def info(self, level: LogLevel) -> None:
        for flow_path in self.flow_paths:
            print(f"Path for Flow (Source: {flow_path.source}, Sink: {flow_path.sink}, Flow: {flow_path.flow}): {flow_path.path}")

        is_valid = self.is_feasible()
        if is_valid:
            print("All constraints satisfied.")
        else:
            print("There are constraint violations.")

        max_flow_to_capacity_ratio = self.calculate_max_flow_to_capacity_ratio()
        print(f"Maximum Flow-to-Capacity Ratio: {max_flow_to_capacity_ratio:.2f}")

        if level == LogLevel.DEBUG:
            edge_flows = self.calculate_edge_flows()
            for edge, flow in edge_flows.items():
                capacity = self.edges[edge]
                if flow <= capacity:
                    print(f"Edge {edge} carries {flow} flow (max capacity: {capacity}) - OK")
                else:
                    print(f"Edge {edge} carries {flow} flow (max capacity: {capacity}) - VIOLATION")
