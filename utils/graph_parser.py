from typing import List
from models.graph import FlowGraph
from models.demand import Demand


def parse_graph_with_demands(file_path: str) -> FlowGraph:
    with open(file_path, 'r') as file:
        lines: List[str] = file.readlines()

    num_edges: int = int(lines[1].strip())
    source: int = int(lines[2].strip())

    G: FlowGraph = FlowGraph()

    for i in range(3, 3 + num_edges):
        u, v, capacity = map(int, lines[i].strip().split())
        G.add_edge(u, v, capacity)

    num_demand_vertices: int = int(lines[3 + num_edges].strip())

    for i in range(4 + num_edges, 4 + num_edges + num_demand_vertices):
        demand_info = list(map(int, lines[i].strip().split()))
        sink = demand_info[0]
        num_demands = demand_info[1]

        for j in range(num_demands):
            flow = demand_info[2 + j]
            demand = Demand(source=source, sink=sink, flow=flow)
            G.add_demand(demand)

    return G
