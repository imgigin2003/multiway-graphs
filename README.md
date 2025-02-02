# Multiway Graphs (Hypergraph)

- py_script/hypergraph.py -> visualizes a hypergraph based on the given info
- py_script/dual_hypergraph.py -> visualizes the dual hypergraph based on the hypergraph
- py_script/main.py -> utilizes a web app for displaying the graph info
- src/main.py -> compiles Python code and handling streamlit

# How to run?

1. install python if you already haven't, verify by running `bash python3 --version`
2. run `bash echo $LIBRARY_PATH` to ensure that the library path is being picked up correctly

- you get something like this: `bash/usr/local/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib`
- update you `bash build.rs` file based on the library path you get.
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

- run ```bash echo $SHELL```

  - if it returns ```bash /bin/bash```, then run -> ```bash echo 'export LIBRARY_PATH=$(python3.13 -config --prefix)/lib' >> ~/.bashrc```
  - if it returns ```bash /bin/zsh```, then run -> ```bash echo 'export LIBRARY_PATH=$(python3.13 -config --prefix)/lib' >> ~/.zshrc```

- based on your shell, run either ```bash source ~/.bashrc``` or ```bash source ~/.zshrc```

4. run the following to compile the program:

- `bash cargo clean`
- `bash cargo build`
- `bash cargo run`

# Usage

- after running, hit 'visualize' in the first tab to get the default graph
- in the 'Graph Properties' and 'Graph Table' tabs, you can see the information about the graph
- in the 'Graph Edit' tab, you can see three subtabs. one for Add, one for Edit, and one for Delete
  - in 'Add' subtab, enter the edge name and nodes you want to include
  - in the 'Edit' subtab, from the dropdown menu, you can choose which edge you want to modify
  - in the 'Delete' subtab, from the dropdown menu, you can choose which edge you want to delete
  - after any modification, make sure to hit the 'visualize' button in the 'Graph Visualize' tab to refresh
    the properties tab and table tab
