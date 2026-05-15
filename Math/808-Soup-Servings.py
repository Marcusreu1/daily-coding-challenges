# 808. Soup Servings
# Difficulty: Medium
# https://leetcode.com/problems/soup-servings/

"""
PROBLEM:
There are two types of soup: type A and type B. Initially, we have n ml of each type of soup. 
There are four kinds of operations:
1. Serve 100 ml of soup A and 0 ml of soup B.
2. Serve 75 ml of soup A and 25 ml of soup B.
3. Serve 50 ml of soup A and 50 ml of soup B.
4. Serve 25 ml of soup A and 75 ml of soup B.
When we serve some soup, we give it to someone, and we no longer have it. Each turn, we will choose 
from the four operations with an equal probability 0.25. If the remaining volume of soup is not enough 
to complete the operation, we will serve as much as possible.
We stop once we no longer have some quantity of both types of soup.

Return the probability that soup A will be empty first, plus half the probability that A and B become empty at the same time.

EXAMPLES:
Input: n = 50   → Output: 0.62500
Explanation: 
If we choose the first two operations, A will become empty first. The probability is 25% + 25% = 0.5.
If we choose the third operation, A and B will become empty at the same time. The probability is 25% * 0.5 = 0.125.
If we choose the fourth operation, B will become empty first. 
Total probability = 0.5 + 0.125 = 0.625.

CONSTRAINTS:
- 0 <= n <= 10^9
- Answers within 10^-5 of the actual answer will be accepted.

LOGIC RULES (NORMALIZATION & ASYMPTOTIC THRESHOLD):
1. Normalization: All serving quantities are multiples of 25. We can divide n by 25 and use math.ceil 
   to handle remainders. The operations become: (4,0), (3,1), (2,2), (1,3).
2. Probability DP: State (a, b) transitions to 4 different states, each with 0.25 probability.
3. The Math Trick (Asymptotic Threshold): On average, we serve 62.5 ml of A and 37.5 ml of B per turn. 
   Soup A empties much faster. As 'n' grows, the probability of A emptying first approaches 1. 
   When n > 4800, the probability is > 0.99999. We can just return 1.0 to avoid Time Limit Exceeded.

VISUALIZATION (Normalized Operations):
Initial: n = 50 -> ceil(50/25) -> A = 2, B = 2

State (2, 2) branches into 4 possibilities (each 0.25 chance):
├── Ops 1 (4, 0) -> New State (-2, 2). A <= 0. Return 1.0. 
├── Ops 2 (3, 1) -> New State (-1, 1). A <= 0. Return 1.0.
├── Ops 3 (2, 2) -> New State ( 0, 0). A <= 0 & B <= 0. Return 0.5.
└── Ops 4 (1, 3) -> New State ( 1,-1). B <= 0. Return 0.0.

Total = 0.25 * (1.0 + 1.0 + 0.5 + 0.0) = 0.25 * 2.5 = 0.625. ✓
"""

# STEP 1: Implement the math trick for N > 4800 to return 1.0 immediately.
# STEP 2: Normalize the soup volume by dividing by 25 (ceiling).
# STEP 3: Define a recursive DFS function with memoization (lru_cache) to store computed probabilities.
# STEP 4: Define base cases for when soup A, B, or both are depleted.
# STEP 5: Calculate and return the sum of the 4 recursive branches multiplied by 0.25.

import math
from functools import lru_cache

class Solution:
    def soupServings(self, n: int) -> float:
        
        # Step 1: Asymptotic Threshold. If the pot is big enough, A is statistically guaranteed to empty first.
        if n > 4800:
            return 1.0
            
        # Step 2: Normalize sizes to chunks of 25
        n = math.ceil(n / 25.0)
        
        # Step 3: Memoized Depth First Search
        @lru_cache(None)
        def dfs(a: int, b: int) -> float:
            
            # Step 4: Base cases
            if a <= 0 and b <= 0:
                return 0.5                                   # Empty at the exact same time
            if a <= 0:
                return 1.0                                   # Soup A emptied first
            if b <= 0:
                return 0.0                                   # Soup B emptied first
                
            # Step 5: Recursive branching
            return 0.25 * (
                dfs(a - 4, b - 0) +
                dfs(a - 3, b - 1) +
                dfs(a - 2, b - 2) +
                dfs(a - 1, b - 3)
            )
            
        # Initialize the recursion with normalized N for both soups
        return dfs(n, n)

"""
WHY EACH PART:
- n > 4800: Without this, n = 10^9 would require a DP table of size (40,000,000 x 40,000,000), 
  which crashes instantly. This single line turns an impossible problem into an O(1) operation for large inputs.
- math.ceil(n / 25.0): If we have 26 ml, we still need 2 "turns" or "chunks" of 25 to empty it. 
  Ceil perfectly translates real ml into DP discrete chunks.
- @lru_cache(None): Python's built-in memoization decorator. It saves the results of dfs(a, b) so if multiple branches 
  lead to the same state (which they do very often), it retrieves the answer in O(1) time instead of recalculating.
- dfs(a - 4, b - 0)...: Matches the normalized operations perfectly. (100ml = 4 chunks, 75ml = 3 chunks, etc.).

HOW IT WORKS (Example: n = 25):

Normalization: ceil(25 / 25.0) = 1. Start dfs(1, 1).

dfs(1, 1) explores 4 branches:
├── dfs(1-4, 1-0) -> dfs(-3, 1): a <= 0. Returns 1.0.
├── dfs(1-3, 1-1) -> dfs(-2, 0): a <= 0 & b <= 0. Returns 0.5.
├── dfs(1-2, 1-2) -> dfs(-1,-1): a <= 0 & b <= 0. Returns 0.5.
└── dfs(1-1, 1-3) -> dfs( 0,-2): a <= 0 & b <= 0. Returns 0.5.

Total = 0.25 * (1.0 + 0.5 + 0.5 + 0.5) = 0.25 * 2.5 = 0.625. ✓

EDGE CASES:
- n = 0: ceil(0/25) is 0. dfs(0,0) hits first base case, returns 0.5 directly. ✓
- Large numbers like n = 1000000: Bypasses DP entirely, returns 1.0 instantly. ✓

TIME COMPLEXITY: O(1)
Wait, O(1)? Yes! Because the maximum N that will ever enter our DP is 4800. 
4800 / 25 = 192. Our DP table will at most be a 192 x 192 grid. 
Since the grid size is strictly capped at a small constant maximum (192), the time complexity is theoretically O(1).

SPACE COMPLEXITY: O(1)
For the exact same reason. The recursion depth and memoization cache will never exceed a 192 x 192 matrix footprint.
"""
