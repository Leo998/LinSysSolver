# Explanation: Gaussian Elimination Algorithm

This document explains the theory and implementation of the Gaussian elimination algorithm used in LinSysSolver.

## Table of Contents
1. [Mathematical Background](#mathematical-background)
2. [The Gaussian Elimination Algorithm](#the-gaussian-elimination-algorithm)
3. [Solution Classification](#solution-classification)
4. [Implementation Details](#implementation-details)
5. [Why Exact Arithmetic?](#why-exact-arithmetic)

---

## Mathematical Background

### Systems of Linear Equations

A system of linear equations is a collection of equations involving the same set of variables. The general form is:

```
a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ = b₁
a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ = b₂
  ⋮
aₘ₁x₁ + aₘ₂x₂ + ... + aₘₙxₙ = bₘ
```

Where:
- **m** = number of equations
- **n** = number of unknowns (variables)
- **aᵢⱼ** = coefficients (known values)
- **xⱼ** = unknowns (values to solve for)
- **bᵢ** = constants (right-hand side values)

### Matrix Representation

This system can be represented as an augmented matrix:

```
[a₁₁  a₁₂  ...  a₁ₙ | b₁]
[a₂₁  a₂₂  ...  a₂ₙ | b₂]
[ ⋮    ⋮   ⋱    ⋮  | ⋮ ]
[aₘ₁  aₘ₂  ...  aₘₙ | bₘ]
```

Or more compactly as: **Ax = b**

Where:
- **A** is the coefficient matrix (m × n)
- **x** is the vector of unknowns (n × 1)
- **b** is the constant vector (m × 1)

### Elementary Row Operations

Three operations preserve the solution set:

1. **Row swapping**: Exchange two rows
2. **Row scaling**: Multiply a row by a non-zero scalar
3. **Row addition**: Add a multiple of one row to another row

### Geometric Interpretation

- Each linear equation represents a **hyperplane** in n-dimensional space
- A solution is a point where all hyperplanes intersect
- Different solution types correspond to different geometric configurations:
  - **Unique solution**: All hyperplanes intersect at exactly one point
  - **No solution**: Hyperplanes are parallel or inconsistent
  - **Infinitely many solutions**: Hyperplanes intersect along a line, plane, or higher-dimensional subspace

---

## The Gaussian Elimination Algorithm

Gaussian elimination systematically transforms the augmented matrix into **row echelon form** using elementary row operations.

### Row Echelon Form

A matrix is in row echelon form when:
1. All rows consisting entirely of zeros are at the bottom
2. The first non-zero element in each row (called the **pivot**) is to the right of the pivot in the row above
3. All entries below each pivot are zero

**Example of row echelon form:**
```
[1  2  3 | 4]
[0  1  5 | 6]
[0  0  1 | 7]
```

### Algorithm Steps 

For each column k from 1 to n:

1. **Select pivot and swap rows**: Sort all rows from row i = k downwards in descending order of absolute value of coefficient a<sub>ik
2. **Eliminate**: For each row z except the pivot row:
   - Compute the elimination factor: factor = a<sub>zk</sub> / a<sub>ik
   - Subtract `factor × (pivot row)` from row z
   - This makes a<sub>zk</sub> = 0
3. **Normalize**: Divide the pivot row by a<sub>ik</sub> to make the pivot equal to 1

After this process, the matrix is in row echelon form (or reduced row echelon form, it depends on how many solutions the system has).

LinSysSolver then classifies the solution type.

---

## Solution Classification

After reduction to row echelon form, the system's solution type is determined by examining the structure.

### Case 1: Unique Solution

**Condition:** 
- Number of non-zero rows = number of unknowns
- Each row has exactly one non-zero coefficient in reduced form (except for the constant term)

**Example:**
```
[1  0  0 | 3]
[0  1  0 | 2]
[0  0  1 | 1]
```

**Solution:** x₁ = 3, x₂ = 2, x₃ = 1

### Case 2: No Solution (Inconsistent)

**Condition:** 
- At least one row is of the form: [0  0  ...  0 | c] where c ≠ 0
- This represents the equation: 0 = c (contradiction)

**Example:**
```
[1  2 | 3]
[0  0 | 5]    ← 0 = 5 (impossible!)
```

### Case 3: Infinitely Many Solutions (Underdetermined)

**Condition:**
- Number of non-zero rows < number of unknowns
- OR at least one row has 2+ non-zero coefficients

**Example:**
```
[1  2  3 | 6]
[0  1  5 | 4]
```

This represents:
```
x₁ + 2x₂ + 3x₃ = 6
x₂ + 5x₃ = 4
```

Three unknowns, two equations → one free parameter.

**Parametric solution:**
```
x₃ = t (free parameter)
x₂ = 4 - 5t
x₁ = 6 - 2x₂ - 3x₃ = 6 - 2(4 - 5t) - 3t = -2 + 7t
```

### Decision Tree

```
Row echelon form achieved
    ↓
Number of non-zero rows > Number of unknowns 
    ├─ Yes → NO SOLUTION
    └─ No
        ↓
    At least one row has all coefficients equal to zero and non-zero constant term?
        ├─ Yes → NO SOLUTION
        └─ No
            ↓
        At least one row has more than one non-zero coefficient?
          ├─ Yes → INFINITELY MANY SOLUTIONS
          └─ No → UNIQUE SOLUTION
```

---

## Implementation Details

### System Minimization

Before elimination, LinSysSolver simplifies the system:

#### 1. Remove Unused Variables

Variables with all-zero coefficients across all equations are removed:

#### 2. Remove Redundant Equations

Equations equivalent to each other (scalar multiples) are removed:

---

## Why Exact Arithmetic?

### Floating-Point Limitations

Standard floating-point arithmetic (Python `float`, C `double`) has limitations:

1. **Finite precision**: Only ~15-17 significant decimal digits
2. **Rounding errors**: Accumulate during operations
3. **Representation errors**: Many decimal numbers cannot be represented exactly

**Example of floating-point error:**
```python
0.1 + 0.2 == 0.3  # False!
0.1 + 0.2  # 0.30000000000000004
```

### Exact Rational Arithmetic

LinSysSolver uses `Fraction` class:

```python
class Fraction:
    num: int  # Numerator
    den: int  # Denominator (always positive)
```

**Advantages:**
1. **Exact representation**: Every rational number is represented precisely
2. **No rounding errors**: Operations are mathematically exact
3. **Predictable**: Results are deterministic and reproducible


### Online Resources

- **Wikipedia**: [Gaussian Elimination](https://en.wikipedia.org/wiki/Gaussian_elimination)
- **Matrixcalc**: [Online matrix calculator](https://www.matrixcalc.org/slu.html)

---

For practical usage, see [Tutorial/How-to](tutorial-how-to.md).  
For complete API documentation, see [Reference](reference.md).