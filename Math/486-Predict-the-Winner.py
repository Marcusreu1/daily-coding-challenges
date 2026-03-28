"""
486. Predict the Winner
Difficulty: Medium
https://leetcode.com/problems/predict-the-winner/

PROBLEM:
    Two players take turns picking numbers from EITHER END of an integer array.
    Each number picked is added to that player's score.
    Player 1 always goes first. Both players play OPTIMALLY.
    Return true if Player 1 can win or tie (score1 >= score2).

EXAMPLES:
    Input: nums = [1,5,2]       → Output: false
        Player 1 picks 1 → Player 2 picks 5 → Player 1 picks 2
        Score: P1=3, P2=5 → Player 1 loses (no matter what P1 does)

    Input: nums = [1,5,233,7]   → Output: true
        Player 1 picks 7 → Player 2 picks 1 → Player 1 picks 233 → Player 2 picks 5
        Score: P1=240, P2=6 → Player 1 wins

CONSTRAINTS:
    1 <= nums.length <= 20
    0 <= nums[i] <= 10^7

KEY INSIGHT:
    This is a MINIMAX game theory problem.
    Instead of tracking both scores separately, we track the
    ADVANTAGE (score difference) of the CURRENT player.

    dp[i][j] = maximum advantage (my_score - opponent_score)
               the CURRENT player can achieve from subarray nums[i..j]

    "Current player" changes each turn — that's the magic!

CHALLENGES:
    Understanding the "perspective switch" between turns
    Why we SUBTRACT dp values (opponent's advantage = my disadvantage)
    Filling the DP table in correct order (small subarrays first)

THE SUBTRACTION TRICK:
    When I pick nums[i], I gain nums[i] points.
    Then it's OPPONENT'S turn on nums[i+1..j].
    Opponent's best advantage on that subarray = dp[i+1][j]

    But opponent's advantage is MY disadvantage!
    So MY advantage = nums[i] - dp[i+1][j]

    Think of it like this:
    ┌──────────────────────────────────────────────┐
    │  I pick nums[i] → I gain nums[i]             │
    │  Opponent plays optimally on what's left      │
    │  Opponent's advantage = dp[i+1][j]            │
    │  My total advantage = nums[i] - dp[i+1][j]   │
    │                        ↑ my gain   ↑ their    │
    │                                      future   │
    │                                      edge     │
    └──────────────────────────────────────────────┘

SOLUTION:
    Use bottom-up DP on subarrays of increasing length.
    For each subarray [i..j], the current player picks the
    option (left or right) that MAXIMIZES their advantage.
    Player 1 wins if dp[0][n-1] >= 0.
"""


# STEP 1: Handle base case (n <= 2 → Player 1 always wins)
# STEP 2: Initialize dp[i][i] = nums[i] (single element → take it)
# STEP 3: Fill DP by subarray length (small → large)
# STEP 4: For each subarray, try picking left or right, take max advantage
# STEP 5: Check if Player 1's advantage >= 0


class Solution:
    def predictTheWinner(self, nums: List[int]) -> bool:

        n = len(nums)

        if n <= 2:                                                    # P1 picks the larger, always wins/ties
            return True

        dp = [[0] * n for _ in range(n)]                              # dp[i][j] = max advantage on nums[i..j]

        for i in range(n):                                            # Base case: one element left
            dp[i][i] = nums[i]                                        # Current player takes it, advantage = nums[i]

        for length in range(2, n + 1):                                # Subarray lengths: 2, 3, ..., n
            for i in range(n - length + 1):                           # Start index of subarray
                j = i + length - 1                                    # End index of subarray

                pick_left  = nums[i] - dp[i + 1][j]                  # Pick left:  gain nums[i], opponent gets [i+1..j]
                pick_right = nums[j] - dp[i][j - 1]                  # Pick right: gain nums[j], opponent gets [i..j-1]

                dp[i][j] = max(pick_left, pick_right)                 # Current player picks the BEST option

        return dp[0][n - 1] >= 0                                     # Player 1 wins if advantage >= 0


"""
WHY EACH PART:
    n <= 2:              With 1-2 elements, Player 1 picks optimally and always wins/ties
    dp[i][i] = nums[i]:  Only one element in subarray → current player takes it, that's their advantage
    length loop:          We must solve smaller subarrays BEFORE larger ones (bottom-up dependency)
    nums[i] - dp[i+1][j]: "I gain nums[i], then opponent has advantage dp[i+1][j] against me"
    max(left, right):     Current player plays OPTIMALLY → picks the better option
    dp[0][n-1] >= 0:      Player 1 starts with full array; wins if advantage is non-negative


HOW IT WORKS (Example: nums = [1, 5, 2]):

    Step 1 — Base cases (length = 1):
    dp[0][0] = 1,  dp[1][1] = 5,  dp[2][2] = 2

    Step 2 — Length = 2:
    dp[0][1]: subarray [1, 5]
    ├── Pick left (1):  1 - dp[1][1] = 1 - 5 = -4
    ├── Pick right (5): 5 - dp[0][0] = 5 - 1 =  4
    └── dp[0][1] = max(-4, 4) = 4

    dp[1][2]: subarray [5, 2]
    ├── Pick left (5):  5 - dp[2][2] = 5 - 2 = 3
    ├── Pick right (2): 2 - dp[1][1] = 2 - 5 = -3
    └── dp[1][2] = max(3, -3) = 3

    Step 3 — Length = 3:
    dp[0][2]: subarray [1, 5, 2]  ← THIS IS THE FULL ARRAY
    ├── Pick left (1):  1 - dp[1][2] = 1 - 3 = -2
    ├── Pick right (2): 2 - dp[0][1] = 2 - 4 = -2
    └── dp[0][2] = max(-2, -2) = -2

    dp[0][2] = -2 < 0 → Player 1 CANNOT win → return false ✓

    Visual of the DP table:
    ┌─────┬───────┬───────┬───────┐
    │ i\j │   0   │   1   │   2   │
    ├─────┼───────┼───────┼───────┤
    │  0  │   1   │   4   │  -2   │  ← answer at dp[0][2]
    │  1  │       │   5   │   3   │
    │  2  │       │       │   2   │
    └─────┴───────┴───────┴───────┘


HOW IT WORKS (Example: nums = [1, 5, 233, 7]):

    Base cases: dp[0][0]=1, dp[1][1]=5, dp[2][2]=233, dp[3][3]=7

    Length = 2:
    dp[0][1] = max(1-5, 5-1)     = max(-4, 4)     = 4
    dp[1][2] = max(5-233, 233-5) = max(-228, 228)  = 228
    dp[2][3] = max(233-7, 7-233) = max(226, -226)  = 226

    Length = 3:
    dp[0][2] = max(1-228, 233-4)    = max(-227, 229) = 229
    dp[1][3] = max(5-226, 7-228)    = max(-221, -221) = -221

    Length = 4:
    dp[0][3] = max(1-(-221), 7-229) = max(222, -222)  = 222

    dp[0][3] = 222 >= 0 → Player 1 WINS → return true ✓


WHY THE SUBTRACTION TRICK WORKS:
    Imagine a simpler game: [3, 9, 1]

    It's MY turn. I can pick 3 (left) or 1 (right).
    If I pick 3:
        Opponent faces [9, 1] → opponent's advantage = dp = 8
        That means opponent outscores me by 8 in the remaining game
        My total advantage: 3 - 8 = -5  (I lose by 5)

    If I pick 1:
        Opponent faces [3, 9] → opponent's advantage = dp = 6
        My total advantage: 1 - 6 = -5  (I lose by 5)

    Either way I lose — makes sense because opponent gets 9!


WHY n <= 2 IS ALWAYS TRUE:
    n = 1: Player 1 takes the only element → wins trivially
    n = 2: Player 1 picks max(nums[0], nums[1]) → always >= half the total


HANDLING SPECIAL CASES:
    All equal elements:  dp values balance to 0 → P1 ties → return true ✓
    Single element:      P1 takes it → return true ✓
    Two elements:        P1 picks larger → return true ✓
    Descending array:    P1 picks largest first → wins ✓


KEY TECHNIQUE:
    Minimax DP:          Model zero-sum games with advantage tracking
    Perspective switch:   dp[i][j] is ALWAYS from "current player" view
    Subtraction trick:    Opponent's gain = my loss → subtract their dp
    Bottom-up filling:    Solve small subarrays before large ones


EDGE CASES:
    Single element [5]:       P1 takes 5 → true ✓
    Two elements [1, 2]:      P1 takes 2 → true ✓
    All zeros [0,0,0]:        Tie → true ✓
    P1 guaranteed loss [1,5,2]: Returns false ✓
    Large values:             Integers handle up to 10^7 × 20 = 2×10^8 → no overflow ✓


TIME COMPLEXITY: O(n²)
    We fill n×n/2 cells of the DP table
    Each cell computed in O(1)

SPACE COMPLEXITY: O(n²)
    The n×n DP table
    (Can be optimized to O(n) with 1D DP, but clarity > optimization here)


CONCEPTS USED:
    Game theory (minimax)
    Dynamic programming (2D, bottom-up)
    Optimal substructure (subarray decomposition)
    Perspective switching (current player abstraction)
    Zero-sum game modeling
"""
