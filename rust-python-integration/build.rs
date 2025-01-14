fn main() {
    // Specify the Python library version. Use 'python3.13' or similar depending on your system.
    println!("cargo:rustc-link-lib=python3.13");

    // Specify the directory containing the Python library.
    println!("cargo:rustc-link-search=native=/Library/Frameworks/Python.framework/Versions/3.13/lib");

    // Add additional paths if needed (e.g., for config files or headers).
    println!("cargo:rustc-link-search=native=/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/config-3.13-darwin");
}
