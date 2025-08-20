import csv

from typing import NamedTuple
from fraction import Fraction
from equation import Equation


class NumberedEquation(NamedTuple):
    equation_number: int
    equation: Equation


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
                unnumbered_system.append(Equation(*[Fraction(number) for number in row]))
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
        """
        """
        unused: bool = True
        deleted_unkwokns: list[int] = []
        for i in range(self.eq_lenght - 1): # Does not check constant term.
            unused = True
            for n_eq in self.system:
                if n_eq.equation.coefficients[i] != 0:
                    unused = False
                    break
            if unused == True:
                deleted_unkwokns.append(i)
        for i in deleted_unkwokns[::-1]:
            for n_eq in self.system:
                del n_eq.equation.coefficients[i]
        self.eq_lenght -= len(deleted_unkwokns)

# if __name__ == "__main__":
#     x = SystemEq.from_csv("csv_files/unused_unknowns.csv")
#     print(x)
#     x.check_unused_unknowns()
#     print(x)
    # x._del_equation_if_zero(0)
    # print(x)
    # x._del_equation_if_zero(2)
    # print(x)
