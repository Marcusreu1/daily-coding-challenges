# 1140. Stone Game II
# Difficulty: Medium
# https://leetcode.com/problems/stone-game-ii/

"""
PROBLEM:
Alice and Bob continue their games with piles of stones. There are a number of piles arranged in a row, 
and each pile has a positive integer number of stones `piles[i]`. The objective is to end with the most stones. 
Alice and Bob take turns, with Alice starting first. Initially, M = 1.
On each player's turn, that player can take all the stones in the first X remaining piles, where 1 <= X <= 2M. 
Then, we set M = max(M, X).
The game continues until all the stones have been taken.
Assuming Alice and Bob play optimally, return the maximum number of stones Alice can get.

EXAMPLES:
Input: piles = [2,7,9,4,4]
Output: 10
Explanation: 
If Alice takes one pile (2), Bob takes two piles (7, 9) and Alice takes the rest (4, 4). Alice gets 2 + 8 = 10.
If Alice takes two piles (2, 7), Bob takes all remaining piles (9, 4, 4). Alice gets 9.
Alice plays optimally, so she takes one pile to maximize her total (10).

CONSTRAINTS:
- 1 <= piles.length <= 100
- 1 <= piles[i] <= 10^4

ALGORITHMIC INTUITION (THE "TRICK"):
This is a classic Game Theory problem that requires the "Minimax" algorithm optimized with 
Dynamic Programming (Memoization).
Since both players play "optimally", every time a player makes a move, they must assume the opponent 
will also make the best possible counter-move.

Instead of simulating both players separately, we can use a universal zero-sum logic:
My Max Score = (Total Stones Remaining) - (Opponent's Max Score in the next turn)

To optimize this, we need two things:
1. Suffix Sum Array: To instantly know the "Total Stones Remaining" from any index `i` to the end in O(1) time.
2. Memoization (Caching): To avoid recalculating the exact same game states (defined by current index `i` and `M`).
"""

# STEP 1: Precompute the suffix sums so we can get the remaining stones in O(1) time.
# STEP 2: Create a memoization dictionary to cache previously calculated states.
# STEP 3: Define a recursive DFS function that represents the maximum stones the CURRENT player can get.
# STEP 4: Base Case 1 -> If we are out of bounds, return 0.
# STEP 5: Base Case 2 -> If we can take all remaining piles (i + 2M >= len), take them all.
# STEP 6: Loop through all possible choices of X (from 1 to 2M).
# STEP 7: Calculate current stones: (Total remaining) - dfs(next_index, new_M).
# STEP 8: Store the maximum possible stones in the memo and return.

from typing import List

class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        
        n = len(piles)
        
        # Step 1: Precompute suffix sums
        # suffix_sum[i] will store the sum of all stones from index i to the end.
        suffix_sum = [0] * n
        suffix_sum[-1] = piles[-1]
        for i in range(n - 2, -1, -1):
            suffix_sum[i] = piles[i] + suffix_sum[i + 1]
            
        memo = {}
        
        # Step 3: DFS function representing a player's turn
        def dfs(i: int, M: int) -> int:
            
            # Step 4: No more piles left
            if i >= n:
                return 0
                
            # Step 5: If the player can take all remaining piles, they definitely should!
            if i + 2 * M >= n:
                return suffix_sum[i]
                
            # Check cache to avoid Time Limit Exceeded (TLE)
            if (i, M) in memo:
                return memo[(i, M)]
                
            max_stones_for_current_player = 0
            
            # Step 6: Explore all valid moves X (1 to 2M)
            for X in range(1, 2 * M + 1):
                
                # The total stones available from index `i` to the end is suffix_sum[i].
                # If we take X piles, the opponent will get dfs(i + X, max(M, X)) stones from the REST of the game.
                # Therefore, our stones = (Total Available) - (Opponent's Future Stones)
                current_stones = suffix_sum[i] - dfs(i + X, max(M, X))
                
                # Step 8: Keep track of the best possible move
                if current_stones > max_stones_for_current_player:
                    max_stones_for_current_player = current_stones
                    
            # Store in cache
            memo[(i, M)] = max_stones_for_current_player
            return max_stones_for_current_player
            
        # Start the game at index 0, with M = 1
        return dfs(0, 1)

"""
WHY EACH PART:
- suffix_sum array: Essential for O(1) mathematical subtraction. Without it, you'd need an O(N) loop to sum remaining stones at every single recursion step.
- Current Score = Total - dfs(...): The elegant core of minimax. You maximize your score by minimizing the opponent's slice of the pie.
- max(M, X): The rule of the game dictates the new M becomes the maximum of the old M and the chosen X.

HOW IT WORKS (Example Walkthrough snippet):
piles = [2, 7, 9, 4, 4], suffix_sum = [26, 24, 17, 8, 4]

Initial Call: dfs(0, 1) -> Alice's turn, M=1. She can pick X=1 or X=2.
├── Option A (X=1): She takes piles[0]=2. Next turn Bob gets dfs(1, 1).
│   └── Bob tries to maximize his stones from [7, 9, 4, 4]. 
│       If Bob plays optimally, he gets 24 - Alice's next turn.
│       It turns out Bob will take (7, 9), leaving Alice with (4, 4).
│       So Bob gets 16. Alice's total for Option A = 26 (total) - 16 (Bob's) = 10.
│
├── Option B (X=2): She takes piles[0,1] = [2, 7] = 9. Next turn Bob gets dfs(2, 2).
│   └── Bob is at index 2, M=2. He can pick up to 2*2=4 piles.
│       Bob simply takes all remaining piles [9, 4, 4] = 17.
│       Alice's total for Option B = 26 (total) - 17 (Bob's) = 9.

Alice compares Option A (10) and Option B (9). She chooses Option A. Returns 10. ✓

TIME COMPLEXITY: O(N^3) - State space is N indices * N possible values of M. For each of the O(N^2) states, the loop runs up to 2M times (which is O(N)). N^2 * N = O(N^3). Since N <= 100, N^3 is 1,000,000, which is very fast.
SPACE COMPLEXITY: O(N^2) - The memoization dictionary will store at most N * N unique states. The recursion stack also goes up to O(N) deep.
"""
