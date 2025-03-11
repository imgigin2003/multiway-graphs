import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def draw_layered_hypergraph(hyperedges):
    """Draw a layered hypergraph in 3D based on a simple hypergraph's hyperedges."""
    if not hyperedges:
        return None

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    node_positions = {}  # Store (node, layer) -> (x, y, z) positions
    layers = {}          # Layer index -> list of nodes in that hyperedge
    layer_index = 0

    # Assign each hyperedge to a layer
    for edge_name, nodes in hyperedges.items():
        layers[layer_index] = list(nodes)  # Convert set to list for ordering
        layer_index += 1

    # Use "viridis" colormap for layers
    colormap = plt.get_cmap("viridis", max(1, layer_index))  # Avoid division by zero
    layer_colors = [colormap(i) for i in range(layer_index)]

    # Position nodes and draw layers
    for layer, nodes in layers.items():
        unique_nodes = sorted(set(nodes))  # Remove duplicates within a layer
        num_nodes = len(unique_nodes)
        
        # Place nodes in a compact grid (adjustable rows/cols)
        cols = min(3, num_nodes)  # Max 3 nodes per row
        rows = (num_nodes + cols - 1) // cols
        for i, node in enumerate(unique_nodes):
            x = (i % cols) * 0.8  # Spacing along X
            y = (i // cols) * 0.4  # Spacing along Y
            z = layer * 1.25      # Layer height
            pos = (x, y, z)
            node_positions[(node, layer)] = pos
            ax.scatter(*pos, color='black', s=50)
            ax.text(x + 0.1, y + 0.1, z + 0.1, node, fontsize=10, ha='left')

        # Draw layer plane (adjust width/height based on node count)
        width = max(1, cols * 0.8 - 0.2)  # Minimum width of 1
        height = max(1, rows * 0.4)       # Minimum height of 1
        vertices = [
            (-0.2, -0.2, layer * 1.25),
            (width, -0.2, layer * 1.25),
            (width, height - 0.2, layer * 1.25),
            (-0.2, height - 0.2, layer * 1.25)
        ]
        ax.add_collection3d(Poly3DCollection([vertices], alpha=0.3, color=layer_colors[layer]))

    # Draw hyperedges within layers
    for layer, nodes in layers.items():
        node_coords = [node_positions[(node, layer)] for node in nodes if (node, layer) in node_positions]
        if len(node_coords) > 1:
            # Connect all pairs of nodes in the hyperedge (undirected)
            for i in range(len(node_coords)):
                for j in range(i + 1, len(node_coords)):
                    x_vals = [node_coords[i][0], node_coords[j][0]]
                    y_vals = [node_coords[i][1], node_coords[j][1]]
                    z_vals = [node_coords[i][2], node_coords[j][2]]
                    ax.plot(x_vals, y_vals, z_vals, linestyle='--', color='gray', alpha=1)

    # Optional: Connect same nodes across layers (comment out if not desired)
    all_nodes = set().union(*hyperedges.values())
    for node in all_nodes:
        node_layers = [layer for layer in layers if node in layers[layer]]
        if len(node_layers) > 1:
            for i in range(len(node_layers) - 1):
                pos1 = node_positions[(node, node_layers[i])]
                pos2 = node_positions[(node, node_layers[i + 1])]
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]], 
                        linestyle=':', color='blue', alpha=0.5)

    # Set axis labels and view
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis (Layers)")
    ax.set_xlim(-0.5, max(3, max(len(set(nodes)) for nodes in layers.values())) * 0.8)
    ax.set_ylim(-0.5, max(1, max((len(set(nodes)) + 2) // 3 * 0.4 for nodes in layers.values())))
    ax.set_zlim(-0.1, layer_index * 1.25)
    ax.view_init(elev=20, azim=60)
    plt.title("Layered Hypergraph from Simple Hypergraph")
    plt.tight_layout()

    return fig
