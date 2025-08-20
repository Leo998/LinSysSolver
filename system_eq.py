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

    @classmethod
    def from_csv(cls, filename) -> "SystemEq":
        with open(filename, newline="") as csv_file:
            reader = csv.reader(csv_file)
            unnumbered_system: list[Equation] = []
            for row in reader:
                unnumbered_system.append(Equation([Fraction(number) for number in row]))
        return SystemEq(*unnumbered_system)

    def __str__(self):
        output: list[str] = []
        for equation in self.system:
            output.append(f"E{equation.equation_number}: {equation.equation}\n")
        return "".join(output)

    def _del_equation(self):
        i = 0
        j = 1
        self.system[i] = NumberedEquation(
            equation_number=self.system[i].equation_number,
            equation=self.system[i].equation - self.system[j].equation * Fraction(5, 1),
        )
        if self.system[2].equation.is_zero():
            del self.system[2]

        # self.system[0].equation = self.system[0].equation -  self.system[1].equation * Fraction(5,1)


if __name__ == "__main__":
    x = SystemEq.from_csv("prova.csv")
    print(x)
    x._del_equation()
    print(x)

    # print(s1.system)
