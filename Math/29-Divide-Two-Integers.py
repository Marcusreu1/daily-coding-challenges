# 29. Divide Two Integers
# Difficulty: Medium
# https://leetcode.com/problems/divide-two-integers/

"""
PROBLEM:
Divide two integers WITHOUT using multiplication (*), division (/), or mod (%).
Return the quotient TRUNCATED toward zero.
If result overflows 32-bit signed integer range, return 2^31 - 1.

KEY INSIGHT:
Division is repeated subtraction. Instead of subtracting one at a time,
subtract in powers of 2 for efficiency (bit shifting).

EXAMPLES:
Input: dividend = 10, divisor = 3   → Output: 3  (10/3 = 3.33... → 3)
Input: dividend = 7, divisor = -3   → Output: -2 (7/-3 = -2.33... → -2)
Input: dividend = -2147483648, divisor = -1 → Output: 2147483647 (overflow case)

CONSTRAINTS:
- -2^31 <= dividend, divisor <= 2^31 - 1
- divisor != 0

APPROACH:
1. Handle overflow edge case
2. Determine result sign
3. Work with absolute values
4. Use bit shifting to find largest (divisor × 2^k) that fits
5. Subtract and accumulate quotient
6. Apply sign to result
"""

# STEP 1: Define 32-bit limits and handle overflow case
# STEP 2: Determine if result should be negative
# STEP 3: Convert to absolute values
# STEP 4: Repeatedly find largest power-of-2 multiple of divisor that fits
# STEP 5: Subtract that multiple, add corresponding power of 2 to quotient
# STEP 6: Apply sign and return

class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        
        INT_MAX = 2**31 - 1                                                      # 2147483647
        INT_MIN = -2**31                                                         # -2147483648
        
        # Overflow case: -2147483648 / -1 = 2147483648 (exceeds INT_MAX)
        if dividend == INT_MIN and divisor == -1:                                # Special overflow case
            return INT_MAX
        
        # XOR of signs: True if result should be negative
        signo_negativo = (dividend < 0) != (divisor < 0)                         # Different signs → negative
        
        dividend = abs(dividend)                                                 # Work with positive values
        divisor = abs(divisor)
        
        cociente = 0                                                             # Build quotient here
        
        while dividend >= divisor:                                               # While divisor fits
            temp = divisor                                                       # Current multiple of divisor
            multiplo = 1                                                         # Corresponding power of 2
            
            while dividend >= (temp << 1):                                       # While double fits
                temp <<= 1                                                       # Double the divisor multiple
                multiplo <<= 1                                                   # Double the count
            
            dividend -= temp                                                     # Subtract largest fitting multiple
            cociente += multiplo                                                 # Add corresponding count
        
        if signo_negativo:                                                       # Apply sign
            cociente = -cociente
        
        return cociente

"""
WHY EACH PART:
- INT_MAX/INT_MIN: Define 32-bit overflow boundaries
- Overflow check: Only -2147483648 / -1 causes overflow (result is 2147483648)
- signo_negativo: XOR (!=) of signs determines result sign
- abs(): Work with positives, apply sign at end (avoids truncation direction issues)
- Outer while: Continue while dividend can still be divided
- Inner while: Find largest 2^k where (divisor × 2^k) <= dividend
- temp << 1: Double without multiplication (left shift = ×2)
- multiplo << 1: Track how many times we're subtracting (power of 2)
- dividend -= temp: Subtract the multiple we found
- cociente += multiplo: Add that many divisors to quotient

HOW IT WORKS (Example: dividend = 43, divisor = 8):
Initial: dividend=43, divisor=8, cociente=0

Round 1:
├── Inner loop: find largest fitting power of 2
│   temp=8, mult=1 → 43 >= 16? Yes → temp=16, mult=2
│   temp=16, mult=2 → 43 >= 32? Yes → temp=32, mult=4
│   temp=32, mult=4 → 43 >= 64? No → stop
├── dividend = 43 - 32 = 11
└── cociente = 0 + 4 = 4

Round 2:
├── Inner loop:
│   temp=8, mult=1 → 11 >= 16? No → stop immediately
├── dividend = 11 - 8 = 3
└── cociente = 4 + 1 = 5

Round 3:
├── 3 >= 8? No → exit outer loop

Result: 5 ✓ (43 ÷ 8 = 5.375 → truncated = 5)

HOW BIT SHIFTING WORKS:
x << 1 = x × 2 (left shift doubles)
x << 2 = x × 4
x << 3 = x × 8
x << n = x × 2^n

Example: 3 << 2 = 3 × 4 = 12
Binary: 011 << 2 = 1100 = 12

KEY TECHNIQUE:
- Bit shifting for multiplication by powers of 2
- Binary search style: find largest fitting multiple
- Greedy: always subtract the largest possible amount
- Sign handling: work with absolutes, apply sign at end

WHY TRUNCATE TOWARD ZERO (not floor):
Python // does floor division:
  7 // 3 = 2
  -7 // 3 = -3 (floor, toward negative infinity)

Problem wants truncation toward zero:
  7 / 3 → 2 (toward zero)
  -7 / 3 → -2 (toward zero, NOT -3)

By using abs() and applying sign at end, we get truncation.

EDGE CASES:
- dividend = divisor (e.g., 5/5): Returns 1 ✓
- dividend < divisor (e.g., 3/5): Returns 0 ✓
- Negative dividend (e.g., -10/3): Returns -3 ✓
- Negative divisor (e.g., 10/-3): Returns -3 ✓
- Both negative (e.g., -10/-3): Returns 3 ✓
- divisor = 1: Returns dividend ✓
- divisor = -1: Returns -dividend (watch overflow) ✓
- Overflow (-2147483648 / -1): Returns 2147483647 ✓
- Large numbers: Handled efficiently with bit shifting ✓

TIME COMPLEXITY: O(log²n) - Outer loop O(log n), inner loop O(log n)
SPACE COMPLEXITY: O(1) - Only fixed number of variables

CONCEPTS USED:
- Bit manipulation (left shift << for ×2)
- Division as repeated subtraction
- Greedy algorithm (largest fitting multiple first)
- Sign handling with XOR logic
- 32-bit integer overflow handling
- Truncation toward zero
"""
