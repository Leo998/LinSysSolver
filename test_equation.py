import pytest

from fraction import Fraction
from equation import Equation

def test_init():
    e1 = Equation([Fraction(2, 4), Fraction(1), Fraction(2.8)])
    assert e1.coefficients[0] == Fraction(1, 2)
    assert e1.coefficients[1] == Fraction(-1, -1)
    assert e1.coefficients[2] == Fraction(2.8, 1)
    with pytest.raises(ValueError):
        Equation([Fraction(-5, 2)])
    

def test_add():
    e1 = Equation([Fraction(2, 4), Fraction(1), Fraction(2.8)])
    e2 = Equation([Fraction(1, 4), Fraction(-2), Fraction(2.3)])
    e3 = Equation([Fraction(3, 4), Fraction(-1), Fraction(51, 10)])
    e4 = Equation([Fraction(1, 4), Fraction(-2)])
    assert e1 + e2 == e3
    with pytest.raises(ValueError):
        e1 + e4
        
def test_sub():
    e1 = Equation([Fraction(2, 4), Fraction(1), Fraction(2.8)])
    e2 = Equation([Fraction(1, 4), Fraction(-2), Fraction(2.3)])
    e3 = Equation([Fraction(1, 4), Fraction(3), Fraction(1, 2)])
    e4 = Equation([Fraction(1, 4), Fraction(-2)])
    assert e1 - e2 == e3
    with pytest.raises(ValueError):
        e1 - e4

def test_mul():
    e1 = Equation([Fraction(2, 4), Fraction(1), Fraction(2.8)])
    f1 = Fraction(1 , 2)
    e3 = Equation([Fraction(1, 4), Fraction(0.5), Fraction(7, 5)])
    assert e1 * f1 == e3
    assert e1 * 0.5 == e3
    assert e1 * 1 == e1
    assert 2.5 * e3 == Equation([Fraction(5, 8), Fraction(5, 4), Fraction(7, 2)])

def test_truediv():
    e1 = Equation([Fraction(2, 4), Fraction(1), Fraction(2.8)])
    f1 = Fraction(1 , 2)
    e3 = Equation([Fraction(1), Fraction(2), Fraction(28, 5)])
    assert e1 / f1 == e3
    assert e1 / 3 == Equation([Fraction(1, 6), Fraction(1, 3), Fraction(14, 15)])
    assert e3 / 1.5 == Equation([Fraction(2, 3), Fraction(4, 3), Fraction(56, 15)])

def test_eq_ne():
    e1 = Equation([Fraction(2, 4), Fraction(1), Fraction(2.8)])
    e2 = Equation([Fraction(2, 4), Fraction(-1), Fraction(2.8)])
    e3 = Equation([Fraction(1, 2), Fraction(5, 5), Fraction(5.6, 2)])
    e4 = Equation([Fraction(1, 4), Fraction(-2)])
    assert e1 == e3
    assert e1 != e2
    with pytest.raises(ValueError):
        e1 == e4

def test_is_zero():
    e1 = Equation([Fraction(2, 4), Fraction(1), Fraction(2.8)])
    e2 = e1 * 0
    assert not e1.is_zero()
    assert e2.is_zero()

def test_str():
    e1 = Equation([Fraction(1, 2), Fraction(5, 5), Fraction(5.4, -2)])
    e2 = Equation([Fraction(-2, 5), Fraction(-1), Fraction(2.8)])
    assert e1.__str__() == "1/2 x1 + 1 x2 - 27/10 = 0"
    assert e2.__str__() == "- 2/5 x1 - 1 x2 + 14/5 = 0"

def test_repr():
    e1 = Equation([Fraction(1, 2), Fraction(5, 5), Fraction(5.4, -2)])
    e2 = Equation([Fraction(-2, 5), Fraction(-1), Fraction(2.8)])
    assert e1.__repr__() == "1/2 x1 + 1 x2 - 27/10 = 0"
    assert e2.__repr__() == "- 2/5 x1 - 1 x2 + 14/5 = 0"