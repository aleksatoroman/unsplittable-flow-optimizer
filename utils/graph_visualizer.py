import matplotlib.pyplot as plt
import networkx as nx
from models.graph import FlowGraph


def visualize_flow_graph(graph: FlowGraph, layout: str = 'spring', seed: int = 42) -> None:
    G = graph.get_graph()

    if layout == 'spring':
        pos = nx.spring_layout(G, seed=seed)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    else:
        pos = nx.spring_layout(G, seed=seed)

    source_node = next(iter(graph.get_demands())).source
    sink_nodes = [demand.sink for demand in graph.get_demands()]
    other_nodes = [node for node in G.nodes() if node != source_node and node not in sink_nodes]

    nx.draw_networkx_nodes(G, pos, nodelist=[source_node], node_color='red', node_size=800, label='Source')
    nx.draw_networkx_nodes(G, pos, nodelist=sink_nodes, node_color='green', node_size=800, label='Sinks')
    nx.draw_networkx_nodes(G, pos, nodelist=other_nodes, node_color='gray', node_size=600, label='Other Nodes')

    edge_labels = {(u, v): f"{G[u][v]['capacity']}" for u, v in G.edges()}
    nx.draw_networkx_edges(G, pos, edge_color='blue', arrows=True, arrowsize=20, width=1)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')

    node_labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

    for demand in graph.get_demands():
        x, y = pos[demand.sink]
        plt.text(x, y - 0.2, f"Demand: {demand.flow}", fontsize=10, ha='center', color='black', zorder=5)

    plt.title('Flow Graph Visualization')
    plt.axis('off')
    plt.show()
