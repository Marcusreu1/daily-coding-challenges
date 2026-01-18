# 62. Unique Paths
# Difficulty: Medium
# https://leetcode.com/problems/unique-paths/

"""
PROBLEM:
A robot is located at the top-left corner of an m x n grid.
The robot can only move either DOWN or RIGHT at any point.
How many unique paths are there to reach the bottom-right corner?

EXAMPLES:
Input: m = 3, n = 7  → Output: 28
Input: m = 3, n = 2  → Output: 3
Input: m = 3, n = 3  → Output: 6

VISUALIZATION (m=3, n=4):
┌───┬───┬───┬───┐
│ S │ → │ → │ → │   S = Start (top-left)
├───┼───┼───┼───┤   E = End (bottom-right)
│ ↓ │   │   │   │
├───┼───┼───┼───┤   Robot can only move → or ↓
│ ↓ │   │   │ E │
└───┴───┴───┴───┘

CONSTRAINTS:
- 1 <= m, n <= 100

KEY INSIGHT:
To go from (0,0) to (m-1, n-1):
- Need exactly (m-1) moves DOWN
- Need exactly (n-1) moves RIGHT
- Total moves: (m-1) + (n-1) = m + n - 2

The question becomes: "In how many ways can we arrange these moves?"
This is a COMBINATION problem!

Answer: C(m+n-2, m-1) = (m+n-2)! / ((m-1)! × (n-1)!)

EXAMPLE CALCULATION (m=3, n=4):
- Total moves = 3 + 4 - 2 = 5
- Down moves = 3 - 1 = 2
- Right moves = 4 - 1 = 3

C(5, 2) = 5! / (2! × 3!)
        = (5 × 4) / (2 × 1)
        = 20 / 2
        = 10 paths ✓
"""

# STEP 1: Calculate total moves needed (m-1 down + n-1 right)
# STEP 2: Choose smaller of (m-1, n-1) for fewer iterations
# STEP 3: Calculate C(total, choose) incrementally to avoid overflow
# STEP 4: Return the combination result

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        
        total_moves = m + n - 2                                                  # Total moves: (m-1) + (n-1)
        choose = min(m - 1, n - 1)                                               # Choose smaller for efficiency
        
        result = 1                                                               # Build result incrementally
        
        for i in range(choose):
            result = result * (total_moves - i) // (i + 1)                       # C(n,k) incremental formula
        
        return result

"""
WHY EACH PART:
- total_moves = m + n - 2: Robot needs (m-1) downs + (n-1) rights to reach end
- choose = min(m-1, n-1): C(n,k) = C(n,n-k), so use smaller k for fewer iterations
- result * (total_moves - i): Numerator part of combination formula
- // (i + 1): Denominator part, integer division always exact for combinations
- Incremental calculation: Avoids computing large factorials that could overflow

HOW THE MATH WORKS:
C(n, k) = n! / (k! × (n-k)!)

Can be rewritten as:
C(n, k) = (n × (n-1) × ... × (n-k+1)) / (k × (k-1) × ... × 1)

Incremental calculation for C(5, 2):
i=0: result = 1 × (5-0) // (0+1) = 1 × 5 // 1 = 5
i=1: result = 5 × (5-1) // (1+1) = 5 × 4 // 2 = 10

This equals: (5 × 4) / (2 × 1) = 20 / 2 = 10 ✓

WHY DIVISION IS ALWAYS EXACT:
At step i, we've computed:
- Numerator: n × (n-1) × ... × (n-i)  [product of (i+1) consecutive numbers]
- Denominator: (i+1)!

Product of any k consecutive integers is always divisible by k!
This is a fundamental property of combinations.

TRACE EXAMPLE (m=3, n=7):
total_moves = 3 + 7 - 2 = 8
choose = min(2, 6) = 2

i=0: result = 1 × (8-0) // (0+1) = 1 × 8 // 1 = 8
i=1: result = 8 × (8-1) // (1+1) = 8 × 7 // 2 = 56 // 2 = 28

Return: 28 ✓

KEY TECHNIQUE:
- Combinatorics: Convert path counting to combination problem
- Incremental calculation: Avoid factorial overflow
- Symmetry: C(n,k) = C(n,n-k), use smaller k

ALTERNATIVE APPROACH (Dynamic Programming 2D):
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[1] * n for _ in range(m)]
        
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        return dp[m-1][n-1]

# Time: O(m×n), Space: O(m×n)
# More intuitive but less efficient

ALTERNATIVE APPROACH (Using math.comb):
import math

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        return math.comb(m + n - 2, m - 1)

# Simplest code, but less educational

CONNECTION TO PASCAL'S TRIANGLE:
The number of paths to cell (i,j) equals C(i+j, i)
This is exactly the entry in Pascal's Triangle at row (i+j), position i!

Pascal's Triangle:
        1           → C(0,0)
       1 1          → C(1,0), C(1,1)
      1 2 1         → C(2,0), C(2,1), C(2,2)
     1 3 3 1        → C(3,0), C(3,1), C(3,2), C(3,3)
    1 4 6 4 1       → ...
   1 5 10 10 5 1

For m=3, n=4: answer is at row 5 (=2+3), position 2 → C(5,2) = 10

EDGE CASES:
- m=1 or n=1: Only one path (straight line) → Returns 1 ✓
- m=1, n=1: Already at destination → Returns 1 ✓
- m=n: Symmetric → C(2n-2, n-1) ✓
- Large values (m=100, n=100): No overflow due to incremental calculation ✓

TIME COMPLEXITY: O(min(m, n)) - Single loop with min(m-1, n-1) iterations
SPACE COMPLEXITY: O(1) - Only use fixed number of variables

CONCEPTS USED:
- Combinatorics (binomial coefficient)
- Incremental calculation to avoid overflow
- Mathematical optimization
- C(n,k) = C(n, n-k) symmetry property
- Path counting as combination problem
"""
