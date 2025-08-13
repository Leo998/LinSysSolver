import pytest

from fraction import Fraction


def test_int_init():
    """
    Given a Fraction initialized with integers or no arguments,
    When the object is created,
    Then it should:
    - Default to 0/1 when no arguments are provided.
    - Correctly store the provided integer numerator and denominator.
    - Default denominator to 1 when only numerator is provided.
    - Raise ZeroDivisionError if denominator is zero.
    """
    f1 = Fraction()
    assert f1 == 0
    assert f1.den == 1

    f2 = Fraction(27, 13)
    assert f2.num == 27 and f2.den == 13

    f3 = Fraction(5)
    assert f3 == 5
    assert f3.num == 5 and f3.den == 1

    with pytest.raises(ZeroDivisionError):
        _ = Fraction(1, 0)


def test_float_init():
    """
    Given a Fraction initialized with float values,
    When the object is created,
    Then it should:
    - Convert single float numerators to exact fractions.
    - Handle scientific notation floats.
    - Convert two float arguments correctly.
    - Handle mix of integer and float numerator or denominator.
    """
    f1 = Fraction(2.8)
    assert f1.num == 14 and f1.den == 5

    f2 = Fraction(1.1e-1)
    assert f2.num == 11 and f2.den == 100

    f3 = Fraction(20.9, 5.5)
    assert f3.num == 19 and f3.den == 5

    f4 = Fraction(5, 1.25)
    assert f4 == 4


def test_string_init():
    """
    Given a Fraction initialized with a string,
    When the object is created,
    Then it should:
    - Parse integer strings into numerator/1.
    - Parse "a/b" strings into numerator and denominator.
    - Raise ValueError if the string format is invalid (e.g. contains floats).
    """
    f1 = Fraction("3")
    assert f1.num == 3 and f1.den == 1

    f2 = Fraction("19/6")
    assert f2.num == 19 and f2.den == 6

    with pytest.raises(ValueError):
        _ = Fraction("19.2/6")



def test_simplify():
    """
    Given a Fraction with a numerator and denominator not in lowest terms,
    When simplify() is called,
    Then it should:
    - Reduce the fraction to its simplest form.
    - Move any negative sign to the numerator.
    """
    f1 = Fraction()
    f1.num = 15
    f1.den = -10
    f1.simplify()
    assert f1.num == -3 and f1.den == 2


def test_add():
    """
    Given two Fractions,
    When they are added,
    Then the result should be their correct sum as a simplified Fraction.
    """
    f1 = Fraction(5, 4)
    f2 = Fraction(3, -2)
    assert f1 + f2 == Fraction(-1, 4)


def test_sub():
    """
    Given two Fractions,
    When one is subtracted from the other,
    Then the result should be their correct difference as a simplified Fraction.
    """
    f1 = Fraction(5, 4)
    f2 = Fraction(3, -2)
    assert f1 - f2 == Fraction(11, 4)


def test_mul():
    """
    Given two Fractions,
    When they are multiplied,
    Then the result should be their correct product as a simplified Fraction.
    """
    f1 = Fraction(5, 4)
    f2 = Fraction(3, -2)
    assert f1 * f2 == Fraction(-15, 8)


def test_truediv():
    """
    Given two Fractions,
    When one is divided by the other,
    Then the result should be their correct quotient as a simplified Fraction.
    """
    f1 = Fraction(5, 4)
    f2 = Fraction(3, -2)
    assert Fraction(-10, 12) == f1 / f2
    assert f1 / f2 == Fraction(-10, 12)


def test_divisionByZero():
    """
    Given two Fractions where the divisor has a zero numerator,
    When a division is attempted,
    Then a ZeroDivisionError should be raised.
    """
    f1 = Fraction(1)
    f2 = Fraction(0)
    with pytest.raises(ZeroDivisionError):
        f1 / f2

def test_eq_ne():
    """
    Given Fractions and integers,
    When equality and inequality comparisons are made,
    Then they should:
    - Return True for equal values.
    - Return False for unequal values.
    - Raise TypeError for unsupported types.
    """
    assert Fraction(2, 4) == Fraction (4, 8)
    assert Fraction(2, 4) != Fraction (4, 7)
    assert Fraction(8, 2) == 4
    assert Fraction(4, 2) != 1
    with pytest.raises(TypeError):
        Fraction(2, 4) == 0.5

def test_str():
    """
    Given a Fraction,
    When __str__() is called,
    Then it should:
    - Return 'numerator/denominator' when denominator is not 1.
    - Return only the numerator when denominator is 1.
    - Properly display negative values.
    """
    f1 = Fraction(7,8)
    assert f1.__str__() == "7/8"
    f2 = Fraction(5, 1)
    assert f2.__str__() == "5"
    f2 = Fraction(5, -1)
    assert f2.__str__() == "-5"

def test_repr():
    """
    Given a Fraction,
    When __repr__() is called,
    Then it should return the exact constructor-style representation.
    """
    f1 = Fraction(7,8)
    assert f1.__repr__() == "Fraction(7, 8)"
