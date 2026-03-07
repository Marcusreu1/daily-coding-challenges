"""
390. Elimination Game
Difficulty: Medium
https://leetcode.com/problems/elimination-game/

PROBLEM:
You have a list arr of all integers in range [1, n] sorted in increasing order.
Apply the following algorithm:
1. Starting from left, remove every other number until end (remove 1st, 3rd, ...)
2. From remaining, starting from right, remove every other number (remove last, 3rd last, ...)
3. Repeat until one number remains

Return the last remaining number.

EXAMPLES:
Input: n = 9
Output: 6
    [1,2,3,4,5,6,7,8,9] → [2,4,6,8] → [2,6] → [6]

Input: n = 1
Output: 1

CONSTRAINTS:
• 1 <= n <= 10⁹

KEY INSIGHT:
Don't simulate the entire list (would be O(n) space/time).
Just track the HEAD element and how it changes.

OBSERVATION:
- Going LEFT→RIGHT: head ALWAYS gets eliminated
- Going RIGHT→LEFT: head survives if remaining count is EVEN
                    head gets eliminated if remaining count is ODD

After each round:
- step doubles (elements are twice as far apart)
- remaining halves
- direction alternates
"""


# ============================================================================
# SOLUTION 1: ITERATIVE (Track head) 
# ============================================================================

class Solution:
    def lastRemaining(self, n: int) -> int:
        
        head = 1                                                 # First element
        step = 1                                                 # Distance between consecutive elements
        remaining = n                                            # Count of remaining elements
        left = True                                              # Direction: True = left→right
        
        while remaining > 1:
            # Head changes when:
            # 1. Going left to right (always)
            # 2. Going right to left AND remaining is odd
            
            if left or remaining % 2 == 1:
                head += step
            
            step *= 2                                            # Distance doubles
            remaining //= 2                                      # Half elements remain
            left = not left                                      # Alternate direction
        
        return head


# ============================================================================
# SOLUTION 2: RECURSIVE (Mathematical relation)
# ============================================================================

class Solution:
    def lastRemaining(self, n: int) -> int:
        """
        Recursive formula:
        f(n) = 2 * (n//2 + 1 - f(n//2))
        
        Base case: f(1) = 1
        """
        if n == 1:
            return 1
        
        # After left→right pass: remaining = [2, 4, 6, ...] = 2 * [1, 2, 3, ...]
        # Next pass is right→left on the "flipped" subproblem
        
        return 2 * (n // 2 + 1 - self.lastRemaining(n // 2))


# ============================================================================
# SOLUTION 3: ITERATIVE (Alternative formulation)
# ============================================================================

class Solution:
    def lastRemaining(self, n: int) -> int:
        
        head = 1
        step = 1
        remaining = n
        going_left = True
        
        while remaining > 1:
            if going_left:
                # Always remove head when going left
                head = head + step
            else:
                # Remove head only if odd count (last element in sequence is removed)
                if remaining % 2 == 1:
                    head = head + step
            
            remaining //= 2
            step *= 2
            going_left = not going_left
        
        return head


# ============================================================================
# SOLUTION 4: ONE-LINER RECURSIVE (Compact)
# ============================================================================

class Solution:
    def lastRemaining(self, n: int) -> int:
        return 1 if n == 1 else 2 * (n // 2 + 1 - self.lastRemaining(n // 2))


"""
HOW IT WORKS (Detailed Trace for n = 9):

═══════════════════════════════════════════════════════════════════
INITIAL STATE:
═══════════════════════════════════════════════════════════════════
head = 1, step = 1, remaining = 9, left = True

Conceptual list: [1, 2, 3, 4, 5, 6, 7, 8, 9]
                  ↑ head

═══════════════════════════════════════════════════════════════════
ROUND 1: left = True (LEFT → RIGHT)
═══════════════════════════════════════════════════════════════════

left=True → head changes
    head = 1 + 1 = 2
    step = 2
    remaining = 9 // 2 = 4
    left = False

After: [2, 4, 6, 8]
        ↑ head=2, step=2

═══════════════════════════════════════════════════════════════════
ROUND 2: left = False (RIGHT → LEFT)
═══════════════════════════════════════════════════════════════════

remaining = 4 (EVEN) → head survives
    head = 2 (unchanged)
    step = 4
    remaining = 4 // 2 = 2
    left = True

After: [2, 6]
        ↑ head=2, step=4

═══════════════════════════════════════════════════════════════════
ROUND 3: left = True (LEFT → RIGHT)
═══════════════════════════════════════════════════════════════════

left=True → head changes
    head = 2 + 4 = 6
    step = 8
    remaining = 2 // 2 = 1
    left = False

After: [6]

═══════════════════════════════════════════════════════════════════
remaining = 1, DONE! Return head = 6 ✓
═══════════════════════════════════════════════════════════════════

ANOTHER TRACE: n = 10

Round 1: left=T, head=1→2, step=1→2, rem=10→5
    [1,2,3,4,5,6,7,8,9,10] → [2,4,6,8,10]

Round 2: left=F, rem=5(ODD)→head changes, head=2→4, step=2→4, rem=5→2
    [2,4,6,8,10] → [4,8]  (eliminated 10,6,2)

Round 3: left=T, head=4→8, step=4→8, rem=2→1
    [4,8] → [8]

Return 8 ✓

═══════════════════════════════════════════════════════════════════

WHY HEAD CHANGES WHEN GOING LEFT:
┌────────────────────────────────────────────────────────────────┐
│  Going LEFT → RIGHT: We start from position 1                  │
│  We eliminate positions 1, 3, 5, 7, ...                        │
│  Position 1 (the head) is ALWAYS eliminated                   │
│  New head becomes what was at position 2 = old_head + step    │
└────────────────────────────────────────────────────────────────┘

WHY HEAD DEPENDS ON ODD/EVEN WHEN GOING RIGHT:
┌────────────────────────────────────────────────────────────────┐
│  Going RIGHT → LEFT: We start from the last position          │
│                                                                │
│  EVEN count (e.g., 4 elements at positions 1,2,3,4):          │
│  Eliminate 4, 2 → Remain 1, 3                                 │
│  Position 1 (head) survives!                                  │
│                                                                │
│  ODD count (e.g., 5 elements at positions 1,2,3,4,5):         │
│  Eliminate 5, 3, 1 → Remain 2, 4                              │
│  Position 1 (head) is eliminated!                             │
│  New head = old_head + step (position 2)                      │
└────────────────────────────────────────────────────────────────┘

RECURSIVE FORMULA EXPLANATION:
┌────────────────────────────────────────────────────────────────┐
│  After left→right pass on [1,2,...,n]:                        │
│  Remaining: [2, 4, 6, ..., 2⌊n/2⌋]                            │
│           = 2 × [1, 2, 3, ..., ⌊n/2⌋]                         │
│                                                                │
│  Next pass is right→left, which is equivalent to:             │
│  - Solving left→right on reversed list                        │
│  - Then mapping back                                          │
│                                                                │
│  If f(k) survives in [1,...,k] going left-first,             │
│  then in reversed order, position (k+1-f(k)) survives.        │
│                                                                │
│  Mapping back to original indices:                            │
│  f(n) = 2 × (⌊n/2⌋ + 1 - f(⌊n/2⌋))                          │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  n = 1   →  Only one element, return 1                        │
│  n = 2   →  [1,2] → [2], return 2                            │
│  n = 3   →  [1,2,3] → [2] → [2], return 2                    │
│  n = 10⁹ →  Works in O(log n) time!                          │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(log n)
├── Each iteration halves remaining
├── Number of iterations = log₂(n)
└── Each iteration is O(1)

SPACE COMPLEXITY: O(1) iterative, O(log n) recursive
├── Iterative: only storing a few variables
└── Recursive: call stack depth = log₂(n)


CONCEPTS USED:
• Mathematical Pattern Recognition
• Simulation without full data structure
• Recursion with mathematical relation
• Parity (odd/even) analysis
"""
