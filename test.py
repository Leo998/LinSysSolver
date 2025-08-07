import pytest

from fraction import Fraction

def test_0():
    f1: Fraction = Fraction(1)
    f2: Fraction = Fraction(2)

    assert f1 + f2 == 3


def test_divisionByZero():
    f1: Fraction = Fraction(1)
    f2: Fraction = Fraction(0)

    with pytest.raises(ZeroDivisionError):
        f1 / f2

def test_num_as_float():
    f1: Fraction = Fraction(2.3)

    assert f1.num == 23 and f1.den == 10

def test_num_as_float_simplified():
    f1: Fraction = Fraction(4.6)

    assert f1.num == 23 and f1.den == 5

def test_floatargument():
    f1: Fraction = Fraction(2.3)
    f2: Fraction = Fraction(23,10)
    assert f1 == f2

    