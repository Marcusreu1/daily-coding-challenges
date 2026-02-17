"""
292. Nim Game
Difficulty: Easy
https://leetcode.com/problems/nim-game/

PROBLEM:
You are playing a Nim Game with your friend:
- There is a heap of n stones on the table
- You and your friend take turns removing 1 to 3 stones
- The one who removes the LAST stone WINS
- You always go FIRST

Both players play OPTIMALLY.
Return TRUE if you can win, FALSE otherwise.

EXAMPLES:
Input: n = 4 → Output: false
    - Take 1 → opponent takes 3 → you lose
    - Take 2 → opponent takes 2 → you lose
    - Take 3 → opponent takes 1 → you lose

Input: n = 1 → Output: true (take 1, win)
Input: n = 2 → Output: true (take 2, win)

CONSTRAINTS:
1 <= n <= 2³¹ - 1

KEY INSIGHT:
The number 4 is "magical" because:
    1 + 3 = 4
    2 + 2 = 4
    3 + 1 = 4

Whatever you take (1,2,3), opponent can complement to 4!

PATTERN DISCOVERY:
n:     1  2  3  4  5  6  7  8  9  10  11  12
Win?:  ✓  ✓  ✓  ✗  ✓  ✓  ✓  ✗  ✓  ✓   ✓   ✗
                ↑           ↑              ↑
             Multiples of 4 = LOSE

SOLUTION:
You LOSE if n is divisible by 4
You WIN if n is NOT divisible by 4
"""


class Solution:
    def canWinNim(self, n: int) -> bool:

        return n % 4 != 0                                        # Win if NOT multiple of 4


"""
WHY THIS WORKS:

Case 1: n = 4k (multiple of 4)
├── You take X stones (1, 2, or 3)
├── Opponent takes (4-X) stones
├── Each round removes exactly 4 stones
├── After k rounds: 4k removed, 0 left
└── Opponent ALWAYS takes last stone → YOU LOSE

Case 2: n = 4k + r where r ∈ {1, 2, 3}
├── You take r stones on first move
├── Remaining: 4k stones (multiple of 4!)
├── Now OPPONENT is in losing position
└── YOU WIN

HOW IT WORKS (Trace):

n = 4:
├── 4 % 4 = 0
├── 0 != 0 → False
└── Return: False (you lose) ✓

n = 7:
├── 7 % 4 = 3
├── 3 != 0 → True
└── Return: True (you win) ✓

n = 12:
├── 12 % 4 = 0
├── 0 != 0 → False
└── Return: False (you lose) ✓

ALTERNATIVE - BITWISE VERSION:
return n & 3 != 0

Why n & 3 works:
├── 3 in binary = 11
├── n & 3 extracts last 2 bits
├── Multiples of 4 have last 2 bits = 00
└── So n & 3 == 0 means multiple of 4

GAME THEORY CONCEPT:
This is "Combinatorial Game Theory"!
├── LOSING POSITION (P-position): n = 4k
├── WINNING POSITION (N-position): n ≠ 4k
├── From LOSING pos → all moves lead to WINNING pos
└── From WINNING pos → at least one move to LOSING pos

EDGE CASES:
n = 1         → 1 % 4 = 1 ≠ 0 → True  ✓
n = 4         → 4 % 4 = 0     → False ✓
n = 2³¹ - 1   → Odd number    → True  ✓

TIME COMPLEXITY: O(1)
├── Single modulo operation
└── Constant time regardless of n

SPACE COMPLEXITY: O(1)
├── No extra data structures
└── Only returning a boolean

CONCEPTS USED:
• Game Theory (optimal play)
• Pattern Recognition
• Mathematical Proof
• Modular Arithmetic
• Bitwise Operations (optimization)
"""
