# Multiway Graphs (Hypergraph)

- py_script/hypergraph.py -> visualizes a hypergraph based on the given info
- py_scrtip/main.py -> utilizes a web app for displaying the graph info

# How to run?

- ensure your python environment it activated
- change the directory paths specified in the 'main.rs' file with your own Python enviroment and installation
- ensure you have 'hypernetx', 'streamlit', 'matplotlib' installed in your Python packages
- enter the rust-python-integration folder
- run 'export LIBRARY_PATH=$(python3.13 -config --prefix)/lib' to avoid any FFI error
- in the terminal, execute the program with 'cargo run'

# Usage

- after running, hit 'visualize' in the first tab to get the default graph
- in the 'Graph Properties' and 'Graph Table' tabs, you can see the information about the graph
- in the 'Graph Edit' tab, you can see three subtabs. one for Add, one for Edit, and one for Delete
  - in 'Add' subtab, enter the edge name and nodes you want to include
  - in the 'Edit' subtab, from the dropdown menu, you can choose which edge you want to modify
  - in the 'Delete' subtab, from the dropdown menu, you can choose which edge you want to delete
  - after any modification, make sure to hit the 'visualize' button in the 'Graph Visualize' tab to refresh
    the properties tab and table tab
