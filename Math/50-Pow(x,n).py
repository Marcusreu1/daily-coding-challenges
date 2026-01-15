 # 50. Pow(x, n)
# Difficulty: Medium
# https://leetcode.com/problems/powx-n/

"""
PROBLEM:
Implement pow(x, n), which calculates x raised to the power n (x^n).

EXAMPLES:
Input: x = 2.00000, n = 10    → Output: 1024.00000
Input: x = 2.10000, n = 3     → Output: 9.26100
Input: x = 2.00000, n = -2    → Output: 0.25000 (1/4)

CONSTRAINTS:
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31 - 1
- n is an integer
- Either x != 0 or n > 0
- -10^4 <= x^n <= 10^4

KEY INSIGHT:
Use binary exponentiation (exponentiation by squaring):
- If n is even: x^n = (x^(n/2))²
- If n is odd:  x^n = x × x^(n-1)

This reduces O(n) to O(log n).

MATHEMATICAL BASIS:
x^13 where 13 = 1101 in binary (8 + 4 + 0 + 1)
x^13 = x^8 × x^4 × x^1

We build powers x, x², x⁴, x⁸, ... and multiply those 
corresponding to '1' bits in n.
"""

# STEP 1: Handle negative exponent (x^(-n) = 1/x^n)
# STEP 2: Use binary exponentiation
# STEP 3: If n is odd, multiply result by current x
# STEP 4: Square x and halve n each iteration
# STEP 5: Return accumulated result

class Solution:
    def myPow(self, x: float, n: int) -> float:
        
        if n == 0:                                                               # x^0 = 1
            return 1
        
        if x == 1:                                                               # 1^n = 1
            return 1
        
        if x == -1:                                                              # (-1)^n depends on parity
            return 1 if n % 2 == 0 else -1
        
        exponente = abs(n)                                                       # Work with positive exponent
        
        if n < 0:                                                                # x^(-n) = (1/x)^n
            x = 1 / x
        
        resultado = 1.0                                                          # Accumulate result here
        
        while exponente > 0:                                                     # Binary exponentiation
            if exponente % 2 == 1:                                               # If current bit is 1
                resultado *= x                                                   # Multiply into result
            x *= x                                                               # Square x for next iteration
            exponente //= 2                                                      # Move to next bit
        
        return resultado

"""
WHY EACH PART:
- n == 0: Any number to power 0 is 1 (except 0^0, undefined but we return 1)
- x == 1: Optimization - 1 to any power is 1
- x == -1: Optimization - result depends only on whether n is even/odd
- exponente = abs(n): Avoid overflow when n = -2^31 (can't negate in int32)
- n < 0 → x = 1/x: Transform negative exponent to positive
- exponente % 2 == 1: Check if current bit is 1 (odd means LSB is 1)
- resultado *= x: Include this power of x in result
- x *= x: Build sequence x, x², x⁴, x⁸, x¹⁶, ...
- exponente //= 2: Shift right, move to next bit

HOW IT WORKS (Example: x = 2, n = 10):

n = 10 in binary: 1010

Iteration | n (binary) | n % 2 | resultado | x
----------|------------|-------|-----------|----
    0     | 1010       |   0   | 1         | 2
    1     | 101        |   1   | 1×4=4     | 4
    2     | 10         |   0   | 4         | 16
    3     | 1          |   1   | 4×256=1024| 256
    4     | 0          | done  | 1024      | -

Result: 1024 ✓

Breakdown:
- Bit 0 (value 1): OFF → don't include x^1
- Bit 1 (value 2): ON  → include x^2 = 4... wait

Actually let me retrace:
n=10 (1010): last bit 0, skip, x=4, n=5
n=5  (101):  last bit 1, res=4, x=16, n=2
n=2  (10):   last bit 0, skip, x=256, n=1
n=1  (1):    last bit 1, res=4*256=1024, n=0

Result: 1024 ✓

KEY TECHNIQUE:
- Binary exponentiation: Reduce time from O(n) to O(log n)
- Bit manipulation insight: Each bit in n corresponds to a power of x
- Build-and-select: Build x^(2^k) sequence, select based on bits of n

EDGE CASES:
- n = 0: Returns 1 ✓
- x = 0, n > 0: Returns 0 (0 to any positive power is 0) ✓
- x = 1: Returns 1 (optimization) ✓
- x = -1, n even: Returns 1 ✓
- x = -1, n odd: Returns -1 ✓
- n = -2147483648: Handled by using abs() ✓
- Large n (10^9): Fast due to O(log n) ✓
- x = 2, n = -2: Returns 0.25 ✓

TIME COMPLEXITY: O(log n) - Halve n each iteration
SPACE COMPLEXITY: O(1) iterative, O(log n) recursive

CONCEPTS USED:
- Binary exponentiation (exponentiation by squaring)
- Bit manipulation / binary representation
- Divide and conquer
- Negative exponent handling
- Integer overflow awareness
- Mathematical properties of exponents
"""
