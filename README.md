# Projectile Motion Simulation with Air Drag

This program visualizes a simple animation of projectile motion with air drag. It uses a combination of Python and a C++ module (via Boost.Python bindings) to simulate the physics and plot the results.

## Requirements

- **Boost.Python**: Used to create Python bindings for the C++ code. For more information, visit the [Boost.Python documentation](https://www.boost.org/doc/libs/1_87_0/libs/python/doc/html/index.html).
- Python 3.12 (originally developed for Python 2.7, but adapted and tested for Python 3.12).
- A C++ compiler (e.g., `g++`) to compile the Boost.Python module.

## Compilation Instructions

1. Navigate to the project directory.
2. Compile the C++/Boost module using the `make` command (Linux):
   ```bash
   make
   ```
3. If the compilation fails, you may need to adjust the library paths in the `Makefile` to match your system's Boost installation.

## Running the Program

### Test Simulation
To run a test simulation with hardcoded parameters, execute:
```bash
python test_anim.py
```

### Full Simulation with GUI Controls
To run the full simulation with a graphical interface (Tkinter-based), execute:
```bash
python main.py
```
The GUI allows you to control the simulation parameters interactively.

## Notes

- Ensure Boost.Python is installed and properly configured on your system before attempting to compile the module.
- The program has been quickly adapted to work with Python 3.12, but you may encounter minor compatibility issues depending on your environment.

## Additional Resources

- [Boost.Python Documentation](https://www.boost.org/doc/libs/1_87_0/libs/python/doc/html/index.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

Feel free to contribute or report issues to improve the project!


