"""
375. Guess Number Higher or Lower II
Difficulty: Medium
https://leetcode.com/problems/guess-number-higher-or-lower-ii/

PROBLEM:
We are playing the Guessing Game:
- I pick a number between 1 and n
- You guess a number
- If wrong, I tell you if it's higher or lower
- Each wrong guess k costs you $k
- Find minimum money to GUARANTEE a win (worst-case)

EXAMPLES:
Input: n = 10 → Output: 16
Input: n = 1 → Output: 0
Input: n = 2 → Output: 1

CONSTRAINTS:
• 1 <= n <= 200

KEY INSIGHT - MINIMAX:
This is a game theory problem:
- WE want to MINIMIZE cost
- The "universe" gives us the WORST case (maximizes our cost)

We choose the guess that MINIMIZES the WORST-CASE cost.

DP DEFINITION:
dp[i][j] = minimum money to GUARANTEE win if number is in [i, j]

TRANSITION:
For each possible guess k in [i, j]:
    cost_k = k + max(dp[i][k-1], dp[k+1][j])
             ↑        ↑            ↑
        cost if   search left   search right
        wrong     (number < k)  (number > k)
    
    dp[i][j] = min(cost_k) for all k in [i, j]

BASE CASE:
dp[i][i] = 0 (only one number, guess it for free)
dp[i][j] = 0 if i > j (invalid range)

ANSWER: dp[1][n]
"""


# ============================================================================
# SOLUTION 1: BOTTOM-UP DP (Iterative)
# ============================================================================

class Solution:
    def getMoneyAmount(self, n: int) -> int:
        
        # dp[i][j] = min cost to guarantee win for range [i, j]
        dp = [[0] * (n + 2) for _ in range(n + 2)]
        
        # Fill by increasing range length
        for length in range(2, n + 1):                           # Range length: 2 to n
            for i in range(1, n - length + 2):                   # Start of range
                j = i + length - 1                                # End of range
                
                dp[i][j] = float('inf')
                
                for k in range(i, j + 1):                        # Try each guess k
                    # Cost = k (if wrong) + worst of left/right
                    left = dp[i][k - 1] if k > i else 0
                    right = dp[k + 1][j] if k < j else 0
                    cost = k + max(left, right)
                    
                    dp[i][j] = min(dp[i][j], cost)
        
        return dp[1][n]


# ============================================================================
# SOLUTION 2: TOP-DOWN DP (Memoization)
# ============================================================================

from functools import lru_cache


class Solution:
    def getMoneyAmount(self, n: int) -> int:
        
        @lru_cache(maxsize=None)
        def dp(i: int, j: int) -> int:
            """Min cost to guarantee win if number is in [i, j]"""
            
            if i >= j:                                           # Base case: 0 or 1 number
                return 0
            
            min_cost = float('inf')
            
            for k in range(i, j + 1):                            # Try each guess
                # k + worst case of left/right subproblems
                cost = k + max(dp(i, k - 1), dp(k + 1, j))
                min_cost = min(min_cost, cost)
            
            return min_cost
        
        return dp(1, n)


# ============================================================================
# SOLUTION 3: OPTIMIZED - BETTER GUESS RANGE
# ============================================================================

class Solution:
    def getMoneyAmount(self, n: int) -> int:
        
        dp = [[0] * (n + 2) for _ in range(n + 2)]
        
        for length in range(2, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                
                # Optimization: don't need to try all k
                # Best k is usually around j - (j-i)//3 due to cost asymmetry
                dp[i][j] = float('inf')
                
                for k in range(i, j + 1):
                    left = dp[i][k - 1]
                    right = dp[k + 1][j]
                    cost = k + max(left, right)
                    dp[i][j] = min(dp[i][j], cost)
                    
                    # Early termination: if left > right, costs will only increase
                    if left >= right:
                        break
        
        return dp[1][n]


# ============================================================================
# SOLUTION 4: CLEANER IMPLEMENTATION
# ============================================================================

class Solution:
    def getMoneyAmount(self, n: int) -> int:
        
        if n == 1:
            return 0
        
        # dp[i][j] = min cost to find number in range [i, j]
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Build solution for increasingly larger ranges
        for size in range(2, n + 1):                             # Size of range
            for left in range(1, n - size + 2):                  # Left boundary
                right = left + size - 1                           # Right boundary
                
                dp[left][right] = float('inf')
                
                # Try every possible first guess
                for guess in range(left, right + 1):
                    # Cost if we guess wrong
                    cost_if_lower = dp[left][guess - 1] if guess > left else 0
                    cost_if_higher = dp[guess + 1][right] if guess < right else 0
                    
                    # Total cost = guess value + worst case
                    total_cost = guess + max(cost_if_lower, cost_if_higher)
                    
                    dp[left][right] = min(dp[left][right], total_cost)
        
        return dp[1][n]


"""
HOW IT WORKS (Detailed Trace for n = 4):

Initialize: dp[i][i] = 0 for all i

═══════════════════════════════════════════════════════════════════
LENGTH 2 (ranges of size 2):
═══════════════════════════════════════════════════════════════════

dp[1][2]: range {1, 2}
    guess 1: 1 + max(dp[0][0], dp[2][2]) = 1 + max(0, 0) = 1
    guess 2: 2 + max(dp[1][1], dp[3][2]) = 2 + max(0, 0) = 2
    dp[1][2] = min(1, 2) = 1

dp[2][3]: range {2, 3}
    guess 2: 2 + max(0, 0) = 2
    guess 3: 3 + max(0, 0) = 3
    dp[2][3] = min(2, 3) = 2

dp[3][4]: range {3, 4}
    guess 3: 3 + max(0, 0) = 3
    guess 4: 4 + max(0, 0) = 4
    dp[3][4] = min(3, 4) = 3

═══════════════════════════════════════════════════════════════════
LENGTH 3 (ranges of size 3):
═══════════════════════════════════════════════════════════════════

dp[1][3]: range {1, 2, 3}
    guess 1: 1 + max(0, dp[2][3]) = 1 + max(0, 2) = 3
    guess 2: 2 + max(dp[1][1], dp[3][3]) = 2 + max(0, 0) = 2  
    guess 3: 3 + max(dp[1][2], 0) = 3 + max(1, 0) = 4
    dp[1][3] = min(3, 2, 4) = 2

dp[2][4]: range {2, 3, 4}
    guess 2: 2 + max(0, dp[3][4]) = 2 + max(0, 3) = 5
    guess 3: 3 + max(dp[2][2], dp[4][4]) = 3 + max(0, 0) = 3  
    guess 4: 4 + max(dp[2][3], 0) = 4 + max(2, 0) = 6
    dp[2][4] = min(5, 3, 6) = 3

═══════════════════════════════════════════════════════════════════
LENGTH 4 (ranges of size 4):
═══════════════════════════════════════════════════════════════════

dp[1][4]: range {1, 2, 3, 4}
    guess 1: 1 + max(0, dp[2][4]) = 1 + 3 = 4
    guess 2: 2 + max(dp[1][1], dp[3][4]) = 2 + max(0, 3) = 5
    guess 3: 3 + max(dp[1][2], dp[4][4]) = 3 + max(1, 0) = 4  
    guess 4: 4 + max(dp[1][3], 0) = 4 + max(2, 0) = 6
    dp[1][4] = min(4, 5, 4, 6) = 4

ANSWER: dp[1][4] = 4 ✓

═══════════════════════════════════════════════════════════════════

WHY MINIMAX?
┌────────────────────────────────────────────────────────────────┐
│  We control: which number to guess                             │
│  We don't control: what the actual number is                   │
│                                                                │
│  We must GUARANTEE a win, so we assume worst case:             │
│  - For each guess k, the number will be in the more           │
│    expensive half (the max of left and right costs)            │
│                                                                │
│  We then MINIMIZE over our choice of guess k                   │
│  → We pick the k that gives smallest worst-case                │
└────────────────────────────────────────────────────────────────┘

WHY COST IS ASYMMETRIC:
┌────────────────────────────────────────────────────────────────┐
│  Range [3, 4] costs 3 (guess 3, worst case pay 3)             │
│  Range [1, 2] costs 1 (guess 1, worst case pay 1)             │
│                                                                │
│  Even though both have 2 elements, [3,4] is more expensive!   │
│  Because wrong guesses cost more (3 > 1, 4 > 2)               │
│                                                                │
│  This is why picking the middle isn't always optimal!         │
│  Better to "fail" on smaller numbers if possible.             │
└────────────────────────────────────────────────────────────────┘

VISUAL DECISION TREE (n = 3, optimal strategy):
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                        Guess 2                                 │
│                       /   |   \                               │
│                     1     2     3                              │
│                   (pay 2) (win) (pay 2)                       │
│                    /               \                           │
│               Guess 1            Guess 3                       │
│                (win)              (win)                        │
│                                                                │
│  Worst case: 2 (either path pays at most 2)                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  n = 1  →  0 (only one number, guess it free)                 │
│  n = 2  →  1 (guess 1: if wrong, guess 2; cost = 1)          │
│  n = 3  →  2 (guess 2: if wrong, one number left; cost = 2)  │
│  n = 10 →  16                                                  │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(n³)
├── O(n²) subproblems (all pairs i, j)
├── O(n) choices per subproblem (each k)
└── Total: O(n³)

SPACE COMPLEXITY: O(n²)
├── dp table of size n × n
└── Total: O(n²)

OPTIMIZATION:
The inner loop can be optimized. The optimal k tends to be
biased toward the higher end (due to cost asymmetry).
With careful analysis, can achieve O(n²) but O(n³) is acceptable.


CONCEPTS USED:
• Game Theory (Minimax)
• Interval DP
• Worst-Case Analysis
• Decision Trees
"""
