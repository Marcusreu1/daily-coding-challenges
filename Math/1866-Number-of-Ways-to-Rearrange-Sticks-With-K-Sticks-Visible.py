# 1866. Number of Ways to Rearrange Sticks With K Sticks Visible
# Difficulty: Hard
# https://leetcode.com/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/

"""
PROBLEM:
There are n uniquely-sized sticks whose lengths are integers from 1 to n. You want to arrange the sticks such that exactly k sticks are visible from the left.
A stick is visible from the left if there are no longer sticks to the left of it.
For example, if the sticks are arranged [1,3,2,5,4], then the sticks with lengths 1, 3, and 5 are visible from the left.
Given n and k, return the number of such arrangements. Since the answer may be large, return it modulo 10^9 + 7.

EXAMPLES:
Input: n = 3, k = 2 → Output: 3
Explanation: [1,3,2], [2,3,1], and [2,1,3] are the only arrangements such that exactly 2 sticks are visible.

Input: n = 5, k = 5 → Output: 1
Explanation: [1,2,3,4,5] is the only arrangement such that all 5 sticks are visible.

Input: n = 20, k = 11 → Output: 647427950

CONSTRAINTS:
- 1 <= k <= n <= 1000

MATH RULES (STIRLING NUMBERS OF THE FIRST KIND):
We can define our state mathematically. Consider placing the shortest stick (length 1) among 'i' sticks:
Option 1: We place it at the very front. It will definitely be visible. The remaining 'i-1' sticks must form 'j-1' visible sticks. -> dp[i-1][j-1] ways.
Option 2: We place it in any of the other 'i-1' positions. It will definitely be hidden by the sticks to its left. The remaining 'i-1' sticks must form 'j' visible sticks. Since there are 'i-1' positions to hide it, there are -> (i-1) * dp[i-1][j] ways.

Recurrence Relation: DP[i][j] = DP[i-1][j-1] + (i-1) * DP[i-1][j].
We can optimize the O(N*K) space complexity down to O(K) by using a 1D array and traversing backwards.

VISUALIZATION (n = 3, k = 2):
Initial state: dp = [1, 0, 0]

i = 1 (1 stick):
  j = 1: dp[1] = dp[0] + 0 * dp[1] = 1 + 0 = 1
  dp[0] = 0
  dp state = [0, 1, 0]

i = 2 (2 sticks):
  j = 2: dp[2] = dp[1] + 1 * dp[2] = 0 + 1 * 0 = 0 (Wait, dp[1] is 1 -> 1 + 0 = 1)
  j = 1: dp[1] = dp[0] + 1 * dp[1] = 0 + 1 * 1 = 1
  dp[0] = 0
  dp state = [0, 1, 1]

i = 3 (3 sticks):
  j = 2: dp[2] = dp[1] + 2 * dp[2] = 1 + 2 * 1 = 3
  j = 1: dp[1] = dp[0] + 2 * dp[1] = 0 + 2 * 1 = 2
  dp[0] = 0
  dp state = [0, 2, 3]

Return dp[2] -> 3 ✓
"""

# STEP 1: Initialize a 1D DP array of size k + 1 to 0, setting dp[0] = 1 as the mathematical base case.
# STEP 2: Loop through the number of sticks 'i' from 1 to n.
# STEP 3: Loop backwards through the number of visible sticks 'j' from min(i, k) down to 1.
# STEP 4: Apply the Stirling recurrence formula to update dp[j] in-place, applying modulo 10^9 + 7.
# STEP 5: Reset dp[0] to 0 after the first iteration since >0 sticks cannot yield 0 visible sticks.
# STEP 6: Return the evaluated answer at dp[k].

class Solution:
    def rearrangeSticks(self, n: int, k: int) -> int:
        
        MOD = 10**9 + 7
        
        # 1D array to optimize space, dp[j] holds the ways to see exactly j sticks
        dp = [0] * (k + 1)
        
        # Base case: 0 sticks, 0 visible
        dp[0] = 1 
        
        # Iteratively build up to n sticks
        for i in range(1, n + 1):
            
            # Traverse backwards to prevent overwriting values needed for the current step
            # We cap the range at min(i, k) because we can't see more sticks than we have
            for j in range(min(i, k), 0, -1):
                
                visible_if_front = dp[j - 1]
                hidden_if_elsewhere = (i - 1) * dp[j]
                
                dp[j] = (visible_if_front + hidden_if_elsewhere) % MOD
                
            # After we start adding sticks (i > 0), it's impossible to have 0 visible sticks
            dp[0] = 0
            
        return dp[k]

"""
WHY EACH PART:
- dp = [0] * (k + 1): Compresses a matrix into a single row, saving massive amounts of memory.
- min(i, k): Minor optimization to avoid calculating impossible states (e.g., trying to see 5 sticks when we only have 3).
- range(..., 0, -1): Iterating backwards ensures that when calculating dp[j], we are pulling the un-updated, "old" dp[j-1] from the previous row (i-1), strictly enforcing the math logic.

KEY TECHNIQUE:
- 1D Dynamic Programming (Space Optimization): Reducing O(N*K) space to O(K) by leveraging state transition dependencies.
- Combinatorial Recurrence: Using logical deduction on the boundary elements (the shortest stick) to deduce global mathematical formulas.

EDGE CASES:
- k == n: Handled natively. The formula will trace exclusively through dp[j-1], resulting in exactly 1 way to arrange them (sorted ascending).
- k == 1: Traces mostly through the (i-1) * dp[j] path, meaning the tallest stick must be up front, resulting in (n-1)! combinations.

TIME COMPLEXITY: O(N * K) - We process two nested loops, exactly N times for the outer loop and up to K times for the inner loop.
SPACE COMPLEXITY: O(K) - The DP state only stores a single array of size K + 1.

CONCEPTS USED:
- Dynamic Programming (Bottom-Up)
- Stirling Numbers
- Combinatorics
- Space Optimization
"""
