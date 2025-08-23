import pytest

from fraction import Fraction
from equation import Equation

def test_init():
    """
    Given a list of Fraction coefficients,
    When an Equation is initialized,
    Then it should:
    - Store the coefficients in simplified Fraction form.
    - Raise ValueError if fewer than two coefficients are provided.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    assert e1.coefficients[0] == Fraction(1, 2)
    assert e1.coefficients[1] == Fraction(-1, -1)
    assert e1.coefficients[2] == Fraction(2.8, 1)
    with pytest.raises(ValueError):
        Equation([Fraction(-5, 2)])
    

def test_add():
    """
    Given two Equations with the same number of coefficients,
    When they are added,
    Then the result should be a new Equation whose coefficients
    are the term-by-term sum.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    e2 = Equation(Fraction(1, 4), Fraction(-2), Fraction(2.3))
    e3 = Equation(Fraction(3, 4), Fraction(-1), Fraction(51, 10))
    assert e1 + e2 == e3
        
def test_sub():
    """
    Given two Equations with the same number of coefficients,
    When one is subtracted from the other,
    Then the result should be a new Equation whose coefficients
    are the term-by-term difference.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    e2 = Equation(Fraction(1, 4), Fraction(-2), Fraction(2.3))
    e3 = Equation(Fraction(1, 4), Fraction(3), Fraction(1, 2))
    assert e1 - e2 == e3

def test_mul():
    """
    Given an Equation and a scalar (Fraction, int, or float),
    When multiplied,
    Then the result should be a new Equation with each coefficient scaled
    by that scalar.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    f1 = Fraction(1 , 2)
    e3 = Equation(Fraction(1, 4), Fraction(0.5), Fraction(7, 5))
    assert e1 * f1 == e3
    assert e1 * 0.5 == e3
    assert e1 * 1 == e1
    assert Fraction(5, 2) * e3 == Equation(Fraction(5, 8), Fraction(5, 4), Fraction(7, 2))
    assert 2.5 * e3 == Equation(Fraction(5, 8), Fraction(5, 4), Fraction(7, 2))

def test_truediv():
    """
    Given an Equation and a scalar (Fraction, int, or float),
    When divided,
    Then the result should be a new Equation with each coefficient divided
    by that scalar.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    f1 = Fraction(1 , 2)
    e3 = Equation(Fraction(1), Fraction(2), Fraction(28, 5))
    assert e1 / f1 == e3
    assert e1 / 3 == Equation(Fraction(1, 6), Fraction(1, 3), Fraction(14, 15))
    assert e3 / 1.5 == Equation(Fraction(2, 3), Fraction(4, 3), Fraction(56, 15))

def test_diff_lenght():
    """
    Given two Equations with different numbers of coefficients,
    When addition is attempted,
    Then a ValueError should be raised.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    e2 = Equation(Fraction(1, 4), Fraction(-2))
    with pytest.raises(ValueError):
        e1 + e2
    with pytest.raises(ValueError):
        e1 - e2
    
def test_eq_ne():
    """
    Given two Equations,
    When equality or inequality is checked,
    Then it should:
    - Return True if all coefficients are equal.
    - Return False if any coefficient differs.
    - Raise ValueError if the Equations have different number of coefficients.
    - Raise TypeError for unsupported types.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    e2 = Equation(Fraction(2, 4), Fraction(-1), Fraction(2.8))
    e3 = Equation(Fraction(1, 2), Fraction(5, 5), Fraction(5.6, 2))
    e4 = Equation(Fraction(1, 4), Fraction(-2))
    assert e1 == e3
    assert e1 != e2
    with pytest.raises(ValueError):
        e1 == e4
    with pytest.raises(TypeError):
        e1 == 5

def test_eq_with_multiple():
    """
    Given two Equations,
    When equality is checked,
    Then it should:
    - Return True if both are the zero equation.
    - Return False if their coefficients cannot be made equal
      by a common scalar factor.
    - Return True if their coefficients are consistent with
      the same scalar factor (i.e. one equation is a multiple of the other).
    """
    e01 = Equation(Fraction(0), Fraction(0), Fraction(0))
    e02 = Equation(Fraction(0), Fraction(0), Fraction(0))
    assert e01 == e02
    e1 = Equation(Fraction(0), Fraction(20), Fraction(0))
    e2 = Equation(Fraction(5.3), Fraction(0), Fraction(-6, 4))
    assert e1 != e2
    e3 = Equation(Fraction(0), Fraction(5.5), Fraction(-16, 2))
    e4 = Equation(Fraction(0), Fraction(7.15), Fraction(-10.4))
    assert e3 == e4

def test_is_zero():
    """
    Given an Equation,
    When is_zero() is called,
    Then it should:
    - Return True if all coefficients are zero.
    - Return False otherwise.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    e2 = e1 * 0
    assert not e1.is_zero()
    assert e2.is_zero()

def test_str():
    """
    Given an Equation,
    When __str__() is called,
    Then it should:
    - Display each term with its sign and variable index.
    - Show the constant term before "= 0".
    - Move negative signs to the term's sign instead of the numerator.
    """
    e1 = Equation(Fraction(1, 2), Fraction(5, 5), Fraction(5.4, -2))
    e2 = Equation(Fraction(-2, 5), Fraction(-1), Fraction(2.8))
    assert e1.__str__() == "1/2 x1 + 1 x2 - 27/10 = 0"
    assert e2.__str__() == "- 2/5 x1 - 1 x2 + 14/5 = 0"

def test_repr():
    """
    Given an Equation,
    When __repr__() is called,
    Then it should return the same formatted string as __str__().
    """
    e1 = Equation(Fraction(1, 2), Fraction(5, 5), Fraction(5.4, -2))
    e2 = Equation(Fraction(-2, 5), Fraction(-1), Fraction(2.8))
    assert e1.__repr__() == "1/2 x1 + 1 x2 - 27/10 = 0"
    assert e2.__repr__() == "- 2/5 x1 - 1 x2 + 14/5 = 0"