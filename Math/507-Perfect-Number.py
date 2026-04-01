"""
507. Perfect Number
Difficulty: Easy
https://leetcode.com/problems/perfect-number/

PROBLEM:
    A perfect number is a positive integer that is equal to the sum of
    its positive divisors, excluding the number itself.
    Given an integer num, return true if it is a perfect number.

EXAMPLES:
    Input: num = 28  → Output: true   (1+2+4+7+14 = 28)
    Input: num = 7   → Output: false  (1 ≠ 7)
    Input: num = 1   → Output: false  (no proper divisors)

CONSTRAINTS:
    1 <= num <= 10^8

KEY INSIGHT:
    Divisors come in PAIRS: if d divides n, then n/d also divides n.
    We only need to check up to √n and add BOTH divisors of each pair.

    This reduces O(n) brute force to O(√n).

CHALLENGES:
    Not counting num itself as a divisor
    Not double-counting when d == n/d (perfect squares)
    Handling num = 1 (no proper divisors)

SOLUTION:
    Start sum at 1 (always a divisor).
    Loop d from 2 to √n.
    For each d that divides n, add both d and n/d.
    Skip n/d if it equals d (avoid double count) or equals n (not proper).
"""


# STEP 1: Handle base case (num <= 1 can't be perfect)
# STEP 2: Start sum at 1 (always a proper divisor for num > 1)
# STEP 3: Loop from 2 to √num, find divisor pairs
# STEP 4: Add both d and num/d (with checks)
# STEP 5: Compare sum with num


from math import isqrt

class Solution:
    def checkPerfectNumber(self, num: int) -> bool:

        if num <= 1:                                                  # 1 and below have no proper divisors
            return False

        sum_divisors = 1                                              # 1 is always a proper divisor

        for d in range(2, isqrt(num) + 1):                           # Check from 2 to √num
            if num % d == 0:                                          # d is a divisor
                sum_divisors += d                                     # Add the small divisor

                pair = num // d                                       # The paired divisor
                if pair != d and pair != num:                         # Avoid double-count and self
                    sum_divisors += pair                              # Add the large divisor

        return sum_divisors == num                                    # Perfect if sum equals num


"""
WHY EACH PART:
    num <= 1:            num=1 has no proper divisors (sum=0≠1), negatives/0 aren't positive
    sum_divisors = 1:    1 divides everything, we always start with it
    range(2, isqrt+1):   Check divisors from 2 up to √num (inclusive)
    num % d == 0:        d divides num evenly → it's a divisor
    sum_divisors += d:   Add the small divisor of the pair
    pair = num // d:     Every divisor d has a partner num/d
    pair != d:           If d = √num, both divisors are the same → count once
    pair != num:         When d=1, pair=num itself → not a proper divisor (we skip d=1 in loop, handle separately)
    sum == num:          Definition of perfect number


HOW IT WORKS (Example: num = 28):

    sum_divisors = 1

    d = 2: 28 % 2 == 0 ✓
    ├── sum_divisors += 2  → sum = 3
    ├── pair = 28 // 2 = 14
    ├── 14 ≠ 2 and 14 ≠ 28? → 14 ≠ 2 ✓, 14 ≠ 28 ✓
    └── sum_divisors += 14 → sum = 17

    d = 3: 28 % 3 = 1 ≠ 0 → skip

    d = 4: 28 % 4 == 0 ✓
    ├── sum_divisors += 4  → sum = 21
    ├── pair = 28 // 4 = 7
    ├── 7 ≠ 4 and 7 ≠ 28? → ✓
    └── sum_divisors += 7  → sum = 28

    d = 5: 28 % 5 = 3 ≠ 0 → skip

    Loop ends (isqrt(28) = 5)

    sum_divisors = 28 == num = 28 → return true 

    Divisors found: {1, 2, 14, 4, 7} → sum = 28 ✓


HOW IT WORKS (Example: num = 7):

    sum_divisors = 1

    d = 2: 7 % 2 = 1 → skip
    
    Loop ends (isqrt(7) = 2)

    sum_divisors = 1 ≠ 7 → return false 
    (7 is prime, only proper divisor is 1)


WHY DIVISOR PAIRS WORK:
    If d divides n, then n = d × (n/d)
    So both d AND n/d are divisors of n.

    For 28:
    ┌──────────┬───────────┬──────────┐
    │   d      │  28 / d   │  pair    │
    ├──────────┼───────────┼──────────┤
    │   1      │    28     │ (1, 28)  │  ← 28 excluded (not proper)
    │   2      │    14     │ (2, 14)  │
    │   4      │     7     │ (4, 7)   │
    └──────────┴───────────┴──────────┘
           ↑ √28 ≈ 5.29 ↑
      small divisors    large divisors

    Every divisor ≤ √n has a partner ≥ √n
    Checking up to √n finds ALL divisors!


WHY CHECK pair != d:
    Example: num = 36, d = 6
    ├── pair = 36 / 6 = 6
    ├── d == pair → they're the SAME divisor
    └── If we add both, we count 6 TWICE! 

    With check: only add 6 once ✓


WHY CHECK pair != num:
    We start sum at 1 (handling d=1 outside the loop).
    But if d=2 and pair = num/2, pair could never equal num
    since d >= 2 means pair <= num/2.
    
    This check is a safety net for edge cases.
    In practice, since d starts at 2, pair = num/d <= num/2 < num.
    So pair != num is always true in our loop, but it's good defensive coding.


WHY isqrt AND NOT int(sqrt()):
    sqrt(num) returns float → precision issues for large numbers
    
    Example: sqrt(10**16) might give 99999999.99999999
    int() of that = 99999999 instead of 100000000!
    
    isqrt(num) returns EXACT integer square root ✓


HANDLING SPECIAL CASES:
    num = 1:             No proper divisors → sum=0 ≠ 1 → false ✓
    Prime numbers:       Only divisor is 1 → sum=1 ≠ num → false ✓
    Perfect squares:     pair != d check prevents double counting ✓
    num = 6:             1+2+3 = 6 → true ✓
    Large perfect (33550336): √33550336 ≈ 5792 → fast ✓


KEY TECHNIQUE:
    Divisor pairs:       d and n/d always come together
    √n optimization:     Only check half the divisors, infer the rest
    Integer square root: isqrt for precision
    Exclusion logic:     Skip self (num) and avoid double-count (d == pair)


EDGE CASES:
    num = 1:             false (no proper divisors) ✓
    num = 2:             false (1 ≠ 2) ✓
    num = 6:             true (1+2+3 = 6) ✓
    num = 28:            true (1+2+4+7+14 = 28) ✓
    num = 496:           true ✓
    num = 8128:          true ✓
    num = 33550336:      true ✓
    num = 100000000:     false ✓
    Prime number (97):   false ✓


TIME COMPLEXITY: O(√n)
    Loop runs from 2 to √n
    Each iteration does O(1) work (modulo + division)
    For n = 10^8: √n = 10^4 → very fast

SPACE COMPLEXITY: O(1)
    Only a few integer variables (sum_divisors, d, pair)


CONCEPTS USED:
    Number theory (divisors, perfect numbers)
    Divisor pair optimization (√n trick)
    Integer square root (isqrt for precision)
    Modular arithmetic (% for divisibility check)
    Defensive programming (edge case guards)
"""
