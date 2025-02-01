import hypernetx as hnx
import matplotlib.pyplot as plt

def create_hypergraph():
    # Define the hypergraph with hyperedges and their associated nodes
    hyperedges = {
        'e1': {'v1', 'v2', 'v3'},
        'e2': {'v3', 'v4'},
        'e3': {'v5', 'v6'},
        'e4': {'v6', 'v7', 'v8'},
        'e5': {'v9', 'v10'},
        'e6': {'v11', 'v12'}
    }

    # Create a hypergraph object using the defined hyperedges
    H = hnx.Hypergraph(hyperedges)
    return H, hyperedges

def draw_hypergraph(H):
    fig, ax = plt.subplots(figsize= (8, 6))

    # Visualize the hypergraph using hypernetx and matplotlib
    hnx.draw(H, with_node_labels=True, with_edge_labels=True, ax = ax)

    return fig