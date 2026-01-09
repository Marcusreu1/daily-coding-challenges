# 9. Palindrome Number
# Difficulty: Easy
# https://leetcode.com/problems/palindrome-number/

"""
PROBLEM:
Given an integer x, return true if x is a palindrome, and false otherwise.
A palindrome reads the same backward as forward.

EXAMPLES:
Input: x = 121    → Output: true  (121 reversed is 121)
Input: x = -121   → Output: false (-121 reversed is "121-")
Input: x = 10     → Output: false (10 reversed is 01 = 1)

CONSTRAINTS:
- -2^31 <= x <= 2^31 - 1

FOLLOW UP: Solve without converting integer to string.

KEY INSIGHT:
- Negative numbers are NEVER palindromes (sign is at start only)
- Numbers ending in 0 (except 0 itself) are NEVER palindromes
- We only need to reverse HALF the number and compare
"""

# STEP 1: Handle edge cases (negatives, trailing zeros)
# STEP 2: Reverse second half of number digit by digit
# STEP 3: Stop when reversed half >= remaining first half
# STEP 4: Compare halves (handle odd-length numbers)

class Solution:
    def isPalindrome(self, x: int) -> bool:
        
        # Negative numbers and numbers ending in 0 (except 0) are not palindromes
        if x < 0 or (x % 10 == 0 and x != 0):                                    # Edge cases
            return False
        
        invertido = 0                                                            # Will hold reversed second half
        
        while x > invertido:                                                     # Until we reach the middle
            digito = x % 10                                                      # Extract last digit
            x = x // 10                                                          # Remove last digit
            invertido = invertido * 10 + digito                                  # Build reversed number
        
        # Even length: x == invertido (e.g., 1221 → x=12, invertido=12)
        # Odd length: x == invertido // 10 (e.g., 121 → x=1, invertido=12, 12//10=1)
        return x == invertido or x == invertido // 10                            # Compare halves

"""
WHY EACH PART:
- x < 0: Negative numbers can't be palindromes ("-" only at start)
- x % 10 == 0 and x != 0: Numbers ending in 0 can't be palindromes (would need leading 0)
- while x > invertido: Stops at middle (reversed half catches up to remaining half)
- x % 10: Extracts rightmost digit
- x // 10: Removes rightmost digit
- invertido * 10 + digito: Builds reversed number from extracted digits
- x == invertido // 10: Handles odd-length numbers (middle digit in invertido)

HOW IT WORKS (Example: x = 12321):
Initial: x = 12321, invertido = 0

Iteration 1:
├── digito = 1, x = 1232, invertido = 1
└── 1232 > 1? Yes, continue

Iteration 2:
├── digito = 2, x = 123, invertido = 12
└── 123 > 12? Yes, continue

Iteration 3:
├── digito = 3, x = 12, invertido = 123
└── 12 > 123? No, exit loop

Compare:
├── x == invertido? → 12 == 123? No
└── x == invertido // 10? → 12 == 12? Yes ✓

Return: True

HOW IT WORKS (Example: x = 1221):
Initial: x = 1221, invertido = 0

Iteration 1: x = 122, invertido = 1
Iteration 2: x = 12, invertido = 12

12 > 12? No, exit loop

Compare: x == invertido → 12 == 12 ✓
Return: True

HOW IT WORKS (Example: x = 123):
Initial: x = 123, invertido = 0

Iteration 1: x = 12, invertido = 3
Iteration 2: x = 1, invertido = 32

1 > 32? No, exit loop

Compare:
├── 1 == 32? No
└── 1 == 3? No

Return: False ✓

KEY TECHNIQUE:
- Reverse half: Only reverse second half, compare with first half
- Early termination: Stop when reversed >= remaining (at middle)
- Odd/even handling: invertido // 10 removes middle digit for odd-length
- No overflow risk: Reversed half never exceeds original number

EDGE CASES:
- Single digit (x=7): Returns True (7 == 7) ✓
- Zero (x=0): Returns True (0 == 0) ✓
- Negative (x=-121): Returns False (immediate) ✓
- Ends in zero (x=10): Returns False (immediate) ✓
- Even palindrome (x=1221): Returns True ✓
- Odd palindrome (x=12321): Returns True ✓
- Not palindrome (x=123): Returns False ✓
- Large palindrome (x=123454321): Returns True ✓

TIME COMPLEXITY: O(log₁₀(x) / 2) ≈ O(log₁₀(x)) - Process half the digits
SPACE COMPLEXITY: O(1) - Only use fixed variables

CONCEPTS USED:
- Modulo operator (%) for digit extraction
- Integer division (//) for digit removal
- Early return for edge cases
- Loop termination at midpoint
- Handling even/odd length numbers
- Mathematical palindrome check without string conversion
"""
