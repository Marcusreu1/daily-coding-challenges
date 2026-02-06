# 231. Power of Two
# Difficulty: Easy
# https://leetcode.com/problems/power-of-two/

"""
PROBLEM:
Given an integer n, return true if it is a power of two. Otherwise, return false.

An integer n is a power of two if there exists an integer x such that n == 2^x.

EXAMPLES:
Input: n = 1   → Output: true   (2⁰ = 1)
Input: n = 16  → Output: true   (2⁴ = 16)
Input: n = 3   → Output: false
Input: n = 0   → Output: false
Input: n = -1  → Output: false

CONSTRAINTS:
- -2³¹ <= n <= 2³¹ - 1

KEY INSIGHT:
Powers of 2 in binary have EXACTLY one bit set to 1:
  1 = 0001,  2 = 0010,  4 = 0100,  8 = 1000, ...

The expression n & (n-1) removes the rightmost set bit.
If n is a power of 2, removing its only set bit gives 0.

FORMULA:
n & (n - 1) == 0  means n has only one bit set (power of 2)

But we also need n > 0 because:
- 0 is not a power of 2
- Negative numbers are not powers of 2

SOLUTION:
return n > 0 and (n & (n - 1)) == 0
"""

# STEP 1: Check if n is positive (0 and negatives are not powers of 2)
# STEP 2: Check if n has exactly one bit set using n & (n-1) == 0

class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        
        return n > 0 and (n & (n - 1)) == 0


"""
WHY EACH PART:
- n > 0: Powers of 2 must be positive (1, 2, 4, 8, ...)
- n & (n - 1): Removes the rightmost set bit
- == 0: If result is 0, n had exactly one bit set → power of 2

HOW IT WORKS (Example: n = 8):

┌─ Binary Analysis ─────────────────────────────────────────┐
│                                                           │
│      n   = 8  = 1000  (binary)                            │
│    n - 1 = 7  = 0111  (binary)                            │
│                                                           │
│  When we subtract 1 from a power of 2:                    │
│  • The single 1 bit becomes 0                             │
│  • All bits to its right become 1                         │
│                                                           │
│     1000  (8)                                             │
│   - 0001  (1)                                             │
│   ──────                                                  │
│     0111  (7)                                             │
│                                                           │
│  Now AND them:                                            │
│     1000  (n)                                             │
│   & 0111  (n-1)                                           │
│   ──────                                                  │
│     0000  = 0  ✓                                          │
│                                                           │
│  Result is 0 → n is a power of 2                          │
└───────────────────────────────────────────────────────────┘

HOW IT WORKS (Example: n = 6, NOT power of 2):

┌─ Binary Analysis ─────────────────────────────────────────┐
│                                                           │
│      n   = 6  = 0110  (binary)                            │
│    n - 1 = 5  = 0101  (binary)                            │
│                                                           │
│     0110  (n)                                             │
│   & 0101  (n-1)                                           │
│   ──────                                                  │
│     0100  = 4  ≠ 0  ✗                                     │
│                                                           │
│  Result is NOT 0 → n is NOT a power of 2                  │
└───────────────────────────────────────────────────────────┘

WHY n & (n-1) REMOVES RIGHTMOST SET BIT:
┌────────────────────────────────────────────────────────────┐
│  When you subtract 1 from any binary number:               │
│                                                            │
│  n     = ...xxxxx10000   (rightmost 1 at some position)   │
│  n-1   = ...xxxxx01111   (that 1→0, all right bits→1)     │
│                                                            │
│  The AND operation:                                        │
│  • Left of rightmost 1: same bits, AND = same             │
│  • At rightmost 1: 1 & 0 = 0                              │
│  • Right of it: 0 & 1 = 0                                 │
│                                                            │
│  Result: rightmost 1 is removed!                          │
└────────────────────────────────────────────────────────────┘

EDGE CASE: n = 0
┌────────────────────────────────────────────────────────────┐
│  0 & (0-1) = 0 & (-1) = 0                                 │
│                                                            │
│  In binary (using 32-bit):                                │
│  0  = 00000000000000000000000000000000                    │
│  -1 = 11111111111111111111111111111111  (all 1s)          │
│                                                            │
│  0 & -1 = 0                                               │
│                                                            │
│  BUT 0 is NOT a power of 2!                               │
│  That's why we check n > 0 first.                         │
└────────────────────────────────────────────────────────────┘

EDGE CASE: n = 1
┌────────────────────────────────────────────────────────────┐
│  1 is 2⁰, so it IS a power of 2.                          │
│                                                            │
│  n = 1 = 0001                                              │
│  n-1 = 0 = 0000                                            │
│  n & (n-1) = 0001 & 0000 = 0000 = 0  ✓                    │
│                                                            │
│  1 > 0? Yes  ✓                                             │
│  Result: True                                              │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION 1 (Loop):

class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        if n <= 0:
            return False
        
        while n > 1:
            if n % 2 != 0:                                                       # Odd number, not power of 2
                return False
            n //= 2
        
        return True                                                              # n == 1

ALTERNATIVE SOLUTION 2 (Bit count):

class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and bin(n).count('1') == 1

ALTERNATIVE SOLUTION 3 (n & -n):

class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and (n & -n) == n

# n & -n isolates the rightmost set bit
# If that equals n, then n has only one bit set

ALTERNATIVE SOLUTION 5 (Bit length):

class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and n == (1 << (n.bit_length() - 1))

# n.bit_length() gives number of bits needed
# 1 << (bit_length - 1) creates power of 2 with same number of bits
# If they're equal, n is a power of 2

VERIFICATION TABLE:
┌──────────┬────────────┬─────────────┬─────────────┬─────────┐
│    n     │   Binary   │   n & (n-1) │  n > 0?     │ Result  │
├──────────┼────────────┼─────────────┼─────────────┼─────────┤
│    1     │    0001    │    0000     │    Yes      │  True   │
│    2     │    0010    │    0000     │    Yes      │  True   │
│    3     │    0011    │    0010     │    Yes      │  False  │
│    4     │    0100    │    0000     │    Yes      │  True   │
│    5     │    0101    │    0100     │    Yes      │  False  │
│    6     │    0110    │    0100     │    Yes      │  False  │
│    7     │    0111    │    0110     │    Yes      │  False  │
│    8     │    1000    │    0000     │    Yes      │  True   │
│    0     │    0000    │    0000     │    No       │  False  │
│   -1     │  (neg)     │    N/A      │    No       │  False  │
│   16     │   10000    │    00000    │    Yes      │  True   │
└──────────┴────────────┴─────────────┴─────────────┴─────────┘

RELATED BIT MANIPULATION TRICKS:
┌────────────────────────────────────────────────────────────┐
│  n & (n-1)    → Remove rightmost set bit                  │
│  n & (-n)     → Isolate rightmost set bit                 │
│  n | (n+1)    → Set rightmost unset bit                   │
│  n ^ (n-1)    → Get mask from rightmost set bit           │
│                                                            │
│  Check power of 2:  n & (n-1) == 0                        │
│  Count set bits:    while n: count+=1; n &= n-1           │
│  Get lowest bit:    n & (-n)                              │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- n = 1: True (2⁰ = 1) ✓
- n = 0: False (not a power of 2) ✓
- n = -1: False (negative) ✓
- n = -16: False (negative) ✓
- n = 2³¹-1: False (not power of 2) ✓
- n = 2³⁰: True (largest power of 2 in range) ✓

TIME COMPLEXITY: O(1)
- Single bitwise AND operation
- Single comparison
- Constant time regardless of input size

SPACE COMPLEXITY: O(1)
- No additional data structures
- Only using input variable

CONCEPTS USED:
- Bit manipulation
- Binary representation of powers of 2
- Bitwise AND operation
- Two's complement (for negative numbers)
- Boolean short-circuit evaluation
"""
