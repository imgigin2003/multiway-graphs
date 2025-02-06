import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from hypergraph import create_hypergraph

def draw_layered_hypergraph(H, hyperedges):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    node_positions = {}  # Store node positions per layer
    node_instances = {}  # Track multiple instances of a node in different layers
    
    # Assign nodes to layers based on their hyperedges
    layers = {}
    current_layer = 0
    
    for edge, nodes in hyperedges.items():
        layers[current_layer] = list(nodes)  # Convert to list to maintain order
        for node in nodes:
            if node not in node_instances:
                node_instances[node] = []
            node_instances[node].append(current_layer)  # Store all layers where node appears
        current_layer += 1
    
    # Use the "viridis" colormap dynamically
    colormap = plt.get_cmap("viridis", current_layer)
    layers_color = [colormap(i) for i in range(current_layer)]
    
    # Draw nodes and layer surfaces
    for layer, nodes in layers.items():
        sorted_nodes = sorted(nodes)  # Sort for consistency
        for i, node in enumerate(sorted_nodes):
            pos = (i, 0, layer)
            node_positions[(node, layer)] = pos  # Store position per layer
            ax.scatter(*pos, color='black', s=50)
            ax.text(pos[0] + 0.1, pos[1] + 0.1, pos[2] + 0.1, node, fontsize=10, ha='left')
        
        # Define a rectangle for the layer
        vertices = [
            (0, -0.5, layer),
            (len(nodes) - 1, -0.5, layer),
            (len(nodes) - 1, 0.5, layer),
            (0, 0.5, layer)
        ]
        ax.add_collection3d(Poly3DCollection([vertices], alpha=0.3, color=layers_color[layer]))
    
    # Draw hyperedges within the same layer only
    for layer, nodes in layers.items():
        points = np.array([node_positions[(node, layer)] for node in nodes])
        ax.plot(points[:, 0], points[:, 1], points[:, 2], linestyle='--', alpha=1, marker='o')
    
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis (Layers)")
    ax.view_init(elev=20, azim=60)
    
    return fig