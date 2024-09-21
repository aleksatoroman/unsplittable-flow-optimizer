from typing import Dict, List
from models.demand import Demand
from models.graph import FlowGraph
from models.log_level import LogLevel


class FlowResult:
    def __init__(self, paths: Dict[int, List[int]], demands: Dict[int, Demand], edges):
        self.paths = paths
        self.demands = demands
        self.edges = edges

    def calculate_edge_flows(self):
        edge_flows = {edge: 0 for edge in self.edges}

        for sink, path in self.paths.items():
            demand_flow = self.demands[sink].flow
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge = (u, v)
                if edge in edge_flows:
                    edge_flows[edge] += demand_flow

        return edge_flows

    def is_feasible(self):
        edge_flows = self.calculate_edge_flows()

        for edge, flow in edge_flows.items():
            capacity = self.edges[edge]
            if flow > capacity:
                return False

        return True

    def calculate_max_flow_to_capacity_ratio(self):
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
        for demand_key, path in self.paths.items():
            demand = self.demands[demand_key]
            print(f"Path for Demand {demand_key} (Sink: {demand.sink}, Demand: {demand.flow}): {path}")

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