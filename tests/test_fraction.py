import pytest

from LinSysSolver.fraction import Fraction


def test_int_init() -> None:
    """
    Tests constructor with no argument or int arguments

    Given a Fraction initialized with integers or no arguments,
    When the object is created,
    Then it should:
    - Default to 0/1 when no arguments are provided.
    - Correctly store the provided integer numerator and denominator.
    - Default denominator to 1 when only numerator is provided.
    - Raise ZeroDivisionError if denominator is zero.
    """
    default_fraction = Fraction()
    assert default_fraction  == 0
    assert default_fraction.den == 1

    integer_fraction = Fraction(27, 13)
    assert integer_fraction.num == 27 and integer_fraction.den == 13

    single_arg_fraction = Fraction(5)
    assert single_arg_fraction == 5
    assert single_arg_fraction.num == 5 and single_arg_fraction.den == 1

    with pytest.raises(ZeroDivisionError):
        _ = Fraction(1, 0)


def test_float_init() -> None:
    """
    Tests constructor with float arguments

    Given a Fraction initialized with float values,
    When the object is created,
    Then it should:
    - Convert single float numerators to exact fractions.
    - Handle scientific notation floats.
    - Convert two float arguments correctly.
    - Handle mix of integer and float numerator or denominator.
    """
    decimal_fraction = Fraction(2.8)
    assert decimal_fraction.num == 14 and decimal_fraction.den == 5

    scientific_notation = Fraction(1.1e-1)
    assert scientific_notation.num == 11 and scientific_notation.den == 100

    mixed_float_args = Fraction(20.9, 5.5)
    assert mixed_float_args.num == 19 and mixed_float_args.den == 5

    int_float_mix = Fraction(5, 1.25)
    assert int_float_mix == 4


def test_string_init() -> None:
    """
    Tests constructor with string arguments

    Given a Fraction initialized with a string,
    When the object is created,
    Then it should:
    - Parse integer strings into numerator/1.
    - Parse "a/b" strings into numerator and denominator.
    - Parse float strings into correct exact fractions.
    - Raise ValueError if the string format is invalid 
      (e.g. contains floats in fraction form).

    Notes
    -----
    The ValueError for "19.2/6" tests the design principle that mixed
    float/fraction notation is prohibited to maintain parsing clarity.
    """
    integer_string = Fraction("3")
    assert integer_string .num == 3 and integer_string .den == 1

    fraction_string = Fraction("19/6")
    assert fraction_string .num == 19 and fraction_string .den == 6

    decimal_string = Fraction("19.6")
    assert decimal_string.num == 98 and decimal_string.den == 5

    with pytest.raises(ValueError):
        _ = Fraction("19.2/6")



def test_simplify() -> None:
    """
    Tests simplify method

    Given a Fraction with a numerator and denominator not in lowest terms,
    When simplify() is called,
    Then it should:
    - Reduce the fraction to its simplest form.
    - Move any negative sign to the numerator.
    """
    test_fraction = Fraction()
    test_fraction.num = 15
    test_fraction.den = -10
    test_fraction.simplify()
    assert test_fraction.num == -3 and test_fraction.den == 2


def test_add() -> None:
    """
    Tests add and radd methods

    Given two Fractions, or a Fraction and an int or float,
    When they are added,
    Then the result should:
    - Be their mathematically correct sum as a simplified Fraction.
    - Support commutative addition (a + b = b + a).
    - Handle mixed types (Fraction + int/float).
    - Automatically reduce the result to lowest terms.
    """
    positive_fraction = Fraction(5, 4)
    negative_fraction = Fraction(3, -2)
    assert positive_fraction + negative_fraction == Fraction(-1, 4)
    assert positive_fraction + 1 == Fraction (9, 4)
    assert negative_fraction + 1.5 == Fraction() # Tests: -3/2 + 3/2 = 0
    assert 1.5 + negative_fraction == Fraction() # Tests commutativity via __radd__


def test_sub() -> None:
    """
    Tests sub and rsub methods

    Given two Fractions, or a Fraction and an int or float,
    When one is subtracted from the other,
    Then the result should:
    - Be their mathematically correct difference as a simplified Fraction.
    - Support both left and right subtraction (a - b and b - a).
    - Handle mixed types correctly.
    - Automatically reduce the result to lowest terms.
    """
    minuend_fraction = Fraction(5, 4)
    subtrahend_fraction = Fraction(3, -2)
    assert minuend_fraction - subtrahend_fraction == Fraction(11, 4)
    assert minuend_fraction - 1 == Fraction(1, 4)
    assert subtrahend_fraction - 1.5 == Fraction(-3, 1)
    assert 2.5 - subtrahend_fraction == 4


def test_mul() -> None:
    """
    Tests mul and rmul methods

    Given two Fractions, or a Fraction and an int or float,
    When they are multiplied,
    Then the result should:
    - Be their mathematically correct product as a simplified Fraction.
    - Support commutative multiplication (a * b = b * a).
    - Handle mixed types correctly.
    - Automatically reduce the result to lowest terms.
    """
    f1 = Fraction(5, 4)
    f2 = Fraction(3, -2)
    assert f1 * f2 == Fraction(-15, 8)
    assert f1 * 2 == Fraction(5, 2)
    assert 2 * f1 == Fraction(5, 2)
    assert f2 * 0.5 == Fraction(-3, 4)
    assert 1.5 * f1 == Fraction(15, 8)


def test_truediv() -> None:
    """
    Tests truediv and rtruediv methods

    Given two Fractions, or a Fraction and an int or float,
    When one is divided by the other,
    Then the result should:
    - Be their mathematically correct quotient as a simplified Fraction.
    - Support both left and right division operations.
    - Handle mixed types correctly.
    - Automatically reduce the result to lowest terms.    
    """
    dividend_fraction = Fraction(5, 4)
    divisor_fraction = Fraction(3, -2)
    assert Fraction(-10, 12) == dividend_fraction / divisor_fraction
    assert Fraction(5, 8) == dividend_fraction / 2
    assert Fraction(5, 6) == dividend_fraction / 1.5
    assert Fraction(-5, 3) == 2.5 / divisor_fraction
    assert dividend_fraction / divisor_fraction == Fraction(-10, 12)


def test_divisionByZero() -> None:
    """
    Tests division by zero

    Given two Fractions where the divisor has a zero numerator,
    When a division is attempted,
    Then a ZeroDivisionError should be raised.
    """
    non_zero_fraction = Fraction(1)
    zero_fraction = Fraction(0)
    with pytest.raises(ZeroDivisionError):
        non_zero_fraction / zero_fraction
    with pytest.raises(ZeroDivisionError):
        3.2 / zero_fraction
    
def test_abs() -> None:
    """
    Tests abs method

    Given a Fraction,
    When abs() is called,
    Then it should:
    - Return a new Fraction with a non-negative numerator.
    - Preserve the denominator.
    - Be mathematically equal to the absolute value of the fraction.
    - Not modify the original fraction (immutable operation).
    """
    negative_num_neg_den = Fraction(-2, -4)
    negative_fraction = Fraction(-1, 3)
    product_fraction = negative_num_neg_den * negative_fraction
    assert abs(negative_num_neg_den) == 0.5
    assert abs(negative_fraction) == Fraction(1, 3)
    assert abs(product_fraction) == Fraction(1, 6)

def test_eq_ne() -> None:
    """
    Tests eq and ne methods

    Given Fractions and integers or floats,
    When equality and inequality comparisons are made,
    Then they should:
    - Return True for equal values.
    - Return False for unequal values.
    - Handle cross-type comparisons (Fraction vs int/float).
    - Raise TypeError for unsupported types.
    """
    assert Fraction(2, 4) == Fraction (4, 8)
    assert Fraction(2, 4) != Fraction (4, 7)
    assert Fraction(2, 4) == 0.5
    assert Fraction(8, 2) == 4
    assert Fraction(4, 2) != 1
    assert 2.5 == Fraction(5, 2)  # Test __eq__ symmetry

    with pytest.raises(TypeError):
        Fraction(2, 4) == "0.5"   # String comparison invalid

def test_lt_eq() -> None:
    """
    Tests lt and le methods

    Given two Fractions or a Fraction compared with a numeric type,
    When the less-than operator (<) is used,
    Then it should:
    - Return True if the first value is mathematically smaller.
    - Support comparison with int and float values.
    - Raise an AttributeError if the type is unsupported.
    """
    f1 = Fraction(-2, -4)
    f2 = Fraction(-1, 3)
    assert f2 < f1
    assert 0 < f1
    assert -0.6 < f2
    assert 0.5 <= f1

    with pytest.raises(TypeError):
        f1 < "ciao"

def test_gt_eq() -> None:
    """
    Tests gt and ge methods

    Given two Fractions or a Fraction compared with a numeric type,
    When the greater-than operator (>) is used,
    Then it should:
    - Return True if the first value is mathematically greater.
    - Support comparison with int and float values.
    - Raise an AttributeError if the type is unsupported.
    """
    f1 = Fraction(-2, -4)
    f2 = Fraction(-1, 3)
    assert f1 > f2
    assert f1 > -1
    assert -0.1 > f2
    assert 0.5 >= f1

    with pytest.raises(TypeError):
        f1 > "ciao"

def test_str() -> None:
    """
    Tests str method

    Given a Fraction,
    When __str__() is called,
    Then it should:
    - Return "numerator/denominator" when denominator is not 1.
    - Return only the numerator when denominator is 1.
    - Properly display negative values with correct sign placement.
    - Provide human-readable representation suitable for print().
    """
    f1 = Fraction(7,8)
    assert f1.__str__() == "7/8"

    f2 = Fraction(5, 1)
    assert f2.__str__() == "5"
    
    f2 = Fraction(5, -1)  # Becomes -5/1 after simplification
    assert f2.__str__() == "-5"

def test_repr() -> None:
    """
    Tests repr method

    Given a Fraction,
    When __repr__() is called,
    Then it should:
    - Return the exact constructor-style representation.
    - Provide unambiguous debugging information.
    """
    f1 = Fraction(7,8)
    assert f1.__repr__() == "Fraction(7, 8)"
