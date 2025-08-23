import csv

from typing import NamedTuple
from fraction import Fraction
from equation import Equation
from itertools import combinations


class NumberedEquation(NamedTuple):
    equation_number: int
    equation: Equation

    def __hash__(self):
        return self.equation_number


class SystemEq:

    def __init__(self, *equations_list: Equation):
        self.system: list[NumberedEquation] = [
            NumberedEquation(equation_number=index, equation=equation)
            for index, equation in enumerate(equations_list, 1)
        ]
        self.eq_lenght: int = len(self.system[0].equation.coefficients)
        for n in self.system:
            if self.eq_lenght != len(n.equation.coefficients):
                raise ValueError("Equations in the system have different leghts")

    @classmethod
    def from_csv(cls, filename) -> "SystemEq":
        with open(filename, newline="") as csv_file:
            reader = csv.reader(csv_file)
            unnumbered_system: list[Equation] = []
            for row in reader:
                unnumbered_system.append(
                    Equation(*[Fraction(number) for number in row])
                )
        return SystemEq(*unnumbered_system)

    def __str__(self) -> str:
        output: list[str] = []
        for equation in self.system:
            output.append(f"E{equation.equation_number}: {equation.equation}\n")
        return "".join(output)

    def _del_equation_if_zero(self, eq_number: int) -> None:
        # i = 0
        # j = 1
        # self.system[i] = NumberedEquation(
        #     equation_number=self.system[i].equation_number,
        #     equation=self.system[i].equation - self.system[j].equation * Fraction(5, 1),
        # )
        if self.system[eq_number].equation.is_zero():
            del self.system[eq_number]

    def check_unused_unknowns(self) -> None:
        """ """
        unused: bool = True
        deleted_unkwokns: list[int] = []
        for i in range(self.eq_lenght - 1):  # Does not check constant term.
            unused = True
            for n_eq in self.system:
                if n_eq.equation.coefficients[i] != 0:
                    unused = False
                    break
            if unused == True:
                deleted_unkwokns.append(i)
        for i in deleted_unkwokns[
            ::-1
        ]:  # Reversed so the list is not affected by the deletion
            for n_eq in self.system:
                del n_eq.equation.coefficients[i]
        self.eq_lenght -= len(deleted_unkwokns)

    def minimize_system(self) -> None:
        self.check_unused_unknowns()
        eq_to_be_erased: set[NumberedEquation] = set()
        for eq1, eq2 in combinations(self.system, 2):
            if eq1.equation == eq2.equation:
                eq_to_be_erased.add(eq2)
        for eq in eq_to_be_erased:
            self.system.remove(eq)

    def sort_by_abs_coeff(
        self, from_row: int = 0, column: int = 0, reverse=True
    ) -> None:
        system_from_row: list[NumberedEquation] = self.system[from_row:]
        system_from_row.sort(
            key=lambda num_eq: abs(num_eq.equation.coefficients[column]),
            reverse=reverse,
        )
        self.system = self.system[:from_row] + system_from_row

    def zeroes_pivot_column(self, pivot_row: int, pivot_column: int) -> None:
        reference_eq_coefficient: Fraction = self.system[
            pivot_row
        ].equation.coefficients[pivot_column]
        factor: Fraction = Fraction()
        new_system: list[NumberedEquation] = []
        for n_equation in self.system[:pivot_row] + self.system[pivot_row + 1 :]:
            factor = (
                n_equation.equation.coefficients[pivot_column]
                / reference_eq_coefficient
            )
            new_system.append(
                NumberedEquation(
                    equation_number=n_equation.equation_number,
                    equation=n_equation.equation
                    - self.system[pivot_row].equation * factor,
                )
            )
        new_system.insert(pivot_row, self.system[pivot_row])
        self.system = new_system

    def solve_system(self) -> None:
        self.minimize_system()
        self.sort_by_abs_coeff()
        self.zeroes_pivot_column()


if __name__ == "__main__":
    s1 = SystemEq.from_csv("csv_files/system_to_sort.csv")
    s1.minimize_system()
    print(s1)
    # s1.sort_by_abs_coeff()
    # print(s1)
    s1.sort_by_abs_coeff(2, 2)
    print(s1)
