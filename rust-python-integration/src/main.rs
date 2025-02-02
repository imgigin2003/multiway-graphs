use std::ffi::CString;
use std::fs;
use std::os::raw::c_char;
use std::process::Command;

extern "C" {
    fn Py_Initialize(); // External function to initialize the Python interpreter.
    fn Py_Finalize(); // External function to finalize (shut down) the Python interpreter.
    fn PyRun_SimpleString(command: *const c_char) -> i32; // External function to execute a Python code string.
}

fn main() {
    unsafe {
        // Initialize the Python interpreter
        Py_Initialize();

        // Path to the external Python file
        let python_file_path = "py_script/main.py";

        // Read the Python script from the file
        let python_code = fs::read_to_string(python_file_path)
            .expect("Failed to read the Python file. Ensure the file exists and is readable.");

        // Convert the Python script into a CString
        let python_cstring = CString::new(python_code)
            .expect("Failed to create CString for Python code.");

        //creates streamlit command line
        let streamlit_command = Command::new("streamlit")
            .arg("run")
            .arg("py_script/main.py")
            .status()
            .expect("Failed to start Streamlit server");

        if streamlit_command.success() {
            println!("Streamlit app is running. Open your browser to view it.");
        } else {
            eprintln!("Failed to run the Streamlit app.");
        }
        
        // Execute the Python script
        if PyRun_SimpleString(python_cstring.as_ptr()) != 0 {
            eprintln!("Error occurred while executing the Python script.");
        }

        // Finalize the Python interpreter
        Py_Finalize();
    }

    println!("Finished executing the Python code from Rust.");
}