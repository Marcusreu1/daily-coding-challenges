"""
754. Reach a Number
Difficulty: Medium
https://leetcode.com/problems/reach-a-number/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

You are standing at position 0 on an infinite number line.
On each move i (starting from 1), you take i steps either
LEFT or RIGHT.

Return the minimum number of moves to reach position `target`.

EXAMPLES:

    Input: target = 2  → Output: 3
        Move 1: 0 → 1 (+1)
        Move 2: 1 → -1 (-2)
        Move 3: -1 → 2 (+3)

    Input: target = 3  → Output: 2
        Move 1: 0 → 1 (+1)
        Move 2: 1 → 3 (+2)

CONSTRAINTS:

    -10^9 <= target <= 10^9
    target != 0

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

1. By SYMMETRY, reaching -t takes the same steps as reaching t.
   So we use target = abs(target).

2. If we go ALL RIGHT: sum = 1 + 2 + 3 + ... + k
   When sum >= target, we've "overshot" by (sum - target).

3. FLIPPING step i from right(+i) to left(-i) changes position
   by exactly 2i. So we need: 2i = sum - target → i = (sum-target)/2

4. This only works when (sum - target) is EVEN.
   If ODD, keep adding steps until the difference becomes EVEN.

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. SYMMETRY: Recognizing negative targets mirror positive ones
2. OVERSHOOT LOGIC: Understanding why we flip a step, not backtrack
3. PARITY: Realizing we need even difference to flip exactly one step
4. AT MOST 2 EXTRA STEPS: Proving we never need more than 2 extra

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Take absolute value of target (symmetry)
STEP 2: Keep adding steps (1+2+3+...) until sum >= target
STEP 3: If (sum - target) is even → done, return step count
STEP 4: If odd → add one more step, check again (at most 2 extra)
"""


class Solution:
    def reachNumber(self, target: int) -> int:

        target = abs(target)                                                      # Symmetry: -t and t need same steps
        steps = 0                                                                 # Count of moves taken
        total = 0                                                                 # Running sum: 1 + 2 + ... + steps

        # ── STEP 1: Keep adding steps until we reach or pass target ──
        while total < target:                                                     # Haven't reached target yet
            steps += 1                                                            # Take next move
            total += steps                                                        # Add step size to position

        # ── STEP 2: Adjust parity — need (total - target) to be EVEN ──
        while (total - target) % 2 != 0:                                          # Difference is odd → can't flip
            steps += 1                                                            # Take one more step
            total += steps                                                        # Update position

        return steps                                                              # Minimum moves needed


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

target = abs(target):
    Reaching position -5 takes the same number of steps as +5.
    Just flip every direction. So we only solve for positive targets.

while total < target:
    We greedily go right (adding 1, 2, 3, ...) until we reach
    or overshoot the target. Going all right gives the minimum
    number of steps to at least cover the distance.

while (total - target) % 2 != 0:
    When we overshoot, the "excess" is (total - target).
    If it's EVEN, we can flip one step of size excess/2 to fix it.
    If it's ODD, no single flip works (2i is always even),
    so we keep adding steps until the excess becomes even.

return steps:
    The total number of moves is our answer. The key insight is
    that the same number of moves achieves the goal — we just
    choose different directions for some of them.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: target = 5):
════════════════════════════════════════════════════════════════

    target = abs(5) = 5

    PHASE 1 — Reach or overshoot:
    ├── step=1: total=1  < 5 → continue
    ├── step=2: total=3  < 5 → continue
    └── step=3: total=6  ≥ 5 → STOP

    PHASE 2 — Fix parity:
    ├── total - target = 6 - 5 = 1 (ODD → can't flip)
    ├── step=4: total=10, diff=5 (ODD → still can't)
    └── step=5: total=15, diff=10 (EVEN ✓ → STOP)

    Verification: flip step 10/2 = 5
    +1 +2 +3 +4 -5 = 10 - 10 = ... let's check:
    1+2+3+4 = 10, then -5 = 5 ✓

    Return: 5

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: target = 3):
════════════════════════════════════════════════════════════════

    target = abs(3) = 3

    PHASE 1 — Reach or overshoot:
    ├── step=1: total=1 < 3
    └── step=2: total=3 ≥ 3 → STOP

    PHASE 2 — Fix parity:
    └── total - target = 3 - 3 = 0 (EVEN ✓ → STOP)

    Return: 2   (simply go +1, +2 = 3) ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: target = 2):
════════════════════════════════════════════════════════════════

    target = abs(2) = 2

    PHASE 1 — Reach or overshoot:
    ├── step=1: total=1 < 2
    └── step=2: total=3 ≥ 2 → STOP

    PHASE 2 — Fix parity:
    ├── total - target = 3 - 2 = 1 (ODD → can't flip)
    └── step=3: total=6, diff=4 (EVEN ✓ → STOP)

    Verification: flip step 4/2 = 2
    +1 -2 +3 = 2 ✓

    Return: 3

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: target = -7):
════════════════════════════════════════════════════════════════

    target = abs(-7) = 7

    PHASE 1:
    ├── step=1: total=1
    ├── step=2: total=3
    ├── step=3: total=6
    └── step=4: total=10 ≥ 7 → STOP

    PHASE 2:
    ├── total - target = 10 - 7 = 3 (ODD)
    └── step=5: total=15, diff=8 (EVEN ✓ → STOP)

    Verification: flip step 8/2 = 4
    +1 +2 +3 -4 +5 = 11 - 4 = 7
    Then negate all for -7: -1 -2 -3 +4 -5 = -7 ✓

    Return: 5

════════════════════════════════════════════════════════════════
WHY FLIPPING A STEP CHANGES POSITION BY 2i:
════════════════════════════════════════════════════════════════

    If step i was going RIGHT:  position includes +i
    If we flip to LEFT:         position includes -i
    Change: (+i) → (-i) = -2i

    So flipping step i reduces our total by 2i.

    We need: total - 2i = target
             2i = total - target
             i  = (total - target) / 2

    This requires (total - target) to be:
    ├── Non-negative (total ≥ target) → guaranteed by phase 1
    ├── Even (divisible by 2) → guaranteed by phase 2
    └── ≤ 2 × steps (i must be a valid step) → always true
        because (total-target) ≤ steps (last step added)
        and steps ≤ 2×steps

    Actually, we might need to flip MULTIPLE steps whose values
    sum to (total - target)/2. But since all values 1..k are
    available, any value from 1 to total can be formed as a
    subset sum (total = 1+2+...+k covers all sums up to total).

════════════════════════════════════════════════════════════════
WHY AT MOST 2 EXTRA STEPS:
════════════════════════════════════════════════════════════════

    After phase 1, (total - target) is some non-negative integer.

    If it's EVEN → done immediately (0 extra steps)

    If it's ODD:
    ├── Add step (k+1):
    │   New diff = old_diff + (k+1)
    │   ODD + ODD = EVEN → done! (1 extra step)
    │   ODD + EVEN = ODD → need one more...
    │
    └── Add step (k+2):
        New diff = prev_diff + (k+2)
        ODD + ODD = EVEN → done! (2 extra steps)
        ODD + EVEN = ... but k+1 and k+2 have different parity,
        so ONE of them must be odd, making the sum even.

    Therefore: at most 2 extra steps beyond the overshoot point.

════════════════════════════════════════════════════════════════
WHY SYMMETRY WORKS (abs(target)):
════════════════════════════════════════════════════════════════

    The number line is symmetric around 0.
    
    To reach +5: +1 +2 -3 +4 +5 -4 ... (some combination)
    To reach -5: -1 -2 +3 -4 -5 +4 ... (flip every direction)

    Same number of moves, just mirrored directions.
    So we solve for |target| and the answer applies to both.

════════════════════════════════════════════════════════════════
THE MATH BEHIND IT:
════════════════════════════════════════════════════════════════

    Each move i has a sign s_i ∈ {+1, -1}:
    position = s_1(1) + s_2(2) + s_3(3) + ... + s_k(k)

    Let R = set of indices where s_i = +1 (go right)
    Let L = set of indices where s_i = -1 (go left)

    position = sum(R) - sum(L)
    total    = sum(R) + sum(L) = k(k+1)/2

    target = sum(R) - sum(L)
    total  = sum(R) + sum(L)

    Adding: sum(R) = (total + target) / 2

    For sum(R) to be an integer: (total + target) must be EVEN
    → (total - target) must be EVEN (same parity)

    This is exactly our condition! ✓

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    target = 1         → 1 (one step right) ✓
    target = -1        → 1 (one step left, abs symmetry) ✓
    target = 3         → 2 (1+2 = 3, exact match) ✓
    target = 2         → 3 (1-2+3 = 2) ✓
    target = 4         → 3 (1-2+3+... → -1+2+3=4? No: 1+2+3=6, diff=2, flip 1 → -1+2+3=4) ✓
    target = 10^9      → Works (sum grows as k², so k ≈ √(2×10^9) ≈ 44721) ✓
    Negative target    → Same as positive (abs) ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(√target)
════════════════════════════════════════════════════════════════

    Phase 1: We sum 1+2+...+k until k(k+1)/2 ≥ target
    → k ≈ √(2 × target) iterations

    Phase 2: At most 2 extra iterations

    Total: O(√target)

    For target = 10^9: about 44,721 iterations → very fast ✓

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(1)
════════════════════════════════════════════════════════════════

    Only three integer variables: target, steps, total.
    No additional data structures.

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Mathematical reasoning (sum of consecutive integers)
    Symmetry exploitation (abs value for negative targets)
    Parity analysis (even/odd determines solvability)
    Greedy approach (go all right first, then flip)
    Bit flipping intuition (changing +i to -i costs 2i)
    Subset sum existence (guaranteed by consecutive integers)
"""
