from typing import Union
import math


class Fraction:
    """
    Representation of a mathematical fraction.

    This class supports arithmetic operations, comparisons, and string
    parsing for fractions. It ensures exact arithmetic by avoiding floating-
    point approximations.

    Attributes
    ----------
    numerator : int, float, or str, optional
        The numerator of the fraction (Defaults to 0).
        Can be:
        - int: integer numerator
        - float: will be converted to an exact fraction
        - str: either an integer string or of the form "a/b"
    denominator : int or float, optional
        The denominator of the fraction (Defaults to 1).
        Cannot be zero.

    Raises
    ------
    ZeroDivisionError
        If denominator is 0.
    TypeError
        If the constructor receives an unsupported type combination.

    Examples
    --------
    >>> f1 = Fraction(2, 3)
    >>> f2 = Fraction(2.5)
    >>> f1 + f2
    Fraction(19, 6)
    """

    def __init__(self, numerator: int | float | str = 0, denominator: int = 1):
        if denominator == 0:
            raise ZeroDivisionError("Error raised by Fraction class' constructor")
        if isinstance(numerator, str):
            f = Fraction.from_str(numerator)
            self.num: int = f.num
            self.den: int = f.den
        else:
            self.num = int(numerator)
            self.den = int(denominator)
            while self.num != numerator or self.den != denominator:
                numerator *= 10
                denominator *= 10
                self.num = int(numerator)
                self.den = int(denominator)
        self.simplify()

    def simplify(self):
        """
        Reduce the fraction to its lowest terms.

        Ensures that the denominator is positive by moving any negative
        sign to the numerator.
        """
        greatest_common_divisor = math.gcd(self.num, self.den)
        self.num //= greatest_common_divisor
        self.den //= greatest_common_divisor
        if self.den < 0:  
            self.num *= -1
            self.den *= -1

    @classmethod
    def from_str(cls, fraction_as_string: str) -> "Fraction":
        """
        Create a Fraction instance from a string.

        Parameters
        ----------
        fraction_as_string : str
            A string representing the fraction. Can be:
            - An integer string (e.g. "5")
            - A string in the form "a/b" where a and b are integers.

        Returns
        -------
        Fraction
            A Fraction instance corresponding to the parsed string.

        Raises
        ------
        ValueError
            If the string is not in a valid integer or "a/b" format.

        Notes
        -----
        Floating-point numbers in string form are not supported.

        Examples
        --------
        >>> Fraction.from_str("3/4")
        Fraction(3, 4)
        >>> Fraction.from_str("7")
        Fraction(7, 1)
        """
        try:
            numerator_as_str: str
            denominator_as_str: str
            numerator_as_str, denominator_as_str = fraction_as_string.split("/")
            numerator = int(numerator_as_str)
            denominator = int(denominator_as_str)
        except ValueError:
            numerator = int(fraction_as_string)
            denominator = 1
        return Fraction(numerator, denominator)

    def __add__(self, other: "Fraction") -> "Fraction":
        """
        Add two fractions.

        Parameters
        ----------
        other : Fraction
            The fraction to add.

        Returns
        -------
        Fraction
            The sum of the two fractions.
        """
        num = self.num * other.den + other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)

    def __sub__(self, other: "Fraction") -> "Fraction":
        """
        Subtract one fraction from another.

        Parameters
        ----------
        other : Fraction
            The fraction to subtract.

        Returns
        -------
        Fraction
            The difference of the two fractions.
        """
        num = self.num * other.den - other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)

    def __mul__(self, other: "Fraction") -> "Fraction":
        """
        Multiply two fractions.

        Parameters
        ----------
        other : Fraction
            The fraction to multiply with.

        Returns
        -------
        Fraction
            The product of the two fractions.
        """
        num = self.num * other.num
        den = self.den * other.den
        return Fraction(num, den)

    def __truediv__(self, other: "Fraction") -> "Fraction":
        """
        Divide one fraction by another.

        Parameters
        ----------
        other : Fraction
            The fraction to divide by.

        Returns
        -------
        Fraction
            The quotient of the two fractions.

        Raises
        ------
        ZeroDivisionError
            If the numerator of other is zero.
        """
        if other.num == 0:
            raise ZeroDivisionError("Error raised by division operator")
        num = self.num * other.den
        den = self.den * other.num
        return Fraction(num, den)

    def __eq__(self, other: Union["Fraction", int]) -> bool:
        """
        Check equality between two fractions or a fraction and an integer.

        Parameters
        ----------
        other : Fraction or int
            The value to compare with.

        Returns
        -------
        bool
            True if the two values are equal, False otherwise.

        Raises
        ------
        TypeError
            If other is neither a Fraction nor an int.
        """
        if isinstance(other, Fraction):
            return self.num * other.den == self.den * other.num
        elif isinstance(other, int):
            return self.num == self.den * other
        raise TypeError("Comparasion between Fraction and invalid type")

    def __ne__(self, other: Union["Fraction", int]) -> bool:
        """
        Check inequality between two fractions or a fraction and an integer.

        Parameters
        ----------
        other : Fraction or int
            The value to compare with.

        Returns
        -------
        bool
            True if the two values are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        Return a human-readable string representation of the fraction.

        Returns
        -------
        str
            String in the form "numerator/denominator" or, if the 
            denominator is 1, in the form on an int (by only displaying
            the numerator)
        """
        if self.den == 1:
            return f"{self.num}"
        return f"{self.num}/{self.den}"

    def __repr__(self):
        """
        Return the formal string representation of the fraction.

        Returns
        -------
        str
            String in the form "Fraction(numerator, denominator)".
        """
        return f"Fraction({self.num}, {self.den})"

