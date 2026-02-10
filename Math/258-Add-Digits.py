# 258. Add Digits
# Difficulty: Easy
# https://leetcode.com/problems/add-digits/

"""
PROBLEM:
Given an integer num, repeatedly add all its digits until the result
has only one digit, and return it.

EXAMPLES:
Input: num = 38  → Output: 2   (3+8=11, 1+1=2)
Input: num = 0   → Output: 0
Input: num = 123 → Output: 6   (1+2+3=6)

CONSTRAINTS:
- 0 <= num <= 2³¹ - 1

FOLLOW UP:
Could you do it without any loop/recursion in O(1) runtime?

KEY INSIGHT:
This is the "Digital Root" problem. There's a mathematical formula!

Any number N ≡ sum_of_digits(N) (mod 9)

Because: N = d₁×10ⁿ + d₂×10ⁿ⁻¹ + ... + dₙ×1
         10ⁿ ≡ 1 (mod 9)  for all n
         So N ≡ d₁ + d₂ + ... + dₙ (mod 9)

FORMULA:
- If num == 0: return 0
- If num % 9 == 0: return 9  (special case for multiples of 9)
- Otherwise: return num % 9

ELEGANT FORMULA:
return 1 + (num - 1) % 9  (handles the 9 case automatically)

SOLUTION:
Use the mathematical formula for O(1) time complexity.
"""

# STEP 1: Handle base case (num = 0)
# STEP 2: Apply digital root formula

class Solution:
    def addDigits(self, num: int) -> int:
        
        if num == 0:                                                             # Special case
            return 0
        
        return 1 + (num - 1) % 9                                                 # Digital root formula


"""
WHY EACH PART:
- if num == 0: Zero is a special case (digital root of 0 is 0)
- (num - 1): Shifts numbers so that 9 maps to 8, 18 maps to 17, etc.
- % 9: Gets the remainder (0-8 range)
- 1 + ...: Shifts back to 1-9 range
- This formula elegantly handles the case where num % 9 == 0 should return 9

HOW IT WORKS (Example: num = 38):

Mathematical approach:
┌───────────────────────────────────────────────────────────┐
│  num = 38                                                 │
│  (num - 1) = 37                                           │
│  37 % 9 = 1                                               │
│  1 + 1 = 2 ✓                                              │
│                                                           │
│  Verification: 3 + 8 = 11, 1 + 1 = 2 ✓                    │
└───────────────────────────────────────────────────────────┘

HOW IT WORKS (Example: num = 18, multiple of 9):

┌───────────────────────────────────────────────────────────┐
│  num = 18                                                 │
│  (num - 1) = 17                                           │
│  17 % 9 = 8                                               │
│  1 + 8 = 9 ✓                                              │
│                                                           │
│  Verification: 1 + 8 = 9 ✓                                │
│                                                           │
│  Without the formula: 18 % 9 = 0 (wrong!)                 │
└───────────────────────────────────────────────────────────┘

HOW IT WORKS (Example: num = 9999):

┌───────────────────────────────────────────────────────────┐
│  num = 9999                                               │
│  (num - 1) = 9998                                         │
│  9998 % 9 = 8                                             │
│  1 + 8 = 9 ✓                                              │
│                                                           │
│  Verification: 9+9+9+9 = 36, 3+6 = 9 ✓                    │
└───────────────────────────────────────────────────────────┘

WHY THE FORMULA WORKS (Mathematical Proof):
┌────────────────────────────────────────────────────────────┐
│  Any decimal number N can be written as:                   │
│                                                            │
│  N = aₙ×10ⁿ + aₙ₋₁×10ⁿ⁻¹ + ... + a₁×10 + a₀              │
│                                                            │
│  Since 10 ≡ 1 (mod 9), we have 10ᵏ ≡ 1 (mod 9)            │
│                                                            │
│  Therefore: N ≡ aₙ + aₙ₋₁ + ... + a₁ + a₀ (mod 9)         │
│                                                            │
│  This means N and sum(digits) have the same remainder      │
│  when divided by 9. Repeating this process always gives    │
│  the same remainder, which is the digital root.            │
│                                                            │
│  Special case: When N is divisible by 9 (but N ≠ 0),      │
│  the digital root is 9, not 0.                            │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION 1 (explicit conditions):

class Solution:
    def addDigits(self, num: int) -> int:
        if num == 0:
            return 0
        elif num % 9 == 0:
            return 9
        else:
            return num % 9

ALTERNATIVE SOLUTION 2 (iterative - O(log n)):

class Solution:
    def addDigits(self, num: int) -> int:
        while num >= 10:                                                         # More than one digit
            digit_sum = 0
            while num > 0:
                digit_sum += num % 10                                            # Add last digit
                num //= 10                                                       # Remove last digit
            num = digit_sum
        return num

ALTERNATIVE SOLUTION 3 (recursive):

class Solution:
    def addDigits(self, num: int) -> int:
        if num < 10:                                                             # Base case: single digit
            return num
        
        digit_sum = sum(int(d) for d in str(num))                                # Sum all digits
        return self.addDigits(digit_sum)                                         # Recurse

ALTERNATIVE SOLUTION 4 (using string conversion):

class Solution:
    def addDigits(self, num: int) -> int:
        while num >= 10:
            num = sum(int(d) for d in str(num))
        return num


DIGITAL ROOT PROPERTIES:
┌────────────────────────────────────────────────────────────┐
│  1. dr(a + b) = dr(dr(a) + dr(b))                          │
│  2. dr(a × b) = dr(dr(a) × dr(b))                          │
│  3. dr(n) = n mod 9 (except when n mod 9 = 0 and n ≠ 0)    │
│  4. A number is divisible by 9 iff dr(n) = 9               │
│  5. A number is divisible by 3 iff dr(n) ∈ {3, 6, 9}       │
└────────────────────────────────────────────────────────────┘

REAL-WORLD APPLICATIONS:
┌────────────────────────────────────────────────────────────┐
│  • Checksum verification (ISBN, credit cards)              │
│  • Divisibility tests (by 3 and 9)                         │
│  • Numerology (pseudoscience, but uses this concept!)      │
│  • Error detection in data transmission                    │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- num = 0: Returns 0 ✓
- num = 9: Returns 9 (not 0) ✓
- num = 10: Returns 1 ✓
- num = 18: Returns 9 ✓
- num = 2147483647: Returns 1 (works for max int) ✓

VERIFICATION TABLE:
┌──────────┬───────────────────┬─────────────────┬───────────┐
│   num    │  (num-1) % 9 + 1  │  Manual check   │  Correct? │
├──────────┼───────────────────┼─────────────────┼───────────┤
│    0     │   special case=0  │       0         │     ✓     │
│    1     │    0 + 1 = 1      │       1         │     ✓     │
│    9     │    8 + 1 = 9      │       9         │     ✓     │
│   10     │    0 + 1 = 1      │     1+0=1       │     ✓     │
│   38     │    1 + 1 = 2      │   3+8=11→1+1=2  │     ✓     │
│  100     │    0 + 1 = 1      │     1+0+0=1     │     ✓     │
│  999     │    8 + 1 = 9      │   27→9          │     ✓     │
└──────────┴───────────────────┴─────────────────┴───────────┘

TIME COMPLEXITY: O(1)
- Single arithmetic operation
- No loops or recursion

SPACE COMPLEXITY: O(1)
- Only using a constant amount of space
- No additional data structures

CONCEPTS USED:
- Digital root / repeated digit sum
- Modular arithmetic
- Number theory (congruence mod 9)
- Mathematical optimization
"""
