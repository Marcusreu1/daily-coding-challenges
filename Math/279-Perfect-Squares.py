# 279. Perfect Squares
# Difficulty: Medium
# https://leetcode.com/problems/perfect-squares/

"""
PROBLEM:
Given an integer n, return the least number of perfect square numbers
that sum to n.

A perfect square is an integer that is the square of an integer.
(1, 4, 9, 16, 25, ...)

EXAMPLES:
Input: n = 12 → Output: 3  (12 = 4 + 4 + 4)
Input: n = 13 → Output: 2  (13 = 4 + 9)
Input: n = 1  → Output: 1  (1 = 1)

CONSTRAINTS:
- 1 <= n <= 10^4

KEY INSIGHT:
This is similar to the "Coin Change" problem where the "coins" are
perfect squares (1, 4, 9, 16, ...).

APPROACHES:
1. Dynamic Programming: dp[i] = min squares to sum to i
2. BFS: Find shortest path from n to 0
3. Mathematical: Use Lagrange's Four Square Theorem

SOLUTION:
We'll implement the DP approach as it's most intuitive, then show
the mathematical approach which is O(√n).
"""

# APPROACH 1: DYNAMIC PROGRAMMING

# STEP 1: Initialize dp array with infinity
# STEP 2: Set base case dp[0] = 0
# STEP 3: For each i, try all perfect squares j² ≤ i
# STEP 4: dp[i] = min(dp[i], dp[i-j²] + 1)

class Solution:
    def numSquares(self, n: int) -> int:
        
        dp = [float('inf')] * (n + 1)                                            # dp[i] = min squares for i
        dp[0] = 0                                                                # Base case: 0 squares for 0
        
        for i in range(1, n + 1):
            
            j = 1
            while j * j <= i:                                                    # Try each perfect square
                dp[i] = min(dp[i], dp[i - j * j] + 1)                            # Take min
                j += 1
        
        return dp[n]


"""
WHY EACH PART:
- dp = [float('inf')] * (n+1): Initialize with "infinity" (haven't found solution yet)
- dp[0] = 0: Zero perfect squares needed to sum to 0
- for i in range(1, n+1): Build solutions for 1, 2, 3, ..., n
- while j * j <= i: Try all perfect squares ≤ i (1, 4, 9, 16, ...)
- dp[i - j*j] + 1: If we use j², we need 1 + (best for remaining)
- min(dp[i], ...): Keep the minimum

HOW IT WORKS (Example: n = 12):

┌─ Building dp array ───────────────────────────────────────┐
│                                                           │
│  i=1:  j=1: dp[1] = min(∞, dp[0]+1) = 1                  │
│                                                           │
│  i=2:  j=1: dp[2] = min(∞, dp[1]+1) = 2                  │
│                                                           │
│  i=3:  j=1: dp[3] = min(∞, dp[2]+1) = 3                  │
│                                                           │
│  i=4:  j=1: dp[4] = min(∞, dp[3]+1) = 4                  │
│        j=2: dp[4] = min(4, dp[0]+1) = 1                  │
│                                                           │
│  i=5:  j=1: dp[5] = min(∞, dp[4]+1) = 2                  │
│        j=2: dp[5] = min(2, dp[1]+1) = 2                  │
│                                                           │
│  ...                                                      │
│                                                           │
│  i=12: j=1: dp[12] = min(∞, dp[11]+1) = 4                │
│        j=2: dp[12] = min(4, dp[8]+1) = 3                 │
│        j=3: dp[12] = min(3, dp[3]+1) = 3 (no change)     │
│                                                           │
│  dp[12] = 3 ✓                                             │
└───────────────────────────────────────────────────────────┘

DP TRANSITION VISUALIZED:

dp[12] = min of:
┌────────────────────────────────────────────────────────────┐
│  • dp[12 - 1²] + 1 = dp[11] + 1 = 3 + 1 = 4              │
│    (use one 1, then best for 11)                          │
│                                                            │
│  • dp[12 - 2²] + 1 = dp[8] + 1 = 2 + 1 = 3   ← BEST      │
│    (use one 4, then best for 8)                           │
│                                                            │
│  • dp[12 - 3²] + 1 = dp[3] + 1 = 3 + 1 = 4               │
│    (use one 9, then best for 3)                           │
│                                                            │
│  Minimum = 3                                               │
└────────────────────────────────────────────────────────────┘

The actual decomposition: 12 = 4 + 4 + 4 (three 4s)
EDGE CASES:
- n = 1: Returns 1 (1 is a perfect square) ✓
- n = 2: Returns 2 (1+1) ✓
- n = 7: Returns 4 (4+1+1+1) ✓
- n = 10000: Returns 1 (100² = 10000) ✓

TIME COMPLEXITY (DP): O(n × √n)
- Outer loop: n iterations
- Inner loop: √n perfect squares to check
- Total: O(n√n)

SPACE COMPLEXITY (DP): O(n)
- dp array of size n+1

CONCEPTS USED:
- Dynamic Programming
- BFS for shortest path
- Number theory (Lagrange's theorem)
- Legendre's three-square theorem
- Perfect squares properties
"""
