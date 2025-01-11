import hypernetx as hnx
import matplotlib.pyplot as plt

# Define the hypergraph with 20 nodes and 10 hyperedges
hyperedges = {
    'e1': {'v1', 'v2', 'v3', 'v4'},
    'e2': {'v3', 'v5', 'v6'},
    'e3': {'v7', 'v8', 'v9'},
    'e4': {'v10', 'v11'},
    'e5': {'v12', 'v13', 'v14', 'v15'},
    'e6': {'v16', 'v17'},
}

# Create the hypergraph object
H = hnx.Hypergraph(hyperedges)

# Visualize the hypergraph
hnx.draw(H, with_node_labels=True, with_edge_labels=True)
plt.title("Hypergraph")
plt.show()
