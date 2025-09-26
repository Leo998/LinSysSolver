from typing import Union
import math


class Fraction:
    """
    Representation of a mathematical fraction with exact arithmetic.

    This class supports arithmetic operations, comparisons, and string
    parsing for fractions. It ensures exact arithmetic by avoiding floating-
    point approximations.

    Mathematical Theory
    -------------------
    A fraction represents a rational number p/q where p (numerator) and q (denominator)
    are integers and q ≠ 0. All fractions are automatically reduced to lowest terms
    using the Greatest Common Divisor (GCD) algorithm, ensuring canonical representation.

    Parameters
    ----------
    numerator : int, float, or str, optional
        The numerator of the fraction (Defaults to 0).
        Can be:
        - int: integer numerator
        - float: will be converted to an exact fraction
        - str: either an integer or float string or of the form "a/b"
    denominator : int or float, optional
        The denominator of the fraction (Defaults to 1).
        Cannot be zero
    
    Attributes
    ----------
    num : int
        The numerator in reduced form.
    den : int
        The denominator in reduced form (always positive).

    Notes
    -----
    Fractions are always stored in simplified form, using the Euclidean
    algorithm (via math.gcd). The denominator is always kept positive,
    with negative signs moved to the numerator.

    Raises
    ------
    ZeroDivisionError
        If denominator is 0.
    TypeError
        If the constructor receives an unsupported type combination.

    Examples
    --------
    Basic fraction creation:
    
    >>> f1 = Fraction(2, 3)
    >>> f2 = Fraction(2.5)
    >>> f1 + f2
    Fraction(19, 6)

    String parsing:
    
    >>> Fraction("3/4")
    Fraction(3, 4)
    >>> Fraction("2.5")
    Fraction(5, 2)
    """

    def __init__(self, numerator: int | float | str = 0, denominator: int | float = 1):
        """
        Initialize a Fraction instance.

        Parameters
        ----------
        numerator : int, float, or str, optional
            The numerator of the fraction (Defaults to 0)
            Can be:
            - int: integer numerator
            - float: will be converted into an exact fraction
            - str: either an integer or float string or a string in the form "a/b"
        denominator : int or float, optional
            The denominator of the fraction (Defaults to 1)
            Cannot be zero

        Raises
        ------
        ZeroDivisionError
            If denominator is 0.
        TypeError
            If the input types cannot be converted into a valid Fraction.

        Notes
        -----
        Float conversion uses decimal expansion: multiplies by powers of 10
        until the float becomes an exact integer, creating equivalent fraction.
        This ensures exact representation without floating-point errors.

        Examples
        --------
        >>> Fraction(3, 4)
        Fraction(3, 4)
        >>> Fraction(2.5)
        Fraction(5, 2)
        >>> Fraction("7/3")
        Fraction(7, 3)
        >>> Fraction("8")
        Fraction(8, 1)
        """
        if denominator == 0:
            raise ZeroDivisionError("Error raised by Fraction class' constructor")
        
        if isinstance(numerator, str):
            fraction_from_string = Fraction.from_str(numerator)
            self.num: int = fraction_from_string.num
            self.den: int = fraction_from_string.den
        else:
            self.num = int(numerator)
            self.den = int(denominator)
            # Convert floats to exact fractions using decimal expansion
            while self.num != numerator or self.den != denominator:
                numerator *= 10
                denominator *= 10
                self.num = int(numerator)
                self.den = int(denominator)
        self.simplify()

    def simplify(self) -> None:
        """
        Reduce the fraction to its lowest terms using the Euclidean algorithm.

        This method applies the Greatest Common Divisor (GCD) to both numerator and
        denominator to ensure the fraction is in canonical form. It also ensures that 
        the denominator is positive by moving any negative sign to the numerator.

        Notes
        -----
        This method modifies the fraction in-place and is automatically called by
        the constructor and all arithmetic operations.

        See Also
        --------
        math.gcd : Built-in function for computing Greatest Common Divisor
        __init__ : Constructor that calls this method automatically

        Examples
        --------
        >>> f = Fraction()
        >>> f.num, f.den = 15, -10  # Manually set non-reduced form
        >>> f.simplify()
        >>> print(f)
        -3/2
        """
        greatest_common_divisor = math.gcd(self.num, self.den)
        self.num //= greatest_common_divisor
        self.den //= greatest_common_divisor
        
        # Moves any negative sign to the numerator
        if self.den < 0:
            self.num *= -1
            self.den *= -1

    @classmethod
    def from_str(cls, fraction_as_string: str) -> "Fraction":
        """
        Create a Fraction instance from a string.

        This method parses various string formats to create fractions,
        handling integer strings, float strings, and explicit fraction notation.

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
        - Floating-point numbers in string form "a/b" are not supported.
        - This method is used internally by __init__ when the
          numerator is a string.

        Examples
        --------
        >>> Fraction.from_str("3/4")
        Fraction(3, 4)
        >>> Fraction.from_str("7")
        Fraction(7, 1)
        """
        numerator: int
        denominator: int
        try:
            # Convert the string into a Fraction if the string is in the form "a/b" 
            numerator_as_str: str
            denominator_as_str: str
            numerator_as_str, denominator_as_str = fraction_as_string.split("/")
            numerator = int(numerator_as_str)
            denominator = int(denominator_as_str)
        except ValueError:
            numerator_float = float(fraction_as_string)
            numerator_int = int(numerator_float)
            denominator = 1
            # Convert float to exact fraction using decimal expansion
            # It also works if it an int by doing nothing
            while numerator_int != numerator_float:
                numerator_float *= 10
                denominator *= 10
                numerator_int = int(numerator_float)
            numerator = numerator_int
        return Fraction(numerator, denominator)

    def __add__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Add two fractions, or a fraction and an integer or float.

        Implements fraction addition using the formula: a/b + c/d = (ad + bc)/(bd).
        Non-fraction operands are automatically converted to fractions before
        the operation.

        Parameters
        ----------
        other : Fraction, int, float
            The fraction to add.

        Returns
        -------
        Fraction
            New Fraction representing the sum, automatically reduced to lowest terms.

        Notes
        -----
        Addition is performed by cross-multiplying denominators to obtain
        a common denominator.

        Examples
        --------
        >>> Fraction(1, 2) + Fraction(1, 3)
        Fraction(5, 6)
        >>> Fraction(3, 2) + 1
        Fraction(5, 2)
        """
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        num = self.num * other.den + other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)

    def __radd__(self, other: int | float) -> "Fraction":
        """
        Add a fraction to an integer or float (right-hand addition). 

        Parameters
        ----------
        other : int, float
            The int or float to add.

        Returns
        -------
        Fraction
            The sum of the two addends.
        """
        other_as_fraction: Fraction = Fraction(other)
        num = self.num * other_as_fraction.den + other_as_fraction.num * self.den
        den = self.den * other_as_fraction.den
        return Fraction(num, den)

    def __sub__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Subtract one fraction from another, or an int or float from a fraction.

        Implements fraction subtraction using: a/b - c/d = (ad - bc)/(bd).

        Parameters
        ----------
        other : Fraction, int, float
            The fraction to subtract.

        Returns
        -------
        Fraction
            The difference of the two fractions.
        
        Examples
        --------
        >>> Fraction(1, 2) - Fraction(1, 3)
        Fraction(1, 6)
        >>> Fraction(3, 2) - 1
        Fraction(1, 2)
        """
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        num = self.num * other.den - other.num * self.den
        den = self.den * other.den
        return Fraction(num, den)

    def __rsub__(self, other: int | float) -> "Fraction":
        """
        Subtract one fraction from an int or float (right-hand subtraction).

        Parameters
        ----------
        other : int, float
            The int or float from which to subtract.

        Returns
        -------
        Fraction
            The difference of the int or float and the fraction.
        """
        other_as_fraction: Fraction = Fraction(other)
        num = other_as_fraction.num * self.den - self.num * other_as_fraction.den
        den = self.den * other_as_fraction.den
        return Fraction(num, den)

    def __mul__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Multiply two fractions, or a fraction and an integer or float.

        Implements fraction multiplication: (a/b) * (c/d) = (ac)/(bd).

        Parameters
        ----------
        other : Fraction, int, float
            The fraction to multiply with.

        Returns
        -------
        Fraction
            The product of the two fractions.

        Examples
        --------
        >>> Fraction(2, 3) * Fraction(3, 4)
        Fraction(1, 2)
        >>> Fraction(5, 2) * 2
        Fraction(5, 1)
        """
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        
        # This makes sure that in case of "Fraction * Equation" the method called
        # is __rmul__ from equation class, and not this one.
        if not isinstance(other, Fraction):
            return NotImplemented
        
        num = self.num * other.num
        den = self.den * other.den
        return Fraction(num, den)

    def __rmul__(self, other: int | float) -> "Fraction":
        """
        Multiply a fraction and an integer or float (right-hand multiplication).

        Parameters
        ----------
        other : int, float
            The int or float to multiply with.

        Returns
        -------
        Fraction
            The product of the two terms.
        """
        other_as_fraction: Fraction = Fraction(other)
        num = self.num * other_as_fraction.num
        den = self.den * other_as_fraction.den
        return Fraction(num, den)

    def __truediv__(self, other: Union["Fraction", int, float]) -> "Fraction":
        """
        Divide one fraction by an integer, a float, or another fraction.

        Implements fraction division: (a/b) ÷ (c/d) = (a/b) * (d/c) = (ad)/(bc).

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

        Notes
        -----
        Division of fractions is equivalent to multiplying the dividend
        by the reciprocal of the divisor.

        Examples
        --------
        >>> Fraction(3, 4) / Fraction(2, 3)
        Fraction(9, 8)
        >>> Fraction(5, 2) / 2
        Fraction(5, 4)
        """
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        if other.num == 0:
            raise ZeroDivisionError("Error raised by division operator")
        num: int = self.num * other.den
        den: int = self.den * other.num
        return Fraction(num, den)

    def __rtruediv__(self, other: int | float) -> "Fraction":
        """
        Divide one int or float by a fraction (right-hand division).

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
        other_as_fraction: Fraction = Fraction(other)
        if self.num == 0:
            raise ZeroDivisionError("Error raised by division operator")
        num: int = self.den * other_as_fraction.num
        den: int = self.num * other_as_fraction.den
        return Fraction(num, den)

    def __abs__(self) -> "Fraction":
        """
        Return the absolute value of the fraction.

        Returns
        -------
        Fraction
            A new Fraction instance with a non-negative numerator
            and the same denominator.

        Notes
        -------------------
        The absolute value of a rational number p/q is |p|/|q|.
        Since denominators are always positive after simplification,
        we only need to take the absolute value of the numerator.
        
        Examples
        --------
        >>> abs(Fraction(-3, 4))
        Fraction(3, 4)
        >>> abs(Fraction(5, -2))
        Fraction(5, 2)
        """
        return Fraction(abs(self.num), self.den)

    def __eq__(self, other: object | int | float) -> bool:
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

        Notes
        -----
        Equality is checked by cross-multiplication to avoid
        floating-point approximations.

        Examples
        --------
        >>> Fraction(1, 2) == Fraction(2, 4)
        True
        >>> Fraction(1, 2) == 0.5
        True
        >>> Fraction(2, 3) == 2
        False
        """
        if isinstance(other, Fraction):
            return self.num * other.den == self.den * other.num
        elif isinstance(other, float) or isinstance(other, int):
            other_as_fraction = Fraction(other)
            return self.num * other_as_fraction.den == self.den * other_as_fraction.num
        raise TypeError("Comparison between Fraction and invalid type")

    def __ne__(self, other: object | int | float) -> bool:
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

    def __lt__(self, other: object | int | float) -> bool:
        """
        Check if this fraction is less than another value.

        Parameters
        ----------
        other : Fraction, int, or float
            The value to compare with.

        Returns
        -------
        bool
            True if this fraction is less than other, False otherwise.

        Raises
        ------
        TypeError
            If other is not a Fraction, int, or float.

        Notes
        -----
        Comparison is done by cross-multiplication to avoid floating-point
        approximations.

        Examples
        --------
        >>> Fraction(1, 2) < Fraction(3, 4)
        True
        >>> Fraction(1, 2) < 1
        True
        >>> Fraction(3, 2) < 1.5
        False
        """
        other_as_fraction: Fraction
        if isinstance(other, int) or isinstance(other, float):
            other_as_fraction = Fraction(other)
        elif isinstance(other, Fraction):
            other_as_fraction = other
        else:
            raise TypeError("Comparison between Fraction and invalid type")
        return (self.num * other_as_fraction.den) < (other_as_fraction.num * self.den)

    def __gt__(self, other: object | int | float) -> bool:
        """
        Check if this fraction is greater than another value.

        Parameters
        ----------
        other : Fraction, int, or float
            The value to compare with.

        Returns
        -------
        bool
            True if this fraction is greater than other, False otherwise.

        Raises
        ------
        TypeError
            If other is not a Fraction, int, or float.

        Notes
        -----
        Comparison is done by cross-multiplication to avoid floating-point
        approximations.

        Examples
        --------
        >>> Fraction(3, 4) > Fraction(1, 2)
        True
        >>> Fraction(2, 1) > 1
        True
        >>> Fraction(1, 2) > 1.5
        False
        """
        other_as_fraction: Fraction
        if isinstance(other, int) or isinstance(other, float):
            other_as_fraction = Fraction(other)
        elif isinstance(other, Fraction):
            other_as_fraction = other
        else:
            raise TypeError("Comparison between Fraction and invalid type")
        return (self.num * other_as_fraction.den) > (other_as_fraction.num * self.den)
    
    def __le__(self, other: object | int | float) -> bool:
        """
        Check if this fraction is less or equal than another value.

        Parameters
        ----------
        other : Fraction, int, or float
            The value to compare with.

        Returns
        -------
        bool
            True if this fraction is less or equal than other, False otherwise.

        Examples
        --------
        >>> Fraction(3, 2) <= 1.5
        True
        """
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other: object | int | float) -> bool:
        """
        Check if this fraction is greater or equal than another value.

        Parameters
        ----------
        other : Fraction, int, or float
            The value to compare with.

        Returns
        -------
        bool
            True if this fraction is greater or equal than other, False otherwise.

        Examples
        --------
        >>> Fraction(2, 1) >= 2
        True
        """
        return self.__gt__(other) or self.__eq__(other)

    def __str__(self) -> str:
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

    def __repr__(self) -> str:
        """
        Return the formal string representation of the fraction.

        Returns
        -------
        str
            String in the form "Fraction(numerator, denominator)".

        Notes
        -----
        This differs from __str__: __repr__ is meant for debugging
        and unambiguous reconstruction, while __str__ is user-friendly.

        Examples
        --------
        >>> x = Fraction("-2.8")
        >>> x
        Fraction(-14, 5)
        """
        return f"Fraction({self.num}, {self.den})"
