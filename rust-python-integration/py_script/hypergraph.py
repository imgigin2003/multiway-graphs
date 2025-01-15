import hypernetx as hnx
import matplotlib.pyplot as plt

def draw_hypergraph():
    # Define the hypergraph with hyperedges and their associated nodes
    hyperedges = {
        'e1': {'v1', 'v2', 'v3', 'v4'},
        'e2': {'v3', 'v5', 'v6'},
        'e3': {'v7', 'v8', 'v9'},
        'e4': {'v10', 'v11'},
        'e5': {'v12', 'v13', 'v14', 'v15'},
        'e6': {'v16', 'v17'},
    }

    # Create a hypergraph object using the defined hyperedges
    H = hnx.Hypergraph(hyperedges)

    # Visualize the hypergraph using hypernetx and matplotlib
    hnx.draw(H, with_node_labels=True, with_edge_labels=True)
    plt.title("Hypergraph")  # Set the title of the plot
    plt.show()  # Display the plot in a window

if __name__ == "__main__":
    draw_hypergraph()
