import math

from fraction import Fraction


class Equation:

    """
    Representation of a linear equation with fractional coefficients.

    This class supports arithmetic operations between equations,
    scalar multiplication/division, comparison, and formatted string
    representation. It ensures exact arithmetic by using `Fraction`
    instances for coefficients.

    Attributes
    ----------
    coefficients : list of Fraction
        List of coefficients representing the equation.
        The last coefficient is considered the constant term.
        Must contain at least two coefficients.

    Raises
    ------
    ValueError
        If fewer than two coefficients are provided during initialization.
        If arithmetic operations are attempted on equations with different
        numbers of coefficients.

    Examples
    --------
    Create an equation with two variables::

        >>> from fraction import Fraction
        >>> eq1 = Equation([Fraction(2), Fraction(-3), Fraction(5)])
        >>> print(eq1)
        2/1 x1 - 3/1 x2 + 5/1 = 0

    Add two equations::

        >>> eq2 = Equation([Fraction(1), Fraction(4), Fraction(-2)])
        >>> eq_sum = eq1 + eq2
        >>> print(eq_sum)
        3/1 x1 + 1/1 x2 + 3/1 = 0

    Multiply by a scalar::

        >>> eq_scaled = eq1 * 2
        >>> print(eq_scaled)
        4/1 x1 - 6/1 x2 + 10/1 = 0
    """

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
        other_as_fraction: Fraction
        if isinstance(other, int)  or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient * other_as_fraction)
        return Equation(new_coefficients)
    
    def __rmul__(self, other: Fraction | int | float) -> "Equation":
        other_as_fraction: Fraction
        if isinstance(other, int)  or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient * other_as_fraction)
        return Equation(new_coefficients)
    
    def __truediv__(self, other: Fraction | int | float) -> "Equation":
        other_as_fraction: Fraction
        if isinstance(other, int)  or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient / other_as_fraction)
        return Equation(new_coefficients)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Equation):
            raise TypeError("Invalid type used for comparison")
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            if coefficient1 != coefficient2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
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

    def __repr__(self) -> str:
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
        return all( c == 0 for c in self.coefficients)


# if __name__ == "__main__":
#     e1 = Equation([Fraction(0, 1), Fraction(0, 4), Fraction(0)])
#     print(e1.is_zero())