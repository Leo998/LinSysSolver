import math

from fraction import Fraction


class Equation:
    """
    Representation of a linear equation with fractional coefficients.

    This class models equations of the form:

        a_1 x1 + a_2 x2 + ... + a_n xn + c = 0

    where each coefficient a_i and constant term c
    is stored as a fraction for exact arithmetic.

    Equations can be:
    - Added or subtracted term by term.
    - Scaled by rational, integer, or floating-point factors.
    - Compared for equivalence (up to a multiplicative factor).
    - Printed in a human-readable algebraic format.

    This class is primarily useful for symbolic manipulation of
    systems of linear equations without introducing floating-point
    approximation errors.

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
    TypeError
        If an unsupported type is used in comparison.

    Examples
    --------
    Create an equation with two variables:

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

    Compare equivalent equations (up to scalar factor):

        >>> eq3 = Equation(Fraction(1), Fraction(-1.5), Fraction(2.5))
        >>> eq1 == eq3
        True
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

        Raises
        ------
        ZeroDivisionError
            If `other` evaluates to zero.
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
        Check if two equations are equivalent.

        Two equations are considered equivalent if:
        - They have the same number of coefficients.
        - Each corresponding coefficient is either zero in both equations
          or is a scalar multiple of the other by the same factor.

        Parameters
        ----------
        other : Equation
            The equation to compare with.

        Returns
        -------
        bool
            True if the equations are equivalent (possibly differing only
            by a scalar multiple of their coefficients). False otherwise.

        Raises
        ------
        TypeError
            If `other` is not an Equation instance.
        ValueError
            If the two equations have different numbers of coefficients.

        Notes
        -----
        This implements the standard linear algebra definition of
        equation equivalence up to a scalar multiple.

        Examples
        --------
        >>> from fraction import Fraction
        >>> from equation import Equation
        >>> eq1 = Equation(Fraction(2), Fraction(-4), Fraction(6))
        >>> eq2 = Equation(Fraction(1), Fraction(-2), Fraction(3))
        >>> eq1 == eq2
        True
        >>> eq1 == Equation(Fraction(2), Fraction(-3), Fraction(6))
        False
        """
        if not isinstance(other, Equation):
            raise TypeError("Invalid type used for comparison")
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        factor: Fraction = Fraction(1)

        # NOTE: Find the first non-zero pair to define the scaling factor
        # and use it to check consistency across all coefficients.
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            if coefficient1 != 0 and coefficient2 != 0:
                factor = coefficient1 / coefficient2
                break
        for coefficient1, coefficient2 in zip(self.coefficients, other.coefficients):
            if not_equal_or_multiple(coefficient1, coefficient2, factor):
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
            "a_1 x1 ± a_2 x2 ± ... ± a_n xn ± c = 0",
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

        # HACK: Temporarily flip the sign of the constant term to format it,
        # then restore the original value.
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


def not_equal_or_multiple(c1: Fraction, c2: Fraction, factor: Fraction) -> bool:
    """
    Check whether two coefficients are consistent with a scaling factor.

    This helper determines if two coefficients belong to equations that are
    equivalent up to a multiplicative constant.

    Parameters
    ----------
    c1 : Fraction
        The first coefficient.
    c2 : Fraction
        The second coefficient.
    factor : Fraction
        The factor expected to relate c1 and c2.

    Returns
    -------
    bool
        True if the coefficients are not consistent (i.e. one is zero and the other is not, or
        they are not multiples of each other by the given factor). False otherwise
        (both zero or related by the factor).

    Examples
    --------
    >>> from fraction import Fractio
    >>> from equation import not_equal_or_multiple
    >>> not_equal_or_multiple(Fraction(2), Fraction(4), Fraction(1, 2))
    False
    >>> not_equal_or_multiple(Fraction(0), Fraction(5), Fraction(1))
    True
    >>> not_equal_or_multiple(Fraction(0), Fraction(0), Fraction(1))
    False
    """
    # NOTE: This helper returns False if coefficients are consistent
    # with the scaling factor, True otherwise (slightly inverted logic).
    if (c1 == 0 and c2 != 0) or (c1 != 0 and c2 == 0):
        return True
    elif c1 == 0 and c2 == 0:
        return False
    elif c1 / c2 == factor:
        return False
    else:
        return True
