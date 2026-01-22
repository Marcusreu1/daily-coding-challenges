# 70. Climbing Stairs
# Difficulty: Easy
# https://leetcode.com/problems/climbing-stairs/

"""
PROBLEM:
You are climbing a staircase with n steps to reach the top.
Each time you can climb either 1 or 2 steps.
In how many distinct ways can you climb to the top?

EXAMPLES:
Input: n = 2  → Output: 2  [(1,1), (2)]
Input: n = 3  → Output: 3  [(1,1,1), (1,2), (2,1)]
Input: n = 4  → Output: 5  [(1,1,1,1), (1,1,2), (1,2,1), (2,1,1), (2,2)]

CONSTRAINTS:
- 1 <= n <= 45

KEY INSIGHT:
To reach step n, you either:
1. Came from step (n-1) with a 1-step jump, OR
2. Came from step (n-2) with a 2-step jump

Therefore: ways(n) = ways(n-1) + ways(n-2)

This is the FIBONACCI sequence!

VISUALIZATION:
            ┌───┐
            │ n │ ← Target
            └─┬─┘
         ┌───┴───┐
         │       │
    ┌────┴───┐ ┌─┴──────┐
    │  n-1   │ │  n-2   │
    │(1 step)│ │(2 steps)│
    └────────┘ └────────┘

ways(n) = ways(n-1) + ways(n-2)

SEQUENCE:
n:     1   2   3   4   5   6   7   8   9  10
ways:  1   2   3   5   8  13  21  34  55  89
"""

# STEP 1: Handle base cases (n <= 2)
# STEP 2: Use two variables to track previous two values
# STEP 3: Iterate from 3 to n, calculating each step
# STEP 4: Return the final result

class Solution:
    def climbStairs(self, n: int) -> int:
        
        if n <= 2:                                                               # Base cases
            return n                                                             # 1 way for n=1, 2 ways for n=2
        
        dos_atras = 1                                                            # ways(1)
        uno_atras = 2                                                            # ways(2)
        
        for i in range(3, n + 1):                                                # Calculate ways(3) to ways(n)
            actual = uno_atras + dos_atras                                       # ways(i) = ways(i-1) + ways(i-2)
            dos_atras = uno_atras                                                # Shift: dos_atras becomes old uno_atras
            uno_atras = actual                                                   # Shift: uno_atras becomes current
        
        return uno_atras                                                         # Return ways(n)

"""
WHY EACH PART:
- n <= 2: Base cases (1 step = 1 way, 2 steps = 2 ways)
- dos_atras = 1: Ways to reach step 1
- uno_atras = 2: Ways to reach step 2
- actual = uno_atras + dos_atras: Fibonacci recurrence
- dos_atras = uno_atras: Slide the window forward
- uno_atras = actual: Update with new value
- return uno_atras: After loop, this holds ways(n)

HOW IT WORKS (Example: n = 5):

Initial: dos_atras=1 (n=1), uno_atras=2 (n=2)

i=3: actual = 2+1 = 3
     dos_atras=2, uno_atras=3
     
i=4: actual = 3+2 = 5
     dos_atras=3, uno_atras=5
     
i=5: actual = 5+3 = 8
     dos_atras=5, uno_atras=8

return 8 ✓

Verification:
n=5 ways: (1,1,1,1,1), (1,1,1,2), (1,1,2,1), (1,2,1,1), (2,1,1,1),
          (1,2,2), (2,1,2), (2,2,1) = 8 ways ✓

KEY TECHNIQUE:
- Dynamic Programming: Build solution from smaller subproblems
- Fibonacci pattern: ways(n) = ways(n-1) + ways(n-2)
- Space optimization: Only keep last 2 values (sliding window)

EDGE CASES:
- n = 1: Returns 1 (only way: one 1-step) ✓
- n = 2: Returns 2 (two 1-steps OR one 2-step) ✓
- n = 45: Returns 1836311903 (works within int range) ✓

TIME COMPLEXITY: O(n) - Single loop from 3 to n
SPACE COMPLEXITY: O(1) - Only use two variables

CONCEPTS USED:
- Dynamic Programming
- Fibonacci sequence
- Space optimization (sliding window)
- Recurrence relation
- Bottom-up vs top-down approach
"""
