# 1872. Stone Game VIII
# Difficulty: Hard
# https://leetcode.com/problems/stone-game-viii/

"""
PROBLEM:
Alice and Bob take turns playing a game, with Alice starting first.
There are n stones arranged in a row. On each player's turn, while there is more than one stone left:
1. Choose an integer x > 1, and remove the leftmost x stones.
2. Add the sum of the removed stones' values to the player's score.
3. Place a new stone, whose value is equal to that sum, on the left side of the row.
The game stops when only one stone is left in the row.
Both players play optimally to maximize their own score minus the opponent's score.
Return the difference in Alice and Bob's score.

EXAMPLES:
Input: stones = [-1,2,-3,4,-5] → Output: 5
Explanation:
- Alice removes the first 4 stones, adds (-1) + 2 + (-3) + 4 = 2 to her score, and places a stone of value 2 on the left. stones = [2,-5].
- Bob removes the first 2 stones, adds 2 + (-5) = -3 to his score, and places a stone of value -3 on the left. stones = [-3].
The game stops because there is only one stone left.
Alice's score is 2 and Bob's score is -3. Difference: 2 - (-3) = 5.

CONSTRAINTS:
- n == stones.length
- 2 <= n <= 10^5
- -10^4 <= stones[i] <= 10^4

MATH RULES (PREFIX SUM REDUCTION & MINIMAX):
Replacing the first 'x' stones with their sum means the array dynamically shrinks, but the total accumulated sum up to any future point remains exactly the same as the original prefix sums.
Therefore, choosing 'x' stones is mathematically identical to choosing an index 'i' (where 1 <= i < n) in the original prefix sum array.
When you choose 'i', you get prefix_sums[i] points, and the opponent is forced to choose an index 'j' strictly greater than 'i'.

Let dp[i] be the maximum score difference a player can achieve if the game starts at index i.
For any index i, the player has two choices:
1. Pick the current index i: Score difference = prefix_sums[i] - dp[i + 1] (Opponent plays optimally from i+1).
2. Skip the current index i: Score difference = dp[i + 1] (We wait for a better prefix further right).

Thus, dp[i] = max(dp[i+1], prefix_sums[i] - dp[i+1]).

VISUALIZATION (stones = [-1, 2, -3, 4, -5]):
Prefix sums = [-1, 1, -2, 2, -3]

Bottom-Up DP starting from the last valid move:
Base case (i = 4): Must take all remaining. dp = prefix_sums[4] = -3.

i = 3:
- Option 1 (Skip): dp = -3
- Option 2 (Take): prefix_sums[3] - dp = 2 - (-3) = 5
- dp = max(-3, 5) = 5

i = 2:
- Option 1 (Skip): dp = 5
- Option 2 (Take): prefix_sums[2] - dp = -2 - 5 = -7
- dp = max(5, -7) = 5

i = 1 (First valid move, x > 1 stones):
- Option 1 (Skip): dp = 5
- Option 2 (Take): prefix_sums[1] - dp = 1 - 5 = -4
- dp = max(5, -4) = 5

Alice's max difference is 5 ✓
"""

from typing import List
import itertools

# STEP 1: Compute the prefix sums of the stones array.
# STEP 2: Initialize the DP variable with the value of taking the entire array (the last prefix sum).
# STEP 3: Iterate backward from the second to last element down to index 1.
# STEP 4: At each step, update the DP variable by choosing the maximum between skipping or taking the current prefix.
# STEP 5: Return the DP variable which now holds the optimal strategy score difference.

class Solution:
    def stoneGameVIII(self, stones: List[int]) -> int:
        
        n = len(stones)
        
        # Calculate prefix sums to evaluate the value of any move in O(1)
        prefix_sums = [0] * n
        prefix_sums[0] = stones[0]
        for i in range(1, n):
            prefix_sums[i] = prefix_sums[i - 1] + stones[i]
            
        # The base case: taking all remaining stones
        dp = prefix_sums[-1]
        
        # Traverse backward to build the optimal minimax choices
        # We stop at 1 because x > 1 means at least 2 stones must be taken
        for i in range(n - 2, 0, -1):
            
            # max(Option 1: Skip, Option 2: Take and subtract opponent's future optimal score)
            dp = max(dp, prefix_sums[i] - dp)
            
        return dp

"""
WHY EACH PART:
- prefix_sums[i] = prefix_sums[i-1] + stones[i]: Standard O(N) precalculation that transforms the dynamic array merging rule into a static lookup table.
- dp = prefix_sums[-1]: If the game reaches the last index, the current player has no choice but to take all remaining stones, instantly earning the total sum and leaving the opponent with no moves (0 points).
- max(dp, prefix_sums[i] - dp): Implements the Minimax decision theory. 'dp' represents the best outcome of skipping, 'prefix_sums[i] - dp' represents the net gain of acting now.
- range(n - 2, 0, -1): Iterating backwards naturally resolves the future dependencies of the DP formula. Stopping at 0 enforces the rule that 1 stone cannot be picked alone.

KEY TECHNIQUE:
- Game Theory Reduction: Realizing that compounding sums is logically equivalent to selecting prefix sums.
- Space Optimization (1D DP): Instead of using an O(N) DP array, a single variable `dp` is repeatedly overwritten since we only ever need the immediately preceding state (dp[i+1]).

EDGE CASES:
- n = 2: The loop doesn't execute (range from 0 to 0). The DP variable simply returns prefix_sums[1], as the only legal move is taking both stones.

TIME COMPLEXITY: O(N) - One pass to compute the prefix sums and one reverse pass to calculate the optimal strategy.
SPACE COMPLEXITY: O(N) - Used for the prefix_sums array. (Can technically be done in O(1) if we overwrite the original stones array).

CONCEPTS USED:
- Dynamic Programming
- Minimax Algorithm
- Prefix Sums
- Game Theory Optimization
"""
