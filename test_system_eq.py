import pytest

from fraction import Fraction
from equation import Equation
from system_eq import NumberedEquation, SystemEq
 
# ----------------------------------------------------------------------
# Constructor and initialization
# ----------------------------------------------------------------------

def test_emptysys_init() -> None:
    """
    Given an empty csv file or no arguments to SystemEq constructor,
    When attempting to create a SystemEq instance,
    Then it should raise TypeError due to insufficient data.
    """
    with pytest.raises(TypeError):
        SystemEq.from_csv("csv_files/empty.csv")
    with pytest.raises(TypeError):
        SystemEq()
        
def test_invalid_init() -> None:
    """
    Given CSV files containing equations with mismatched coefficient counts,
    When attempting to create a SystemEq instance,
    Then it should raise ValueError for inconsistent equation dimensions.
    """
    with pytest.raises(ValueError):
        SystemEq.from_csv("csv_files/unpaired1.csv")
    with pytest.raises(ValueError):
        SystemEq.from_csv("csv_files/unpaired2.csv")
    with pytest.raises(ValueError):
        SystemEq.from_csv("csv_files/unpaired3.csv")

def test_init() -> None:
    """
    Given a valid CSV file with consistent equation dimensions,
    When creating a SystemEq instance,
    Then it should:
    - Store equations with proper fractional coefficients
    - Assign sequential equation numbers starting from 1
    - Correctly track the number of coefficients per equation
    """
    system_from_csv = SystemEq.from_csv("csv_files/system.csv")
    assert system_from_csv.num_coefficients == 4
    assert system_from_csv.system[0].equation == Equation(Fraction(5.3), Fraction(-2), Fraction(3), Fraction(8.8))
    assert system_from_csv.system[0].equation_number == 1
    assert system_from_csv.system[1].equation == Equation(Fraction(-3), Fraction(4.2), Fraction(3), Fraction("2/7"))
    assert system_from_csv.system[1].equation_number == 2
    assert system_from_csv.system[2].equation == Equation(Fraction(1), Fraction("-5/3"), Fraction(6.2), Fraction(4))
    assert system_from_csv.system[2].equation_number == 3

# ----------------------------------------------------------------------
# String representation
# ----------------------------------------------------------------------

def test_str() -> None:
    """
    Given a SystemEq instance,
    When converting to string representation,
    Then it should:
    - Display each equation with its identifier (E1, E2, ...)
    - Show coefficients in simplified fractional form
    - Use proper mathematical notation with variable subscripts
    - Include newlines for readable multi-equation display
    """
    system_for_display = SystemEq.from_csv("csv_files/system.csv")
    assert system_for_display.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""

# ----------------------------------------------------------------------
# Internal helpers
# ----------------------------------------------------------------------

def test_del_eq_if_zero() -> None:
    """
    Given a system containing zero equations,
    When calling _del_equation_if_zero on those equations,
    Then it should:
    - Remove equations where all coefficients are zero
    - Preserve non-zero equations unchanged
    - Maintain correct equation numbering for remaining equations
    - Handle index shifts properly after deletions
    """
    system_with_zeros = SystemEq.from_csv("csv_files/row_all_zero.csv")
    system_with_zeros._del_equation_if_zero(0)
    assert system_with_zeros.system[0].equation == Equation(Fraction(5.3), Fraction(-2), Fraction(3), Fraction(8.8))
    assert system_with_zeros.system[0].equation_number == 1
    system_with_zeros._del_equation_if_zero(1)
    assert system_with_zeros.system[1].equation == Equation(Fraction(1), Fraction(-5, 3), Fraction(6.2), Fraction(4))
    assert system_with_zeros.system[1].equation_number == 3
    with pytest.raises(IndexError):
        system_with_zeros.system[2].equation

def test_unused_unknowns() -> None:
    """
    Given a system with variables that have zero coefficients in all equations,
    When calling _check_unused_unknowns,
    Then it should:
    - Identify variables with all-zero coefficient columns
    - Remove unused variables from all equations
    - Update system dimension (num_coefficients)
    - Preserve relative relationships between remaining variables
    """
    system_with_unused = SystemEq.from_csv("csv_files/unused_unknowns.csv")
    assert system_with_unused.num_coefficients == 6
    assert system_with_unused.__str__() == """E1: 0 x1 + 53/10 x2 - 2 x3 + 3 x4 + 0 x5 + 44/5 = 0
E2: 0 x1 - 3 x2 + 21/5 x3 + 3 x4 + 0 x5 + 2/7 = 0
E3: 0 x1 + 1 x2 - 5/3 x3 + 31/5 x4 + 0 x5 + 4 = 0
"""
    system_with_unused._check_unused_unknowns()
    assert system_with_unused.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""
    assert system_with_unused.num_coefficients == 4

def test_minimize() -> None:
    """
    Given systems with redundant or equivalent equations,
    When calling _minimize_system,
    Then it should:
    - Remove duplicate equations (same coefficients)
    - Remove equivalent equations (scalar multiples)
    - Eliminate unused variables first
    - Preserve one representative of each equivalence class
    """
    standard_system = SystemEq.from_csv("csv_files/system.csv")
    redundant_system = SystemEq.from_csv("csv_files/system_to_minimize1.csv")
    mixed_redundancy_system = SystemEq.from_csv("csv_files/system_to_minimize2.csv")
    standard_system._minimize_system()
    redundant_system._minimize_system()
    mixed_redundancy_system._minimize_system()
    
    # System with no redundancy remains unchanged
    assert standard_system.__str__() == """E1: 53/10 x1 - 2 x2 + 3 x3 + 44/5 = 0
E2: - 3 x1 + 21/5 x2 + 3 x3 + 2/7 = 0
E3: 1 x1 - 5/3 x2 + 31/5 x3 + 4 = 0
"""
    # Redundant system reduces to single equation
    assert redundant_system.__str__() == """E1: 1 x1 + 2 x2 + 3 x3 + 4 = 0
"""
    # Mixed system keeps non-equivalent equations
    assert mixed_redundancy_system.__str__() == """E1: 1 x1 + 2 x2 + 3 x3 + 4 = 0
E2: - 7/2 x1 + 14/5 x2 + 6/5 x3 - 1 = 0
E5: 1/2 x1 + 1 x2 + 3/2 x3 + 3 = 0
"""

def test_sort_by_abs() -> None:
    """
    Given a system of equations,
    When calling _sort_by_abs_coeff with specific row and column parameters,
    Then it should:
    - Sort equations from specified row onwards by absolute coefficient value
    - Use the specified column for comparison
    - Maintain relative order for equations above the starting row
    - Default to descending order (largest absolute values first)
    """
    system_to_sort = SystemEq.from_csv("csv_files/system_to_sort.csv")
    system_to_sort._sort_by_abs_coeff(2, 2)
    assert system_to_sort.__str__() == """E1: 1 x1 + 2 x2 + 0 x3 + 4 x4 + 14/5 = 0
E2: - 7/2 x1 + 14/5 x2 + 6/5 x3 - 1 x4 + 5/2 = 0
E3: - 3 x1 - 6 x2 - 9 x3 - 12 x4 - 1/2 = 0
E5: 1/2 x1 + 1 x2 + 3/2 x3 + 3 x4 - 46/5 = 0
E4: 7/2 x1 - 14/5 x2 - 6/5 x3 + 1 x4 + 11/10 = 0
"""

def test_zeroes_pivot_column() -> None:
    """
    Given a system with a designated pivot row and column,
    When calling _zeroes_pivot_column,
    Then it should:
    - Eliminate the pivot column entry in all other rows
    - Preserve the pivot row unchanged
    - Use proper elimination factors (ratio of coefficients)
    """
    system_for_elimination = SystemEq.from_csv("csv_files/system_to_zeroes.csv")
    system_for_elimination._zeroes_pivot_column(1, 1)
    assert system_for_elimination.__str__() == """E1: 1 x1 + 0 x2 + 15/7 x3 + 33/7 x4 + 71/70 = 0
E2: 0 x1 + 14/5 x2 + 6/5 x3 - 1 x4 + 5/2 = 0
E3: 0 x1 + 0 x2 - 45/7 x3 - 99/7 x4 + 34/7 = 0
E4: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 18/5 = 0
E5: 0 x1 + 0 x2 + 15/14 x3 + 47/14 x4 - 1413/140 = 0
"""

# ----------------------------------------------------------------------
# Solving scenarios
# ----------------------------------------------------------------------

def test_solve_unique(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Given systems with unique solutions,
    When calling solve_system,
    Then it should:
    - Reduce to row echelon form with identity matrix pattern
    - Identify and output the unique solution values
    - Handle systems of various dimensions correctly
    - Print clear solution messages to stdout
    """
    system_unique_5x5 = SystemEq.from_csv("csv_files/test1.csv")
    system_unique_5x5.solve_system()
    assert system_unique_5x5.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 585830/858663 = 0
E2: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 - 60824/22017 = 0
E4: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 0 x5 - 873/2327 = 0
E5: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 80872/22017 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 1 x5 - 2113490/858663 = 0
"""
    system_unique_6x6 = SystemEq.from_csv("csv_files/test2.csv")
    system_unique_6x6.solve_system()
    assert system_unique_6x6.__str__() == """E2: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 0 x6 + 424071540/61148341 = 0
E4: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 0 x6 - 120601020/428038387 = 0
E5: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 0 x5 + 0 x6 - 443940960/428038387 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 + 0 x6 - 2460164040/428038387 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 1 x5 + 0 x6 + 108458940/428038387 = 0
E6: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 1 x6 - 2081307180/428038387 = 0
"""
    single_equation_system = SystemEq.from_csv("csv_files/single_eq_system.csv")
    single_equation_system.solve_system()
    assert single_equation_system.__str__() == """E1: 1 x1 + 5/2 = 0\n"""

    # Verify solution output messages
    captured = capsys.readouterr()
    assert """This system has only one solution, which is:
x1 = -585830/858663
x2 = 60824/22017
x3 = 873/2327
x4 = 80872/22017
x5 = 2113490/858663""" in captured.out
    assert """This system has only one solution, which is:
x1 = -424071540/61148341
x2 = 120601020/428038387
x3 = 443940960/428038387
x4 = 2460164040/428038387
x5 = -108458940/428038387
x6 = 2081307180/428038387""" in captured.out
    assert """This system has only one solution, which is:
x1 = -5/2""" in captured.out

def test_solve_no_solution(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Given inconsistent systems of equations,
    When calling solve_system,
    Then it should:
    - Detect inconsistency (0 = non-zero constant)
    - Report which equation reveals the contradiction
    - Print appropriate "no solution" message
    - Preserve the reduced system state showing the inconsistency
    """
    inconsistent_system_1 = SystemEq.from_csv("csv_files/test4.csv")
    inconsistent_system_1.solve_system()
    assert inconsistent_system_1.__str__() == """E3: 1 x1 + 0 x2 + 1/3 x3 + 0 x4 + 1/5 x5 - 3/2 = 0
E4: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 6/5 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 2/5 = 0
E2: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 2/5 = 0
"""
    inconsistent_system_2 = SystemEq.from_csv("csv_files/test5.csv")
    inconsistent_system_2.solve_system()
    assert inconsistent_system_2.__str__() == """E2: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 7/4 = 0
E4: 0 x1 + 1 x2 - 2/3 x3 + 1/2 x4 - 2/5 x5 + 1/2 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 1/2 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 5/4 = 0
"""
    simple_inconsistent_system = SystemEq.from_csv("csv_files/es11.csv")
    simple_inconsistent_system.solve_system()
    assert simple_inconsistent_system.__str__() == """E1: 1 x1 + 0 x2 - 13 = 0
E2: 0 x1 + 1 x2 - 9 = 0
E3: 0 x1 + 0 x2 - 7 = 0
"""

    # Verify contradiction detection messages
    captured = capsys.readouterr()
    assert """From equation 2: 0 = 2/5
Impossible: this system has no solution.""" in captured.out
    assert """From equation 3: 0 = 5/4
Impossible: this system has no solution.""" in captured.out
    assert """From equation 3: 0 = 7
Impossible: this system has no solution.""" in captured.out

def test_solve_infinitely_many_solutions(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Given underdetermined systems of equations,
    When calling solve_system,
    Then it should:
    - Detect underdetermined condition (more variables than equations)
    - Express solutions in terms of free variables
    - Identify which variables are free (unconstrained)
    - Format solution expressions properly
    """
    underdetermined_system = SystemEq.from_csv("csv_files/test3.csv")
    underdetermined_system.solve_system()
    assert underdetermined_system.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E3: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E2: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 63/100 x5 - 39/5 = 0
E4: 0 x1 + 0 x2 + 0 x3 + 1 x4 - 1/25 x5 - 8/5 = 0
"""
    single_equation_underdetermined = SystemEq.from_csv("csv_files/single_eq_system2.csv")
    single_equation_underdetermined.solve_system()
    assert single_equation_underdetermined.__str__() == """E1: 1 x1 - 5 x2 + 5/2 = 0\n"""

    # Verify parameterized solution output
    captured = capsys.readouterr()
    assert """This system has 5 unknowns in 4 equations, so it has infinitely many solutions.
x1 = 0
x2 = 0
x3 = - 63/100 x5 + 39/5
x4 =  1/25 x5 + 8/5
x5 = any value""" in captured.out
    assert """This system has 2 unknowns in 1 equations, so it has infinitely many solutions.
x1 =  5 x2 - 5/2
x2 = any value""" in captured.out

def test_all_zeroes(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Given a system where all equations are identically zero,
    When calling solve_system,
    Then it should:
    - Recognize the trivial system (0 = 0 for all equations)
    - Report that any values satisfy the system
    - Handle this degenerate case without errors
    """
    all_zero_system = SystemEq.from_csv("csv_files/all_zero.csv")
    all_zero_system.solve_system()
    assert all_zero_system.__str__() == """E1: 0 = 0\n"""

    captured = capsys.readouterr()
    assert """The system is composed by only zeroes, any value of any unknown is a solution.""" in captured.out

def test_multiple_solve() -> None:
    """
    Given systems that have already been solved,
    When calling solve_system multiple times,
    Then it should:
    - Not further modify already-reduced systems
    - Preserve solution classification and output
    - Handle repeated solving without corruption
    """
    underdetermined_system = SystemEq.from_csv("csv_files/test3.csv")
    underdetermined_system.solve_system()
    underdetermined_system.solve_system()
    assert underdetermined_system.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E3: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 0 = 0
E2: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 63/100 x5 - 39/5 = 0
E4: 0 x1 + 0 x2 + 0 x3 + 1 x4 - 1/25 x5 - 8/5 = 0
"""
    inconsistent_system = SystemEq.from_csv("csv_files/test4.csv")
    inconsistent_system.solve_system()
    inconsistent_system.solve_system()
    assert inconsistent_system.__str__() == """E3: 1 x1 + 0 x2 + 1/3 x3 + 0 x4 + 1/5 x5 - 3/2 = 0
E4: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 + 6/5 = 0
E1: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 2/5 = 0
E2: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 - 2/5 = 0
"""
    system_unique = SystemEq.from_csv("csv_files/test1.csv")
    system_unique.solve_system()
    system_unique.solve_system()
    assert system_unique.__str__() == """E1: 1 x1 + 0 x2 + 0 x3 + 0 x4 + 0 x5 + 585830/858663 = 0
E2: 0 x1 + 1 x2 + 0 x3 + 0 x4 + 0 x5 - 60824/22017 = 0
E4: 0 x1 + 0 x2 + 1 x3 + 0 x4 + 0 x5 - 873/2327 = 0
E5: 0 x1 + 0 x2 + 0 x3 + 1 x4 + 0 x5 - 80872/22017 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 x4 + 1 x5 - 2113490/858663 = 0
"""
