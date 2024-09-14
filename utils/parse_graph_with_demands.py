from models.graph import FlowGraph
from models.demand import Demand


def parse_graph_with_demands(file_content):
    """
    Parses the input file content to create the graph and demands.
    :param file_content: The raw content of the graph and demand input.
    :return: A tuple containing the FlowGraph instance and a list of Demand instances.
    """
    lines = file_content.strip().splitlines()
    num_vertices = int(lines[0])  # Number of vertices
    num_edges = int(lines[1])  # Number of edges
    source = int(lines[2])  # Source node for all demands

    # Create the graph
    G = FlowGraph()

    # Read the edges and capacities
    for i in range(3, 3 + num_edges):
        u, v, capacity = map(int, lines[i].split())
        G.add_edge(u, v, capacity)

    # Read the number of sinks/demands
    num_sinks = int(lines[3 + num_edges])

    # Create the demands, one for each sink
    demands = []
    for i in range(4 + num_edges, 4 + num_edges + num_sinks):
        sink, flow = map(int, lines[i].split())
        demands.append(Demand(source=source, sink=sink, flow=flow))

    return G, demands
