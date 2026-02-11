# 263. Ugly Number
# Difficulty: Easy
# https://leetcode.com/problems/ugly-number/

"""
PROBLEM:
An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5.
Given an integer n, return true if n is an ugly number.

EXAMPLES:
Input: n = 6   → Output: true   (6 = 2 × 3)
Input: n = 1   → Output: true   (1 has no prime factors)
Input: n = 14  → Output: false  (14 = 2 × 7, has prime factor 7)

CONSTRAINTS:
- -2³¹ <= n <= 2³¹ - 1

KEY INSIGHT:
If a number is ugly, removing ALL factors of 2, 3, and 5 should leave 1.
If anything else remains, it has other prime factors → not ugly.

ALGORITHM:
1. Handle edge case: n <= 0 is not ugly
2. Divide by 2 while divisible
3. Divide by 3 while divisible
4. Divide by 5 while divisible
5. If result is 1 → ugly, else → not ugly

SOLUTION:
Repeatedly divide by 2, 3, 5 and check if 1 remains.
"""

# STEP 1: Handle non-positive numbers
# STEP 2: Remove all factors of 2, 3, and 5
# STEP 3: Check if result is 1

class Solution:
    def isUgly(self, n: int) -> bool:
        
        if n <= 0:                                                               # Non-positive = not ugly
            return False
        
        for factor in [2, 3, 5]:                                                 # Ugly factors only
            while n % factor == 0:                                               # While divisible
                n //= factor                                                     # Remove this factor
        
        return n == 1                                                            # If 1 remains, it's ugly


"""
WHY EACH PART:
- n <= 0: By definition, ugly numbers are POSITIVE integers
- for factor in [2, 3, 5]: Only these three primes are allowed
- while n % factor == 0: Keep dividing while divisible
- n //= factor: Remove one instance of this factor
- return n == 1: If only 2,3,5 were factors, n should be 1 now

HOW IT WORKS (Example: n = 30):

┌─ Initial ─────────────────────────────────────────────────┐
│  n = 30                                                   │
│  30 = 2 × 3 × 5                                           │
└───────────────────────────────────────────────────────────┘

┌─ Factor = 2 ──────────────────────────────────────────────┐
│  30 % 2 == 0? Yes → n = 30 // 2 = 15                      │
│  15 % 2 == 0? No  → exit while                            │
│  n = 15                                                   │
└───────────────────────────────────────────────────────────┘

┌─ Factor = 3 ──────────────────────────────────────────────┐
│  15 % 3 == 0? Yes → n = 15 // 3 = 5                       │
│   5 % 3 == 0? No  → exit while                            │
│  n = 5                                                    │
└───────────────────────────────────────────────────────────┘

┌─ Factor = 5 ──────────────────────────────────────────────┐
│  5 % 5 == 0? Yes → n = 5 // 5 = 1                         │
│  1 % 5 == 0? No  → exit while                             │
│  n = 1                                                    │
└───────────────────────────────────────────────────────────┘

┌─ Result ──────────────────────────────────────────────────┐
│  n == 1? Yes → return True ✓                              │
└───────────────────────────────────────────────────────────┘

HOW IT WORKS (Example: n = 14, NOT ugly):

┌─ Factor = 2 ──────────────────────────────────────────────┐
│  14 % 2 == 0? Yes → n = 14 // 2 = 7                       │
│   7 % 2 == 0? No  → exit while                            │
│  n = 7                                                    │
└───────────────────────────────────────────────────────────┘

┌─ Factor = 3 ──────────────────────────────────────────────┐
│  7 % 3 == 0? No → skip                                    │
│  n = 7                                                    │
└───────────────────────────────────────────────────────────┘

┌─ Factor = 5 ──────────────────────────────────────────────┐
│  7 % 5 == 0? No → skip                                    │
│  n = 7                                                    │
└───────────────────────────────────────────────────────────┘

┌─ Result ──────────────────────────────────────────────────┐
│  n == 1? No (n = 7) → return False ✗                      │
│  The factor 7 could not be removed!                       │
└───────────────────────────────────────────────────────────┘

WHY ORDER DOESN'T MATTER:
┌────────────────────────────────────────────────────────────┐
│  n = 60 = 2² × 3 × 5                                       │
│                                                            │
│  Order 2,3,5:  60 → 15 → 5 → 1 ✓                          │
│  Order 3,5,2:  60 → 20 → 4 → 1 ✓                          │
│  Order 5,2,3:  60 → 12 → 3 → 1 ✓                          │
│                                                            │
│  All orders give the same result!                         │
│  (Because multiplication/division is commutative)          │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION 1 (explicit loops):

class Solution:
    def isUgly(self, n: int) -> bool:
        if n <= 0:
            return False
        
        while n % 2 == 0:
            n //= 2
        
        while n % 3 == 0:
            n //= 3
        
        while n % 5 == 0:
            n //= 5
        
        return n == 1

ALTERNATIVE SOLUTION 2 (recursive):

class Solution:
    def isUgly(self, n: int) -> bool:
        if n <= 0:
            return False
        if n == 1:
            return True
        
        if n % 2 == 0:
            return self.isUgly(n // 2)
        if n % 3 == 0:
            return self.isUgly(n // 3)
        if n % 5 == 0:
            return self.isUgly(n // 5)
        
        return False                                                             # Has other prime factors

ALTERNATIVE SOLUTION 3 (one-liner using reduce):

from functools import reduce

class Solution:
    def isUgly(self, n: int) -> bool:
        if n <= 0:
            return False
        
        # Remove all factors of 2, 3, 5
        for p in [2, 3, 5]:
            while n % p == 0:
                n //= p
        
        return n == 1

WHY n = 1 IS UGLY:
┌────────────────────────────────────────────────────────────┐
│  1 has NO prime factors at all.                            │
│                                                            │
│  The definition says: "prime factors LIMITED TO 2, 3, 5"   │
│                                                            │
│  Having no prime factors doesn't violate this - it's       │
│  actually the most "pure" case of being ugly.              │
│                                                            │
│  Think of it as: 1 = 2⁰ × 3⁰ × 5⁰                          │
│                                                            │
│  1 is the "base case" of ugly numbers, from which all      │
│  other ugly numbers are built by multiplying by 2, 3, or 5.│
└────────────────────────────────────────────────────────────┘

MATHEMATICAL REPRESENTATION:
┌────────────────────────────────────────────────────────────┐
│  A number is ugly if and only if it can be written as:     │
│                                                            │
│       n = 2ᵃ × 3ᵇ × 5ᶜ                                     │
│                                                            │
│  where a, b, c >= 0                                        │
│                                                            │
│  Examples:                                                 │
│  1  = 2⁰ × 3⁰ × 5⁰                                         │
│  2  = 2¹ × 3⁰ × 5⁰                                         │
│  6  = 2¹ × 3¹ × 5⁰                                         │
│  30 = 2¹ × 3¹ × 5¹                                         │
│  36 = 2² × 3² × 5⁰                                         │
└────────────────────────────────────────────────────────────┘

RELATED PROBLEMS:
┌────────────────────────────────────────────────────────────┐
│  263. Ugly Number      - Check if n is ugly (this problem) │
│  264. Ugly Number II   - Find nth ugly number              │
│  313. Super Ugly Number - Generalized with k primes        │
│  1201. Ugly Number III - Count ugly numbers up to n        │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- n = 0: Returns False (not positive) ✓
- n = 1: Returns True (no prime factors) ✓
- n = -6: Returns False (negative) ✓
- n = 2: Returns True ✓
- n = 7: Returns False (7 is prime, not 2,3,5) ✓
- n = 8: Returns True (2³) ✓
- n = 14: Returns False (2 × 7) ✓
- Large ugly: n = 2³⁰ → Returns True ✓

VERIFICATION TABLE:
┌──────────┬────────────────────┬─────────────┬───────────┐
│    n     │  Prime Factors     │  Remaining  │  Ugly?    │
├──────────┼────────────────────┼─────────────┼───────────┤
│    1     │  (none)            │      1      │    ✓      │
│    2     │  2                 │      1      │    ✓      │
│    6     │  2 × 3             │      1      │    ✓      │
│    7     │  7                 │      7      │    ✗      │
│    8     │  2³                │      1      │    ✓      │
│   14     │  2 × 7             │      7      │    ✗      │
│   30     │  2 × 3 × 5         │      1      │    ✓      │
│   49     │  7²                │      49     │    ✗      │
│  100     │  2² × 5²           │      1      │    ✓      │
│  101     │  101 (prime)       │     101     │    ✗      │
└──────────┴────────────────────┴─────────────┴───────────┘

TIME COMPLEXITY: O(log n)
- In worst case, we divide by 2 about log₂(n) times
- Total divisions bounded by log₂(n) + log₃(n) + log₅(n) = O(log n)

SPACE COMPLEXITY: O(1)
- Only using a constant amount of space
- No additional data structures

CONCEPTS USED:
- Prime factorization
- Divisibility testing
- Loop until condition
- Integer division
"""
