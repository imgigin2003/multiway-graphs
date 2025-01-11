use pyo3::prelude::*;
use std::ffi::CString;

fn run_python_code() -> PyResult<()> {
    // Initialize the Python interpreter
    Python::with_gil(|py| {
        // Define the Python code as a string
        let code = r#"
import hypernetx as hnx
import matplotlib.pyplot as plt

# Define the hypergraph with 20 nodes and 10 hyperedges
hyperedges = {
    'e1': {'v1', 'v2', 'v3', 'v4'},
    'e2': {'v3', 'v5', 'v6'},
    'e3': {'v7', 'v8', 'v9'},
    'e4': {'v10', 'v11'},
    'e5': {'v12', 'v13', 'v14', 'v15'},
    'e6': {'v16', 'v17'},
}

# Create the hypergraph object
H = hnx.Hypergraph(hyperedges)

# Visualize the hypergraph
hnx.draw(H, with_node_labels=True, with_edge_labels=True)
plt.title("Hypergraph")
plt.show()
"#;

        // Convert the Rust string to a C-style string
        let c_code = CString::new(code).unwrap();  // This creates a C-style string (CStr)
        
        // Now run the Python code
        py.run(c_code.as_c_str(), None, None)?;

        Ok(())
    })
}

fn main() {
    // Run the Python code from Rust
    if let Err(e) = run_python_code() {
        eprintln!("Error: {:?}", e);
    }
}
