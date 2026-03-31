"""
504. Base 7
Difficulty: Easy
https://leetcode.com/problems/base-7/

PROBLEM:
    Given an integer num, return a string of its base 7 representation.

EXAMPLES:
    Input: num = 100  → Output: "202"   (2×49 + 0×7 + 2×1 = 100)
    Input: num = -7   → Output: "-10"   (-(1×7 + 0×1) = -7)
    Input: num = 0    → Output: "0"

CONSTRAINTS:
    -10^7 <= num <= 10^7

KEY INSIGHT:
    Repeatedly divide by 7 and collect remainders.
    Remainders (read in reverse) form the base 7 digits.
    
    num % 7  → extracts the current rightmost digit
    num // 7 → removes that digit, shifts number right

CHALLENGES:
    Handling negative numbers (work with absolute value, add sign at end)
    Handling zero (special case, loop won't execute)

SOLUTION:
    Handle 0 and negative sign separately.
    Divide by 7 repeatedly, collect remainders.
    Reverse the collected digits to get final answer.
"""


# STEP 1: Handle special case num = 0
# STEP 2: Handle negative sign separately
# STEP 3: Repeatedly divide by 7, collect remainders
# STEP 4: Reverse digits and join with sign


class Solution:
    def convertToBase7(self, num: int) -> str:

        if num == 0:                                                  # Special case: 0 in any base is "0"
            return "0"

        sign = "-" if num < 0 else ""                                 # Save sign, work with positive
        n = abs(num)                                                  # Work with absolute value

        digits = []                                                   # Collect digits (reversed order)

        while n > 0:                                                  # Extract digits one by one
            digits.append(str(n % 7))                                 # Remainder = current rightmost digit
            n //= 7                                                   # Remove that digit

        digits.reverse()                                              # Digits were collected backwards

        return sign + "".join(digits)                                 # Combine sign + digits


"""
WHY EACH PART:
    num == 0:            While loop won't execute for 0, must return "0" directly
    sign:                Store sign before converting to positive — reattach at end
    abs(num):            Division/modulo works cleanly with positive numbers
    digits = []:         Collect remainders as strings for easy joining
    n % 7:               Extracts the rightmost base-7 digit
    n //= 7:             Removes that digit (like shifting right in base 7)
    digits.reverse():    We collected least-significant first, need most-significant first
    sign + "".join():    Reconstruct the final string with sign


HOW IT WORKS (Example: num = 100):

    sign = "", n = 100

    Iteration 1: n = 100
    ├── 100 % 7 = 2   → digits = ["2"]
    └── 100 // 7 = 14 → n = 14

    Iteration 2: n = 14
    ├── 14 % 7 = 0    → digits = ["2", "0"]
    └── 14 // 7 = 2   → n = 2

    Iteration 3: n = 2
    ├── 2 % 7 = 2     → digits = ["2", "0", "2"]
    └── 2 // 7 = 0    → n = 0

    n = 0 → STOP
    reverse → ["2", "0", "2"]
    return "" + "202" = "202" ✅

    Verification: 2×7² + 0×7¹ + 2×7⁰ = 98 + 0 + 2 = 100 ✓


HOW IT WORKS (Example: num = -7):

    sign = "-", n = 7

    Iteration 1: n = 7
    ├── 7 % 7 = 0     → digits = ["0"]
    └── 7 // 7 = 1    → n = 1

    Iteration 2: n = 1
    ├── 1 % 7 = 1     → digits = ["0", "1"]
    └── 1 // 7 = 0    → n = 0

    n = 0 → STOP
    reverse → ["1", "0"]
    return "-" + "10" = "-10" ✅

    Verification: -(1×7¹ + 0×7⁰) = -(7 + 0) = -7 ✓


WHY % AND // EXTRACT DIGITS:
    Think of decimal: how do you get the last digit of 345?
        345 % 10 = 5  (last digit)
        345 // 10 = 34 (remaining digits)

    Same principle, just replace 10 with 7:
        100 % 7 = 2   (last base-7 digit)
        100 // 7 = 14  (remaining base-7 digits)

    It's like "peeling off" digits from right to left!


WHY REVERSE AT THE END:
    We collect digits RIGHT to LEFT (least significant first):
    
    100 → remainders: 2, 0, 2
                      ↑        ↑
                   rightmost  leftmost
    
    But we read numbers LEFT to RIGHT:
    Result: "202" (leftmost first)
    
    So we reverse! [2, 0, 2] → [2, 0, 2] (same in this case)
    
    Another example: 50 → remainders: 1, 0, 1 → reverse → "101"
        50 % 7 = 1,  50 // 7 = 7
         7 % 7 = 0,   7 // 7 = 1
         1 % 7 = 1,   1 // 7 = 0
    Collected: ["1","0","1"] → reversed: ["1","0","1"] → "101"
    Check: 1×49 + 0×7 + 1×1 = 50 ✓


HANDLING SPECIAL CASES:
    num = 0:             Return "0" directly (loop doesn't execute) ✓
    Negative numbers:    Save sign, work with abs, reattach at end ✓
    num = 1:             1 % 7 = 1, 1 // 7 = 0 → "1" ✓
    num = 7:             Returns "10" (1×7 + 0 = 7) ✓
    Large num (10^7):    log₇(10^7) ≈ 8.3 → max ~9 digits ✓


KEY TECHNIQUE:
    Repeated division:   Classic base conversion algorithm
    Modulo operator:     Extracts rightmost digit in target base
    Integer division:    Shifts number right in target base
    Reverse collection:  Digits come out backwards, reverse to fix
    Sign handling:       Process absolute value, prepend sign


EDGE CASES:
    num = 0:             "0" ✓
    num = 1:             "1" ✓
    num = 7:             "10" ✓
    num = -1:            "-1" ✓
    num = -7:            "-10" ✓
    num = 10^7:          "150666343" (fits in string) ✓
    num = -10^7:         "-150666343" ✓


TIME COMPLEXITY: O(log₇ n)
    Each iteration divides n by 7
    Number of iterations = number of digits in base 7
    = floor(log₇(n)) + 1

SPACE COMPLEXITY: O(log₇ n)
    Store the digits of the base 7 representation
    At most ~9 digits for n up to 10^7


CONCEPTS USED:
    Number base conversion
    Modular arithmetic (% for digit extraction)
    Integer division (// for digit removal)
    String manipulation (reverse + join)
    Sign handling for negative numbers
"""
