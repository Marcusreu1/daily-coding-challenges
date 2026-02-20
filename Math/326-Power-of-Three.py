"""
326. Power of Three
Difficulty: Easy
https://leetcode.com/problems/power-of-three/

PROBLEM:
Given an integer n, return true if it is a power of three.
Otherwise, return false.

An integer n is a power of three if there exists an integer x
such that n == 3^x.

EXAMPLES:
Input: n = 27 → Output: true  (27 = 3³)
Input: n = 0  → Output: false (no power of 3 equals 0)
Input: n = 9  → Output: true  (9 = 3²)
Input: n = 45 → Output: false (45 = 9 × 5 = 3² × 5)

CONSTRAINTS:
• -2³¹ <= n <= 2³¹ - 1

FOLLOW UP: Can you solve it without loops/recursion?

POWERS OF 3 (for reference):
3⁰ = 1
3¹ = 3
3² = 9
3³ = 27
3⁴ = 81
3⁵ = 243
3⁶ = 729
3⁷ = 2,187
3⁸ = 6,561
3⁹ = 19,683
3¹⁰ = 59,049
...
3¹⁹ = 1,162,261,467  ← max in 32-bit signed int
"""


# ============================================================================
# SOLUTION 1: LOOP (Most intuitive)
# ============================================================================

class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        
        if n <= 0:                                               # Powers of 3 are positive
            return False
        
        while n % 3 == 0:                                        # While divisible by 3
            n //= 3                                              # Divide by 3
        
        return n == 1                                            # Should reduce to 1

# ============================================================================
# SOLUTION 2: RECURSION
# ============================================================================

class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        
        if n <= 0:
            return False
        
        if n == 1:                                               # Base case: 3⁰ = 1
            return True
        
        if n % 3 != 0:                                           # Not divisible by 3
            return False
        
        return self.isPowerOfThree(n // 3)                       # Recurse with n/3


"""
HOW EACH SOLUTION WORKS:

SOLUTION 1 - LOOP:
┌────────────────────────────────────────────────────────────┐
│  n = 27                                                    │
│  ├── 27 % 3 == 0 → n = 27 // 3 = 9                        │
│  ├── 9 % 3 == 0  → n = 9 // 3 = 3                         │
│  ├── 3 % 3 == 0  → n = 3 // 3 = 1                         │
│  ├── 1 % 3 == 1  → exit loop                              │
│  └── n == 1? YES → return True ✓                          │
│                                                            │
│  n = 45                                                    │
│  ├── 45 % 3 == 0 → n = 45 // 3 = 15                       │
│  ├── 15 % 3 == 0 → n = 15 // 3 = 5                        │
│  ├── 5 % 3 == 2  → exit loop                              │
│  └── n == 1? NO (n=5) → return False ✓                    │
└────────────────────────────────────────────────────────────┘

SOLUTION 2 - MATH TRICK:
┌────────────────────────────────────────────────────────────┐
│  Key: 3 is PRIME, so 3^19 only has 3 as prime factor      │
│                                                            │
│  n = 27 = 3³                                               │
│  ├── n > 0? YES                                            │
│  ├── 1162261467 % 27 = 0? YES (3^19 % 3³ = 3^16 × 0)      │
│  └── return True ✓                                         │
│                                                            │
│  n = 45 = 3² × 5                                           │
│  ├── n > 0? YES                                            │
│  ├── 1162261467 % 45 = 12 ≠ 0 (5 doesn't divide 3^19)     │
│  └── return False ✓                                        │
│                                                            │
│  n = 6 = 2 × 3                                             │
│  ├── n > 0? YES                                            │
│  ├── 1162261467 % 6 = 3 ≠ 0 (2 doesn't divide 3^19)       │
│  └── return False ✓                                        │
└────────────────────────────────────────────────────────────┘

WHY MATH TRICK WORKS (PROOF):
┌────────────────────────────────────────────────────────────┐
│  3 is prime, so:                                           │
│  3^19 = 3 × 3 × 3 × ... × 3 (only prime factor is 3)      │
│                                                            │
│  Case 1: n = 3^k where k ≤ 19                              │
│  → 3^19 = 3^k × 3^(19-k)                                   │
│  → 3^19 % 3^k = 0  ✓                                       │
│                                                            │
│  Case 2: n has prime factor p ≠ 3                          │
│  → 3^19 has no factor p                                    │
│  → 3^19 % n ≠ 0  ✓                                         │
│                                                            │
│  Case 3: n = 3^k where k > 19                              │
│  → n > 3^19                                                │
│  → 3^19 % n = 3^19 ≠ 0  ✓                                  │
│  (But this case doesn't exist in 32-bit int range)        │
└────────────────────────────────────────────────────────────┘

WHY THIS TRICK ONLY WORKS FOR PRIMES:
┌────────────────────────────────────────────────────────────┐
│  Example: "Power of 4" with same trick?                    │
│                                                            │
│  4^7 = 16384 (max power of 4 in reasonable range)          │
│  8 = 2³                                                    │
│  16384 % 8 = 0 ✓  BUT 8 is NOT power of 4!                │
│                                                            │
│  Why? 4 = 2², so 4^7 = 2^14                               │
│  8 = 2³ divides 2^14, but 8 ≠ 4^x for any integer x       │
│                                                            │
│  Only works when base is PRIME!                            │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────┐
│  n = 0   → False (0 is not positive)                       │
│  n = 1   → True  (3⁰ = 1)                                  │
│  n = -3  → False (negative, not power of 3)                │
│  n = -27 → False (negative)                                │
│  n = 2   → False (not power of 3)                          │
│  n = 3^19 = 1162261467 → True (max power in range)         │
└────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1 (Loop):     O(log₃ n)                          │
│  Solution 2 (Math):     O(1)  ← Best!                      │
│  Solution 3 (Log):      O(1)                               │
│  Solution 4 (Recursion): O(log₃ n)                         │
└────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1 (Loop):     O(1)                               │
│  Solution 2 (Math):     O(1)  ← Best!                      │
│  Solution 3 (Log):      O(1)                               │
│  Solution 4 (Recursion): O(log₃ n) - call stack            │
└────────────────────────────────────────────────────────────┘

COMPARISON TABLE:
┌─────────────┬───────────┬─────────┬─────────────────────────┐
│ Approach    │ Time      │ Space   │ Notes                   │
├─────────────┼───────────┼─────────┼─────────────────────────┤
│ Loop        │ O(log n)  │ O(1)    │ Most intuitive          │
│ Math Trick  │ O(1)      │ O(1)    │ Best! No loops          │
│ Logarithm   │ O(1)      │ O(1)    │ Floating point issues   │
│ Recursion   │ O(log n)  │ O(log n)│ Stack overhead          │
└─────────────┴───────────┴─────────┴─────────────────────────┘

COMMON MISTAKES:
Forgetting n <= 0 case
Using floating point log without precision check
Not knowing 3 must be PRIME for math trick
Integer overflow (not an issue in Python)

CONCEPTS USED:
• Prime Numbers
• Divisibility
• Logarithms
• Mathematical Properties
• Number Theory
"""
