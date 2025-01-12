use std::process::Command; // Import the Command struct from the std::process module

fn main() {
    // Define the Python interpreter and script path
    let python_interpreter = "python";
    // let script_path = "/documents/github/multiway-graphs/rust-python/integration/sample.py";
    let script_path = "sample.py";

    // Execute the Python script using the Command struct using new() method
    let output = Command::new(python_interpreter)
        // Add the script path as an argument to the Python interpreter
        .arg(script_path)
        // Output the result of the Python script execution
        .output();

    // Match the output of the Python script execution
    match output {
        // If the Python script execution is successful
        Ok(result) => {
            // Check if the Python script executed successfully
            if result.status.success() {
                // Print a success message
                println!("Python script executed successfully.");
            } else {
                // Print an error message with the stderr output
                eprintln!(
                    "Python script failed with error: {}",
                    // Convert the stderr output to a string
                    String::from_utf8_lossy(&result.stderr)
                );
            }
        }
        // If the Python script execution fails with an error message
        Err(e) => eprintln!("Failed to execute Python script: {}", e),
    }
}
