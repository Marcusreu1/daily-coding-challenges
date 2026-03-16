"""
441. Arranging Coins
Difficulty: Easy
https://leetcode.com/problems/arranging-coins/

PROBLEM:
You have n coins and you want to build a staircase with them.
The staircase consists of k rows where the i-th row has exactly
i coins. The last row of the staircase may be incomplete.

Given n, return the number of COMPLETE rows of the staircase.

EXAMPLES:
Input: n = 5  → Output: 2
    Row 1: *       (1 coin)
    Row 2: * *     (2 coins)
    Row 3: * *     (incomplete, only 2 of 3)
    → 2 complete rows

Input: n = 8  → Output: 3
    Row 1: *         (1 coin)
    Row 2: * *       (2 coins)
    Row 3: * * *     (3 coins)
    Row 4: * *       (incomplete, only 2 of 4)
    → 3 complete rows

CONSTRAINTS:
    1 <= n <= 2^31 - 1

KEY INSIGHT:
k complete rows need k×(k+1)/2 coins (triangular number).
Find the largest k where k×(k+1)/2 ≤ n.
This is a quadratic equation: k = ⌊(-1 + √(1+8n)) / 2⌋

CHALLENGES:
    Brute force subtraction is O(√n) — works but slow
    Binary search is O(log n) — good but overkill
    Math formula is O(1) — optimal!
    Floating point precision for large n

MATHEMATICAL DERIVATION:
    k×(k+1)/2 = n
    k² + k - 2n = 0
    k = (-1 + √(1 + 8n)) / 2    (quadratic formula, positive root)
    Take floor for complete rows only

SOLUTION:
    Apply quadratic formula directly → O(1)
"""

# STEP 1: Apply quadratic formula
# STEP 2: Take integer part (floor) for complete rows

from math import isqrt

class Solution:
    def arrangeCoins(self, n: int) -> int:

        return (isqrt(8 * n + 1) - 1) // 2                              # Quadratic formula with integer math

"""
WHY EACH PART:

    8 * n + 1: The discriminant (1 + 8n) from the quadratic formula
    isqrt(...): Integer square root — exact, no floating point errors
    - 1: The "-1" in (-1 + √(1+8n))
    // 2: Integer division by 2 gives us floor automatically
    Combined: ⌊(-1 + √(1+8n)) / 2⌋ in one clean expression

HOW IT WORKS (Example: n = 8):

    8 * 8 + 1 = 65
    isqrt(65) = 8       (√65 = 8.06..., integer part = 8)
    8 - 1 = 7
    7 // 2 = 3

    Verification: 3×4/2 = 6 ≤ 8 ✓, 4×5/2 = 10 > 8 ✓
    Result: 3 ✓

HOW IT WORKS (Example: n = 5):

    8 * 5 + 1 = 41
    isqrt(41) = 6       (√41 = 6.40..., integer part = 6)
    6 - 1 = 5
    5 // 2 = 2

    Verification: 2×3/2 = 3 ≤ 5 ✓, 3×4/2 = 6 > 5 ✓
    Result: 2 ✓

HOW IT WORKS (Example: n = 1):

    8 * 1 + 1 = 9
    isqrt(9) = 3        (√9 = 3, exact!)
    3 - 1 = 2
    2 // 2 = 1

    Verification: 1×2/2 = 1 ≤ 1 ✓
    Result: 1 ✓

WHY isqrt INSTEAD OF sqrt:

    math.sqrt(n) returns FLOAT → precision errors for large n
    ├── sqrt(65) = 8.06225774...  (approximate)
    └── For n near 2^31, could round wrong way

    math.isqrt(n) returns EXACT INTEGER → no precision issues
    ├── isqrt(65) = 8  (exact integer square root)
    └── Always correct, even for n = 2^31 - 1 ✓

WHY // 2 INSTEAD OF / 2:

    / 2 returns float:  7 / 2 = 3.5
    // 2 returns int:   7 // 2 = 3  (floor division)

    We need floor because partial rows don't count.
    Integer division gives us floor automatically ✓

ALTERNATIVE APPROACHES:

    Approach 1 — Brute Force O(√n):
        k = 0
        while n >= k + 1:
            k += 1
            n -= k
        return k
        Simple but slow for n = 2^31

    Approach 2 — Binary Search O(log n):
        lo, hi = 1, n
        while lo <= hi:
            mid = (lo + hi) // 2
            if mid*(mid+1)//2 <= n:
                lo = mid + 1
            else:
                hi = mid - 1
        return hi
        Good but more code than needed

    Approach 3 — Math Formula O(1) (this solution):
        return (isqrt(8*n + 1) - 1) // 2
        One line, optimal ✓

TRIANGULAR NUMBERS REFERENCE:

    k:     1   2   3   4    5    6    7
    T(k):  1   3   6   10   15   21   28
    
    T(k) = k×(k+1)/2
    
    Given n coins, find largest k where T(k) ≤ n

EDGE CASES:

    n = 1: Only 1 row → returns 1 ✓
    n = 2: Row1=1, Row2 incomplete → returns 1 ✓
    n = 3: Row1=1, Row2=2, exact → returns 2 ✓
    n = 6: Exactly 3 rows (1+2+3=6) → returns 3 ✓
    n = 2^31-1: isqrt handles large values correctly ✓
    Perfect triangular n: Returns exact k (no leftover) ✓

TIME COMPLEXITY: O(1)
    Single arithmetic expression
    isqrt is O(1) for fixed-size integers

SPACE COMPLEXITY: O(1)
    No extra data structures, just arithmetic

CONCEPTS USED:
    Triangular numbers (1+2+...+k = k(k+1)/2)
    Quadratic formula (ax² + bx + c = 0)
    Integer square root (avoids floating point errors)
    Floor division for "complete" counting
    Mathematical optimization (O(n) → O(1))
"""
