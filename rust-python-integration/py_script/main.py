import streamlit as st #import the streamlit library
from hypergraph import create_hypergraph, draw_hypergraph #import the hypergraph.py file
from layered_hypergraph import draw_layered_hypergraph #import the layered_hypergraph.py
from dual_hypergraph import create_dual_graph, draw_dual_graph #import the dual_hypergraph.py
import hypernetx as hnx #import hypernetx library
import pandas as pd #import pandas to work with tabular data


def main():
    H, hyperedges = create_hypergraph() #calling the create_hypergraph function from hypergraph.py

    if "hyperedges" not in st.session_state:
        _, hyperedges = create_hypergraph()
        st.session_state.hyperedges = hyperedges

    st.title("Intractive Hypergraph") #display the title of the web app
    tabs = st.tabs([
        "HyperGraph Visualization", 
        "Layered HyperGraph Visualization",
        "Dual HyperGraph Visualization",
        "Graph Properties", 
        "Graph Table", 
        "Graph Edit"
    ]) #create tabs for the web app
    
    with tabs[0]:  # HyperGraph Visualization Tab
        st.write("### HyperGraph Visualization")

        # Create a hypergraph dynamically from session state
        H = hnx.Hypergraph(st.session_state.hyperedges)

        # Add a button to refresh the graph visualization manually
        if st.button("Visualize HyperGraph✨"):
            st.session_state.refresh = True

        if "refresh" in st.session_state:
            # Visualize the hypergraph
            fig = draw_hypergraph(H)  
            st.pyplot(fig)

    with tabs[1]: # Layered HyperGraph Visualization Tab
        st.write("### Layered HyperGraph Visualization")

        # Add a button to refresh the graph visualization manually
        if st.button("Visualize Layered HyperGraph✨"):
            st.session_state.refresh_layered = True

        if "refresh_layered" in st.session_state:
            # Visualize the Layered hypergraph
            fig = draw_layered_hypergraph(H, st.session_state.hyperedges)
            st.pyplot(fig)


    with tabs[2]:  # Dual HyperGraph Visualization Tab
        st.write("### Dual HyperGraph Visualization")

        # Create the original hypergraph dynamically
        H = hnx.Hypergraph(st.session_state.hyperedges)

        # Create the dual hypergraph
        H_dual = create_dual_graph(H)

        # Add a button to refresh the graph visualization manually
        if st.button("Visualize Dual HyperGraph✨"):
            st.session_state.refresh_dual = True

        if "refresh_dual" in st.session_state:
            # Visualize the dual hypergraph
            fig = draw_dual_graph(H_dual)
            st.pyplot(fig)
            

    with tabs[3]: #third tab
        st.write("### Graphs Properties")
        display_properties(H, "HyperGraph") #displays the properties for the original graph

        H_dual = create_dual_graph(H)
        display_properties(H_dual, "Dual HyperGraph") #displays the propeties for the dual graph

    with tabs[4]: #forth tab
        st.write("### Graphs Tables")
        display_table(st.session_state.hyperedges, "HyperGraph") #displays the table for the original graph

        H_dual = create_dual_graph(H)
        display_table(H_dual, "Dual HyperGraph") #displays the table for the dual graph

    with tabs[5]: #fifth tab
        st.write("### Graph Edit")
        edit_sub_tabs = st.tabs(["Add Hyperedge", "Edit Hyperedge", "Delete Hyperedge"])  # Renamed to 'edit_sub_tabs'

        # Add Hyperedge Subtab
        with edit_sub_tabs[0]:
            st.write("#### Add Hyperedge") #display the title of the subtab
            new_edge_id = st.text_input("Enter new edge ID (e.g., e7):", key="new_edge_id") #takes new edge from text input
            new_nodes = st.text_input("Enter nodes for the new edge (comma-separated):", key="new_nodes") #takes new nodes from text input
            if st.button("Add Hyperedge"):
                if new_edge_id and new_nodes: #check if each text inputs aren't empty
                    nodes_set = set(new_nodes.split(",")) #split the nodes list with ','
                    if new_edge_id in st.session_state.hyperedges: #if edge exists in the edges list
                        st.warning("Edge ID already exists!")
                    else:
                        st.session_state.hyperedges[new_edge_id] = nodes_set #add the new nodes set to the visualize session
                        st.success(f"Hyperedge '{new_edge_id}' added with nodes {nodes_set}!") #display a success operation
                
        # Edit Hyperedge Subtab
        with edit_sub_tabs[1]:
            st.write("### Edit Hyperedge") # Display the title of the subtab
            edge_to_edit = st.selectbox( # Dropdown to select an edge to edit
                "Select an edge to edit:", options=st.session_state.hyperedges.keys()
            )  
            edited_nodes = st.text_input( # Text input for new nodes for the selected edge
                "Enter new nodes for the selected edge (comma-separated):", key="edit_nodes" 
            ) 
            if st.button("Edit Hyperedge"): 
                if edge_to_edit and edited_nodes: #check if the text inputs arent't empty
                    new_nodes_set = set(edited_nodes.split(",")) #split the nodes list with ','
                    st.session_state.hyperedges[edge_to_edit] = new_nodes_set #set the edited edges to the new node lise
                    st.success(f"Hyperedge '{edge_to_edit}' updated with nodes '{new_nodes_set}") #display a success operation
                    st.session_state.refresh = True  # Set refresh flag to True
    
        # Delete Hyperedge Subtab
        with edit_sub_tabs[2]:
            st.write("### Delete Hyperedge") # Display the title of the subtab
            edges_to_delete = st.selectbox( # Dropdown to select an edge to delete
                "Select an edge tp delete:", options=list(st.session_state.hyperedges.keys()) 
            )
            if st.button("Delete Hyperedge"): # Button to delete the selected edge
                if edges_to_delete:  # Check if the selected edge is not empty
                    del st.session_state.hyperedges[edges_to_delete] #delete the selected edge
                    st.success(f"Hyperedge '{edges_to_delete}' deleted successfully.") #display a success operation
                    st.session_state.refresh = True # Set refresh flag to True


#defining a function to display the graph properties
def display_properties(H, graph_type):
    # Display the title of the tab
    st.write(f"### {graph_type} Properties")

    # Display the number of nodes and edges in the hypergraph
    nodes_list = list(H.nodes())
    edges_list = list(H.edges())

    st.write(f"Nodes: {nodes_list}")
    st.write(f"Number of nodes: {len(nodes_list)}\n")
    st.write(f"Edges: {edges_list}")
    st.write(f"Number of edges: {len(edges_list)}")


# Define a function to display the graph table
def display_table(graph, graph_type):
    st.write(f"### {graph_type} Table")

    if isinstance(graph, dict): #The function checks whether graph is a dictionary
        #(which could represent an edge list or hypergraph where keys are edges and values are nodes connected by those edges)
        edge_data = [
            {"Edge ID": edge_id, "Nodes": ", ".join(str(node) for node in nodes)}
            for edge_id, nodes in graph.items()
        ]

    else: #this block is expected to be a mapping where keys are nodes and values are the edges that the node is part of
        edge_data = []
        node_to_edges = {}
        for node, edges in graph.incidence_dict.items():
            node_to_edges[node] = {str(edge) for edge in edges}
        for node, edges in node_to_edges.items():
            edge_data.append({"Node": str(node), "Edges": ", ".join(sorted(edges))})

    df = pd.DataFrame(edge_data) #visualizes it as tabular data
    st.dataframe(df) # Display the table


if __name__ == "__main__":
    main()