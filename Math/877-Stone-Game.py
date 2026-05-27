# 877. Stone Game
# Difficulty: Medium
# https://leetcode.com/problems/stone-game/

"""
PROBLEM:
Alice and Bob play a game with piles of stones. There are an EVEN number of piles arranged in a row, 
and each pile has a positive integer number of stones `piles[i]`.
The objective of the game is to end with the most stones. The total number of stones across 
all piles is ODD, so there are no ties.
Alice and Bob take turns, with Alice starting first. Each turn, a player takes the entire pile 
of stones either from the beginning or from the end of the row. 
Return `true` if Alice wins the game (assuming both play optimally), or `false` if Bob wins.

EXAMPLES:
Input: piles = [5,3,4,5]
Output: true
Explanation: 
Alice starts and can take 5 from the left or 5 from the right. If she takes the 5 on the left, 
the row becomes [3, 4, 5]. Bob might take the 5 on the right, leaving [3, 4]. Alice takes the 4, 
Bob takes the 3. Alice wins 9 to 8.

CONSTRAINTS:
- 2 <= piles.length <= 500
- piles.length is even.
- 1 <= piles[i] <= 500
- sum(piles) is odd.

THE "TRICK" (MATHEMATICAL GAME THEORY):
This problem contains a brilliant mathematical loophole based on the constraints:
1. The number of piles is EVEN.
2. The total sum is ODD (no ties).

Because the array has an even length, we can conceptually color the piles into alternating 
EVEN and ODD indices: [Even, Odd, Even, Odd, ..., Even, Odd].
Since the total sum is odd, the sum of all 'Even' index piles will NEVER equal the sum of 
all 'Odd' index piles. One sum is strictly greater than the other.

Because Alice goes first, she controls the parity of the game:
- If she wants all Even-indexed piles, she takes the pile at index 0. This forces Bob to choose 
  between index 1 and index N-1 (both Odd). Whichever he picks, he exposes another Even index for Alice.
- If she wants all Odd-indexed piles, she takes the pile at index N-1. This forces Bob to pick 
  an Even index, exposing another Odd index for Alice.


SOLUTION: The O(N^2) Dynamic Programming Approach (Minimax)
In a real interview, you must explain the math trick, but the interviewer might ask: 
"What if the number of piles was odd? Or what if ties were possible? Write the general solution."

We use a 2D DP table where dp[i][j] represents the maximum relative score (My Score - Opponent Score) 
a player can achieve from the subarray piles[i...j].

dp[i][j] = max(
    piles[i] - dp[i+1][j],  // Take the left pile, minus the best the opponent can do with the rest
    piles[j] - dp[i][j-1]   // Take the right pile, minus the best the opponent can do with the rest
)

If dp[0][N-1] > 0, Alice wins.
"""

class SolutionDP:
    def stoneGame(self, piles: List[int]) -> bool:
        n = len(piles)
        
        # dp[i][j] stores the max net score a player can get from piles[i] to piles[j]
        dp = [[0] * n for _ in range(n)]
        
        # Base case: subarray of length 1 (i == j). The player takes that single pile.
        for i in range(n):
            dp[i][i] = piles[i]
            
        # Build the table diagonally (length of subarray from 2 to n)
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                # Player chooses left or right, subtracting the opponent's best future net score
                take_left = piles[i] - dp[i + 1][j]
                take_right = piles[j] - dp[i][j - 1]
                
                dp[i][j] = max(take_left, take_right)
                
        # If the net score over the entire array is positive, the first player (Alice) wins.
        return dp[0][n - 1] > 0

"""
WHY EACH PART (DP Solution):
- dp[i][j]: Represents the zero-sum nature of the game. It calculates the maximum difference in scores.
- piles[i] - dp[i+1][j]: If Alice takes `piles[i]`, she gains those points. But Bob is now playing optimally on the subarray `piles[i+1...j]`. Bob's best net score on that subarray is `dp[i+1][j]`. Since it's a zero-sum game, Bob's gain is Alice's loss, hence the subtraction.

TIME COMPLEXITY: 
- Mathematical approach: O(1)
- DP approach: O(N^2) because we fill an N x N matrix.
SPACE COMPLEXITY: 
- Mathematical approach: O(1)
- DP approach: O(N^2) to store the DP table. (Can be optimized to O(N) by only storing the previous row).

CONCEPTS USED:
- Game Theory (Dominant Strategy & Parity)
- Dynamic Programming
- Minimax Algorithm (Zero-Sum Games)
"""
