"""
464. Can I Win
Difficulty: Medium
https://leetcode.com/problems/can-i-win/

PROBLEM:
Two players take turns picking numbers from 1 to maxChoosableInteger
(each number can only be used ONCE). Numbers are added to a running total.
The player who causes the total to reach or exceed desiredTotal wins.

Given both players play OPTIMALLY, return true if the FIRST player
can force a win.

EXAMPLES:
Input: maxChoosableInteger=10, desiredTotal=11 → Output: false
    No matter what player 1 picks, player 2 can always reach 11

Input: maxChoosableInteger=10, desiredTotal=0  → Output: true
    desiredTotal already reached, player 1 wins immediately

Input: maxChoosableInteger=10, desiredTotal=1  → Output: true
    Player 1 picks any number ≥ 1, wins immediately

CONSTRAINTS:
    1 <= maxChoosableInteger <= 20
    0 <= desiredTotal <= 300

KEY INSIGHT:
Use BITMASK to represent which numbers have been used (state).
With max 20 numbers → 2^20 ≈ 1M states (manageable).
For each state, current player tries all unused numbers:
    - If picking a number reaches the target → current player wins
    - If picking a number leads to opponent LOSING → current player wins
Memoize results by bitmask.

CHALLENGES:
    Game tree is exponentially large without memoization (20!)
    Need to think recursively: "I win if my opponent loses"
    Bitmask representation of used numbers
    Proving bitmask alone determines the game state

SOLUTION:
    1. Handle edge cases (total ≤ 0, impossible to reach)
    2. Recursive function: try each unused number
    3. Win if: number reaches target OR opponent can't win after
    4. Memoize by bitmask (determines used numbers → determines remaining)
"""

# STEP 1: Handle edge cases
# STEP 2: Define recursive function with bitmask state
# STEP 3: Try each unused number, check win conditions
# STEP 4: Memoize and return result

class Solution:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:

        if desiredTotal <= 0:                                            # Already reached → first player wins
            return True

        total_sum = maxChoosableInteger * (maxChoosableInteger + 1) // 2  # Sum of all available numbers

        if total_sum < desiredTotal:                                     # Even using ALL numbers can't reach target
            return False

        memo = {}                                                        # bitmask → can current player win?

        def canWin(used: int, remaining: int) -> bool:

            if used in memo:                                             # Already computed this state
                return memo[used]

            for i in range(1, maxChoosableInteger + 1):                  # Try each number 1 to max
                mask = 1 << i                                            # Bitmask for number i

                if used & mask == 0:                                     # Number i is still available
                    if i >= remaining:                                   # Picking i reaches the target → I WIN
                        memo[used] = True
                        return True

                    if not canWin(used | mask, remaining - i):           # Opponent can't win after I pick i
                        memo[used] = True                                # → I WIN
                        return True

            memo[used] = False                                           # No winning move found → I LOSE
            return False

        return canWin(0, desiredTotal)                                   # Start: nothing used, full target

"""
WHY EACH PART:

    desiredTotal <= 0: Target already met before game starts → instant win
    total_sum < desiredTotal: Impossible to reach even with all numbers
    memo = {}: Maps bitmask → True/False (can current player win?)
    used (bitmask): Which numbers have been chosen (bit i = number i used)
    remaining: How much more is needed to reach desiredTotal
    1 << i: Creates bitmask with only bit i set (represents number i)
    used & mask == 0: Checks if bit i is 0 (number i available)
    i >= remaining: Picking i reaches/exceeds the target → win
    not canWin(used | mask, remaining - i): After I pick i, opponent LOSES
    memo[used] = True/False: Cache result to avoid recomputation
    canWin(0, desiredTotal): Start with no numbers used

HOW IT WORKS (Example: maxChoosable=3, desiredTotal=4):

    Available: {1, 2, 3}, target = 4

    canWin(000, 4):  ← J1's turn
    ├── Try 1: 1 < 4 → canWin(010, 3)?  ← J2's turn
    │   ├── Try 2: 2 < 3 → canWin(110, 1)?  ← J1's turn
    │   │   └── Try 3: 3 ≥ 1 → TRUE (J1 wins!)
    │   │   canWin(110, 1) = True → J1 wins
    │   ├── NOT True = False → picking 2 doesn't help J1
    │   ├── Try 3: 3 ≥ 3 → TRUE (J2 wins!)
    │   └── canWin(010, 3) = True (J2 CAN win)
    ├── not True = False → picking 1 doesn't guarantee J1 wins
    │
    ├── Try 2: 2 < 4 → canWin(100, 2)?  ← J2's turn
    │   ├── Try 1: 1 < 2 → canWin(110, 1)? = True (cached!)
    │   ├── not True = False
    │   ├── Try 3: 3 ≥ 2 → TRUE (J2 wins!)
    │   └── canWin(100, 2) = True (J2 CAN win)
    ├── not True = False → picking 2 doesn't guarantee J1 wins
    │
    ├── Try 3: 3 < 4 → canWin(1000, 1)?  ← J2's turn
    │   ├── Try 1: 1 ≥ 1 → TRUE (J2 wins!)
    │   └── canWin(1000, 1) = True (J2 CAN win)
    ├── not True = False → picking 3 doesn't guarantee J1 wins
    │
    └── No winning move → canWin(000, 4) = False

    Result: false ✓ (J1 cannot force a win)

WHY BITMASK IS SUFFICIENT AS STATE:

    Bitmask 0110 means numbers 2 and 3 are used.
    ├── Sum used = 2 + 3 = 5
    ├── remaining = desiredTotal - 5  (determined by bitmask!)
    └── Available numbers: {1, 4, 5...}  (determined by bitmask!)

    The bitmask FULLY determines the game state:
    ├── Which numbers are available
    ├── What the current total is
    └── Whose turn it is (count of 1-bits: even = J1, odd = J2)

    So memo[bitmask] is enough — no need to store 'remaining' separately.
    (We pass 'remaining' for convenience but don't use it as cache key)

WHY "not canWin()" MEANS I WIN:

    Game theory alternation:
    ├── canWin returns whether the CURRENT player can win
    ├── After I pick number i, it becomes OPPONENT's turn
    ├── canWin(new_state) = can OPPONENT win?
    ├── not canWin(new_state) = opponent CANNOT win
    └── If opponent can't win → I WIN ✓

    This is the core of MINIMAX:
    My best move = opponent's worst outcome

WHY THE ORDER OF CHECKS MATTERS:

    if i >= remaining:                    ← CHECK THIS FIRST
        return True
    if not canWin(used | mask, remaining - i):  ← THEN THIS

    If i >= remaining, the game is OVER — I win by picking i.
    No need to recurse further (and remaining-i could be ≤ 0).

    If we recurse with remaining ≤ 0, the next call would
    immediately return True for the opponent — WRONG!

BITMASK OPERATIONS EXPLAINED:

    1 << i:          Create mask with bit i set
                     1 << 3 = 0...01000 (represents number 3)

    used & mask:     Check if bit i is set
                     0110 & 0100 = 0100 (≠ 0, so number 3 is used)
                     0110 & 0001 = 0000 (= 0, so number 1 is available)

    used | mask:     Set bit i (mark number i as used)
                     0110 | 0001 = 0111 (added number 1 to used set)

MEMOIZATION IMPACT:

    Without memo: up to 20! ≈ 2.4 × 10^18 paths (IMPOSSIBLE)
    With memo:    up to 2^20 ≈ 1,048,576 states (< 1 second)

    Each state computed ONCE, then cached.
    Massive reduction from factorial to exponential.

EDGE CASES:

    desiredTotal = 0: First player wins immediately → true ✓
    maxChoosable = 1, desired = 1: Pick 1, win → true ✓
    Sum < desired: Impossible to reach → false ✓
    maxChoosable ≥ desired: Pick desired, win directly → true ✓
    maxChoosable = 20: 2^20 ≈ 1M states, manageable ✓
    Both optimal: Minimax handles this naturally ✓
    Tie (all numbers used, target not reached): false ✓

TIME COMPLEXITY: O(2^n × n)
    2^n possible states (bitmasks), where n = maxChoosableInteger
    For each state, try up to n numbers → O(n) per state
    Total: O(n × 2^n)
    With n = 20: 20 × 2^20 ≈ 20 million operations ✓

SPACE COMPLEXITY: O(2^n)
    Memo dictionary stores up to 2^n states
    Recursion stack depth up to n levels
    Total: O(2^n)

CONCEPTS USED:
    Game theory (Minimax algorithm)
    Bitmask to represent set of used numbers
    Memoization (top-down dynamic programming)
    Recursive state exploration
    Optimal play assumption (both players play best)
    Bit manipulation (shift, AND, OR)
"""
