import os
import networkx as nx
import random
import hashlib

class GraphGenerator:
    def __init__(self, num_nodes, edge_prob, source_node, num_demands, demand_type='balanced'):
        self.num_nodes = num_nodes
        self.edge_prob = edge_prob
        self.source_node = source_node
        self.num_demands = num_demands
        self.demand_type = demand_type

        self.edge_lower_bound = 10
        self.edge_upper_bound = 40

    def generate_graph(self):
        G = nx.gnp_random_graph(self.num_nodes, self.edge_prob, directed=True)

        for u, v in G.edges():
            G.edges[u, v]['capacity'] = random.randint(self.edge_lower_bound, self.edge_upper_bound)

        return G

    def remove_outgoing_edges_from_sinks(self, G, demands):
        for sink in demands.keys():
            outgoing_edges = list(G.out_edges(sink))
            for u, v in outgoing_edges:
                G.remove_edge(u, v)
                print(f"Removed outgoing edge from sink {u} to {v}.")

    def ensure_path_to_demands(self, G, demands):
        for demand_node in demands.keys():
            if not nx.has_path(G, self.source_node, demand_node):
                print(f"No path exists from {self.source_node} to {demand_node}, adding intermediate path.")
                self.create_multi_hop_path(G, self.source_node, demand_node)

    def create_multi_hop_path(self, G, source, sink):
        available_nodes = set(G.nodes()) - {source, sink} - set(G.out_edges(sink))

        if len(available_nodes) == 0:
            print(f"No available intermediate nodes to create a path from {source} to {sink}.")
            return

        available_nodes = list(available_nodes)

        num_hops = random.randint(2, min(4, len(available_nodes)))
        intermediate_nodes = random.sample(available_nodes, num_hops)
        path = [source] + intermediate_nodes + [sink]

        for u, v in zip(path[:-1], path[1:]):
            if not G.has_edge(u, v):
                capacity = random.randint(self.edge_lower_bound, self.edge_upper_bound)
                G.add_edge(u, v, capacity=capacity)
                print(f"Added edge from {u} to {v} with capacity {capacity}.")

    def generate_demands(self, G) -> dict[int, list[int]]:
        nodes = list(G.nodes())
        nodes.remove(self.source_node)
        sinks = random.sample(nodes, self.num_demands)

        demands = {}
        for sink in sinks:
            num_vertex_demands = self.determine_number_of_demands()

            sink_demands = []
            for _ in range(num_vertex_demands):
                min_capacity = self.edge_lower_bound
                demand_value = random.randint(1, min_capacity)
                sink_demands.append(demand_value)

            demands[sink] = sink_demands

        return demands


    def alter_source_edges(self, G):
        incoming_edges = list(G.in_edges(self.source_node))

        for u, v in incoming_edges:
            if random.random() < 0.5:
                G.remove_edge(u, v)
                G.add_edge(v, u, capacity=G[v][u]['capacity'] if (v, u) in G.edges else random.randint(1, 50))
                print(f"Reversed edge from {u} -> {v} to {v} -> {u}")
            else:
                G.remove_edge(u, v)
                print(f"Removed edge from {u} -> {v}")

    def determine_number_of_demands(self) -> int:
        if self.demand_type == 'balanced':
            return random.randint(1, 2)
        elif self.demand_type == 'large':
            return random.randint(1, 3)
        else:
            return 1

    def serialize_graph(self, G, demands):
        serialized_graph = []
        serialized_graph.append(f"{self.num_nodes}")
        serialized_graph.append(f"{G.number_of_edges()}")
        serialized_graph.append(f"{self.source_node}")

        for u, v, data in G.edges(data=True):
            capacity = data['capacity']
            serialized_graph.append(f"{u} {v} {capacity}")

        serialized_graph.append(f"{len(demands)}")
        for sink, sink_demands in demands.items():
            serialized_graph.append(f"{sink} {len(sink_demands)} {' '.join(map(str, sink_demands))}")

        return serialized_graph

    def calculate_hash(self, serialized_graph):
        serialized_str = ''.join(serialized_graph).encode('utf-8')
        return hashlib.md5(serialized_str).hexdigest()[:8]



class GraphGeneratorManager:
    def __init__(self, output_dir="graphs"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def write_graph_to_file(self, serialized_graph, filename):
        with open(os.path.join(self.output_dir, filename), 'w') as f:
            for line in serialized_graph:
                f.write(line + '\n')

    def generate_and_save_graph(self, graph_generator, graph_type):
        G = graph_generator.generate_graph()
        demands = graph_generator.generate_demands(G)

        graph_generator.remove_outgoing_edges_from_sinks(G, demands)
        graph_generator.ensure_path_to_demands(G, demands)
        graph_generator.alter_source_edges(G)

        serialized_graph = graph_generator.serialize_graph(G, demands)
        graph_hash = graph_generator.calculate_hash(serialized_graph)
        filename = f"{graph_type}_{graph_hash}.txt"

        self.write_graph_to_file(serialized_graph, filename)

    def generate_small_graph(self):
        graph_generator = GraphGenerator(num_nodes=random.randint(5, 10), edge_prob=0.2, source_node=1,
                                         num_demands=random.randint(1, 3), demand_type='balanced')
        self.generate_and_save_graph(graph_generator, "small_graph")

    def generate_medium_graph(self, demand_type='balanced'):
        graph_generator = GraphGenerator(num_nodes=random.randint(15, 25), edge_prob=0.15, source_node=1,
                                         num_demands=random.randint(3, 6), demand_type=demand_type)
        self.generate_and_save_graph(graph_generator, f"medium_graph_{demand_type}")

    def generate_large_graph(self, demand_type='balanced'):
        graph_generator = GraphGenerator(num_nodes=random.randint(30, 50), edge_prob=0.1, source_node=1,
                                         num_demands=random.randint(5, 10), demand_type=demand_type)
        self.generate_and_save_graph(graph_generator, f"large_graph_{demand_type}")
