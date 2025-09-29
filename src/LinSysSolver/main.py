import argparse
from LinSysSolver.system_eq import SystemEq


def main():
    parser = argparse.ArgumentParser(
        prog="LinSysSolver",
        description="Solve systems of linear equations using Gaussian elimination. "
                    "Input must be a CSV file where each row corresponds to an equation."
    )
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
        print(f"Error: File '{args.filename}' not found.")
    except Exception as e:
        print(f"An error occurred while solving the system: {e}")
    
if __name__ == "__main__":
    main()