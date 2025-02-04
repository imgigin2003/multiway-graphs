import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from hypergraph import create_hypergraph

def draw_layered_hypergraph(H, hyperedges):
    fig = plt.figure(figsize=(10, 8))  # Creates a figure with dimensions 10x8
    ax = fig.add_subplot(111, projection='3d')  # Adds a 3D subplot

    # Assign nodes to layers based on their hyperedges
    layers = {}
    node_layer = {}  # Dictionary to track which layer a node belongs to
    current_layer = 0

    for edge, nodes in hyperedges.items():
        layers[current_layer] = nodes  # Assign each hyperedge to a layer
        for node in nodes:
            node_layer[node] = current_layer  # Store node-layer mapping
        current_layer += 1  # Move to the next layer

    # Use a dynamic colormap for more layer color options
    colormap = plt.get_cmap("tab20", current_layer)  # Colormap for up to 20 layers
    layers_color = [colormap(i) for i in range(current_layer)]
    
    node_positions = {}  # Stores the 3D positions of nodes

    for layer, nodes in layers.items():
        sorted_nodes = sorted(nodes)  # Sort nodes for consistent layout
        for i, node in enumerate(sorted_nodes):
            pos = (i, 0, layer)  # (x, y, z) coordinates
            node_positions[node] = pos  # Save node position
            ax.scatter(*pos, color='black', s=50)  # Plot nodes as black dots
            ax.text(pos[0] + 0.1, pos[1] + 0.1, pos[2] + 0.1, node, fontsize=10, ha='left')  # Shift labels slightly

        # Define a rectangle for the layer
        vertices = [
            (0, -0.5, layer),
            (len(nodes) - 1, -0.5, layer),
            (len(nodes) - 1, 0.5, layer),
            (0, 0.5, layer)
        ]
        ax.add_collection3d(Poly3DCollection([vertices], alpha=0.3, color=layers_color[layer % len(layers_color)]))  # Layer polygon

    # Draw hyperedges as dashed lines connecting nodes
    for edge, nodes in hyperedges.items():
        points = np.array([node_positions[node] for node in nodes])
        ax.plot(points[:, 0], points[:, 1], points[:, 2], linestyle='--', alpha=1, marker='o')  # Connect nodes

    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis (Layers)")
    ax.view_init(elev=20, azim=60)  # Adjust 3D view
    plt.show()

if __name__ == "__main__":
    H, hyperedges = create_hypergraph()
    draw_layered_hypergraph(H, hyperedges)
