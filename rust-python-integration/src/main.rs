use std::ffi::CString; // Import CString to work with C-style strings in Rust.
use std::os::raw::c_char; // Import c_char, a type representing a C-style char.

extern "C" {
    fn Py_Initialize(); // External function to initialize the Python interpreter.
    fn Py_Finalize(); // External function to finalize (shut down) the Python interpreter.
    fn PyRun_SimpleString(command: *const c_char) -> i32; // External function to execute a Python code string.
}

fn main() {
    unsafe { // Unsafe block to allow interaction with C libraries and raw pointers.
        // Initialize the Python interpreter
        Py_Initialize(); // Start the Python interpreter and set it up for execution.

        // Add the virtual environment's `site-packages` to `sys.path`
        let setup_code = CString::new(r#"
import sys
sys.path.insert(0, '/Users/gigin/Documents/GitHub/multiway-graphs/.venv/lib/python3.13/site-packages')"#) 
            // Define a Python script to modify `sys.path` by adding the virtual environment's package directory.
            .expect("CString::new failed"); // Ensure that converting the Rust string to CString does not fail.

        PyRun_SimpleString(setup_code.as_ptr()); 
        // Execute the setup Python script to ensure the virtual environment is configured.

        // Define the main Python script as a string.
        let python_code = CString::new(r#"
import hypernetx as hnx
import matplotlib.pyplot as plt

def draw_hypergraph():
    # Define the hypergraph with hyperedges and their associated nodes
    hyperedges = {
        'e1': {'v1', 'v2', 'v3', 'v4'},
        'e2': {'v3', 'v5', 'v6'},
        'e3': {'v7', 'v8', 'v9'},
        'e4': {'v10', 'v11'},
        'e5': {'v12', 'v13', 'v14', 'v15'},
        'e6': {'v16', 'v17'},
    }

    # Create a hypergraph object using the defined hyperedges
    H = hnx.Hypergraph(hyperedges)

    # Visualize the hypergraph using hypernetx and matplotlib
    hnx.draw(H, with_node_labels=True, with_edge_labels=True)
    plt.title("Hypergraph") # Set the title of the plot
    plt.show() # Display the plot in a window

if __name__ == "__main__":
    draw_hypergraph() # Call the function to draw the hypergraph
"#).expect("CString::new failed"); // Ensure that the conversion to CString does not fail.

        PyRun_SimpleString(python_code.as_ptr()); 
        // Execute the main Python script, which draws the hypergraph.

        // Finalize the Python interpreter
        Py_Finalize(); // Shut down the Python interpreter and clean up resources.
    }
}
