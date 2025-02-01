import hypernetx as hnx
import matplotlib.pyplot as plt

def create_dual_graph(H):
    dual_edges = {}

    # Iterate through the incidence dictionary of the original hypergraph
    for edge_id, nodes in H.incidence_dict.items():
        for node in nodes:
            if node not in dual_edges:
                dual_edges[node] = set()
            dual_edges[node].add(edge_id)

    # Construct the dual hypergraph using HyperNetX
    H_dual = hnx.Hypergraph(dual_edges)
    return H_dual

def draw_dual_graph(H_dual):
    fig, ax = plt.subplots(figsize=(10, 8))
    hnx.draw(H_dual, with_node_labels= True, with_edge_labels= True,  ax=ax)
    return fig