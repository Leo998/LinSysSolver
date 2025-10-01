# Tutorial and How-to Guide

This guide covers practical aspects of using LinSysSolver, from formatting CSV files correctly to handling various system types and exporting results.

## Table of Contents
1. [CSV File Format Specification](#csv-file-format-specification)
2. [Complete Examples with Output](#complete-examples-with-output)
3. [Handling Large Systems](#handling-large-systems)
4. [Exporting Results](#exporting-results)

---

## CSV File Format Specification

### Basic Rules

LinSysSolver reads systems of linear equations from CSV (Comma-Separated Values) files. Each row represents one equation, and each column represents a coefficient.

**Critical Requirements:**
- Each row must have the same number of columns
- The last column is always the constant term
- Equations must be in the form: `a₁x₁ + a₂x₂ + ... + aₙxₙ + c = 0`
- No empty rows are allowed
- No header row should be included

### Supported Number Formats

You can use three different formats for coefficients:

#### 1. Integers
```csv
2,3,5
1,-1,1
```

#### 2. Decimal Numbers (Floats)
```csv
2.5,3.7,-4.2
1.0,-0.5,2.8
```

#### 3. Fractions
Written as `numerator/denominator` where both must be integers:
```csv
1/2,3/4,5/6
2/3,-1/2,1/4
```

#### 4. Mixed Formats
You can mix formats within the same file:
```csv
2,0.5,1/3,-7
1/2,3,-2.5,4
```

### Converting Standard Equations to CSV Format

#### Example:

**Initial form:**
```
x₁ + x₂ + x₃ = 6
2x₁ - x₂ + x₃ = 3
x₁ + 2x₂ - x₃ = 2
```

**Convert to required form:**
```
x₁ + x₂ + x₃ - 6 = 0
2x₁ - x₂ + x₃ - 3 = 0
x₁ + 2x₂ - x₃ - 2 = 0
```

**CSV file:**
```csv
1,1,1,-6
2,-1,1,-3
1,2,-1,-2
```

### Common Mistakes to Avoid

**Wrong: Including header row**
```csv
x1,x2,constant
2,3,-5
1,-1,-1
```

**Wrong: Empty rows**
```csv
2,3,-5

1,-1,-1
```

**Wrong: Inconsistent number of columns**
```csv
2,3,-5
1,-1
```

**Wrong: Wrong sign on constant term**
```csv
2,3,5
1,-1,1
```
This represents `2x₁ + 3x₂ + 5 = 0` (not `= 5`)

---

## Complete Examples with Output

### Example 1: System with Unique Solution

**Problem:** Solve the system
```
x₁ + 2x₂ - x₃ = 1
x₂ + 2x₃ = 1
x₁ + 2x₂ = 0
```

**Create file `es5.csv`:**
```csv
1,2,-1,-1
0,1,2,-1
1,2,0,0
```

**Run command:**
```bash
LinSysSolver tests/csv_files/es5.csv
```

**Complete output:**
```
This is the system we'll start from:
E1: 1 x1 + 2 x2 - 1 x3 - 1 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0
E3: 1 x1 + 2 x2 + 0 x3 + 0 = 0

We order the equations in descending order of absolute value from row number 1 downwards based on the coefficient of x1 because we want it to be different from zero.
E1: 1 x1 + 2 x2 - 1 x3 - 1 = 0
E3: 1 x1 + 2 x2 + 0 x3 + 0 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0

Now we divide the coefficient of x1 (from E1) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E1 multiplied by that factor from the other row/equation. We repeat this process for every row/equation.
From E3 we subtract 1 * E1
From E2 we subtract 0 * E1
E1: 1 x1 + 2 x2 - 1 x3 - 1 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0

We then divide E1 by its own coefficient of x1 (1) in order to make it equal to 1 for convenience.
E1: 1 x1 + 2 x2 - 1 x3 - 1 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0

We order the equations in descending order of absolute value from row number 2 downwards based on the coefficient of x2 because we want it to be different from zero.
E1: 1 x1 + 2 x2 - 1 x3 - 1 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0

Now we divide the coefficient of x2 (from E2) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E2 multiplied by that factor from the other row/equation. We repeat this process for every row/equation.
From E1 we subtract 2 * E2
From E3 we subtract 0 * E2
E1: 1 x1 + 0 x2 - 5 x3 + 1 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0

We then divide E2 by its own coefficient of x2 (1) in order to make it equal to 1 for convenience.
E1: 1 x1 + 0 x2 - 5 x3 + 1 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0

We order the equations in descending order of absolute value from row number 3 downwards based on the coefficient of x3 because we want it to be different from zero.
E1: 1 x1 + 0 x2 - 5 x3 + 1 = 0
E2: 0 x1 + 1 x2 + 2 x3 - 1 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0

Now we divide the coefficient of x3 (from E3) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E3 multiplied by that factor from the other row/equation. We repeat this process for every row/equation.
From E1 we subtract -5 * E3
From E2 we subtract 2 * E3
E1: 1 x1 + 0 x2 + 0 x3 + 6 = 0
E2: 0 x1 + 1 x2 + 0 x3 - 3 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0

We then divide E3 by its own coefficient of x3 (1) in order to make it equal to 1 for convenience.
E1: 1 x1 + 0 x2 + 0 x3 + 6 = 0
E2: 0 x1 + 1 x2 + 0 x3 - 3 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0

This is now our final system (with any zero equations deleted).
E1: 1 x1 + 0 x2 + 0 x3 + 6 = 0
E2: 0 x1 + 1 x2 + 0 x3 - 3 = 0
E3: 0 x1 + 0 x2 + 1 x3 + 1 = 0

This system has only one solution, which is:
x1 = -6
x2 = 3
x3 = -1
```

### Example 2: Same System with Silent Mode

**Run command:**
```bash
LinSysSolver -s tests/csv_files/es5.csv
```

**Output:**
```
This system has only one solution, which is:
x1 = -6
x2 = 3
x3 = -1
```

### Example 3: System with No Solution

**Problem:** Solve the contradictory system
```
-2x₁ + 3x₂ = 1
x₁ - 2x₂ = -5
-x₁ + x₂ = 3
```

**Create file `es11.csv`:**
```csv
-2,3,-1
1,-2,5
-1,1,-3
```

**Run command:**
```bash
LinSysSolver tests/csv_files/es11.csv
```

**Output (excerpt):**
```
This is the system we'll start from:
E1: - 2 x1 + 3 x2 - 1 = 0
E2: 1 x1 - 2 x2 + 5 = 0
E3: - 1 x1 + 1 x2 - 3 = 0

We order the equations in descending order of absolute value from row number 1 downwards based on the coefficient of x1 because we want it to be different from zero.
E1: - 2 x1 + 3 x2 - 1 = 0
E2: 1 x1 - 2 x2 + 5 = 0
E3: - 1 x1 + 1 x2 - 3 = 0

Now we divide the coefficient of x1 (from E1) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E1 multiplied by that factor from the other row/equation. We repeat this process for every row/equation.
From E2 we subtract -1/2 * E1
From E3 we subtract 1/2 * E1
E1: - 2 x1 + 3 x2 - 1 = 0
E2: 0 x1 - 1/2 x2 + 9/2 = 0
E3: 0 x1 - 1/2 x2 - 5/2 = 0

We then divide E1 by its own coefficient of x1 (-2) in order to make it equal to 1 for convenience.
E1: 1 x1 - 3/2 x2 + 1/2 = 0
E2: 0 x1 - 1/2 x2 + 9/2 = 0
E3: 0 x1 - 1/2 x2 - 5/2 = 0

We order the equations in descending order of absolute value from row number 2 downwards based on the coefficient of x2 because we want it to be different from zero.
E1: 1 x1 - 3/2 x2 + 1/2 = 0
E2: 0 x1 - 1/2 x2 + 9/2 = 0
E3: 0 x1 - 1/2 x2 - 5/2 = 0

Now we divide the coefficient of x2 (from E2) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E2 multiplied by that factor from the other row/equation. We repeat this process for every row/equation.
From E1 we subtract 3 * E2
From E3 we subtract 1 * E2
E1: 1 x1 + 0 x2 - 13 = 0
E2: 0 x1 - 1/2 x2 + 9/2 = 0
E3: 0 x1 + 0 x2 - 7 = 0

We then divide E2 by its own coefficient of x2 (-1/2) in order to make it equal to 1 for convenience.
E1: 1 x1 + 0 x2 - 13 = 0
E2: 0 x1 + 1 x2 - 9 = 0
E3: 0 x1 + 0 x2 - 7 = 0

This is now our final system (with any zero equations deleted).
E1: 1 x1 + 0 x2 - 13 = 0
E2: 0 x1 + 1 x2 - 9 = 0
E3: 0 x1 + 0 x2 - 7 = 0

From equation 3: 0 = 7
Impossible: this system has no solution.
```

### Example 4: System with Infinitely Many Solutions

**Problem:** Solve the underdetermined system
```
-x₁ + 3x₃ = 2
2x₁ + x₂ + x₃ = 1
x₁ + x₂ + 4x₃ = 3
```

**Create file `es13.csv`:**
```csv
-1,0,3,-2
2,1,1,-1
1,1,4,-3
```

**Run command:**
```bash
LinSysSolver tests/csv_files/es13.csv
```

**Output (final part):**
```
This is the system we'll start from:
E1: - 1 x1 + 0 x2 + 3 x3 - 2 = 0
E2: 2 x1 + 1 x2 + 1 x3 - 1 = 0
E3: 1 x1 + 1 x2 + 4 x3 - 3 = 0

We order the equations in descending order of absolute value from row number 1 downwards based on the coefficient of x1 because we want it to be different from zero.
E2: 2 x1 + 1 x2 + 1 x3 - 1 = 0
E1: - 1 x1 + 0 x2 + 3 x3 - 2 = 0
E3: 1 x1 + 1 x2 + 4 x3 - 3 = 0

Now we divide the coefficient of x1 (from E2) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E2 multiplied by that factor from the other row/equation. We repeat this process for every row/equation.
From E1 we subtract -1/2 * E2
From E3 we subtract 1/2 * E2
E2: 2 x1 + 1 x2 + 1 x3 - 1 = 0
E1: 0 x1 + 1/2 x2 + 7/2 x3 - 5/2 = 0
E3: 0 x1 + 1/2 x2 + 7/2 x3 - 5/2 = 0

We then divide E2 by its own coefficient of x1 (2) in order to make it equal to 1 for convenience.
E2: 1 x1 + 1/2 x2 + 1/2 x3 - 1/2 = 0
E1: 0 x1 + 1/2 x2 + 7/2 x3 - 5/2 = 0
E3: 0 x1 + 1/2 x2 + 7/2 x3 - 5/2 = 0

We order the equations in descending order of absolute value from row number 2 downwards based on the coefficient of x2 because we want it to be different from zero.
E2: 1 x1 + 1/2 x2 + 1/2 x3 - 1/2 = 0
E1: 0 x1 + 1/2 x2 + 7/2 x3 - 5/2 = 0
E3: 0 x1 + 1/2 x2 + 7/2 x3 - 5/2 = 0

Now we divide the coefficient of x2 (from E1) by the coefficient of the same unknown from another row/equation, obtaining a factor, and then we subtract E1 multiplied by that factor from the other row/equation. We repeat this process for every row/equation.
From E2 we subtract 1 * E1
From E3 we subtract 1 * E1
E2: 1 x1 + 0 x2 - 3 x3 + 2 = 0
E1: 0 x1 + 1/2 x2 + 7/2 x3 - 5/2 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 = 0

We then divide E1 by its own coefficient of x2 (1/2) in order to make it equal to 1 for convenience.
E2: 1 x1 + 0 x2 - 3 x3 + 2 = 0
E1: 0 x1 + 1 x2 + 7 x3 - 5 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 = 0

We order the equations in descending order of absolute value from row number 3 downwards based on the coefficient of x3 because we want it to be different from zero.
All coefficients of this unknown are already zero, so we move to the next one.
There are no more unknowns to go through.
E2: 1 x1 + 0 x2 - 3 x3 + 2 = 0
E1: 0 x1 + 1 x2 + 7 x3 - 5 = 0
E3: 0 x1 + 0 x2 + 0 x3 + 0 = 0

This is now our final system (with any zero equations deleted).
E2: 1 x1 + 0 x2 - 3 x3 + 2 = 0
E1: 0 x1 + 1 x2 + 7 x3 - 5 = 0

This system has 3 unknowns in 2 equations, so it has infinitely many solutions.

x1 =  3 x3 - 2
x2 = - 7 x3 + 5
x3 = any value
```

**Interpretation:**
- x₃ is a free parameter (can be any value)
- x₁ and x₂ are expressed in terms of x₃
- For example, if x₃ = 0: x₁ = -2, x₂ = 5
- If x₃ = 5: x₁ = 15 - 2 = 13, x₂ = -35 - 5 = -30

---

## Handling Large Systems

1. **Use silent mode** to reduce output overhead:
   ```bash
   LinSysSolver large_system.csv --silent
   ```

2. **Consider alternatives** for production/research such as numpy.linalg.solve

## Exporting Results

### Method 1: Shell Redirection (Recommended)

Redirect output to a text file:

```bash
# Save full output with explanations
LinSysSolver system.csv > results.txt

# Save only solution (silent mode)
LinSysSolver system.csv --silent > solution.txt

# Append to existing file
LinSysSolver system.csv >> all_results.txt
```

### Method 2: Combining with Other Commands

**Save and display:**
```bash
LinSysSolver system.csv | tee results.txt
```

## Troubleshooting

### Issue: "FileNotFoundError"
**Solution:** Verify the CSV file path is correct. Use absolute paths if needed:
```bash
LinSysSolver /full/path/to/system.csv
```

### Issue: "Invalid CSV format"
**Causes:**
- Empty rows in CSV
- Inconsistent number of columns
- Non-numeric values

**Solution:** Open CSV in a text editor and verify format

---

For detailed API documentation, see [Reference](reference.md).  
For theoretical background, see [Explanation](explanation.md).