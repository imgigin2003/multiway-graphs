import streamlit as st #import the streamlit library
from hypergraph import create_hypergraph, draw_hypergraph #import the hypergraph.py file
import hypernetx as hnx
import pandas as pd
import sys
import os

# Add the python/ directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "python"))

def main():
    H, hyperedges = create_hypergraph() #calling the create_hypergraph function from hypergraph.py

    if "hyperedges" not in st.session_state:
        _, hyperedges = create_hypergraph()
        st.session_state.hyperedges = hyperedges
    
    st.title("Intractive Hypergraph") #display the title of the web app
    tabs = st.tabs([
        "Graph Visualization",
        "Graph Source Code", 
        "Graph Properties", 
        "Graph Table", 
        "Graph Edit"
    ]) #create tabs for the web app
    
    with tabs[0]:  # Graph Visualization Tab
        st.write("### Graph Visualization")

        # Create a hypergraph dynamically from session state
        H = hnx.Hypergraph(st.session_state.hyperedges)

        # Add a button to refresh the graph visualization manually
        if st.button("Visualize ✨"):
            st.session_state.refresh = True

        if "refresh" in st.session_state:
            fig = draw_hypergraph(H)  # Visualize the updated hypergraph
            st.pyplot(fig)

    with tabs[1]: #second tab
        st.write("### Graph Code Snippet") #display the title of the tab
        st.code("""
import hypernetx as hnx
import matplotlib.pyplot as plt

def create_hypergraph():
    # Define the hypergraph with hyperedges and their associated nodes
    hyperedges = {
        'e1': {'v1', 'v2', 'v3', 'v4'},
        'e2': {'v3', 'v5', 'v6'},
        'e3': {'v6','v7', 'v8', 'v9'},
        'e4': {'v10', 'v11'},
        'e5': {'v12', 'v13', 'v14'},
        'e6': {'v14', 'v15', 'v16'},
    }

    # Create a hypergraph object using the defined hyperedges
    H = hnx.Hypergraph(hyperedges)
    return H

def draw_hypergraph(H):
    fig, ax = plt.subplots(figsize= (8, 6))

    # Visualize the hypergraph using hypernetx and matplotlib
    hnx.draw(H, with_node_labels=True, with_edge_labels=True, ax = ax)

    return fig
        """)

    with tabs[2]: #third tab
        display_properties(H) #calling the display_properties function

    with tabs[3]: #forth tab
        display_table(hyperedges)

    with tabs[4]: #fifth tab
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
    

#defining a function to display the graph properties
def display_properties(H):
    # Display the title of the tab
    st.write("### Graph Properties")

    # Display the number of nodes and edges in the hypergraph
    nodes_list = list(H.nodes())
    edges_list = list(H.edges())

    st.write(f"Nodes: {nodes_list}")
    st.write(f"Number of nodes: {len(nodes_list)}\n")
    st.write(f"Edges: {edges_list}")
    st.write(f"Number of edges: {len(edges_list)}")


# Define a function to display the graph table
def display_table(hyperedges):
    st.write("### Graph Table")

    # Create a DataFrame for edges and nodes
    edge_data = [
        {"Edge ID": edge_id, "Nodes": ", ".join(nodes)}
        for edge_id, nodes in hyperedges.items()
    ]
    df = pd.DataFrame(edge_data)

    # Display the table
    st.dataframe(df)

if __name__ == "__main__":
    main()