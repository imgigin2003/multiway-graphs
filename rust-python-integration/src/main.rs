use std::ffi::CString;
use std::fs;
use std::os::raw::c_char;

extern "C" {
    fn Py_Initialize(); // External function to initialize the Python interpreter.
    fn Py_Finalize(); // External function to finalize (shut down) the Python interpreter.
    fn PyRun_SimpleString(command: *const c_char) -> i32; // External function to execute a Python code string.
}

fn main() {
    unsafe {
        // Initialize the Python interpreter
        Py_Initialize();

        // Define the path to the virtual environment's Python executable
        let venv_path = "/Users/gigin/Documents/GitHub/multiway-graphs/myenv/lib/python3.13/site-packages";
        let setup_code = format!(
            r#"
import sys
sys.path.insert(0, '{}')
"#,
            venv_path
        );

        // Convert the setup code to a C-style string and execute it
        let setup_string = CString::new(setup_code).expect("Failed to create CString for setup code.");
        PyRun_SimpleString(setup_string.as_ptr());

        // Path to the external Python file
        let python_file_path = "py_script/main.py";

        // Read the Python script from the file
        let python_code = fs::read_to_string(python_file_path)
            .expect("Failed to read the Python file. Ensure the file exists and is readable.");

        // Convert the Python script into a CString
        let python_cstring = CString::new(python_code)
            .expect("Failed to create CString for Python code.");

        // Execute the Python script
        if PyRun_SimpleString(python_cstring.as_ptr()) != 0 {
            eprintln!("Error occurred while executing the Python script.");
        }

        // Finalize the Python interpreter
        Py_Finalize();
    }

    println!("Finished executing the Python code from Rust.");
}