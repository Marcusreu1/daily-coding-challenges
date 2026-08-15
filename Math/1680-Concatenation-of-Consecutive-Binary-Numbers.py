# 1680. Concatenation of Consecutive Binary Numbers
# Difficulty: Medium
# https://leetcode.com/problems/concatenation-of-consecutive-binary-numbers/

"""
PROBLEM:
Given an integer n, return the decimal value of the binary string formed by concatenating the binary representations of 1 to n in order, modulo 10^9 + 7.

EXAMPLES:
Input: n = 1 → Output: 1
Explanation: "1" in binary is "1", which translates to 1 in decimal.

Input: n = 3 → Output: 27
Explanation: In binary, 1, 2, and 3 are "1", "10", and "11".
Concatenating them gives "11011". "11011" in decimal is 27.

Input: n = 12 → Output: 505379714
Explanation: The concatenated binary string is "1101110010111011110001001101010111100".
The decimal value is 118505380540.
Modulo 10^9 + 7, the result is 505379714.

CONSTRAINTS:
- 1 <= n <= 10^5

BITWISE CONCATENATION RULES:
To concatenate a new binary number 'i' to our current result:
1. Find how many bits 'i' occupies (let's call it 'length').
2. Shift the current result to the left by 'length' positions to make room for 'i'.
3. Add 'i' to the result (using bitwise OR | or addition +).
4. Apply modulo 10^9 + 7 to prevent integer overflow and massive memory consumption.

VISUALIZATION (n=3):
Modulo = 10^9 + 7
Initial result = 0

i = 1 (binary "1", length = 1):
  result = (result << 1) | 1 = (0 << 1) | 1 = 0 | 1 = 1

i = 2 (binary "10", length = 2):
  result = (result << 2) | 2 = (1 << 2) | 2 = 4 | 2 = 6 (binary "110")

i = 3 (binary "11", length = 2):
  result = (result << 2) | 3 = (6 << 2) | 3 = 24 | 3 = 27 (binary "11011")

Result: 27 ✓
"""

# STEP 1: Initialize the result to 0 and define the modulo constant.
# STEP 2: Iterate through every number from 1 to n.
# STEP 3: Find the binary length of the current number.
# STEP 4: Left-shift the current result by that length, bitwise OR the current number, and apply modulo.
# STEP 5: Return the final result.

class Solution:
    def concatenatedBinary(self, n: int) -> int:
        
        result = 0                                                           # Accumulator for the final decimal value
        MOD = 10**9 + 7                                                      # Required modulo value
        
        for i in range(1, n + 1):                                            # Iterate from 1 up to n
            
            length = i.bit_length()                                          # Calculate how many bits 'i' needs
            
            result = ((result << length) | i) % MOD                          # Shift left, merge with 'i', and apply modulo
            
        return result

"""
WHY EACH PART:
- result = 0: Safe starting point for bitwise shifting and logical OR.
- MOD = 10**9 + 7: Standard modulo to keep the integer sizes manageable.
- range(1, n + 1): We must process every integer exactly in order from 1 to n inclusive.
- i.bit_length(): Efficient built-in Python method. Faster than len(bin(i)) - 2.
- result << length: Shifting bits left acts as a base-2 multiplication (e.g., shifting by 2 is multiplying by 4) to make exact space.
- | i: Bitwise OR combines the shifted result with the new number. (Since the shifted space is filled with 0s, OR works identically to addition).
- % MOD: Keeps the number within limits at every step. Arithmetic rules allow modulo distribution across additions/multiplications.

HOW IT WORKS (Example: n = 2):

Initial: n = 2, result = 0, MOD = 1000000007

Iteration 1 (i = 1):
├── length = 1.bit_length() = 1
├── result << 1 = 0 << 1 = 0
├── 0 | 1 = 1
├── result = 1 % MOD
└── result = 1

Iteration 2 (i = 2):
├── length = 2.bit_length() = 2 (since 2 is "10" in binary)
├── result << 2 = 1 << 2 = 4 (binary "100")
├── 4 | 2 = 6 (binary "110")
├── result = 6 % MOD
└── result = 6

Exit: Loop finishes

return 6 ✓ (which is binary "110" -> "1" concatenated with "10")

KEY TECHNIQUE:
- Bit manipulation: Operating directly on bits instead of converting to strings prevents memory allocation overhead.
- Step-by-step Modulo: Prevents numbers from reaching a size where Python's arbitrarily large integers become computationally expensive to multiply/shift.

EDGE CASES:
- n = 1: Loop runs once, returning 1 correctly.
- n = 10^5: Maximum constraint. Evaluates efficiently without memory exhaustion due to the bitwise approach and modulo truncation.

TIME COMPLEXITY: O(n) - We iterate exactly n times, and bit_length() combined with shift/or runs in O(1) time.
SPACE COMPLEXITY: O(1) - We only store three integer variables (result, MOD, length) regardless of n's size.

CONCEPTS USED:
- Bitwise Operations (Left Shift, OR)
- Modulo Arithmetic Properties
- Integer Bit Length
"""
