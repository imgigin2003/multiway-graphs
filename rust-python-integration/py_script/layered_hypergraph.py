import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib.patches import Ellipse

def draw_layered_hypergraph(hyperedges):
    """Draw a layered hypergraph in 3D with grouped hyperedges and dynamic inter-layer connections."""
    if not hyperedges:
        return None

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Group hyperedges by layer
    layer_groups = {0: [], 1: [], 2: []}  # Top, Middle, Lower
    for edge_name, edge_data in hyperedges.items():
        layer = edge_data.get("layer", 2)  # Default to lower layer if not specified
        if layer in layer_groups:
            layer_groups[layer].append(edge_name)

    # Node positions: (node, layer) -> (x, y, z)
    node_positions = {}
    layer_nodes = {0: set(), 1: set(), 2: set()}  # Nodes in each layer

    # Use custom colors for layers (matching the target image)
    layer_colors = ['#90EE90', '#DDA0DD', '#ADD8E6']  # Green (top), Purple (middle), Blue (lower)

    # Position nodes in each layer
    for layer, edges in layer_groups.items():
        if not edges:
            continue
        # Collect all nodes in this layer
        nodes_in_layer = set()
        for edge in edges:
            nodes_in_layer.update(hyperedges[edge]["nodes"])
        layer_nodes[layer] = nodes_in_layer

        # Create a NetworkX graph for this layer to compute a 2D layout
        import networkx as nx
        G = nx.Graph()
        for node in nodes_in_layer:
            G.add_node(node)
        for edge in edges:
            nodes = list(hyperedges[edge]["nodes"])
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    G.add_edge(nodes[i], nodes[j])

        # Compute 2D positions using spring layout with adjusted parameters
        pos_2d = nx.spring_layout(G, scale=1.5, k=0.5, iterations=50, seed=42)  # Reduced scale and k for compactness

        # Manually adjust positions for single-node hyperedges to avoid overlap
        edge_positions = {}  # Track the center position of each hyperedge
        for edge in edges:
            nodes = list(hyperedges[edge]["nodes"])
            if len(nodes) == 1:
                # Single-node hyperedge: Adjust position to avoid overlap
                node = nodes[0]
                base_pos = pos_2d[node]
                # Check for overlap with other single-node hyperedges
                min_dist = 0.5  # Minimum distance between single-node hyperedges
                for other_edge, other_pos in edge_positions.items():
                    dist = np.linalg.norm(np.array(base_pos) - np.array(other_pos))
                    if dist < min_dist:
                        # Offset the position
                        offset = (min_dist - dist) * np.array([1, 0])  # Offset along x-axis
                        base_pos = (base_pos[0] + offset[0], base_pos[1] + offset[1])
                        pos_2d[node] = base_pos
                edge_positions[edge] = base_pos
            else:
                # Multi-node hyperedge: Compute centroid for reference
                edge_pos = np.mean([pos_2d[node] for node in nodes], axis=0)
                edge_positions[edge] = edge_pos

        # Map 2D positions to 3D by adding the z-coordinate for the layer (reversed)
        z = (2 - layer) * 2.0  # Layer 0 at z=4, layer 2 at z=0
        for node in nodes_in_layer:
            x, y = pos_2d[node]
            node_positions[(node, layer)] = (x, y, z)

    # Draw layer planes
    for layer in range(3):
        z = (2 - layer) * 2.0
        vertices = [
            (-3, -3, z),
            (3, -3, z),
            (3, 3, z),
            (-3, 3, z)
        ]
        ax.add_collection3d(Poly3DCollection([vertices], alpha=0.3, color=layer_colors[layer]))

    # Draw hyperedges as ellipses within each layer
    for edge_name, edge_data in hyperedges.items():
        layer = edge_data.get("layer", 2)
        z = (2 - layer) * 2.0
        node_list = list(edge_data["nodes"])
        points = np.array([node_positions[(node, layer)][:2] for node in node_list])  # 2D points (x, y)
        
        # Modification: Adjust sizes for the bottom layer
        size_multiplier = 3.0 if layer == 2 else 1.0  # Keep the multiplier for multi-node hyperedges
        base_size = 0.5 if layer == 2 else 0.2  # Increase base size for single-node hyperedges in bottom layer
        
        if len(points) == 1:
            # Single node: Draw a circle with a larger base size for the bottom layer
            circle = Ellipse(points[0], base_size * size_multiplier, base_size * size_multiplier, zorder=z, color=layer_colors[layer], alpha=0.6)
            ax.add_patch(circle)
            from mpl_toolkits.mplot3d import art3d
            art3d.pathpatch_2d_to_3d(circle, z=z, zdir="z")
        else:
            # Multiple nodes: Draw an ellipse
            center = np.mean(points, axis=0)
            max_dist = max(np.linalg.norm(p - center) for p in points)
            width = max_dist * 2.9 * size_multiplier
            height = width * 1.5
            angle = np.degrees(np.arctan2(points[1][1] - points[0][1], points[1][0] - points[0][0])) if len(points) >= 2 else 0
            ellipse = Ellipse(center, width, height, angle=angle, zorder=z, color=layer_colors[layer], alpha=0.7)
            ax.add_patch(ellipse)
            from mpl_toolkits.mplot3d import art3d
            art3d.pathpatch_2d_to_3d(ellipse, z=z, zdir="z")

        # Label the edge near the centroid with a background
        centroid_x = np.mean([node_positions[(node, layer)][0] for node in node_list])
        centroid_y = np.mean([node_positions[(node, layer)][1] for node in node_list])
        ax.text(centroid_x, centroid_y, z + 0.4, edge_name, fontsize=10, color="black", ha="center", va="bottom",
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))

    # Draw nodes after ellipses with a higher zorder to ensure they are on top
    for (node, layer), (x, y, z) in node_positions.items():
        ax.scatter(x, y, z, color='black', s=60, zorder=1000)  # Increased zorder
        # Node labels without background, adjusted position
        ax.text(x, y + 0.1, z + 0.1, f"x{node}", fontsize=6, ha='center', va='bottom', zorder=1001)

    # Draw inter-layer dashed lines between adjacent layers
    all_nodes = set()
    for edge_data in hyperedges.values():
        all_nodes.update(edge_data["nodes"])

    for node in all_nodes:
        # Find the layers this node appears in
        node_layers = []
        for layer, edges in layer_groups.items():
            for edge in edges:
                if node in hyperedges[edge]["nodes"]:
                    node_layers.append((layer, edge))
        node_layers.sort()  # Sort by layer

        # Connect the node between adjacent layers (0->1, 1->2)
        for i in range(len(node_layers) - 1):
            layer1, edge1 = node_layers[i]
            layer2, edge2 = node_layers[i + 1]
            if layer2 == layer1 + 1:  # Only connect adjacent layers
                pos1 = node_positions[(node, layer1)]
                pos2 = node_positions[(node, layer2)]
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]], 
                        linestyle='--', color='black', alpha=0.7, lw=1)

    # Configure axes
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis (Layers)")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-0.5, 5)
    ax.view_init(elev=20, azim=60)
    plt.title("Layers of a Hypergraph")
    plt.tight_layout()

    return fig