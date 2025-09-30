from LinSysSolver.fraction import Fraction


class Equation:
    """
    Representation of a linear equation with fractional coefficients.

    This class models homogeneous linear equations of the form:

        a_1 x1 + a_2 x2 + ... + a_n xn + c = 0

    where each coefficient a_i and constant term c
    is stored as a fraction for exact arithmetic.

    Mathematical Theory
    -------------------
    Linear equations represent hyperplanes in n-dimensional space. Two equations
    are considered equivalent if one can be obtained from the other by multiplication
    with a non-zero scalar. This class implements exact rational arithmetic for 
    symbolic manipulation of linear systems.

    Equations can be:
    - Added or subtracted term by term.
    - Scaled by rational, integer, or floating-point factors.
    - Compared for equivalence (up to a multiplicative factor).
    - Printed in a human-readable algebraic format.

    This class is primarily useful for symbolic manipulation of
    systems of linear equations without introducing floating-point
    approximation errors.

    Parameters
    ----------
    *coefficients : Fraction
        Variable coefficients followed by the constant term.
        Must provide at least 2 coefficients (1 variable + constant).

    Attributes
    ----------
    coefficients : list of Fraction
        List of coefficients representing the equation.
        The last coefficient is the constant term.
        All coefficients are stored in simplified Fraction form.

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

        >>> from LinSysSolver.fraction import Fraction
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
        Initialize an Equation instance with given coefficients.

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

        Notes
        -----
        Coefficients are stored as-is without modification. The Fraction class
        ensures they are automatically in simplified form.
        The minimum of 2 coefficients ensures the equation represents at least
        one variable plus a constant term.

        Examples
        --------
        >>> from LinSysSolver.fraction import Fraction
        >>> Equation(Fraction(2), Fraction(-3), Fraction(5))
        2 x1 - 3 x2 + 5 = 0
        """
        self.coefficients: list[Fraction] = list(coefficients)
        if len(self.coefficients) < 1:
            raise ValueError("Empty row left in the system")
        if len(self.coefficients) < 2:
            raise ValueError("Not enough coefficients given to be an equation")

    def __add__(self, other: "Equation") -> "Equation":
        """
        Add two equations term by term.

        Implements vector addition of coefficient vectors, representing
        the linear combination of two hyperplanes.

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
        
        Examples
        --------
        >>> eq1 = Equation(Fraction(2), Fraction(-1), Fraction(3))  
        >>> eq2 = Equation(Fraction(1), Fraction(2), Fraction(-1)) 
        >>> eq_sum = eq1 + eq2
        >>> print(eq_sum)
        3 x1 + 1 x2 + 2 = 0
        """
        if len(self.coefficients) != len(other.coefficients):
            raise ValueError("Equation instances have different number of coefficients")
        added_coefficients: list[Fraction] = []
        for self_coeff, other_coeff in zip(self.coefficients, other.coefficients):
            added_coefficients.append(self_coeff + other_coeff)
        return Equation(*added_coefficients)

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
        subtracted_coefficients: list[Fraction] = []
        for self_coeff, other_coeff in zip(self.coefficients, other.coefficients):
            subtracted_coefficients.append(self_coeff - other_coeff)
        return Equation(*subtracted_coefficients)

    def __mul__(self, other: Fraction | int | float) -> "Equation":
        """
        Multiply the equation by a scalar.

        Implements scalar multiplication of the equation, which geometrically
        represents the same hyperplane with scaled normal vector.

        Parameters
        ----------
        other : Fraction, int, or float
            The scalar value to multiply each coefficient by.

        Returns
        -------
        Equation
            A new Equation instance with scaled coefficients.
        
        Examples
        --------
        >>> eq = Equation(Fraction(2), Fraction(-3), Fraction(1))
        >>> scaled_eq = eq * Fraction(1, 2)
        >>> print(scaled_eq)
        1 x1 - 3/2 x2 + 1/2 = 0
        """
        other_as_fraction: Fraction
        if isinstance(other, int) or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        multiplied_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            multiplied_coefficients.append(coefficient * other_as_fraction)
        return Equation(*multiplied_coefficients)

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
        multiplied_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            multiplied_coefficients.append(coefficient * other_as_fraction)
        return Equation(*multiplied_coefficients)

    def __truediv__(self, other: Fraction | int | float) -> "Equation":
        """
        Divide the equation by a scalar.

        Equivalent to multiplication by the reciprocal of the scalar.

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
        
        Notes
        -----
        Zero division is handled by the Fraction class, which raises
        ZeroDivisionError when attempting to divide by zero.

        Examples
        --------
        >>> eq = Equation(Fraction(4), Fraction(-2), Fraction(6))
        >>> divided_eq = eq / 2
        >>> print(divided_eq)
        2 x1 - 1 x2 + 3 = 0
        """
        other_as_fraction: Fraction
        if isinstance(other, int) or isinstance(other, float):
            other_as_fraction = Fraction(other)
        else:
            other_as_fraction = other
        divided_coefficients: list[Fraction] = []
        for coefficient in self.coefficients:
            divided_coefficients.append(coefficient / other_as_fraction)
        return Equation(*divided_coefficients)

    def __eq__(self, other: object) -> bool:
        """
        Check if two equations are equivalent.

        Two equations are equivalent if they represent the same hyperplane; 
        one can be obtained from the other by scalar multiplication.

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
            If other is not an Equation instance.
        ValueError
            If the two equations have different numbers of coefficients.

        Notes
        -----
        This implements the standard linear algebra definition of
        equation equivalence up to a scalar multiple.

        Examples
        --------
        >>> from LinSysSolver.fraction import Fraction
        >>> from LinSysSolver.equation import Equation
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
        for self_coeff, other_coeff in zip(self.coefficients, other.coefficients):
            if self_coeff != 0 and other_coeff != 0:
                factor = self_coeff / other_coeff
                break
        
        # Verify all coefficient pairs are consistent with this factor
        for self_coeff, other_coeff in zip(self.coefficients, other.coefficients):
            # Returns True if NOT consistent
            if are_coefficients_inconsistent(self_coeff, other_coeff, factor):
                return False   # So equation is not equal
        return True

    def __ne__(self, other: object) -> bool:
        """
        Check if two equations are not equivalent.

        Parameters
        ----------
        other : Equation
            The equation to compare.

        Returns
        -------
        bool
            True if equations are not equivalent, False if they are equivalent.
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

        Notes
        -----
        The representation follows mathematical convention:
        - Positive terms: "+ coefficient xi"
        - Negative terms: "- |coefficient| xi"  
        - First term omits leading "+" sign
        - Constant term appears before "= 0

        Examples
        --------
        >>> eq = Equation(Fraction(2), Fraction(-3), Fraction(5))
        >>> str(eq)
        '2 x1 - 3 x2 + 5 = 0'
        """
        output: list[str] = []
        current_sign: str = ""

        # Process variables' coefficients without modifying object state
        for subscript, coefficient in enumerate(self.coefficients[:-1], 1):
            if coefficient.num < 0:
                current_sign = "-"
                coefficient = coefficient * -1
            output.append(f"{current_sign} {coefficient} x{subscript} ")
            current_sign = "+"
        
        # Process constant term without modifying object state
        constant_term: Fraction = self.coefficients[-1]
        if constant_term.num < 0:
            current_sign = "-"
            constant_term = constant_term * -1
            output.append(f"{current_sign} {constant_term} = 0")
        else:
            output.append(f"{current_sign} {constant_term} = 0")
        
        # Remove leading space from first term
        output[0] = output[0].lstrip()
        return "".join(output)

    def __repr__(self) -> str:
        """
        Return the formal string representation of the equation.

        Returns
        -------
        str
            Same format as __str__(), showing coefficients and variables.

        Notes
        -----
        For equations, __repr__ and __str__ provide the same output since
        the algebraic representation is both human-readable and unambiguous.
        """
        output: list[str] = []
        current_sign: str = ""

        # Process variables' coefficients without modifying object state
        for subscript, coefficient in enumerate(self.coefficients[:-1], 1):
            if coefficient.num < 0:
                current_sign = "-"
                coefficient = coefficient * -1
            output.append(f"{current_sign} {coefficient} x{subscript} ")
            current_sign = "+"
        
        # Process constant term without modifying object state
        constant_term: Fraction = self.coefficients[-1]
        if constant_term.num < 0:
            current_sign = "-"
            constant_term = constant_term * -1
            output.append(f"{current_sign} {constant_term} = 0")
        else:
            output.append(f"{current_sign} {constant_term} = 0")
        
        # Remove leading space from first term
        output[0] = output[0].lstrip()
        return "".join(output)

    def is_zero(self) -> bool:
        """
        Check if the equation is identically zero.

        Returns
        -------
        bool
            True if all coefficients are zero, False otherwise.
        
        Notes
        -----
        This is useful for detecting degenerate cases in linear system solving
        and for identifying equations that provide no information.

        Examples
        --------
        >>> eq1 = Equation(Fraction(2), Fraction(-1), Fraction(3))
        >>> eq1.is_zero()
        False

        >>> zero_eq = eq1 * 0  
        >>> zero_eq.is_zero()  
        True
        """
        return all(c == 0 for c in self.coefficients)


def are_coefficients_inconsistent(c1: Fraction, c2: Fraction, factor: Fraction) -> bool:
    """
    Check if two coefficients are inconsistent with a given scaling factor.

    This helper function determines whether two coefficients violate the
    requirement that one equation is a scalar multiple of another.

    Parameters
    ----------
    c1 : Fraction
        The first coefficient.
    c2 : Fraction
        The second coefficient.
    factor : Fraction
        The expected scaling factor relating c1 and c2.

    Returns
    -------
    bool
        True if the coefficients are inconsistent  (i.e. one is zero and the other is not, or
        they are not multiples of each other by the given factor). False otherwise
        (both zero or related by the factor).

    See Also
    --------
    Equation.__eq__ : Uses this function to check coefficient consistency

    Examples
    --------
    >>> from LinSysSolver.fraction import Fraction
    >>> # Consistent coefficients (factor = 1/2)
    >>> are_coefficients_inconsistent(Fraction(2), Fraction(4), Fraction(1, 2))
    False

    >>> # Inconsistent: one zero, other non-zero  
    >>> are_coefficients_inconsistent(Fraction(0), Fraction(5), Fraction(1))
    True

    >>> # Consistent: both zero
    >>> are_coefficients_inconsistent(Fraction(0), Fraction(0), Fraction(2))
    False

    >>> # Inconsistent: wrong ratio
    >>> are_coefficients_inconsistent(Fraction(3), Fraction(4), Fraction(1, 2))  
    True
    """
    # Case 1: One is zero, other is not (inconsistent)
    if (c1 == 0 and c2 != 0) or (c1 != 0 and c2 == 0):
        return True
    # Case 2: Both are zero (consistent)  
    elif c1 == 0 and c2 == 0:
        return False
    # Case 3: Both non-zero, check if ratio matches expected factor
    elif c1 / c2 == factor:
        return False  # Consistent
    else:
        return True   # Inconsistent ratio
