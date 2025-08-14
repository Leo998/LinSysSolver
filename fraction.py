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
            - A float string (e.g. "2.7")
            - A string in the form "a/b" where a and b are integers.

        Returns
        -------
        Fraction
            A Fraction instance corresponding to the parsed string.

        Raises
        ------
        ValueError
            If the string is not in a valid integer, float or "a/b" format.

        Notes
        -----
        Floating-point numbers in string form "a/b" are not supported.

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
            numerator_float = float(fraction_as_string)
            numerator = int(numerator_float)
            denominator: int = 1
            while(numerator != numerator_float):
                numerator_float *= 10
                denominator *= 10
                numerator = int(numerator_float)
        return Fraction(numerator, denominator)

    def __add__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Add two fractions, or a fraction and an integer or float.

        Parameters
        ----------
        other : Fraction, int, float
            The fraction to add.

        Returns
        -------
        Fraction
            The sum of the two fractions.
        """
        if isinstance(other, int | float):
            other = Fraction(other)
        num = self.num * other.den + other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)
    
    def __radd__(self, other: int | float) -> "Fraction":
        """
        Add a fraction to an integer or float.

        Parameters
        ----------
        other : int, float
            The int or float to add.

        Returns
        -------
        Fraction
            The sum of the two addends.
        """
        other: Fraction = Fraction(other)
        num = self.num * other.den + other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)

    def __sub__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Subtract one fraction from another, or an int or float from a fraction.

        Parameters
        ----------
        other : Fraction, int, float
            The fraction to subtract.

        Returns
        -------
        Fraction
            The difference of the two fractions.
        """
        if isinstance(other, int | float):
            other = Fraction(other)
        num = self.num * other.den - other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)
    
    def __rsub__(self, other: int | float) -> "Fraction":
        """
        Subtract one fraction from an int or float.

        Parameters
        ----------
        other : int, float
            The int or float from which to subtract.

        Returns
        -------
        Fraction
            The difference of the int or float and the fraction.
        """
        other: Fraction = Fraction(other)
        num = other.num * self.den - self.num * other.den
        den = self.den * other.den
        return Fraction(num, den)

    def __mul__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Multiply two fractions, or a fraction and an integer or float.

        Parameters
        ----------
        other : Fraction, int, float
            The fraction to multiply with.

        Returns
        -------
        Fraction
            The product of the two fractions.
        """
        if isinstance(other, int | float):
            other = Fraction(other)
        num = self.num * other.num
        den = self.den * other.den
        return Fraction(num, den)

    def __rmul__(self, other: int | float) -> "Fraction":
            """
            Multiply a fraction and an integer or float.

            Parameters
            ----------
            other : int, float
                The int or float to multiply with.

            Returns
            -------
            Fraction
                The product of the two terms.
            """
            other: Fraction = Fraction(other)
            num = self.num * other.num
            den = self.den * other.den
            return Fraction(num, den)

    def __truediv__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Divide one fraction by an integer, a float, or another fraction.

        Parameters
        ----------
        other : Fraction, int, float
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
        if isinstance(other, int | float):
            other = Fraction(other)
        if other.num == 0:
            raise ZeroDivisionError("Error raised by division operator")
        num: int = self.num * other.den
        den: int = self.den * other.num
        return Fraction(num, den)
    
    def __rtruediv__(self, other: int | float) -> "Fraction":
        """
        Divide one int or float by a fraction.

        Parameters
        ----------
        other : int, float
            The int or float divided.

        Returns
        -------
        Fraction
            The quotient of the dividend and divisor.

        Raises
        ------
        ZeroDivisionError
            If the numerator of the fraction is zero.
        """
        other: Fraction = Fraction(other)
        if self.num == 0:
            raise ZeroDivisionError("Error raised by division operator")
        num: int = self.den * other.num
        den: int = self.num * other.den
        return Fraction(num, den)

    def __eq__(self, other: Union["Fraction", int, float]) -> bool:
        """
        Check equality between two fractions or a fraction and an integer or a float.

        Parameters
        ----------
        other : Fraction or int or float
            The value to compare with.

        Returns
        -------
        bool
            True if the two values are equal, False otherwise.

        Raises
        ------
        TypeError
            If other is an unsupported type.
        """
        if isinstance(other, Fraction):
            return self.num * other.den == self.den * other.num
        elif isinstance(other, int):
            return self.num == self.den * other
        elif isinstance(other, float):
            other_as_fraction = Fraction(other)
            return self.num * other_as_fraction.den == self.den * other_as_fraction.num
        raise TypeError("Comparasion between Fraction and invalid type")

    def __ne__(self, other: Union["Fraction", int, float]) -> bool:
        """
        Check inequality between two fractions or a fraction and an integer or a float.

        Parameters
        ----------
        other : Fraction or int or float
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
        
        Examples
        --------
        >>> x = Fraction("-2.8")
        >>> print(x)
        -14/5
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
        
        Examples
        --------
        >>> x = Fraction("-2.8")
        >>> print(x)
        Fraction(-14, 5)
        """
        return f"Fraction({self.num}, {self.den})"

