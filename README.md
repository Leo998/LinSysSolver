# LinSysSolver

**LinSysSolver** is a Python program for solving systems of linear equations using **Gaussian elimination**.  
It can output both the **step-by-step process** (to help students learn the method) and the **final solution**.

This project was developed for the *Software and Computing for Applied Physics* course.

---

## Features
- Solve systems of linear equations from CSV input
- Step-by-step explanations of Gaussian elimination
- Silent mode to output only the final solution
- Exact arithmetic using a custom `Fraction` class (no floating-point rounding errors)

---

## Installation
Installation is recommended only within a virtual environment.
Clone the repository and install dependencies:

```bash
git clone https://github.com/Leo998/LinSysSolver.git
cd LinSysSolver
python -m venv venv
. venv/bin/activate
pip install .
# No external dependencies required (only Python standard library)
