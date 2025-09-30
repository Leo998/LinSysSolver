import argparse
import sys
from LinSysSolver.system_eq import SystemEq


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="LinSysSolver",
        description="Solve systems of linear equations using Gaussian elimination with exact rational arithmetic."
                    " Input must be a CSV file where each row corresponds to an equation.",
                    epilog='''
Examples:
  LinSysSolver system.csv              Solve with full step-by-step explanation
  LinSysSolver -s system.csv -s        Show only the solution

CSV Format:
  Each row represents one equation with coefficients in order.
  The last column is the constant term.
  Equations are in the form: a₁x₁ + a₂x₂ + ... + c = 0
  
  Example for the system:
    2x₁ + 3x₂ = 5  →  2x₁ + 3x₂ - 5 = 0
    x₁ - x₂ = 1    →  x₁ - x₂ - 1 = 0
  
  Create system.csv:
    2,3,-5
    1,-1,-1

For more information, see the documentation at:
https://github.com/Leo998/LinSysSolver/docs
''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("filename",
                        help= "Path to CSV file containing the system of equations (see documentation)")
    parser.add_argument('-s', '--silent',
                    action='store_true',
                    help= "only print the final solution (suppress step-by-step explanation)")
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="LinSysSolver 0.1.0"
    )
    args = parser.parse_args()
    try:
        system_of_equation: SystemEq = SystemEq.from_csv(args.filename)
        system_of_equation.solve_system(args.silent)
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid CSV format - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
if __name__ == "__main__":
    main()