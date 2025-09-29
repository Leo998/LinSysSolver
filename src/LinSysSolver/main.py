import argparse
from LinSysSolver.system_eq import SystemEq


def main():
    parser = argparse.ArgumentParser(description="Linear system of equation solver")
    parser.add_argument("filename",
                        help= "Name of csv file containing the system of equation (see documentation)")
    parser.add_argument('-s', '--silent',
                    action='store_true',
                    help= "Only the solutions are printed (no explanation)")
    args = parser.parse_args()
    system_of_equation: SystemEq = SystemEq.from_csv(args.filename)
    system_of_equation.solve_system(args.silent)
    
if __name__ == "__main__":
    main()