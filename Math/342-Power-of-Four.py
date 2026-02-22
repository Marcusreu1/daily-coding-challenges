"""
342. Power of Four
Difficulty: Easy
https://leetcode.com/problems/power-of-four/

PROBLEM:
Given an integer n, return true if it is a power of four.
Otherwise, return false.

An integer n is a power of four if there exists an integer x
such that n == 4^x.

EXAMPLES:
Input: n = 16 → Output: true  (16 = 4²)
Input: n = 5  → Output: false (not a power of 4)
Input: n = 1  → Output: true  (1 = 4⁰)
Input: n = 8  → Output: false (8 = 2³, power of 2 but not 4)

CONSTRAINTS:
• -2³¹ <= n <= 2³¹ - 1

FOLLOW UP: Can you solve it without loops/recursion?

POWERS OF 4:
4⁰  = 1
4¹  = 4
4²  = 16
4³  = 64
4⁴  = 256
4⁵  = 1,024
...
4¹⁵ = 1,073,741,824  ← max in 32-bit signed int

KEY INSIGHT:
4 = 2², so 4^x = 2^(2x)
Powers of 4 are powers of 2 with EVEN exponents!

In binary, powers of 4 have their single 1-bit at EVEN positions:
    1  = 0001  (position 0) ✓
    4  = 0100  (position 2) ✓
    16 = 10000 (position 4) ✓

Powers of 2 that are NOT powers of 4 have 1-bit at ODD positions:
    2  = 0010  (position 1) ✗
    8  = 1000  (position 3) ✗
    32 = 100000 (position 5) ✗
"""


# ============================================================================
# SOLUTION 1: LOOP (Most intuitive)
# ============================================================================

class Solution:
    def isPowerOfFour(self, n: int) -> bool:
        
        if n <= 0:                                               # Powers of 4 are positive
            return False
        
        while n % 4 == 0:                                        # While divisible by 4
            n //= 4                                              # Divide by 4
        
        return n == 1                                            # Should reduce to 1


# ============================================================================
# SOLUTION 2: BITMASK (Most elegant - No loops!)
# ============================================================================

class Solution:
    def isPowerOfFour(self, n: int) -> bool:
        
        # Condition 1: n > 0 (must be positive)
        # Condition 2: n & (n-1) == 0 (must be power of 2)
        # Condition 3: n & 0x55555555 != 0 (bit at EVEN position)
        
        return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


# ============================================================================
# SOLUTION 3: LOGARITHM
# ============================================================================

import math


class Solution:
    def isPowerOfFour(self, n: int) -> bool:
        
        if n <= 0:
            return False
        
        log_result = math.log(n) / math.log(4)                   # log₄(n)
        
        return abs(log_result - round(log_result)) < 1e-10       # Check if integer


# ============================================================================
# SOLUTION 4: RECURSION
# ============================================================================

class Solution:
    def isPowerOfFour(self, n: int) -> bool:
        
        if n <= 0:
            return False
        
        if n == 1:                                               # Base case: 4⁰ = 1
            return True
        
        if n % 4 != 0:                                           # Not divisible by 4
            return False
        
        return self.isPowerOfFour(n // 4)                        # Recurse with n/4


"""
WHY EACH SOLUTION WORKS:

SOLUTION 1 - LOOP:
┌────────────────────────────────────────────────────────────┐
│  n = 64                                                    │
│  ├── 64 % 4 == 0 → n = 64 // 4 = 16                       │
│  ├── 16 % 4 == 0 → n = 16 // 4 = 4                        │
│  ├── 4 % 4 == 0  → n = 4 // 4 = 1                         │
│  ├── 1 % 4 == 1  → exit loop                              │
│  └── n == 1? YES → return True ✓                          │
│                                                            │
│  n = 8                                                     │
│  ├── 8 % 4 == 0  → n = 8 // 4 = 2                         │
│  ├── 2 % 4 == 2  → exit loop                              │
│  └── n == 1? NO (n=2) → return False ✓                    │
└────────────────────────────────────────────────────────────┘

SOLUTION 2 - BITMASK:
┌────────────────────────────────────────────────────────────┐
│  0x55555555 = 0101 0101 0101 0101 0101 0101 0101 0101     │
│               1s at EVEN positions (0, 2, 4, 6, ...)      │
│                                                            │
│  n = 16:                                                   │
│  ├── n > 0? YES ✓                                         │
│  ├── 16 & 15 = 10000 & 01111 = 0? YES ✓ (power of 2)     │
│  ├── 16 & 0x55555555 = 10000 & ...0101 = 10000 ≠ 0? YES ✓│
│  └── return True ✓                                        │
│                                                            │
│  n = 8:                                                    │
│  ├── n > 0? YES ✓                                         │
│  ├── 8 & 7 = 1000 & 0111 = 0? YES ✓ (power of 2)         │
│  ├── 8 & 0x55555555 = 1000 & ...0101 = 0? NO ✗           │
│  └── return False ✓                                       │
└────────────────────────────────────────────────────────────┘

SOLUTION 3 - MOD 3:
┌────────────────────────────────────────────────────────────┐
│  Why 4^k % 3 == 1?                                        │
│                                                            │
│  4 = 3 + 1, so 4 ≡ 1 (mod 3)                              │
│  4^k ≡ 1^k ≡ 1 (mod 3)                                    │
│                                                            │
│  Powers of 2 (not 4) give remainder 2:                    │
│  2^1 = 2  → 2 % 3 = 2                                     │
│  2^3 = 8  → 8 % 3 = 2                                     │
│  2^5 = 32 → 32 % 3 = 2                                    │
│                                                            │
│  Pattern for 2^k mod 3:                                   │
│  k=0: 1%3=1  k=1: 2%3=2  k=2: 4%3=1  k=3: 8%3=2 ...      │
│  Alternates between 1 and 2!                              │
│  Even k → 1 (power of 4)  Odd k → 2 (not power of 4)     │
└────────────────────────────────────────────────────────────┘

WHY 0x55555555?

┌────────────────────────────────────────────────────────────┐
│  Hex digit 5 = 0101 in binary                              │
│                                                            │
│  0x55555555 = 0101 0101 0101 0101 0101 0101 0101 0101     │
│                                                            │
│  Position:    31   27   23   19   15   11   7    3        │
│               0101 0101 0101 0101 0101 0101 0101 0101     │
│               ↑ ↑  ↑ ↑  ↑ ↑  ↑ ↑  ↑ ↑  ↑ ↑  ↑ ↑  ↑ ↑     │
│               30   26   22   18   14   10   6    2  0     │
│                28   24   20   16   12   8    4            │
│                                                            │
│  All 1s are at EVEN positions (0, 2, 4, 6, 8, ...)        │
│                                                            │
│  Powers of 4 have single bit at even position → AND ≠ 0   │
│  Powers of 2 (not 4) have bit at odd position → AND = 0   │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE MASK - 0xAAAAAAAA:
┌────────────────────────────────────────────────────────────┐
│  0xAAAAAAAA = 1010 1010 1010 1010 1010 1010 1010 1010     │
│  Has 1s at ODD positions                                   │
│                                                            │
│  Power of 4: n & 0xAAAAAAAA == 0 (no bit at odd position) │
│  Can also use: n & 0xAAAAAAAA == 0 instead of             │
│                n & 0x55555555 != 0                         │
└────────────────────────────────────────────────────────────┘

COMPARISON WITH POWER OF 2 AND POWER OF 3:

┌─────────────────────────────────────────────────────────────┐
│  Problem       │  Solution                                  │
├─────────────────────────────────────────────────────────────┤
│  Power of 2    │  n > 0 and n & (n-1) == 0                 │
│  Power of 3    │  n > 0 and 1162261467 % n == 0            │
│  Power of 4    │  n > 0 and n & (n-1) == 0 and             │
│                │      (n & 0x55555555 != 0  OR  n % 3 == 1)│
└─────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────┐
│  n = 0   → False (0 is not positive)                       │
│  n = 1   → True  (4⁰ = 1)                                  │
│  n = 2   → False (power of 2, not 4)                       │
│  n = 4   → True  (4¹ = 4)                                  │
│  n = 8   → False (2³, power of 2, not 4)                   │
│  n = -4  → False (negative)                                │
│  n = -16 → False (negative)                                │
│  n = 4¹⁵ = 1073741824 → True (max power of 4 in range)    │
└────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1 (Loop):     O(log₄ n)                          │
│  Solution 2 (Bitmask):  O(1)  ← Best!                      │
│  Solution 3 (Mod 3):    O(1)  ← Best!                      │
│  Solution 4 (Log):      O(1)                               │
│  Solution 5 (Recursion): O(log₄ n)                         │
└────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1-4:          O(1)                               │
│  Solution 5 (Recursion): O(log₄ n) - call stack            │
└────────────────────────────────────────────────────────────┘

COMMON MISTAKES:
Confusing power of 2 with power of 4
Forgetting n <= 0 case
Using wrong bitmask (0xAAAAAAAA vs 0x55555555)
Not understanding why mod 3 works

WHY CAN'T WE USE THE "LARGEST POWER" TRICK LIKE POWER OF 3?
┌────────────────────────────────────────────────────────────┐
│  For Power of 3: 3 is PRIME, so 3^19 only divisible by    │
│  powers of 3. We can use: 3^19 % n == 0                   │
│                                                            │
│  For Power of 4: 4 = 2² is NOT prime!                     │
│  4^15 = 2^30 is divisible by ALL powers of 2:             │
│  2^30 % 8 = 0, but 8 is NOT a power of 4!                 │
│                                                            │
│  The "largest power" trick ONLY works for prime bases!    │
└────────────────────────────────────────────────────────────┘

CONCEPTS USED:
• Bit Manipulation
• Bitmasks
• Modular Arithmetic
• Number Theory
• Binary Representation
"""
