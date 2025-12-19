-- 610. Triangle Judgement
-- Difficulty: Easy
-- https://leetcode.com/problems/triangle-judgement/

/*
PROBLEM:
Determine if three line segments can form a valid triangle.
For each row in the Triangle table, report whether the three sides can form a triangle.
Return 'Yes' if they can form a triangle, 'No' otherwise.

TABLES:
- Triangle (x, y, z)
  - x, y, z: lengths of three line segments

EXPECTED OUTPUT:
| x  | y  | z  | triangle |
|----|----|----|----------|
| 13 | 15 | 30 | No       |
| 10 | 20 | 15 | Yes      |

EXAMPLE:
Input data:
| x  | y  | z  |
|----|----|----|
| 13 | 15 | 30 |
| 10 | 20 | 15 |

Analysis:
Row 1: (13, 15, 30)
  - Check: 13 + 15 > 30 → 28 > 30 → FALSE ✗
  - Fails triangle inequality
  - Result: 'No'

Row 2: (10, 20, 15)
  - Check: 10 + 20 > 15 → 30 > 15 → TRUE ✓
  - Check: 10 + 15 > 20 → 25 > 20 → TRUE ✓
  - Check: 20 + 15 > 10 → 35 > 10 → TRUE ✓
  - All conditions satisfied
  - Result: 'Yes'
*/

-- STEP 1: Apply Triangle Inequality Theorem
-- Three sides can form a triangle if and only if:
-- The sum of any two sides is GREATER than the third side

-- STEP 2: Check all three conditions with AND
-- Condition 1: x + y > z
-- Condition 2: x + z > y
-- Condition 3: y + z > x
-- All three must be true simultaneously

-- STEP 3: Use CASE WHEN to return 'Yes' or 'No'
-- If all conditions true → 'Yes'
-- Otherwise → 'No'

SELECT 
    x,                                                       -- First side length
    y,                                                       -- Second side length
    z,                                                       -- Third side length
    CASE 
        WHEN ((x + y > z) AND (x + z > y) AND (z + y > x))   -- All 3 conditions must be true
        THEN 'Yes'                                           -- Forms valid triangle
        ELSE 'No'                                            -- Cannot form triangle
    END AS triangle                                          -- Result column
FROM Triangle;

/*
WHY EACH PART:
- Triangle Inequality Theorem:
  Fundamental geometric rule for valid triangles
  - States: Sum of any two sides must exceed the third side
  - Must check ALL three combinations
  - If ANY condition fails → NOT a valid triangle
  
- (x + y > z):
  First condition: sum of sides x and y must be greater than z
  - Example: (3, 4, 5) → 3 + 4 = 7 > 5 ✓
  - Example: (1, 2, 10) → 1 + 2 = 3 > 10 ✗
  
- (x + z > y):
  Second condition: sum of sides x and z must be greater than y
  - Example: (3, 4, 5) → 3 + 5 = 8 > 4 ✓
  
- (z + y > x):
  Third condition: sum of sides z and y must be greater than x
  - Example: (3, 4, 5) → 5 + 4 = 9 > 3 ✓
  
- AND operator:
  Ensures ALL conditions are true simultaneously
  - TRUE AND TRUE AND TRUE = TRUE → 'Yes'
  - TRUE AND TRUE AND FALSE = FALSE → 'No'
  - Any single FALSE makes entire expression FALSE
  
- > (strictly greater than):
  Must be strictly greater, not equal
  - x + y = z is NOT valid (would be a degenerate line, not triangle)
  - Example: (5, 5, 10) → 5 + 5 = 10 NOT > 10 ✗
  
- CASE WHEN ... THEN ... ELSE ... END:
  Conditional expression that returns different values based on condition
  - WHEN: condition to evaluate
  - THEN: value if condition is true
  - ELSE: value if condition is false
  - END: closes the CASE expression
  

KEY CONCEPT - Triangle Inequality Theorem:
Mathematical rule that determines if three lengths can form a triangle.

Explanation:
Valid triangle (3, 4, 5):
     /\
  5 /  \ 4
   /____\
      3
All sides can connect: 3+4=7>5 ✓, 3+5=8>4 ✓, 4+5=9>3 ✓

Invalid triangle (1, 2, 10):
Sides 1 and 2 cannot reach across gap of 10: 1+2=3 NOT > 10 ✗

WHY ALL THREE CONDITIONS ARE NECESSARY:
Cannot skip any condition, as each checks different pair:
- Only checking x+y>z: Could miss case where x=1, y=100, z=2 (1+2 NOT > 100)
- Only checking x+z>y: Could miss case where y is too long
- Only checking y+z>x: Could miss case where x is too long

Example showing why all 3 matter:
Sides (1, 100, 2):
- 1 + 100 > 2 → TRUE ✓
- 1 + 2 > 100 → FALSE ✗ (fails here!)
- 100 + 2 > 1 → TRUE ✓
Result: NOT a triangle (one condition failed)

ALTERNATIVE APPROACHES:
1. Using IF instead of CASE (MySQL specific):
   SELECT 
       x, y, z,
       IF((x+y>z) AND (x+z>y) AND (y+z>x), 'Yes', 'No') AS triangle
   FROM Triangle;

EDGE CASES:
- Equilateral triangle (5, 5, 5): All conditions true ✓
  - 5+5=10 > 5 ✓ for all combinations
  
- Isosceles triangle (5, 5, 8): Valid triangle ✓
  - 5+5=10 > 8 ✓
  - 5+8=13 > 5 ✓
  
- Degenerate triangle (5, 5, 10): NOT valid ✗
  - 5+5=10 NOT > 10 (equal, not greater)
  
- Scalene triangle (3, 4, 5): Valid right triangle ✓
  - Famous Pythagorean triple
  
- One very long side (1, 2, 100): NOT valid ✗
  - 1+2=3 NOT > 100
  
- Zero or negative values: Invalid by definition
  - (0, 5, 5): 0+5 NOT > 5
  - (-1, 5, 5): Negative length meaningless

OPERATOR PRECEDENCE:
Parentheses clarify evaluation order:
- ((x+y>z) AND (x+z>y) AND (z+y>x))
- Arithmetic (+) evaluates first: x+y, x+z, z+y
- Comparison (>) evaluates next: three boolean results
- Logical AND evaluates last: combines all three booleans
- Outer parentheses ensure entire condition evaluated for WHEN

Without parentheses (still works but less clear):
- x+y>z AND x+z>y AND z+y>x
- SQL operator precedence handles correctly, but harder to read

CONCEPTS USED:
- CASE WHEN for conditional logic
- AND operator for combining multiple conditions
- Arithmetic operators (+) for addition
- Comparison operator (>) for greater than
- Triangle Inequality Theorem from geometry
- String literals ('Yes', 'No')
- Column aliasing with AS
*/
