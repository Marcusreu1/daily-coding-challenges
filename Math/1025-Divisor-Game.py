# 1025. Divisor Game
# Difficulty: Easy
# https://leetcode.com/problems/divisor-game/

"""
PROBLEM:
Alice and Bob take turns playing a game, with Alice starting first.
Initially, there is a number `n` on the chalkboard. On each player's turn, that player makes a move consisting of:
1. Choosing any x with 0 < x < n and n % x == 0.
2. Replacing the number n on the chalkboard with n - x.
Also, if a player cannot make a move, they lose the game.
Return true if and only if Alice wins the game, assuming both players play optimally.

EXAMPLES:
Input: n = 2
Output: true (Alice chooses 1, and Bob has no more moves since 1 has no valid x).

Input: n = 3
Output: false (Alice must choose 1, leaving 2 for Bob. Bob chooses 1, leaving 1 for Alice. Alice has no moves).

CONSTRAINTS:
- 1 <= n <= 1000

MATHEMATICAL REDUCTION (Game Theory):
Instead of simulating the game using Dynamic Programming or recursion, we can solve this using math (parity).
Rule 1: The divisors of an ODD number are ALWAYS ODD. (Odd - Odd = Even).
Rule 2: An EVEN number always has at least one ODD divisor, which is 1. (Even - Odd = Odd).
Rule 3: The number 1 is ODD, and whoever receives 1 loses the game (since no 0 < x < 1 exists).

If Alice starts with an EVEN number:
- She can always choose x = 1 (an odd divisor).
- This forces Bob to receive an ODD number.
- Bob is mathematically forced to subtract an odd divisor, which gives Alice an EVEN number back.
- Alice maintains control, always handing Bob an ODD number. Eventually, Bob will be handed the number 1 and lose.

If Alice starts with an ODD number:
- She is forced to hand Bob an EVEN number.
- Bob will then use the optimal strategy against her, eventually handing her the number 1.

Conclusion: Alice wins if and only if 'n' is EVEN.

VISUALIZATION (n = 4):
Start: n = 4 (Even)
├── Alice's Turn: Chooses x = 1 (since 4 % 1 == 0). Board becomes 4 - 1 = 3.
├── Bob's Turn: n = 3 (Odd). Divisors of 3 are 1. Must choose x = 1. Board becomes 3 - 1 = 2.
├── Alice's Turn: n = 2 (Even). Chooses x = 1. Board becomes 2 - 1 = 1.
├── Bob's Turn: n = 1. No valid moves (0 < x < 1). Bob loses.

Result: True ✓
"""

# STEP 1: Understand that optimal play revolves around parity control.
# STEP 2: Return True if the starting number is Even (Alice can control the game).
# STEP 3: Return False if the starting number is Odd (Alice is forced into a losing pattern).

class Solution:
    def divisorGame(self, n: int) -> bool:
        
        return n % 2 == 0                                                      # Alice wins if and only if 'n' is even

"""
WHY EACH PART:
- n % 2 == 0: Evaluates to True if n is an even number, perfectly encapsulating the entire Game Theory proof in a single boolean expression.

HOW IT WORKS (Example: n = 2):

Initial State:
├── n = 2

Mathematical Check:
├── 2 % 2 == 0 -> True

Exit:
return True ✓

KEY TECHNIQUE:
- Game Theory / Math. Recognizing the invariant property (Parity) transforms an overlapping subproblem (O(N^2) DP) into an O(1) mathematical fact.

EDGE CASES:
- n = 1: 1 % 2 == 0 is False. Alice loses immediately. ✓
- Large numbers (n = 1000): The math holds up instantly without needing to simulate 1000 recursive turns. ✓

TIME COMPLEXITY: O(1) - The solution performs a single modulo operation, executing in constant time.
SPACE COMPLEXITY: O(1) - No extra memory is allocated.

CONCEPTS USED:
- Math
- Game Theory
- Brainteaser
"""
