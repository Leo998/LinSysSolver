# LinSysSolver

**LinSysSolver** is a Python program for solving systems of linear equations using **Gaussian elimination** with exact rational arithmetic.  
Designed for educational purposes, it provides step-by-step explanations of the solution process.

---

## Features
- **Exact arithmetic**: Uses rational number representation (fractions) to avoid floating-point errors
- **Educational output**: Explains each step of the Gaussian elimination process
- **Flexible input**: Reads systems from CSV files
- **Partial pivoting**: Implements numerical stability through coefficient sorting

---

## Quick Start

### Installation
Installation is recommended only within a virtual environment.
Clone the repository and install:

```bash
git clone https://github.com/Leo998/LinSysSolver.git
cd LinSysSolver
python -m venv venv
. venv/bin/activate
pip install .
# No external dependencies required (only Python standard library)
```

### Basic Usage

```bash
# Solve a system with full explanation
LinSysSolver system.csv

# Solve a system with only the solution (no explanation)
LinSysSolver -s system.csv 
```

### CSV File Format

Create a CSV file where each row represents one equation. Each column represents a coefficient, with the last column being the constant term.

For the system:
```
2x₁ + 3x₂ + 5 = 0
x₁ - x₂ + 1 = 0
```

Create `system.csv`:
```csv
2,3,5
1,-1,1
```

**Note: Equations are in the form `a₁x₁ + a₂x₂ + ... + c = 0`, so constant terms should have opposite sign.**

## Testing

```bash
# Run tests (requires pytest) with coverage and doctest
make test
```

## Requirements

- Python 3.11
- No external dependencies for core functionality
- Dependencies for development contained in **[Requirements](requirements.txt)**

## License

MIT License

## Author

Leonardo Ossino
University of Bologna - Master Degree in Physics
University Project for *Software and Computing for Applied Physics* course

