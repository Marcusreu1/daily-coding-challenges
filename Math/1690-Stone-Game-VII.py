# 1690. Stone Game VII
# Difficulty: Medium
# https://leetcode.com/problems/stone-game-vii/

"""
PROBLEM:
Alice and Bob take turns playing a game, with Alice starting first.
There are n stones arranged in a row. On each player's turn, they can remove either the leftmost stone or the rightmost stone.
The player receives points equal to the sum of the remaining stones' values in the row.
The game ends when there are no stones left.
Alice's goal is to maximize the difference in score (Alice's score - Bob's score).
Bob's goal is to minimize the difference in score (Alice's score - Bob's score), which means maximizing his own difference.
Return the difference in Alice and Bob's score if they both play optimally.

EXAMPLES:
Input: stones = [5,3,1,4,2] → Output: 6
Explanation:
- Alice removes 2 and gets 5 + 3 + 1 + 4 = 13 points. Alice = 13, Bob = 0, stones = [5,3,1,4].
- Bob removes 5 and gets 3 + 1 + 4 = 8 points. Alice = 13, Bob = 8, stones = [3,1,4].
- Alice removes 4 and gets 3 + 1 = 4 points. Alice = 17, Bob = 8, stones = [3,1].
- Bob removes 3 and gets 1 point. Alice = 17, Bob = 9, stones = [1].
- Alice removes 1 and gets 0 points. Alice = 17, Bob = 9, stones = [].
Score difference: 17 - 9 = 6.

CONSTRAINTS:
- n == stones.length
- 2 <= n <= 1000
- 1 <= stones[i] <= 1000

MATH RULES (MINIMAX & DYNAMIC PROGRAMMING):
Let DP(i, j) be the maximum score difference the current player can achieve from the subarray stones[i...j].
If the player removes the left stone (i), they gain sum(i+1, j). The opponent is left with stones[i+1...j], and will optimally get a difference of DP(i+1, j).
Net difference = sum(i+1, j) - DP(i+1, j).

If the player removes the right stone (j), they gain sum(i, j-1). The opponent gets DP(i, j-1).
Net difference = sum(i, j-1) - DP(i, j-1).

The optimal choice is:
DP(i, j) = max( sum(i+1, j) - DP(i+1, j), sum(i, j-1) - DP(i, j-1) )
"""

from typing import List

# STEP 1: Precompute prefix sums to query subarray sums in O(1) time.
# STEP 2: Initialize a 1D DP array to store the maximum score differences (optimizing space from 2D to 1D).
# STEP 3: Iterate through all possible lengths of the subarray, from 2 up to n.
# STEP 4: Iterate through all possible starting indices (left) for the current length.
# STEP 5: Calculate the score differences for both left and right choices, taking the maximum.
# STEP 6: Return the final evaluated difference at dp[0].

class Solution:
    def stoneGameVII(self, stones: List[int]) -> int:
        
        n = len(stones)
        
        # Calculate prefix sums to quickly get the sum of any subarray
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + stones[i]
            
        def get_sum(left: int, right: int) -> int:
            return prefix_sum[right + 1] - prefix_sum[left]
            
        # dp[left] will store the max difference for a subarray starting at 'left'
        dp = [0] * n
        
        # Build the DP table bottom-up based on subarray lengths
        for length in range(2, n + 1):
            for left in range(n - length + 1):
                right = left + length - 1
                
                # Option 1: Remove the leftmost stone
                score_remove_left = get_sum(left + 1, right) - dp[left + 1]
                
                # Option 2: Remove the rightmost stone
                score_remove_right = get_sum(left, right - 1) - dp[left]
                
                # The current player optimally chooses the maximum difference
                dp[left] = max(score_remove_left, score_remove_right)
                
        return dp[0]

"""
WHY EACH PART:
- prefix_sum array: Calculating the sum of a subarray iteratively takes O(n). With prefix sums, it takes O(1).
- dp = [0] * n: Replaces a 2D matrix DP[i][j]. Since length L only relies on results from length L-1, a 1D array continuously overwritten saves massive amounts of memory.
- score_remove_left / right: It directly implements the Minimax theorem. (My immediate reward) - (Opponent's optimal future reward).

HOW IT WORKS (Example: stones = [3, 1, 4]):

Initial Setup:
Prefix Sums: [0, 3, 4, 8]
dp = [0, 0, 0] (Length 1 subarrays yield 0 points)

Length = 2:
- left=0, right=1 (stones [3, 1]):
  remove left (3): gain sum(1..1)=1 - dp[1]=0 -> 1
  remove right (1): gain sum(0..0)=3 - dp[0]=0 -> 3
  dp[0] = max(1, 3) = 3
  
- left=1, right=2 (stones [1, 4]):
  remove left (1): gain sum(2..2)=4 - dp[2]=0 -> 4
  remove right (4): gain sum(1..1)=1 - dp[1]=0 -> 1
  dp[1] = max(4, 1) = 4
  
dp is now [3, 4, 0]

Length = 3:
- left=0, right=2 (stones [3, 1, 4]):
  remove left (3): gain sum(1..2)=5 - dp[1]=4 -> 1
  remove right (4): gain sum(0..1)=4 - dp[0]=3 -> 1
  dp[0] = max(1, 1) = 1

Return dp[0] -> 1 ✓

KEY TECHNIQUE:
- 1D Dynamic Programming: Reducing spatial complexity from O(n^2) to O(n) by recognizing the sliding dependency window.
- Minimax Algorithm: Reducing a two-player zero-sum game into a single subtraction sequence.

EDGE CASES:
- n = 2: Automatically skips to length 2 evaluation and returns the max immediately.

TIME COMPLEXITY: O(n^2) - We have a nested loop iterating over subarray lengths and starting indices.
SPACE COMPLEXITY: O(n) - We only store 1D arrays for prefix sums and the DP states.

CONCEPTS USED:
- Dynamic Programming (Bottom-Up)
- Minimax Concept
- Prefix Sums
- Space Optimization
"""
