# 2029. Stone Game IX
# Difficulty: Medium
# https://leetcode.com/problems/stone-game-ix/

"""
PROBLEM:
Alice and Bob continue their games with stones. There is an array of stones, and Alice plays first.
On each turn, a player removes a stone from the array. The game maintains a running sum of the removed stones.
- If a player's turn makes the running sum divisible by 3, they lose immediately.
- If no stones are left and nobody has lost by the divisible-by-3 rule, Bob wins.
Return true if Alice can guarantee a win, assuming both players play optimally.

EXAMPLES:
Input: stones = [2,1] → Output: true
Explanation: 
- Alice picks 2. Running sum is 2. (2 % 3 != 0).
- Bob must pick 1. Running sum is 3. (3 % 3 == 0). Bob loses. Alice wins.

Input: stones = [2] → Output: false
Explanation: Alice picks 2. Running sum is 2. No stones left. Bob wins by default.

Input: stones = [5,1,2,4,3] → Output: false

CONSTRAINTS:
- 1 <= stones.length <= 10^5
- 1 <= stones[i] <= 10^4

MATH RULES (GAME THEORY & MODULO ARITHMETIC):
The absolute values of the stones are irrelevant. We only care about their values modulo 3.
All stones fall into three buckets: 0s, 1s, and 2s.
- Choosing a '0' stone does not change the running sum modulo 3. It effectively acts as a "Skip Turn" card.
- If Alice starts with a '1', the safe sequence of moves modulo 3 MUST be: 1 -> 1 -> 2 -> 1 -> 2 -> 1 -> 2...
- If Alice starts with a '2', the safe sequence of moves modulo 3 MUST be: 2 -> 2 -> 1 -> 2 -> 1 -> 2 -> 1...

Since '0's just reverse the turn burden, their parity (even or odd) decides the game's dynamic:
1. Even number of '0's: They cancel each other out. Alice just needs both '1's and '2's to exist to win. If one is missing, Alice is forced into a path where she exhausts her safe options, allowing Bob to win by default.
2. Odd number of '0's: Bob gains an extra "Skip Turn" card, flipping the parity of the game. To counter this and force Bob to crash, Alice needs a severe imbalance between '1's and '2's (a difference strictly greater than 2).

VISUALIZATION (stones = [5,1,2,4,3]):
Mod 3 classes: [2, 1, 2, 1, 0].
Counts:
count[0] = 1
count[1] = 2
count[2] = 2

Condition check:
Is count[0] even? 1 % 2 == 1 (False).
Move to odd logic: abs(count[1] - count[2]) > 2
abs(2 - 2) > 2 -> 0 > 2 -> False!
Bob can successfully stall and force Alice to crash or run out of stones.
Result: False ✓
"""

from typing import List

# STEP 1: Create an array of size 3 to count the occurrences of stones yielding remainder 0, 1, and 2 modulo 3.
# STEP 2: Iterate through the stones and populate the frequency map.
# STEP 3: If the count of '0' stones is EVEN, Alice wins if she has at least one '1' stone and one '2' stone.
# STEP 4: If the count of '0' stones is ODD, Alice wins only if the absolute difference between '1's and '2's is > 2.

class Solution:
    def stoneGameIX(self, stones: List[int]) -> bool:
        
        # Array to hold the count of stones that are 0, 1, or 2 modulo 3
        count = [0] * 3
        
        for stone in stones:
            count[stone % 3] += 1
            
        # If the number of "skip turn" (0) stones is even, their effect is neutralized.
        if count[0] % 2 == 0:
            # Alice can win as long as she has both options available to start her sequence.
            return count[1] > 0 and count[2] > 0
            
        # If the number of "skip turn" (0) stones is odd, the parity of the game is flipped.
        # Alice needs a large surplus of one stone type to force Bob into a trap.
        return abs(count[1] - count[2]) > 2

"""
WHY EACH PART:
- count[stone % 3] += 1: Maps the physical values of the stones strictly into Game Theory state buckets.
- if count[0] % 2 == 0: Separates the equilibrium logic. Even '0's mean standard gameplay. Odd '0's mean inverted gameplay.
- count[1] > 0 and count[2] > 0: If Alice only has 1s, she plays 1, Bob plays 1, sum=2. Alice MUST play 1 (sum=3, loses). Bob wins. She needs both to survive.

KEY TECHNIQUE:
- Mathematical Invariants: Reducing infinite gameplay permutations into a simple mathematical state check.
- Parity Evaluation: Realizing that "no-op" moves (mod 0) are just turn-inverters.

EDGE CASES:
- Only '0's in the array: count[1]=0, count[2]=0. Returns False. Bob wins by default as no one can make a move without making the sum 0 (which is divisible by 3).
- Massive arrays up to 10^5 elements: Solved in pure O(N) time without recursive Minimax trees.

TIME COMPLEXITY: O(N) - We iterate through the stones array exactly once to build the counts.
SPACE COMPLEXITY: O(1) - The count array is strictly of size 3, regardless of the input size N.
"""
