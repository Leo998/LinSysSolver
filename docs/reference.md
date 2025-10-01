# Reference Documentation

Complete technical reference for LinSysSolver architecture, classes, and methods.

## Table of Contents
1. [Program Architecture](#program-architecture)
2. [Module: fraction](#module-fraction)
3. [Module: equation](#module-equation)
4. [Module: system_eq](#module-system_eq)
5. [Command-Line Interface](#command-line-interface)

---

## Program Architecture

### Overview

LinSysSolver is structured as a Python package with four main components:

```
src/LinSysSolver/
├── fraction.py      # Exact rational arithmetic
├── equation.py      # Linear equation representation
├── system_eq.py     # System solver with Gaussian elimination
└── main.py          # CLI interface
```

### Design Philosophy

1. **Exact Arithmetic**: Uses `Fraction` class to avoid floating-point errors
2. **Educational Output**: Provides detailed step-by-step explanations
3. **Separation of Concerns**:
   - `Fraction`: Mathematical operations on rational numbers
   - `Equation`: Representation and operations on single equations
   - `SystemEq`: System-level operations and solving algorithm
   - `main`: User interface and I/O handling

---

## Module: fraction

### Class: `Fraction`

```python
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
```
##### Constructor

```Python
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
```

##### `simplify()` 
```python
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
```
##### `from_str(fraction_as_string)` (classmethod)
```python
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
```

#### Arithmetic Operations

```python
    def __add__(self, other: Union["Fraction", int, float]) -> "Fraction":
    def __radd__(self, other: int | float) -> "Fraction":
    def __sub__(self, other: Union["Fraction", int, float]) -> "Fraction":
    def __rsub__(self, other: int | float) -> "Fraction":
    def __mul__(self, other: Union["Fraction", int, float]) -> "Fraction":
    def __rmul__(self, other: int | float) -> "Fraction":
    def __truediv__(self, other: Union["Fraction", int, float]) -> "Fraction":
    def __rtruediv__(self, other: int | float) -> "Fraction":
    def __abs__(self) -> "Fraction":
```

**Examples:**
```python
Fraction(1, 2) + Fraction(1, 3)  # Fraction(5, 6)
Fraction(3, 4) + 2               # Fraction(11, 4)
1 + Fraction(1, 2)               # Fraction(3, 2)
Fraction(3, 4) - Fraction(1, 4)  # Fraction(1, 2)
Fraction(5, 2) - 2               # Fraction(1, 2)
3 - Fraction(1, 2)               # Fraction(5, 2)
Fraction(2, 3) * Fraction(3, 4)  # Fraction(1, 2)
Fraction(3, 4) * 2               # Fraction(3, 2)
2 * Fraction(3, 4)               # Fraction(3, 2)
Fraction(3, 4) / Fraction(2, 3)  # Fraction(9, 8)
Fraction(5, 2) / 2               # Fraction(5, 4)
3 / Fraction(2, 1)               # Fraction(3, 2)
abs(Fraction(-3, 4))   # Fraction(3, 4)
abs(Fraction(5, 2))    # Fraction(5, 2)
```

#### Comparison Operations

```python
    def __eq__(self, other: object | int | float) -> bool:
    def __ne__(self, other: object | int | float) -> bool:
    def __lt__(self, other: object | int | float) -> bool:
    def __gt__(self, other: object | int | float) -> bool:
    def __le__(self, other: object | int | float) -> bool:
    def __ge__(self, other: object | int | float) -> bool:
```

**Examples:**
```python
Fraction(1, 2) == Fraction(2, 4)  # True (both simplify to 1/2)
Fraction(1, 2) < Fraction(3, 4)   # True
Fraction(3, 2) > 1                # True
Fraction(1, 2) != 0.5             # False
```

#### String Representation

##### `__str__()`
```python
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
```

##### `__repr__()`
```python
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
```

---

## Module: equation

### Class: `Equation`

```Python
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
```

#### Constructor

```python
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
```

#### Methods

#### Arithmetic Operations

```python
    def __add__(self, other: "Equation") -> "Equation":
    def __sub__(self, other: "Equation") -> "Equation":
    def __mul__(self, other: Fraction | int | float) -> "Equation":
    def __rmul__(self, other: Fraction | int | float) -> "Equation":
    def __truediv__(self, other: Fraction | int | float) -> "Equation":
```

**Examples:**
```python
eq1 = Equation(Fraction(2), Fraction(-1), Fraction(3))
eq2 = Equation(Fraction(1), Fraction(2), Fraction(-1))
eq_sum = eq1 + eq2  # Equation(3, 1, 2)
print(eq_sum)  # "3 x1 + 1 x2 + 2 = 0"
eq = Equation(Fraction(2), Fraction(-3), Fraction(1))
scaled = eq * Fraction(1, 2)
print(scaled)  # "1 x1 - 3/2 x2 + 1/2 = 0"
eq = Equation(Fraction(4), Fraction(-2), Fraction(6))
divided = eq / 2
print(divided)  # "2 x1 - 1 x2 + 3 = 0"
```

#### Comparison Operations

##### Equality
```python
    def __eq__(self, other: object) -> bool:
    def __ne__(self, other: object) -> bool:
```

**Examples:**
```python
eq1 = Equation(Fraction(2), Fraction(-4), Fraction(6))
eq2 = Equation(Fraction(1), Fraction(-2), Fraction(3))
eq1 == eq2  # True (eq1 = 2 * eq2)
eq1 == Equation(Fraction(2), Fraction(-3), Fraction(6))  # False
```

#### Utility Methods

##### `is_zero()`
```python
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
```

#### String Representation

##### `__str__()` and `__repr__()`
```python
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
```

### Helper Function: `are_coefficients_inconsistent()`

```python
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
```

---

## Module: system_eq

### Class: `NumberedEquation`

```python
class NumberedEquation(NamedTuple):
    """
    Simple container for an Equation with a unique identifier.

    Attributes
    ----------
    equation_number : int
        Identifier of the equation (e.g. its index in the system).
    equation : Equation
        The equation object itself.
    """
```

### Class: `SystemEq`

```python
    Representation and solver for linear systems of equations.

    This class stores a set of Equation objects, wrapped as
    NumberedEquation for identification, and provides methods
    to reduce and solve the system using Gaussian elimination
    with partial pivoting.

    Parameters
    ----------
    *equations_list : Equation
        Variable number of Equation objects representing the system.

    Attributes
    ----------
    system : list of NumberedEquation
        List of equations with unique identifiers.
    num_coefficients : int
        Number of coefficients (including constant term) per equation.
    process_and_solutions: list of tuple
        Container for output flag and output strings
    Raises
    ------
    ValueError
        If the provided equations have different lengths.

    See Also
    --------
    Equation : Represents a single linear equation.
    Fraction : Rational number implementation used for exact arithmetic.

    Notes
    -----
    The solution process is pedagogical: each step prints explanatory
    messages about Gaussian elimination. For numerical work, prefer
    numpy.linalg.solve.

    References
    ----------
    .. [1] Gaussian elimination algorithm:
           https://en.wikipedia.org/wiki/Gaussian_elimination

    Examples
    --------
    >>> from LinSysSolver.fraction import Fraction
    >>> from LinSysSolver.equation import Equation
    >>> e1 = Equation(Fraction(2), Fraction(1), Fraction(-1))
    >>> e2 = Equation(Fraction(1), Fraction(-1), Fraction(3))
    >>> system = SystemEq(e1, e2)
    >>> system.__str__()
    'E1: 2 x1 + 1 x2 - 1 = 0\\nE2: 1 x1 - 1 x2 + 3 = 0\\n'
```

#### Constructor

```python
    def __init__(self, *equations_list: Equation):
        """
        **Parameters:**
            `*equations_list` : variable number of `Equation` objects

        Raises:
            `TypeError`: If no equations provided
            `ValueError`: If equations have different numbers of coefficients

        Examples:
            from LinSysSolver.system_eq import SystemEq
            from LinSysSolver.equation import Equation
            from LinSysSolver.fraction import Fraction

            eq1 = Equation(Fraction(2), Fraction(1), Fraction(-1))
            eq2 = Equation(Fraction(1), Fraction(-1), Fraction(3))
            system = SystemEq(eq1, eq2)
        """
```

#### Class Methods

##### `from_csv()`
```python
def from_csv(cls, filename: str) -> "SystemEq":
        """
        Build a system of equations from a CSV file.

        Parameters
        ----------
        filename : str
            Path to the CSV file. Each row represents an equation.

        Returns
        -------
        SystemEq
            New system of equations built from the file.
        """
```

#### Public Methods

##### `solve_system()`
```python
def solve_system(self, silent: bool = False) -> None:
        """
        Solve the system using Gaussian elimination.

        Applies forward elimination with pivoting, reduces the
        system to row-echelon form, and classifies the solution into:
        - Unique solution
        - No solution (inconsistent system)
        - Infinitely many solutions (underdetermined system)

        Notes
        -----
        Prints detailed step-by-step explanations for educational purposes.
        """
```

**Process:**
1. Minimize system (remove redundant equations and unused variables)
2. Forward elimination with pivoting
3. Row echelon form reduction
4. Solution classification and presentation


##### `__str__()`
```python
def __str__(self) -> str:
        """
        String representation of the system.

        Returns
        -------
        str
            Human-readable string showing all equations with identifiers.
        """
```

#### Private Methods

These methods are used internally by `solve_system()`:

##### `_minimize_system(silent: bool = False)`
Remove redundant equations and unused variables.

##### `_check_unused_unknowns(silent: bool = False)`
Detect and remove variables with all-zero coefficients.

##### `_sort_by_abs_coeff(from_row: int = 0, column: int = 0, reverse: bool = True)`
Sort equations by absolute value of coefficient (partial pivoting).

##### `_zeroes_pivot_column(pivot_row: int, pivot_column: int, silent: bool = False)`
Eliminate pivot column below and above pivot row.

##### `_del_equation_if_zero(eq_number: int)`
Remove equation if all coefficients are zero.

##### `_no_solution()`
Print message when system has no solution.

##### `_unique_solution()`
Print the unique solution.

##### `_infinitely_many_solutions()`
Print parametric solution for underdetermined systems.

---

## Command-Line Interface

### Synopsis

```bash
LinSysSolver [-h] [-s] [--version] FILE
```

### Arguments

**Positional:**

`FILE`
- Path to CSV file containing the system
- Required

**Optional:**

`-h, --help`
- Show help message and exit

`-s, --silent`
- Print only solution without step-by-step explanation
- Default: `False`

`--version`
- Show program version number and exit

### Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Error (file not found, invalid CSV, etc.) |

## Usage Examples

### Example 1: Programmatic Use

```python
from LinSysSolver.system_eq import SystemEq
from LinSysSolver.equation import Equation
from LinSysSolver.fraction import Fraction

# Create equations manually
eq1 = Equation(Fraction(2), Fraction(3), Fraction(-5))
eq2 = Equation(Fraction(1), Fraction(-1), Fraction(-1))

# Create system
system = SystemEq(eq1, eq2)

# Solve with full output
system.solve_system(silent=False)

# Or solve silently
system.solve_system(silent=True)
```

### Example 2: From CSV File

```python
from LinSysSolver.system_eq import SystemEq

# Load from CSV
system = SystemEq.from_csv("my_system.csv")

# Solve
system.solve_system()
```

### Example 3: Working with Fractions

```python
from LinSysSolver.fraction import Fraction

# Create fractions
f1 = Fraction("3/4")
f2 = Fraction(0.5)
f3 = Fraction(2, 3)

# Arithmetic
result = f1 + f2      # Fraction(5, 4)
result = f1 * f2      # Fraction(3, 8)
result = f1 / f2      # Fraction(3, 2)

# Comparisons
f1 > f2               # True
f1 == Fraction(3, 4)  # True

# Convert to float if needed
float(f1)             # 0.75
```

---

For practical usage examples, see [Tutorial/How-to](tutorial-how-to.md).  
For theoretical background, see [Explanation](explanation.md)  
For complete docstrings for every method/function see source code.