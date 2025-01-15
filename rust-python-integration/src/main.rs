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

        // Define the path to the virtual environment's Python executable
        //(set this to your virtual environment's Python executable path)
        let venv_path = "/Users/gigin/Documents/GitHub/multiway-graphs/.venv/lib/python3.13/site-packages";
        // Add the virtual environment's `site-packages` to `sys.path` we defined in ven_path
        let setup_code = format!(
            r#"
import sys
sys.path.insert(0, '{}')
"#,
            venv_path
        );

        // Convert the setup code to a C-style string
        let setup_string = CString::new(setup_code).expect("Failed to read CString.");
        // Execute the setup code to add the virtual environment to `sys.path`
        PyRun_SimpleString(setup_string.as_ptr());

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
    println!("Finished executing the Python code from Rust.");
}
