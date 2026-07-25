# 1406. Stone Game III
# Difficulty: Hard
# https://leetcode.com/problems/stone-game-iii/

"""
PROBLEM:
Alice and Bob continue their games with piles of stones. There is an array of integers `stoneValue`.
Alice and Bob take turns, with Alice starting first. On each player's turn, that player can take 
1, 2, or 3 stones from the first remaining stones in the row.
The score of each player is the sum of the values of the stones taken. The score of each player is 0 initially.
The objective of the game is to end with the highest score, and the winner is the player with the highest score.
Assuming Alice and Bob play optimally, return "Alice" if Alice will win, "Bob" if Bob will win, or "Tie" if they will end the game with the same score.

EXAMPLES:
Input: stoneValue = [1,2,3,7]
Output: "Bob"
(Explanation: Alice will always lose. Her best move will be to take three piles and the score become 6. Now the row of stones is [7]. Bob takes it and wins 7 to 6.)

Input: stoneValue = [1,2,3,-9]
Output: "Alice"
(Explanation: Alice must choose all the three piles at the first move to win and leave Bob with the negative pile. If she chooses one pile her score will be 1 and the next move Bob's score becomes 5. That way Alice will lose.)

Input: stoneValue = [1,2,3,6]
Output: "Tie"

CONSTRAINTS:
- 1 <= stoneValue.length <= 50000
- -1000 <= stoneValue[i] <= 1000

ALGORITHM LOGIC (Game Theory Minimax & Suffix Dynamic Programming):
1. In a zero-sum game played optimally, maximizing one's own score is equivalent to maximizing the difference between one's score and the opponent's score.
2. Let dp[i] be the maximum score difference the current player can achieve starting from index `i`.
3. If the player takes `k` stones (where k is 1, 2, or 3), they gain the sum of those `k` stones.
4. However, the game transitions to index `i + k`, and it becomes the opponent's turn. The opponent will play optimally, securing a score difference of dp[i + k] relative to the current player.
5. Therefore, the net score difference for taking `k` stones is:
   (Sum of k stones) - dp[i + k]
6. We calculate this backwards from the end of the array to the beginning.
7. The result at dp[0] reveals the final score difference for Alice. If it's > 0, Alice wins. If < 0, Bob wins. Otherwise, it's a tie.

VISUALIZATION (stoneValue = [1, 2, 3, 7]):
dp array initialized to -inf. Base case dp[4] = 0.

i = 3 (Value: 7): 
- Take 1: 7 - dp[4] = 7 - 0 = 7. 
dp[3] = 7. (If Bob starts here, he gets 7).

i = 2 (Value: 3):
- Take 1 (3): 3 - dp[3] = 3 - 7 = -4.
- Take 2 (3, 7): 10 - dp[4] = 10 - 0 = 10.
dp[2] = max(-4, 10) = 10.

i = 1 (Value: 2):
- Take 1 (2): 2 - dp[2] = 2 - 10 = -8.
- Take 2 (2, 3): 5 - dp[3] = 5 - 7 = -2.
- Take 3 (2, 3, 7): 12 - dp[4] = 12 - 0 = 12.
dp[1] = max(-8, -2, 12) = 12.

i = 0 (Value: 1):
- Take 1 (1): 1 - dp[1] = 1 - 12 = -11.
- Take 2 (1, 2): 3 - dp[2] = 3 - 10 = -7.
- Take 3 (1, 2, 3): 6 - dp[3] = 6 - 7 = -1.
dp[0] = max(-11, -7, -1) = -1.

dp[0] is -1. Bob wins. ✓
"""

import math

# STEP 1: Initialize the DP array with negative infinity, size N + 1
# STEP 2: Set the base case dp[N] = 0 (No stones left means 0 score difference)
# STEP 3: Iterate backwards from N-1 down to 0
# STEP 4: In each state, evaluate taking 1, 2, or 3 stones, keeping a running sum of the taken stones
# STEP 5: Apply the Minimax formula: max(current_max, taken_stones - dp[i + k])
# STEP 6: Evaluate dp[0] to determine the winner

class Solution:
    def stoneGameIII(self, stoneValue: list[int]) -> str:
        
        n = len(stoneValue)
        dp = [-math.inf] * (n + 1)                                   # Represents the max relative score advantage
        dp[n] = 0                                                    # Base case: 0 advantage when no stones exist
        
        for i in range(n - 1, -1, -1):                               # Suffix DP: Work backwards
            
            take_sum = 0
            
            # The current player can take 1, 2, or 3 stones (k represents the offset)
            for k in range(1, 4):
                if i + k - 1 < n:                                    # Ensure we don't grab stones out of bounds
                    take_sum += stoneValue[i + k - 1]                # Accumulate the value of the stones taken
                    
                    # Update DP: My optimal move is the max of my current stones minus the opponent's future advantage
                    dp[i] = max(dp[i], take_sum - dp[i + k])
                    
        # dp[0] holds Alice's max score difference playing perfectly from the start
        if dp[0] > 0:
            return "Alice"
        elif dp[0] < 0:
            return "Bob"
        else:
            return "Tie"

"""
WHY EACH PART:
- dp = [-math.inf] * (n + 1): Negative infinity is required because stones can have negative values. Initializing with 0 would incorrectly mask valid negative optimal paths.
- for k in range(1, 4): Simulates the rules of the game explicitly (take 1, 2, or 3 stones).
- take_sum += stoneValue[i + k - 1]: Instead of recalculating `sum(stoneValue[i:i+k])` which takes O(k) time, we dynamically accumulate it in O(1) time as the loop progresses.
- take_sum - dp[i + k]: The core game theory principle. What I take `take_sum` is penalized by the best advantage my opponent will secure from the remaining board `dp[i + k]`.

HOW IT WORKS (Math logic):
If the array is [1, 2, 3, -9], working backwards guarantees that when evaluating index 0 (Alice's start), Alice already knows that leaving Bob at index 3 (where the -9 is) forces Bob to take -9. 
Alice taking 3 stones (1+2+3 = 6) leaves Bob at index 3. 
Alice's net = 6 - (-9) = 15. Alice easily wins.

KEY TECHNIQUE:
- Game Theory (Minimax Algorithm)
- Suffix Dynamic Programming (Backward State Evaluation)
- State Reduction (Tracking difference instead of two absolute scores)

EDGE CASES:
- Only one stone exists: Handled flawlessly. The `k` loop runs once, then limits out of bounds. ✓
- All negative stones (e.g., [-1, -2, -3]): The algorithm will expertly take only -1 to force the opponent into worse negatives. ✓

TIME COMPLEXITY: O(N) - We iterate backward through the array of N stones. At each step, we do a maximum of 3 constant-time operations. O(3 * N) simplifies to O(N).
SPACE COMPLEXITY: O(N) - We use an array of size N + 1. (Note: This can technically be optimized to O(1) by only keeping track of the last 3 DP states, but an array O(N) is infinitely more readable for educational documentation without failing any system constraints).
"""
