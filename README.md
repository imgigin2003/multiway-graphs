# Multiway Graphs (Hypergraph)

- py_script/hypergraph.py -> visualizes a hypergraph based on the given info
- py_script/dual_hypergraph.py -> visualizes the dual hypergraph based on the hypergraph
- py_script/main.py -> utilizes a web app for displaying the graph info
- src/main.py -> compiles Python code and handling streamlit

# How to run?

1. install python if you already haven't, verify by running `python3 --version`
2. run `echo $LIBRARY_PATH` to ensure that the library path is being picked up correctly

- you get something like this: `/usr/local/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib`
- update your `build.rs` file based on the library path you get.
- E.g:

  - ```rust
      fn main() {
        // Link the Python 3.13 library
        println!("cargo:rustc-link-lib=python3.13");

        // Specify the search path for the Python libraries
        println!("cargo:rustc-link-search=native=/usr/local/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib");

        // Ensure Rust rebuilds when Python version changes
        println!("cargo:rerun-if-env-changed=PYTHON_SYS_EXECUTABLE");
      }
    ```

3. to be more sure that you won't get any FFI erros, complete the following steps:

- run ```echo $SHELL```

  - if it returns ```/bin/bash```, then run -> ```echo 'export LIBRARY_PATH=$(python3.13 -config --prefix)/lib' >> ~/.bashrc```
  - if it returns ```/bin/zsh```, then run -> ```echo 'export LIBRARY_PATH=$(python3.13 -config --prefix)/lib' >> ~/.zshrc```

- based on your shell, run either ```source ~/.bashrc``` or ```source ~/.zshrc```

4. run the following to compile the program:

- `cargo clean`
- `cargo build`
- `cargo run`

# Usage

- after running, you have two visualization tabs. one for Hypergraph and the other for Dual hypergraph
- in the 'Graph Properties' and 'Graph Table' tabs, you can see the information about the graphs
- in the 'Graph Edit' tab, you can see three subtabs. one for Add, one for Edit, and one for Delete

* BE AWARE THAT YOU CAN ONLY MAKE CHANGED ON THE ORIGINAL GRAPH
  - in 'Add' subtab, enter the edge name and nodes you want to include
  - in the 'Edit' subtab, from the dropdown menu, you can choose which edge you want to modify
  - in the 'Delete' subtab, from the dropdown menu, you can choose which edge you want to delete
  - after any modification, make sure to hit the 'visualize' button in the 'Graph Visualize' tab to refresh
    the properties tab and table tab
