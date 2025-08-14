import math

from fraction import Fraction


class Equation:


    def __init__(self, coefficients: list[Fraction]):
        self.coefficients: list[Fraction] = coefficients
        if len(self.coefficients) < 2:
            raise ValueError("Not enough fraction given to the costructor to be an equation")
    
    def __add__(self, other: "Equation") -> "Equation":
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        new_coefficients: list[Fraction] = []
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            new_coefficients.append(coefficient1 + coefficient2)
        return Equation(new_coefficients)
    
    def __sub__(self, other: "Equation") -> "Equation":
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        new_coefficients: list[Fraction] = []
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            new_coefficients.append(coefficient1 - coefficient2)
        return Equation(new_coefficients)
    
    def __mul__(self, other: Fraction | int | float) -> "Equation":
        if isinstance(other, int)  or isinstance(other, float):
            other: Fraction = Fraction(other)
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient * other)
        return Equation(new_coefficients)
    
    def __rmul__(self, other: Fraction | int | float) -> "Equation":
        if isinstance(other, int)  or isinstance(other, float):
            other: Fraction = Fraction(other)
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient * other)
        return Equation(new_coefficients)
    
    def __truediv__(self, other: Fraction | int | float) -> "Equation":
        if isinstance(other, int)  or isinstance(other, float):
            other: Fraction = Fraction(other)
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient / other)
        return Equation(new_coefficients)

    def __eq__(self, other: "Equation") -> bool:
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            if coefficient1 != coefficient2:
                return False
        return True

    def __ne__(self, other: "Equation") -> bool:
        return not self.__eq__(other)

    def __str__(self):
        output: list[str] = []
        sign: str = ""
        for subscript, coefficient in enumerate(self.coefficients[:-1], 1):
            if coefficient.num < 0:
                sign = "-"
                coefficient = coefficient * Fraction(-1)
            output.append(f"{sign} {coefficient} x{subscript} ")
            sign = "+"
        if self.coefficients[-1].num < 0:
            sign = "-"
            self.coefficients[-1] = self.coefficients[-1] * Fraction(-1)
            output.append(f"{sign} {self.coefficients[-1]} = 0")
            self.coefficients[-1] = self.coefficients[-1] * Fraction(-1)
        else:
            output.append(f"{sign} {self.coefficients[-1]} = 0")
        output[0] = output[0].lstrip()
        return "".join(output)

    def __repr__(self):
        output: list[str] = []
        sign: str = ""
        for subscript, coefficient in enumerate(self.coefficients[:-1], 1):
            if coefficient.num < 0:
                sign = "-"
                coefficient = coefficient * Fraction(-1)
            output.append(f"{sign} {coefficient} x{subscript} ")
            sign = "+"
        if self.coefficients[-1].num < 0:
            sign = "-"
            self.coefficients[-1] = self.coefficients[-1] * Fraction(-1)
            output.append(f"{sign} {self.coefficients[-1]} = 0")
            self.coefficients[-1] = self.coefficients[-1] * Fraction(-1)
        else:
            output.append(f"{sign} {self.coefficients[-1]} = 0")
        output[0] = output[0].lstrip()
        return "".join(output)
    
    def is_zero(self) -> bool:
        return all(map(lambda x: x == 0, self.coefficients))


# if __name__ == "__main__":
#     e1 = Equation([Fraction(0, 1), Fraction(0, 4), Fraction(0)])
#     print(e1.is_zero())