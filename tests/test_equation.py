import pytest

from LinSysSolver.fraction import Fraction
from LinSysSolver.equation import Equation

def test_init() -> None:
    """
    Tests constructor (also with not enough arguments)

    Given a list of Fraction coefficients,
    When an Equation is initialized,
    Then it should:
    - Store the coefficients in simplified Fraction form.
    - Raise ValueError if fewer than two coefficients are provided.
    """
    test_equation = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    assert test_equation.coefficients[0] == Fraction(1, 2)
    assert test_equation.coefficients[1] == Fraction(-1, -1)
    assert test_equation.coefficients[2] == Fraction(2.8, 1)
    with pytest.raises(ValueError):
        Equation(Fraction(-5, 2))
    

def test_add() -> None:
    """
    Tests add method

    Given two Equations with the same number of coefficients,
    When they are added,
    Then the result should be a new Equation whose coefficients
    are the term-by-term sum.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    e2 = Equation(Fraction(1, 4), Fraction(-2), Fraction(2.3))
    expected_sum = Equation(Fraction(3, 4), Fraction(-1), Fraction(51, 10))
    assert e1 + e2 == expected_sum
        
def test_sub() -> None:
    """
    Tests sub method

    Given two Equations with the same number of coefficients,
    When one is subtracted from the other,
    Then the result should be a new Equation whose coefficients
    are the term-by-term difference.
    """
    e1 = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    e2 = Equation(Fraction(1, 4), Fraction(-2), Fraction(2.3))
    expected_difference = Equation(Fraction(1, 4), Fraction(3), Fraction(1, 2))
    assert e1 - e2 == expected_difference

def test_mul() -> None:
    """
    Tests mul and rmul methods

    Given an Equation and a scalar (Fraction, int, or float),
    When multiplied,
    Then the result should be a new Equation with each coefficient scaled
    by that scalar.
    """
    base_equation = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    scalar_fraction = Fraction(1 , 2)
    expected_scaled = Equation(Fraction(1, 4), Fraction(0.5), Fraction(7, 5))
    assert base_equation * scalar_fraction == expected_scaled
    assert base_equation * 0.5 == expected_scaled
    assert base_equation * 1 == base_equation
    assert Fraction(5, 2) * expected_scaled == Equation(Fraction(5, 8), Fraction(5, 4), Fraction(7, 2))
    assert 2.5 * expected_scaled == Equation(Fraction(5, 8), Fraction(5, 4), Fraction(7, 2))

def test_truediv() -> None:
    """
    Tests truediv method (also with division by zero)

    Given an Equation and a scalar (Fraction, int, or float),
    When divided,
    Then the result should be a new Equation with each coefficient divided
    by that scalar.
    """
    dividend_equation = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    divisor_scalar = Fraction(1 , 2)
    expected_quotient = Equation(Fraction(1), Fraction(2), Fraction(28, 5))
    zero_fraction = Fraction(0)
    assert dividend_equation / divisor_scalar == expected_quotient
    assert dividend_equation / 3 == Equation(Fraction(1, 6), Fraction(1, 3), Fraction(14, 15))
    assert expected_quotient / 1.5 == Equation(Fraction(2, 3), Fraction(4, 3), Fraction(56, 15))
    with pytest.raises(ZeroDivisionError):
        dividend_equation / zero_fraction

def test_diff_lenght() -> None:
    """
    Tests operations between equation of different lenght

    Given two Equations with different numbers of coefficients,
    When addition is attempted,
    Then a ValueError should be raised.
    """
    three_coeff_equation = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    two_coeff_equation = Equation(Fraction(1, 4), Fraction(-2))
    with pytest.raises(ValueError):
        three_coeff_equation + two_coeff_equation
    with pytest.raises(ValueError):
        three_coeff_equation - two_coeff_equation
    with pytest.raises(ValueError):
        three_coeff_equation == two_coeff_equation
    
def test_eq_ne() -> None:
    """
    Tests eq and ne methods (also with unsupported types)

    Given two Equations,
    When equality or inequality is checked,
    Then it should:
    - Return True if all coefficients are equal.
    - Return False if any coefficient differs.
    - Raise ValueError if the Equations have different number of coefficients.
    - Raise TypeError for unsupported types.
    """
    base_equation = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    different_equation = Equation(Fraction(2, 4), Fraction(-1), Fraction(2.8))
    equivalent_equation = Equation(Fraction(1, 2), Fraction(5, 5), Fraction(5.6, 2))
    incompatible_equation = Equation(Fraction(1, 4), Fraction(-2))
    assert base_equation == equivalent_equation
    assert base_equation != different_equation
    with pytest.raises(TypeError):
        base_equation == 5

def test_eq_with_multiple() -> None:
    """
    Tests eq and ne methods for equivalent (not equal) equations

    Given two Equations,
    When equality is checked,
    Then it should:
    - Return True if both are the zero equation.
    - Return False if their coefficients cannot be made equal
      by a common scalar factor.
    - Return True if their coefficients are consistent with
      the same scalar factor (i.e. one equation is a multiple of the other).
    """
    zero_equation_1 = Equation(Fraction(0), Fraction(0), Fraction(0))
    zero_equation_2 = Equation(Fraction(0), Fraction(0), Fraction(0))
    assert zero_equation_1 == zero_equation_2
    partial_zero_equation_1 = Equation(Fraction(0), Fraction(20), Fraction(0))
    partial_zero_equation_2 = Equation(Fraction(5.3), Fraction(0), Fraction(-6, 4))
    assert partial_zero_equation_1 != partial_zero_equation_2
    proportional_equation_1 = Equation(Fraction(0), Fraction(5.5), Fraction(-16, 2))
    proportional_equation_2 = Equation(Fraction(0), Fraction(7.15), Fraction(-10.4))
    assert proportional_equation_1 == proportional_equation_2

def test_is_zero() -> None:
    """
    Tests is_zero method

    Given an Equation,
    When is_zero() is called,
    Then it should:
    - Return True if all coefficients are zero.
    - Return False otherwise.
    """
    non_zero_equation = Equation(Fraction(2, 4), Fraction(1), Fraction(2.8))
    zero_equation = non_zero_equation * 0
    assert not non_zero_equation.is_zero()
    assert zero_equation.is_zero()

def test_str() -> None:
    """
    Tests str method

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

def test_repr() -> None:
    """
    Tests repr method

    Given an Equation,
    When __repr__() is called,
    Then it should return the same formatted string as __str__().
    """
    e1 = Equation(Fraction(1, 2), Fraction(5, 5), Fraction(5.4, -2))
    e2 = Equation(Fraction(-2, 5), Fraction(-1), Fraction(2.8))
    assert e1.__repr__() == "1/2 x1 + 1 x2 - 27/10 = 0"
    assert e2.__repr__() == "- 2/5 x1 - 1 x2 + 14/5 = 0"