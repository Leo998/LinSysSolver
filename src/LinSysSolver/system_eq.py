import csv

from typing import NamedTuple
from LinSysSolver.fraction import Fraction
from LinSysSolver.equation import Equation
from itertools import combinations

NORMAL_OUTPUT: str = "normal output"
SILENT_OUTPUT: str = ""


class NumberedEquation(NamedTuple):
    """
    Simple container for an Equation with a unique identifier.

    Parameters
    ----------
    equation_number : int
        Identifier of the equation (e.g. its index in the system).
    equation : Equation
        The equation object itself.
    """
    equation_number: int
    equation: Equation

    def __hash__(self) -> int:
        return self.equation_number


class SystemEq:
    """
    Representation and solver for linear systems of equations.

    This class stores a set of Equation objects, wrapped as
    NumberedEquation for identification, and provides methods
    to reduce and solve the system using Gaussian elimination
    with partial pivoting.

    Parameters
    ----------
    *equations_list : Equation
        Variable number of Equation objects representing the system.

    Attributes
    ----------
    system : list of NumberedEquation
        List of equations with unique identifiers.
    num_coefficients : int
        Number of coefficients (including constant term) per equation.
    process_and_solutions: list of tuple

    Raises
    ------
    ValueError
        If the provided equations have different lengths.

    See Also
    --------
    Equation : Represents a single linear equation.
    Fraction : Rational number implementation used for exact arithmetic.

    Notes
    -----
    The solution process is pedagogical: each step prints explanatory
    messages about Gaussian elimination. For numerical work, prefer
    numpy.linalg.solve.

    References
    ----------
    .. [1] Gaussian elimination algorithm:
           https://en.wikipedia.org/wiki/Gaussian_elimination

    Examples
    --------
    >>> from LinSysSolver.fraction import Fraction
    >>> from LinSysSolver.equation import Equation
    >>> e1 = Equation(Fraction(2), Fraction(1), Fraction(-1))
    >>> e2 = Equation(Fraction(1), Fraction(-1), Fraction(3))
    >>> system = SystemEq(e1, e2)
    >>> system.__str__()
    'E1: 2 x1 + 1 x2 - 1 = 0\\nE2: 1 x1 - 1 x2 + 3 = 0\\n'
    """
    def __init__(self, *equations_list: Equation):
        self.system: list[NumberedEquation] = [
            NumberedEquation(equation_number=index, equation=equation)
            for index, equation in enumerate(equations_list, 1)
        ]
        
        # Check if there is at least one equation
        try:
            self.num_coefficients: int = len(self.system[0].equation.coefficients)
        except IndexError: 
            raise TypeError("Constructor requires at least one equation.")
        
        # Check if all equations have the same number of unknowns
        for n in self.system:
            if self.num_coefficients != len(n.equation.coefficients):
                raise ValueError("Equations in the system have different legths")
        self.process_and_solutions: list[tuple[str, str]] = []

    @classmethod
    def from_csv(cls, filename: str) -> "SystemEq":
        """
        Build a system of equations from a CSV file.

        Parameters
        ----------
        filename : str
            Path to the CSV file. Each row represents an equation.

        Returns
        -------
        SystemEq
            New system of equations built from the file.
        """
        with open(filename, newline="") as system_as_csv_file:
            reader = csv.reader(system_as_csv_file)
            unnumbered_system: list[Equation] = []
            for row in reader:
                unnumbered_system.append(Equation(*[Fraction(number) for number in row]))
        return SystemEq(*unnumbered_system)

    def __str__(self) -> str:
        """
        String representation of the system.

        Returns
        -------
        str
            Human-readable string showing all equations with identifiers.
        """
        output: list[str] = []
        for equation in self.system:
            output.append(f"E{equation.equation_number}: {equation.equation}\n")
        return "".join(output)

    def _del_equation_if_zero(self, eq_number: int) -> None:
        """
        Delete an equation from the system if it is identically zero.

        Parameters
        ----------
        eq_number : int
            Index of the equation in the system.
        """
        if self.system[eq_number].equation.is_zero():
            del self.system[eq_number]

    def _check_unused_unknowns(self) -> None:
        """
        Remove unused unknowns from the system.

        Unknowns that always have zero coefficients across all
        equations are eliminated to reduce dimensionality.
        """
        unused: bool = True
        unused_variables: list[int] = []

        # Add all unused variables' indexes to the list of unused variables
        # Does not check constant term.
        for coeff_index in range(self.num_coefficients - 1): 
            unused = True
            for numb_equation in self.system:
                if numb_equation.equation.coefficients[coeff_index] != 0:
                    unused = False
                    break
            if unused == True:
                unused_variables.append(coeff_index)            

        # Remove the unused variables from the system and update num_coefficients.
        # Reversed so the list is not affected by the deletion
        for i in unused_variables[::-1]:
            for numb_equation in self.system:
                del numb_equation.equation.coefficients[i]
        self.num_coefficients -= len(unused_variables)

        if unused_variables != []:
            self.process_and_solutions.append((NORMAL_OUTPUT, "The system has been checked and there were some unknowns that were not used (always had their coefficient equal to zero), so they were excluded from the system\n"))
            self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))

    def _minimize_system(self) -> None:
        """
        Remove redundant equations from the system.

        Equations equivalent to one another are detected and
        only one representative is kept.
        """
        self._check_unused_unknowns()

        # Add all equivalent equations (except one representative) to the list of redundant equations
        eq_to_be_erased: set[NumberedEquation] = set()
        for numb_equation1, numb_equation2 in combinations(self.system, 2):
            if numb_equation1.equation == numb_equation2.equation:
                eq_to_be_erased.add(numb_equation2)
        
        # Remove all redundant equations.
        for eq in eq_to_be_erased:
            self.system.remove(eq)
        
        if eq_to_be_erased:
            self.process_and_solutions.append((NORMAL_OUTPUT, "The system has been ckecked and some equations were equivalent to each other: only one of them has been kept\n"))
            self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))

    def _sort_by_abs_coeff(self, from_row: int = 0, column: int = 0, reverse: bool=True) -> None:
        """
        Sort equations by the absolute value of a coefficient.

        Parameters
        ----------
        from_row : int, default=0
            Row index from which sorting begins.
        column : int, default=0
            Column index of the coefficient used for sorting.
        reverse : bool, default=True
            Whether to sort in descending order.

        Notes
        -----
        This implements partial pivoting, improving numerical stability.
        """
        system_from_row: list[NumberedEquation] = self.system[from_row:]
        system_from_row.sort(
            key=lambda numb_equation: abs(numb_equation.equation.coefficients[column]),
            reverse=reverse,
        )
        self.system = self.system[:from_row] + system_from_row

    def _zeroes_pivot_column(self, pivot_row: int, pivot_column: int) -> None:
        """
        Zero out the pivot column for all rows except the pivot row.

        Parameters
        ----------
        pivot_row : int
            Index of the pivot row.
        pivot_column : int
            Index of the pivot column.
        """
        self.process_and_solutions.append((NORMAL_OUTPUT, f"Now we divide the coefficient of x{pivot_column+1} (from E{self.system[pivot_row].equation_number}) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E{self.system[pivot_row].equation_number} multiplied by that factor from the other row/equation. We repeat this process for every row/equation.\n"))
        pivot_coefficient: Fraction = self.system[pivot_row].equation.coefficients[pivot_column]
        elimination_factor: Fraction = Fraction()
        updated_system: list[NumberedEquation] = []

        # For each row of the system (except the pivot row) find the elimination factor
        for n_equation in self.system[:pivot_row] + self.system[pivot_row + 1 :]:
            elimination_factor = (
                n_equation.equation.coefficients[pivot_column]
                / pivot_coefficient
            )
            # Subtract scaled pivot row to eliminate the pivot column entry.
            updated_system.append(
                NumberedEquation(
                    equation_number=n_equation.equation_number,
                    equation=n_equation.equation
                    - self.system[pivot_row].equation * elimination_factor,
                )
            )
            self.process_and_solutions.append((NORMAL_OUTPUT, f"From E{n_equation.equation_number} we subtract {elimination_factor} * E{self.system[pivot_row].equation_number}\n"))
            
        # HACK: Rebuild the system instead of modifying in place,
        # to avoid overwriting the pivot row during elimination.
        updated_system.insert(pivot_row, self.system[pivot_row])
        self.system = updated_system

    def solve_system(self) -> None:
        """
        Solve the system using Gaussian elimination.

        Applies forward elimination with pivoting, reduces the
        system to row-echelon form, and classifies the solution into:
        - Unique solution
        - No solution (inconsistent system)
        - Infinitely many solutions (underdetermined system)

        Notes
        -----
        Prints detailed step-by-step explanations for educational purposes.
        """
        self.process_and_solutions.append((NORMAL_OUTPUT, "This is the system we'll start from:\n"))
        self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))
        self._minimize_system()

        # Check if system is composed by only zeroes
        if self.num_coefficients == 1 and self.system[0].equation.coefficients[0] == 0:
            self.process_and_solutions.append((NORMAL_OUTPUT, "The system is composed by only zeroes, any value of any unknown is a solution.\n"))
            print("".join([x[1] for x in self.process_and_solutions]))
            return
        
        # Algorithm that reduces the system to row-echelon form
        for current_row in range(len(self.system)):
            for pivot_column in range(current_row, self.num_coefficients - 1):
                self.process_and_solutions.append((NORMAL_OUTPUT, f"We order the equations in descending order of absolute value from row number {current_row+1} downwards based on the coefficient of x{pivot_column+1} because we want it to be different from zero.\n"))
                self._sort_by_abs_coeff(current_row, pivot_column)
                if self.system[current_row].equation.coefficients[pivot_column] == 0:
                    self.process_and_solutions.append((NORMAL_OUTPUT, "All coefficients of this unknown are already zero, so we move to the next one.\n"))
                    if pivot_column == self.num_coefficients - 2:
                        self.process_and_solutions.append((NORMAL_OUTPUT, "There are no more unknowns to go through.\n"))
                        self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))
                    # NOTE: Skip pivoting if all coefficients in this column are zero.
                    # Otherwise, division by zero would occur in elimination.
                    continue
                self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))
                self._zeroes_pivot_column(current_row, pivot_column)
                self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))
                self.process_and_solutions.append((NORMAL_OUTPUT, f"We then divide E{self.system[current_row].equation_number} by its own coefficient of x{pivot_column+1} in order to make it equal to 1 for convenience.\n"))
                
                # Normalize pivot row.
                self.system[current_row] = NumberedEquation(
                    equation_number=self.system[current_row].equation_number,
                    equation=self.system[current_row].equation
                    / self.system[current_row].equation.coefficients[pivot_column],
                )
                self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))
                break
        
        # Deletes any null equation (all coefficients are zero)
        # Reversed so the list is not affected by the deletion
        for current_row in range(len(self.system) - 1, -1, -1):
            self._del_equation_if_zero(current_row)
        self.process_and_solutions.append((NORMAL_OUTPUT, "This is now our final system (with any zero equations deleted).\n"))
        self.process_and_solutions.append((NORMAL_OUTPUT, self.__str__() + "\n"))
        
        # Classify the solution type 
        number_of_unknowns: int = self.num_coefficients - 1
        number_of_equations: int = len(self.system)
        if number_of_equations > number_of_unknowns:
            self._no_solution()
            print("".join([x[1] for x in self.process_and_solutions]))
            return
        else:
            not_zero_coefficients: list[int] = []
            for equation in self.system:
                not_zero_coefficients.append(sum([x != 0 for x in equation.equation.coefficients[:-1]]))
            
            # At least on row has all coefficients equal to zero except the constant term
            if not all(not_zero_coefficients):
                self._no_solution()
                print("".join([x[1] for x in self.process_and_solutions]))
                return
            
            # One row has two or more coefficients that are not equal to zero
            if any([x > 1 for x in not_zero_coefficients]):
                self._infinitely_many_solutions()
                print("".join([x[1] for x in self.process_and_solutions]))
                return
            
            # Every row has exactly one non zero coefficient
            self._unique_solution()
            print("".join([x[1] for x in self.process_and_solutions]))

    def _no_solution(self) -> None:
        """
        Print that the system has no solution.

        Notes
        -----
        Triggered when a row reduces to 0 = c, with c non-zero.
        """
        self.process_and_solutions.append((SILENT_OUTPUT, f"From equation {self.system[-1].equation_number}: 0 = {-1* self.system[-1].equation.coefficients[-1]}\n"))
        self.process_and_solutions.append((SILENT_OUTPUT, "Impossible: this system has no solution."))

    def _unique_solution(self) -> None:
        """
        Print the unique solution of the system.

        Notes
        -----
        Triggered when the system is square and non-singular.
        """
        self.process_and_solutions.append((SILENT_OUTPUT, "This system has only one solution, which is:\n"))
        for n in range(self.num_coefficients - 1):
            self.process_and_solutions.append((SILENT_OUTPUT, f"x{n+1} = {-1* self.system[n].equation.coefficients[-1]}\n"))

    def _infinitely_many_solutions(self) -> None:
        """
        Print that the system has infinitely many solutions.

        Notes
        -----
        Triggered when the system is underdetermined.
        """
        self.process_and_solutions.append((SILENT_OUTPUT, f"This system has {self.num_coefficients - 1} unknowns in {len(self.system)} equations, so it has infinitely many solutions.\n"))
        
        # Print the unknowns and their parameters (if present)
        for numb_equation in self.system:
            output: list[str] = []
            current_sign: str = ""
            for i, coeff in enumerate(numb_equation.equation.coefficients[:-1]):
                if not output and coeff != 0:
                    output.append(f"\nx{i+1} =")
                elif output and coeff != 0:
                    coeff = coeff * -1
                    if coeff < 0:
                        current_sign = "-"
                        coeff = coeff * -1
                    output.append(f" {current_sign} {coeff} x{i+1} ")
                    current_sign = "+"
            
            # Print the constant term (if not 0)
            constant_term: Fraction = numb_equation.equation.coefficients[-1]
            if constant_term != 0 or output[-1].endswith("="):
                constant_term = constant_term * -1
                if constant_term < 0:
                    current_sign = "-"
                constant_term = constant_term * -1
                output.append(f"{current_sign} {abs(constant_term)}")
            
            self.process_and_solutions.append((SILENT_OUTPUT, "".join(output)))
        
        # Print variables that can take any value
        for n in range(len(self.system), self.num_coefficients - 1):
            self.process_and_solutions.append((SILENT_OUTPUT, f"\nx{n+1} = any value"))



# if __name__ == "__main__":
#     s1 = SystemEq.from_csv("csv_files/all_zero.csv")
#     s1.solve_system()
    #print(s1)
