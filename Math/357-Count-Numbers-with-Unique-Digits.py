"""
357. Count Numbers with Unique Digits
Difficulty: Medium
https://leetcode.com/problems/count-numbers-with-unique-digits/

PROBLEM:
Given an integer n, return the count of all numbers with unique digits x,
where 0 <= x < 10^n.

EXAMPLES:
Input: n = 2 → Output: 91
    Range [0, 100): all numbers 0-99 except 11,22,33,44,55,66,77,88,99
    91 numbers have unique digits

Input: n = 0 → Output: 1
    Range [0, 1): only 0

CONSTRAINTS:
• 0 <= n <= 8

KEY INSIGHT:
Count combinatorially by number of digits.

For k-digit numbers (k >= 2):
- First digit: 9 choices (1-9, can't be 0)
- Second digit: 9 choices (0-9 minus first)
- Third digit: 8 choices (0-9 minus first two)
- ...and so on

Formula: count(k) = 9 × 9 × 8 × 7 × ... × (11-k)

LIMIT:
Only 10 unique digits exist (0-9).
Cannot have 11+ digit number with all unique digits.
So for n > 10, result equals result for n = 10.

TABLE OF VALUES:
┌─────┬────────────────────────────┬───────────┐
│  n  │  Formula                   │  Result   │
├─────┼────────────────────────────┼───────────┤
│  0  │  1                         │     1     │
│  1  │  10                        │    10     │
│  2  │  10 + 9×9                  │    91     │
│  3  │  91 + 9×9×8                │   739     │
│  4  │  739 + 9×9×8×7             │  5275     │
│  5  │  5275 + 9×9×8×7×6          │ 32491     │
└─────┴────────────────────────────┴───────────┘
"""


# ============================================================================
# SOLUTION 1: ITERATIVE (Most intuitive)
# ============================================================================

class Solution:
    def countNumbersWithUniqueDigits(self, n: int) -> int:
        
        if n == 0:
            return 1                                             # Only 0
        
        # Start with single digit numbers (0-9)
        total = 10
        unique_digits = 9                                        # First digit choices (1-9)
        available = 9                                            # Remaining digit choices
        
        for i in range(2, n + 1):                               # For 2-digit to n-digit numbers
            unique_digits *= available                           # Multiply by available choices
            total += unique_digits                               # Add to total
            available -= 1                                       # One less choice for next position
            
            if available < 0:                                    # Can't have more than 10 digits
                break
        
        return total


# ============================================================================
# SOLUTION 2: MATHEMATICAL WITH FORMULA
# ============================================================================

class Solution:
    def countNumbersWithUniqueDigits(self, n: int) -> int:
        
        if n == 0:
            return 1
        
        if n > 10:                                               # Cap at 10 (max unique digits)
            n = 10
        
        total = 10                                               # 1-digit: 0-9
        
        for k in range(2, n + 1):
            # k-digit numbers with unique digits
            # = 9 × 9 × 8 × 7 × ... × (11-k)
            count_k = 9
            for j in range(9, 10 - k, -1):                       # 9, 8, 7, ...
                count_k *= j
            total += count_k
        
        return total


# ============================================================================
# SOLUTION 3: USING PERMUTATION FORMULA
# ============================================================================

import math


class Solution:
    def countNumbersWithUniqueDigits(self, n: int) -> int:
        
        if n == 0:
            return 1
        
        n = min(n, 10)                                           # Cap at 10
        
        total = 10                                               # 1-digit numbers
        
        for k in range(2, n + 1):
            # count(k) = 9 × P(9, k-1) = 9 × 9!/(10-k)!
            total += 9 * math.perm(9, k - 1)
        
        return total


# ============================================================================
# SOLUTION 4: DYNAMIC PROGRAMMING
# ============================================================================

class Solution:
    def countNumbersWithUniqueDigits(self, n: int) -> int:
        
        if n == 0:
            return 1
        
        # dp[k] = count of k-digit numbers with unique digits
        dp = [0] * 11
        dp[1] = 10
        
        for k in range(2, 11):
            # First digit: 9 choices
            # Remaining k-1 digits: P(9, k-1) choices
            dp[k] = 9
            available = 9
            for _ in range(k - 1):
                dp[k] *= available
                available -= 1
        
        # Sum up to n digits
        return sum(dp[1:min(n, 10) + 1])


"""
HOW EACH SOLUTION WORKS:

SOLUTION 1 - ITERATIVE:
┌────────────────────────────────────────────────────────────┐
│  n = 3:                                                    │
│  ├── Start: total = 10 (digits 0-9)                       │
│  │                                                        │
│  ├── i = 2 (2-digit numbers):                             │
│  │   unique_digits = 9 × 9 = 81                           │
│  │   total = 10 + 81 = 91                                 │
│  │   available = 8                                        │
│  │                                                        │
│  ├── i = 3 (3-digit numbers):                             │
│  │   unique_digits = 81 × 8 = 648                         │
│  │   total = 91 + 648 = 739                               │
│  │   available = 7                                        │
│  │                                                        │
│  └── Return 739 ✓                                         │
└────────────────────────────────────────────────────────────┘

VISUAL EXPLANATION:

For 3-digit numbers (100 to 999):
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   Position:     [___]  [___]  [___]                       │
│                  1st    2nd    3rd                        │
│                                                            │
│   Choices:       9   ×   9   ×   8   =  648               │
│                  ↓       ↓       ↓                        │
│               (1-9)  (0-9     (0-9                        │
│              can't   minus    minus                       │
│              be 0    1st)     1st,2nd)                    │
│                                                            │
└────────────────────────────────────────────────────────────┘

WHY FIRST DIGIT HAS 9 CHOICES, NOT 10?
┌────────────────────────────────────────────────────────────┐
│  A k-digit number cannot start with 0!                     │
│                                                            │
│  Example: "052" is NOT a 3-digit number, it's just "52"   │
│                                                            │
│  So first digit must be 1-9 → 9 choices                   │
│  Second digit can be 0-9 minus first → 9 choices          │
│  Third digit can be 0-9 minus first two → 8 choices       │
└────────────────────────────────────────────────────────────┘

COUNTING BREAKDOWN FOR n = 2:
┌────────────────────────────────────────────────────────────┐
│  1-digit (0-9):                                            │
│  └── 10 numbers, ALL have unique digits                   │
│                                                            │
│  2-digit (10-99):                                          │
│  ├── Total: 90 numbers                                    │
│  ├── Non-unique: 11,22,33,44,55,66,77,88,99 = 9 numbers  │
│  └── Unique: 90 - 9 = 81 numbers                          │
│      OR: 9 × 9 = 81 (combinatorial)                       │
│                                                            │
│  Total: 10 + 81 = 91 ✓                                    │
└────────────────────────────────────────────────────────────┘

WHY CAP AT n = 10?
┌────────────────────────────────────────────────────────────┐
│  Only 10 unique digits exist: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9│
│                                                            │
│  An 11-digit number MUST repeat at least one digit!       │
│  (Pigeonhole principle)                                    │
│                                                            │
│  Maximum unique-digit number:                              │
│  9,876,543,210 (uses each digit exactly once)             │
│                                                            │
│  For n > 10, count of 11+ digit unique numbers = 0        │
│  So result is same as n = 10                              │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────┐
│  n = 0  →  Range [0,1) = {0} → 1                          │
│  n = 1  →  Range [0,10) = {0-9} → 10                      │
│  n = 8  →  Result = 2,345,851 (constraint max)            │
│  n > 10 →  Same as n = 10 → 8,877,691                     │
└────────────────────────────────────────────────────────────┘

MATHEMATICAL FORMULA:
┌────────────────────────────────────────────────────────────┐
│  For k-digit numbers (k ≥ 2):                              │
│                                                            │
│  count(k) = 9 × P(9, k-1)                                 │
│           = 9 × 9!/(10-k)!                                │
│           = 9 × 9 × 8 × 7 × ... × (11-k)                  │
│                                                            │
│  Where P(n,r) = n!/(n-r)! is the permutation formula      │
│                                                            │
│  Total = 10 + Σ(k=2 to n) count(k)                        │
└────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1-4:  O(n) or O(n²) depending on implementation │
│  Solution 5:    O(1) with precomputed table               │
│                                                            │
│  Since n ≤ 8 (or effectively ≤ 10), all are O(1)         │
└────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1-3:  O(1)                                       │
│  Solution 4:    O(n) for DP array                         │
│  Solution 5:    O(1) but requires precomputation          │
└────────────────────────────────────────────────────────────┘

CONCEPTS USED:
• Combinatorics (permutations)
• Counting Principles
• Dynamic Programming (optional)
• Mathematical Formulas
"""
