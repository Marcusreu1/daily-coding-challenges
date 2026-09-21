# 1927. Sum Game
# Difficulty: Medium
# https://leetcode.com/problems/sum-game/

"""
PROBLEM:
Alice and Bob play a game on a string of even length `num`, consisting of digits and '?'.
Alice and Bob take turns to replace a '?' with a digit from '0' to '9'. Alice plays first.
- Alice wins if the sum of the first half of the string is NOT equal to the sum of the second half.
- Bob wins if the sum of the first half is EQUAL to the sum of the second half.
Return true if Alice wins, assuming both players play optimally, otherwise return false.

EXAMPLES:
Input: num = "5023" → Output: false
Explanation: There are no '?' characters. The left half sum is 5 + 0 = 5. The right half sum is 2 + 3 = 5. They are equal, so Bob wins (return false).

Input: num = "25??" → Output: true
Explanation: Alice can replace the first '?' with '9'. The string becomes "259?".
Left sum is 7. Right sum is currently 9. No matter what Bob plays, the right sum will be at least 9, which is != 7. Alice wins.

Input: num = "?3295???" → Output: false
Explanation: Bob can maintain equality by matching Alice's moves mathematically.

CONSTRAINTS:
- 2 <= num.length <= 10^5
- num.length is even.
- num consists of only digits and '?'.

MATH RULES (GAME THEORY & PAIRING STRATEGY):
Instead of simulating the game tree, we use a combinatorial invariant.
1. Turn Advantage: If the total number of '?' is odd, Alice gets the final move. She can always choose a digit that breaks any balance Bob tried to create. Alice immediately wins.
2. Neutralization (Bob's Pairing): If the total '?' is even, Bob gets the last move. Bob will use a pairing strategy:
   - If Alice plays on one side and there is a '?' on the other side, Bob mimics her digit 'x'. Net difference: 0.
   - If Alice plays on one side and the only '?' left are on the same side, Bob plays '9 - x'. The sum of their two moves is strictly forced to be 9.
Because Bob can guarantee that every pair of '?' adds exactly 9 to the board, each individual '?' mathematically represents an average value of 4.5.
For Bob to win, the initial difference in the known sums (sum1 - sum2) must perfectly equal the maximum compensation his remaining '?' can provide: (q2 - q1) * 4.5.

VISUALIZATION (num = "?3295???"):
Left half ("?329"): sum1 = 14, q1 = 1
Right half ("5???"): sum2 = 5, q2 = 3

Total '?' = 1 + 3 = 4 (Even -> Bob has the last word).

Check formula: sum1 - sum2 == (q2 - q1) * 4.5
14 - 5 == (3 - 1) * 4.5
9 == 2 * 4.5
9 == 9 -> True! Bob wins! Return False. ✓
"""

# STEP 1: Split the string in half and compute the sums of known digits and the count of '?' for both sides.
# STEP 2: Check the parity of the total '?'. If it's odd, Alice gets the final move and wins automatically.
# STEP 3: If even, apply the optimal pairing formula. Check if the sum difference is exactly balanced by the '?' difference multiplied by 4.5.
# STEP 4: If the formula holds, Bob wins (False). Otherwise, Alice wins (True).

class Solution:
    def sumGame(self, num: str) -> bool:
        n = len(num)
        half = n // 2
        
        sum1 = sum2 = 0
        q1 = q2 = 0
        
        # Calculate states for the left half
        for i in range(half):
            if num[i] == '?':
                q1 += 1
            else:
                sum1 += int(num[i])
                
        # Calculate states for the right half
        for i in range(half, n):
            if num[i] == '?':
                q2 += 1
            else:
                sum2 += int(num[i])
                
        # Odd number of moves means Alice plays last. She can easily break any equality.
        if (q1 + q2) % 2 != 0:
            return True
            
        # Bob wins ONLY if the difference in values is perfectly matched by the 4.5 average of the '?' difference
        if float(sum1 - sum2) == (q2 - q1) * 4.5:
            return False
            
        # If it doesn't match perfectly, the initial imbalance is too big for Bob to fix. Alice wins.
        return True

"""
WHY EACH PART:
- (q1 + q2) % 2 != 0: The ultimate short-circuit. It avoids math evaluations when the game state inherently favors the first player with an extra move.
- float(sum1 - sum2): Casting to float cleanly avoids integer division truncation issues when comparing against 4.5.
- (q2 - q1) * 4.5: Represents the net mathematical power Bob holds to shift the equilibrium. 

KEY TECHNIQUE:
- Game Theory Reduction: Bypassing Minimax/Simulation algorithms by identifying the terminal mathematical equilibrium of optimal counter-play.

EDGE CASES:
- No question marks (e.g., "5023"): q1 = 0, q2 = 0. Condition `float(5 - 5) == (0 - 0) * 4.5` -> `0 == 0` -> Bob wins (False). Handled flawlessly.

TIME COMPLEXITY: O(N) - We iterate through the string of length N exactly once to tally the sums and question marks.
SPACE COMPLEXITY: O(1) - The algorithm evaluates state strictly using 4 integer variables, requiring no extra memory scaling with N.

CONCEPTS USED:
- Game Theory
- Invariant Logic
- Zero-Sum Equilibrium
"""
