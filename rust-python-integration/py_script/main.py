import streamlit as st #import the streamlit library
from hypergraph import create_hypergraph, draw_hypergraph #import the hypergraph.py file
import sys
import os

# Add the python/ directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "python"))

def main():
    H = create_hypergraph() #calling the create_hypergraph function from hypergraph.py

    st.title("Intractive Hypergraph") #display the title of the web app
    tabs = st.tabs(["Graph Visualization", "Graph Source Code", "Graph Properties", "Graph Table", "Graph Edit"]) #create tabs for the web app

    with tabs[0]: #first tab
        st.write("### Graph Visualization") #display the title of the tab
        fig = draw_hypergraph(H) #calling the draw_hypergraph function from hypergraph.py
        st.pyplot(fig) #display the graph using the pyplot function from the streamlit library

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
        display_properties(H)
        
def display_properties(H):
    st.write("### Graph Properties")
    nodes_list = list(H.nodes())
    edges_list = list(H.edges())

    st.write(f"Nodes: {nodes_list}")
    st.write(f"Number of nodes: {len(nodes_list)}\n")
    st.write(f"Edges: {edges_list}")
    st.write(f"Number of edges: {len(edges_list)}")

if __name__ == "__main__":
    main()