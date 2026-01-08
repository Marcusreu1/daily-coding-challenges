# 7. Reverse Integer
# Difficulty: Medium
# https://leetcode.com/problems/reverse-integer/

"""
PROBLEM:
Given a signed 32-bit integer x, return x with its digits reversed.
If reversing x causes the value to go outside the signed 32-bit integer range
[-2^31, 2^31 - 1], then return 0.

CONSTRAINTS:
- -2^31 <= x <= 2^31 - 1
- Cannot store 64-bit integers

EXAMPLES:
Input: x = 123    → Output: 321
Input: x = -123   → Output: -321
Input: x = 120    → Output: 21
Input: x = 1534236469 → Output: 0 (overflow)

32-BIT SIGNED INTEGER RANGE:
- Minimum: -2,147,483,648 (-2^31)
- Maximum:  2,147,483,647 (2^31 - 1)
"""

# STEP 1: Define 32-bit integer limits
# STEP 2: Save sign and work with absolute value
# STEP 3: Extract digits using modulo, build reversed number
# STEP 4: Restore original sign
# STEP 5: Check for overflow, return 0 if out of range

class Solution:
    def reverse(self, x: int) -> int:
        
        INT_MAX = 2**31 - 1                                                      # 2147483647
        INT_MIN = -2**31                                                         # -2147483648
        
        signo = -1 if x < 0 else 1                                               # Save sign
        x = abs(x)                                                               # Work with positive
        
        resultado = 0                                                            # Build reversed number here
        
        while x != 0:                                                            # While there are digits
            digito = x % 10                                                      # Extract last digit
            x = x // 10                                                          # Remove last digit
            resultado = resultado * 10 + digito                                  # Append digit to result
        
        resultado = signo * resultado                                            # Restore sign
        
        if resultado < INT_MIN or resultado > INT_MAX:                           # Check overflow
            return 0
        
        return resultado

"""
WHY EACH PART:
- INT_MAX/INT_MIN: Define valid range for 32-bit signed integers
- signo: Preserves negative sign, allows working with positive numbers
- abs(x): Simplifies digit extraction (% works predictably with positives)
- x % 10: Extracts rightmost digit (123 % 10 = 3)
- x // 10: Removes rightmost digit (123 // 10 = 12)
- resultado * 10 + digito: Shifts existing digits left, appends new digit
- Overflow check at end: Python handles big ints, so we check after building

HOW IT WORKS (Example: x = 123):
Initial: x=123, resultado=0

Iteration 1:
├── digito = 123 % 10 = 3
├── x = 123 // 10 = 12
└── resultado = 0 * 10 + 3 = 3

Iteration 2:
├── digito = 12 % 10 = 2
├── x = 12 // 10 = 1
└── resultado = 3 * 10 + 2 = 32

Iteration 3:
├── digito = 1 % 10 = 1
├── x = 1 // 10 = 0
└── resultado = 32 * 10 + 1 = 321

x = 0, exit loop
Return: 321 ✓

KEY TECHNIQUE:
- Digit extraction: Use modulo (%) and integer division (//)
- Number building: Multiply by 10 and add (shifts digits left)
- Sign handling: Process absolute value, restore sign at end
- Overflow detection: Compare against 32-bit limits

# Note: String approach is simpler but uses more memory and
# may not be allowed in interviews focusing on math manipulation

EDGE CASES:
- Single digit (x=5): Returns 5 ✓
- Zero (x=0): Returns 0 ✓
- Negative (x=-123): Returns -321 ✓
- Trailing zeros (x=120): Returns 21 (leading zeros disappear) ✓
- Overflow positive (x=1534236469): Returns 0 ✓
- Overflow negative (x=-1534236469): Returns 0 ✓
- Max int (x=2147483647): Returns 0 (7463847412 > max) ✓
- Min int (x=-2147483648): Returns 0 (overflow) ✓

TIME COMPLEXITY: O(log₁₀(x)) - Process each digit once (≈10 iterations max for 32-bit)
SPACE COMPLEXITY: O(1) - Only use fixed number of variables

CONCEPTS USED:
- Modulo operator (%) for digit extraction
- Integer division (//) for digit removal
- Number construction by multiplication and addition
- Sign preservation with absolute value
- 32-bit integer overflow handling
- While loop with mathematical termination condition
"""
