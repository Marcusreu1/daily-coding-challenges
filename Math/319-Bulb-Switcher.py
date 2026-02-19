"""
319. Bulb Switcher
Difficulty: Medium
https://leetcode.com/problems/bulb-switcher/

PROBLEM:
There are n bulbs that are initially off. You perform n rounds:
- Round 1: Turn on every bulb
- Round 2: Toggle every 2nd bulb (2, 4, 6, ...)
- Round 3: Toggle every 3rd bulb (3, 6, 9, ...)
- Round i: Toggle every i-th bulb
- ...
- Round n: Toggle only the n-th bulb

Return the number of bulbs that are ON after n rounds.

EXAMPLES:
Input: n = 3 → Output: 1
    Round 1: 🟡🟡🟡 (all on)
    Round 2: 🟡⚫🟡 (toggle 2)
    Round 3: 🟡⚫⚫ (toggle 3)
    Result: 1 bulb on

Input: n = 0 → Output: 0 (no bulbs)
Input: n = 1 → Output: 1 (toggle once, stays on)

CONSTRAINTS:
• 0 <= n <= 10⁹

KEY INSIGHT:
Bulb k is toggled once for each divisor of k.
- Even number of divisors → ends OFF
- Odd number of divisors  → ends ON

Only PERFECT SQUARES have odd number of divisors!
Why? Divisors come in pairs (d, n/d), except when d = n/d (i.e., d² = n)

SOLUTION:
Count perfect squares from 1 to n = floor(√n)

EXAMPLES OF DIVISORS:
    6:  {1,2,3,6}     → 4 divisors (pairs: 1×6, 2×3)      → OFF
    9:  {1,3,9}       → 3 divisors (pairs: 1×9, 3×3)      → ON
                                          ↑ same!
    12: {1,2,3,4,6,12} → 6 divisors                       → OFF
    16: {1,2,4,8,16}   → 5 divisors (pairs: 1×16,2×8,4×4) → ON
                                                  ↑ same!
"""

import math


class Solution:
    def bulbSwitch(self, n: int) -> int:
        
        return int(math.sqrt(n))                                 # Count of perfect squares ≤ n


"""
ALTERNATIVE IMPLEMENTATIONS:
"""


# Method 1: Using math.isqrt (Python 3.8+, returns integer directly)
class Solution:
    def bulbSwitch(self, n: int) -> int:
        
        return math.isqrt(n)                                     # Integer square root


# Method 2: Using power operator
class Solution:
    def bulbSwitch(self, n: int) -> int:
        
        return int(n ** 0.5)                                     # n^0.5 = √n


# Method 3: Explicit floor
class Solution:
    def bulbSwitch(self, n: int) -> int:
        
        return math.floor(math.sqrt(n))


"""
WHY EACH PART:

int(math.sqrt(n)):
├── math.sqrt(n) → calculates √n as float
├── int()        → truncates to integer (same as floor for positive)
└── Result       → number of perfect squares from 1 to n

HOW IT WORKS (Trace):

n = 5:
├── sqrt(5) = 2.236...
├── int(2.236) = 2
├── Perfect squares ≤ 5: {1, 4} = 2 numbers
└── Return: 2 ✓

n = 10:
├── sqrt(10) = 3.162...
├── int(3.162) = 3
├── Perfect squares ≤ 10: {1, 4, 9} = 3 numbers
└── Return: 3 ✓

n = 16:
├── sqrt(16) = 4.0
├── int(4.0) = 4
├── Perfect squares ≤ 16: {1, 4, 9, 16} = 4 numbers
└── Return: 4 ✓

n = 99:
├── sqrt(99) = 9.949...
├── int(9.949) = 9
├── Perfect squares ≤ 99: {1,4,9,16,25,36,49,64,81} = 9 numbers
└── Return: 9 ✓

DETAILED PROOF:

Step 1: Bulb k toggles when?
┌────────────────────────────────────────────────────────────┐
│  Bulb k toggles in round i  ⟺  i divides k                │
│  Total toggles for bulb k = number of divisors of k       │
└────────────────────────────────────────────────────────────┘

Step 2: When is bulb ON at the end?
┌────────────────────────────────────────────────────────────┐
│  Starts OFF, each toggle flips state                       │
│  OFF → ON → OFF → ON → ...                                 │
│                                                            │
│  Odd toggles  → ON                                         │
│  Even toggles → OFF                                        │
└────────────────────────────────────────────────────────────┘

Step 3: When does a number have ODD divisors?
┌────────────────────────────────────────────────────────────┐
│  Divisors come in pairs: if d|n, then (n/d)|n              │
│  Example: 12 → (1,12), (2,6), (3,4) = 6 divisors           │
│                                                            │
│  EXCEPT when d = n/d, i.e., d² = n (perfect square)        │
│  Example: 9 → (1,9), (3,3) but 3 counts once = 3 divisors  │
│                                                            │
│  Only PERFECT SQUARES have odd number of divisors!         │
└────────────────────────────────────────────────────────────┘

Step 4: Count perfect squares ≤ n
┌────────────────────────────────────────────────────────────┐
│  Perfect squares: 1², 2², 3², ..., k² where k² ≤ n        │
│  Maximum k: k ≤ √n → k = floor(√n)                        │
│  Answer: floor(√n)                                        │
└────────────────────────────────────────────────────────────┘

VISUAL EXAMPLE (n = 12):

Bulb:        1    2    3    4    5    6    7    8    9   10   11   12
Divisors:   {1} {1,2}{1,3}{1, {1,5}{1,2,{1,7}{1,2,{1, {1,2,{1, {1,2,
                          2,4}     3,6}     4,8} 3,9} 5,10}11} 3,4,
                                                              6,12}
Count:       1    2    2    3    2    4    2    4    3    4    2    6
Parity:     odd even even odd even even even even odd even even even
State:       🟡   ⚫   ⚫   🟡   ⚫   ⚫   ⚫   ⚫   🟡   ⚫   ⚫   ⚫

ON bulbs: 1, 4, 9 (the perfect squares!)
Count: 3 = floor(√12) = floor(3.46) = 3 ✓

EDGE CASES:
n = 0  → sqrt(0) = 0   → 0 bulbs on ✓
n = 1  → sqrt(1) = 1   → 1 bulb on (bulb 1 = 1²) ✓
n = 2  → sqrt(2) ≈ 1.4 → 1 bulb on ✓
n = 10⁹ → sqrt(10⁹) ≈ 31622 → works in O(1) ✓

TIME COMPLEXITY: O(1)
├── Single square root operation
└── Constant time regardless of n

SPACE COMPLEXITY: O(1)
├── No extra data structures
└── Only returning an integer

WHY SIMULATION FAILS:
n = 10⁹ bulbs, n rounds
Operations = 10⁹ + 10⁹/2 + 10⁹/3 + ... ≈ 10⁹ × ln(10⁹) ≈ 2×10¹⁰
Way too slow!

CONCEPTS USED:
• Number Theory (divisors)
• Perfect Squares
• Mathematical Pattern Recognition
• Parity (odd/even)
"""
