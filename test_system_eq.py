import pytest

from fraction import Fraction
from equation import Equation
from system_eq import NumberedEquation, SystemEq

def test_init():
    with pytest.raises(TypeError):
        SystemEq.from_csv("csv_files/empty.csv")
    s1 = SystemEq.from_csv("csv_files/system.csv")
    assert s1.num_coefficients == 4
    assert s1.system[2].equation_number == 3
    with pytest.raises(ValueError):
        SystemEq.from_csv("csv_files/unpaired1.csv")
    with pytest.raises(ValueError):
        SystemEq.from_csv("csv_files/unpaired2.csv")
    with pytest.raises(ValueError):
        SystemEq.from_csv("csv_files/unpaired3.csv")
 
def test_str():
    s1 = SystemEq.from_csv("csv_files/system.csv")
    assert s1.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""

def test_del_eq_if_zero():
    s1 = SystemEq.from_csv("csv_files/row_all_zero.csv")
    s1._del_equation_if_zero(0)
    assert s1.system[0].equation == Equation(Fraction(5.3), Fraction(-2), Fraction(3), Fraction(8.8))
    assert s1.system[0].equation_number == 1
    assert s1.system[1].equation == Equation(Fraction(), Fraction(), Fraction(), Fraction())
    assert s1.system[1].equation_number == 2
    assert s1.system[2].equation == Equation(Fraction(1), Fraction(-5, 3), Fraction(6.2), Fraction(4))
    assert s1.system[2].equation_number == 3
    s1._del_equation_if_zero(1)
    assert s1.system[1].equation == Equation(Fraction(1), Fraction(-5, 3), Fraction(6.2), Fraction(4))
    assert s1.system[1].equation_number == 3
    with pytest.raises(IndexError):
        s1.system[2].equation
    assert s1.system[0].equation == Equation(Fraction(5.3), Fraction(-2), Fraction(3), Fraction(8.8))
    assert s1.system[0].equation_number == 1

def test_unused_unknowns():
    s1 = SystemEq.from_csv("csv_files/unused_unknowns.csv")
    s2 = SystemEq.from_csv("csv_files/system.csv")
    assert s1.num_coefficients == 6
    assert s2.num_coefficients == 4
    assert s2.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""
    assert s1.__str__() == """E1: 0 x1 + 53/10 x2 - 2 x3 + 3 x4 + 0 x5 + 44/5 = 0
E2: 0 x1 - 3 x2 + 21/5 x3 + 3 x4 + 0 x5 + 2/7 = 0
E3: 0 x1 + 1 x2 - 5/3 x3 + 31/5 x4 + 0 x5 + 4 = 0
"""
    s2._check_unused_unknowns()
    assert s2.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""
    assert s2.num_coefficients == 4
    s1._check_unused_unknowns()
    assert s1.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""

def test_minimize():
    s1 = SystemEq.from_csv("csv_files/system.csv")
    s2 = SystemEq.from_csv("csv_files/system_to_minimize1.csv")
    s3 = SystemEq.from_csv("csv_files/system_to_minimize2.csv")
    s1._minimize_system()
    s2._minimize_system()
    s3._minimize_system()
    assert s1.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""
    assert s2.__str__() == """E1: 1 x1 + 2 x2 + 3 x3 + 4 = 0
"""
    assert s3.__str__() == """E1: 1 x1 + 2 x2 + 3 x3 + 4 = 0
E2: - 7/2 x1 + 14/5 x2 + 6/5 x3 - 1 = 0
E5: 1/2 x1 + 1 x2 + 3/2 x3 + 3 = 0
"""
def test_sort_by_abs():
    s1 = SystemEq.from_csv("csv_files/system_to_sort.csv")
    s1._sort_by_abs_coeff(2, 2)
    assert s1.__str__() == """E1: 1 x1 + 2 x2 + 0 x3 + 4 x4 + 14/5 = 0
E2: - 7/2 x1 + 14/5 x2 + 6/5 x3 - 1 x4 + 5/2 = 0
E3: - 3 x1 - 6 x2 - 9 x3 - 12 x4 - 1/2 = 0
E5: 1/2 x1 + 1 x2 + 3/2 x3 + 3 x4 - 46/5 = 0
E4: 7/2 x1 - 14/5 x2 - 6/5 x3 + 1 x4 + 11/10 = 0
"""

def test_zeroes_pivot_column():
    s1 = SystemEq.from_csv("csv_files/system_to_zeroes.csv")
    s1._zeroes_pivot_column(1, 1)
    assert s1.__str__() == """E1: 1 x1 + 0 x2 + 15/7 x3 + 33/7 x4 + 71/70 = 0
E2: 0 x1 + 14/5 x2 + 6/5 x3 - 1 x4 + 5/2 = 0
E3: 0 x1 + 0 x2 - 45/7 x3 - 99/7 x4 + 34/7 = 0
E4: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 18/5 = 0
E5: 0 x1 + 0 x2 + 15/14 x3 + 47/14 x4 - 1413/140 = 0
"""

def test_solve_unique():
    s1 = SystemEq.from_csv("csv_files/test1.csv")
    s1.solve_system()
    assert s1.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 585830/858663 = 0
E2: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 - 60824/22017 = 0
E4: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 0 x5 - 873/2327 = 0
E5: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 80872/22017 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 1 x5 - 2113490/858663 = 0
"""
    s2 = SystemEq.from_csv("csv_files/test2.csv")
    s2.solve_system()
    assert s2.__str__() == """E2: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 0 x6 + 424071540/61148341 = 0
E4: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 0 x6 - 120601020/428038387 = 0
E5: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 0 x5 + 0 x6 - 443940960/428038387 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 + 0 x6 - 2460164040/428038387 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 1 x5 + 0 x6 + 108458940/428038387 = 0
E6: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 1 x6 - 2081307180/428038387 = 0
"""
    s3 = SystemEq.from_csv("csv_files/single_eq_system.csv")
    s3.solve_system()
    assert s3.__str__() == """E1: 1 x1 + 5/2 = 0\n"""

def test_solve_no_solution():
    s1 = SystemEq.from_csv("csv_files/test4.csv")
    s1.solve_system()
    assert s1.__str__() == """E3: 1 x1 + 0 x2 + 1/3 x3 + 0 x4 + 1/5 x5 - 3/2 = 0
E4: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 6/5 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 2/5 = 0
E2: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 2/5 = 0
"""
    s2 = SystemEq.from_csv("csv_files/test5.csv")
    s2.solve_system()
    assert s2.__str__() == """E2: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 7/4 = 0
E4: 0 x1 + 1 x2 - 2/3 x3 + 1/2 x4 - 2/5 x5 + 1/2 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 1/2 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 5/4 = 0
"""
    s3 = SystemEq.from_csv("csv_files/es11.csv")
    s3.solve_system()
    assert s3.__str__() == """E1: 1 x1 + 0 x2 - 13 = 0
E2: 0 x1 + 1 x2 - 9 = 0
E3: 0 x1 + 0 x2 - 7 = 0
"""

def test_solve_infinitely_many_solutions():
    s1 = SystemEq.from_csv("csv_files/test3.csv")
    s1.solve_system()
    assert s1.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E3: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E2: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 63/100 x5 - 39/5 = 0
E4: 0 x1 + 0 x2 + 0 x3 + 1 x4 - 1/25 x5 - 8/5 = 0
"""
    s2 = SystemEq.from_csv("csv_files/single_eq_system2.csv")
    s2.solve_system()
    assert s2.__str__() == """E1: 1 x1 - 5 x2 + 5/2 = 0\n"""

def test_all_zeroes():
    s1 = SystemEq.from_csv("csv_files/all_zero.csv")
    s1.solve_system()
    assert s1.__str__() == """E1: 0 = 0
"""

def test_multiple_solve():
    s1 = SystemEq.from_csv("csv_files/test3.csv")
    s1.solve_system()
    s1.solve_system()
    assert s1.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E3: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E2: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 63/100 x5 - 39/5 = 0
E4: 0 x1 + 0 x2 + 0 x3 + 1 x4 - 1/25 x5 - 8/5 = 0
"""
    s2 = SystemEq.from_csv("csv_files/test4.csv")
    s2.solve_system()
    s2.solve_system()
    assert s2.__str__() == """E3: 1 x1 + 0 x2 + 1/3 x3 + 0 x4 + 1/5 x5 - 3/2 = 0
E4: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 6/5 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 2/5 = 0
E2: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 2/5 = 0
"""
    s3 = SystemEq.from_csv("csv_files/test1.csv")
    s3.solve_system()
    s3.solve_system()
    assert s3.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 585830/858663 = 0
E2: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 - 60824/22017 = 0
E4: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 0 x5 - 873/2327 = 0
E5: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 80872/22017 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 1 x5 - 2113490/858663 = 0
"""
