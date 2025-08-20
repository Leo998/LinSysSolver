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
        >>> eq1 = Equation(Fraction(2), Fraction(-3), Fraction(5))
        >>> print(eq1)
        2 x1 - 3 x2 + 5 = 0

    Add two equations::

        >>> eq2 = Equation(Fraction(1), Fraction(4), Fraction(-2))
        >>> eq_sum = eq1 + eq2
        >>> print(eq_sum)
        3 x1 + 1 x2 + 3 = 0

    Multiply by a scalar::

        >>> eq_scaled = eq1 * 2
        >>> print(eq_scaled)
        4 x1 - 6 x2 + 10 = 0
    """

    def __init__(self, *coefficients: Fraction):
        """
        Initialize an Equation instance.

        Parameters
        ----------
        *coefficients : Fraction
        Positional arguments representing the coefficients of the equation.
        Must include at least two coefficients, with the last one being
        the constant term.

        Raises
        ------
        ValueError
            If fewer than two coefficients are provided.

        Examples
        --------
        >>> from fraction import Fraction
        >>> Equation(Fraction(2), Fraction(-3), Fraction(5))
        2 x1 - 3 x2 + 5 = 0
        """
        self.coefficients: list[Fraction] = list(coefficients)
        if len(self.coefficients) < 2:
            raise ValueError(
                "Not enough fraction given to the costructor to be an equation"
            )

    def __add__(self, other: "Equation") -> "Equation":
        """
        Add two equations term by term.

        Parameters
        ----------
        other : Equation
            The equation to add.

        Returns
        -------
        Equation
            A new Equation instance representing the sum.

        Raises
        ------
        ValueError
            If the two equations have different numbers of coefficients.
        """
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        new_coefficients: list[Fraction] = []
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            new_coefficients.append(coefficient1 + coefficient2)
        return Equation(*new_coefficients)

    def __sub__(self, other: "Equation") -> "Equation":
        """
        Subtract one equation from another term by term.

        Parameters
        ----------
        other : Equation
            The equation to subtract.

        Returns
        -------
        Equation
            A new Equation instance representing the difference.

        Raises
        ------
        ValueError
            If the two equations have different numbers of coefficients.
        """
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        new_coefficients: list[Fraction] = []
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            new_coefficients.append(coefficient1 - coefficient2)
        return Equation(*new_coefficients)

    def __mul__(self, other: Fraction | int | float) -> "Equation":
        """
        Multiply the equation by a scalar.

        Parameters
        ----------
        other : Fraction, int, or float
            The scalar value to multiply each coefficient by.

        Returns
        -------
        Equation
            A new Equation instance with scaled coefficients.
        """
        other_as_fraction: Fraction
        if isinstance(other, int) or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient * other_as_fraction)
        return Equation(*new_coefficients)

    def __rmul__(self, other: Fraction | int | float) -> "Equation":
        """
        Multiply the equation by a scalar (right-hand multiplication).

        Parameters
        ----------
        other : Fraction, int, or float
            The scalar value to multiply each coefficient by.

        Returns
        -------
        Equation
            A new Equation instance with scaled coefficients.
        """
        other_as_fraction: Fraction
        if isinstance(other, int) or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient * other_as_fraction)
        return Equation(*new_coefficients)

    def __truediv__(self, other: Fraction | int | float) -> "Equation":
        """
        Divide the equation by a scalar.

        Parameters
        ----------
        other : Fraction, int, or float
            The scalar value to divide each coefficient by.

        Returns
        -------
        Equation
            A new Equation instance with scaled coefficients.
        """
        other_as_fraction: Fraction
        if isinstance(other, int) or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        new_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            new_coefficients.append(coefficient / other_as_fraction)
        return Equation(*new_coefficients)

    def __eq__(self, other: object) -> bool:
        """
        Check if two equations are equal.

        Parameters
        ----------
        other : Equation
            The equation to compare.

        Returns
        -------
        bool
            True if all corresponding coefficients are equal, False otherwise.

        Raises
        ------
        ValueError
            If the two equations have different numbers of coefficients.
        """
        if not isinstance(other, Equation):
            raise TypeError("Invalid type used for comparison")
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            if coefficient1 != coefficient2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        """
        Check if two equations are not equal.

        Parameters
        ----------
        other : Equation
            The equation to compare.

        Returns
        -------
        bool
            True if any corresponding coefficients differ, False otherwise.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the equation.

        Returns
        -------
        str
            A string in the form:
            "a1 x1 ± a2 x2 ± ... ± an = 0",
            with proper signs and spacing.
        """
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
        """
        Return the formal string representation of the equation.

        Returns
        -------
        str
            Same format as __str__(), showing coefficients and variables.
        """
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
        """
        Check if the equation is identically zero.

        Returns
        -------
        bool
            True if all coefficients are zero, False otherwise.
        """
        return all(c == 0 for c in self.coefficients)


# if __name__ == "__main__":
#     e1 = Equation([Fraction(0, 1), Fraction(0, 4), Fraction(0)])
#     print(e1.is_zero())
