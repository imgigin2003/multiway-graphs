# Multiway Graphs (Hypergraph)

- py_script/hypergraph.py -> visualizes a hypergraph based on the given info
- py_scrtip/main.py -> utilizes a web app for displaying the graph info

# How to run?

- ensure your python enviroment it activated
- change the directory paths specified in the 'main.rs' file with your own python enviroment and installation
- ensure you have 'hypernetx', 'streamlit', 'matplotlib' installed in your python packages
- enter the rust-python-integration folder
- run 'export LIBRARY_PATH=$(python3.13 -config --prefix)/lib' to avoid any FFI error
- in the terminal, execute the program with 'cargo run'

# Usage

- after running, hit 'visualize' in the first tab to get the default graph
- in the 'Graph Source Code' tab you can see the code snippet
- in the 'Graph Properties' and 'Graph Table' tabs, you can see the informations about the graph
- in the 'Graph Edit' tab, you can see three subtabs. one for Add, one for Edit and one for Delete
  - in 'Add' subtab, enter the edge name and nodex you want to include
  - in 'Edit' subtab, from the dropdown menu, you can chose which edge you want to modify
  - in 'Delete' subtab, from the dropdown menu, you can chose which edge you want to delete
  - after any modification, make sure to hit the 'visualize' button in the 'Graph Visualize' tab to refresh
    the properties tab and table tab
