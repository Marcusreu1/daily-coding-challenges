"""
728. Self Dividing Numbers
Difficulty: Easy
https://leetcode.com/problems/self-dividing-numbers/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

A self-dividing number is a number that is divisible by every digit
it contains. It must NOT contain the digit zero.

Given two integers left and right, return a list of all self-dividing
numbers in the range [left, right].

EXAMPLES:

    Input: left=1, right=22
    Output: [1,2,3,4,5,6,7,8,9,11,12,15,22]

    Input: left=47, right=85
    Output: [48,55,66,77]

CONSTRAINTS:

    1 <= left <= right <= 10^4

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

For each number in the range, extract every digit and check:
    1. No digit is zero (division by zero is undefined)
    2. The number is divisible by each of its digits

This is a straightforward simulation problem — no tricks needed.

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. DIGIT ZERO: Must reject numbers containing 0 before dividing
2. DIGIT EXTRACTION: Correctly pulling out each digit
3. EARLY EXIT: Stop checking as soon as one digit fails

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Iterate through each number in [left, right]
STEP 2: For each number, extract digits using modulo (% 10)
STEP 3: Check if digit is 0 OR number is not divisible by digit
STEP 4: If ALL digits pass, add to result list
"""


class Solution:
    def selfDividingNumbers(self, left: int, right: int) -> list:

        result = []                                                               # Collect all self-dividing numbers

        for num in range(left, right + 1):                                        # Check every number in range
            temp = num                                                            # Copy to extract digits from
            is_self_dividing = True                                               # Assume valid until proven otherwise

            while temp > 0:                                                       # Extract digits one by one
                digit = temp % 10                                                 # Get last digit

                if digit == 0 or num % digit != 0:                                # Zero digit OR not divisible
                    is_self_dividing = False                                       # Mark as invalid
                    break                                                         # No need to check more digits

                temp //= 10                                                       # Remove last digit, continue

            if is_self_dividing:                                                  # All digits passed the check
                result.append(num)                                                # Add to result list

        return result


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

result = []:
    Accumulator list for all self-dividing numbers found.

for num in range(left, right + 1):
    We must check every single number in the given range.
    right + 1 because range() is exclusive on the upper bound.

temp = num:
    We need a copy because we'll destroy temp while extracting
    digits, but we still need the original num for the modulo check.

is_self_dividing = True:
    Optimistic assumption. We only flip to False if a digit fails.
    This pattern avoids complex flag logic.

digit = temp % 10:
    Extracts the last (rightmost) digit.
    Example: 128 % 10 = 8

digit == 0:
    If any digit is zero, the number is immediately disqualified.
    Division by zero is undefined, so we can't even check.

num % digit != 0:
    The core check — is the ORIGINAL number divisible by this digit?
    We use num (not temp) because temp is being modified.

break:
    Early exit optimization. Once one digit fails, there's no point
    checking the remaining digits — the number is already invalid.

temp //= 10:
    Removes the last digit by integer division.
    Example: 128 // 10 = 12 → next iteration gets digit 2.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: num = 128):
════════════════════════════════════════════════════════════════

    temp = 128

    Iteration 1:
    ├── digit = 128 % 10 = 8
    ├── digit != 0 ✓
    ├── 128 % 8 = 0 ✓ (divisible)
    └── temp = 128 // 10 = 12

    Iteration 2:
    ├── digit = 12 % 10 = 2
    ├── digit != 0 ✓
    ├── 128 % 2 = 0 ✓ (divisible)
    └── temp = 12 // 10 = 1

    Iteration 3:
    ├── digit = 1 % 10 = 1
    ├── digit != 0 ✓
    ├── 128 % 1 = 0 ✓ (divisible)
    └── temp = 1 // 10 = 0

    temp == 0 → STOP
    is_self_dividing = True → append 128 ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: num = 26):
════════════════════════════════════════════════════════════════

    temp = 26

    Iteration 1:
    ├── digit = 26 % 10 = 6
    ├── digit != 0 ✓
    ├── 26 % 6 = 2 ✗ (NOT divisible!)
    ├── is_self_dividing = False
    └── BREAK (early exit, skip digit 2)

    is_self_dividing = False → skip ✗

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: num = 102):
════════════════════════════════════════════════════════════════

    temp = 102

    Iteration 1:
    ├── digit = 102 % 10 = 2
    ├── digit != 0 ✓
    ├── 102 % 2 = 0 ✓
    └── temp = 102 // 10 = 10

    Iteration 2:
    ├── digit = 10 % 10 = 0
    ├── digit == 0 ✗ (ZERO DETECTED!)
    ├── is_self_dividing = False
    └── BREAK (zero = immediate disqualification)

    is_self_dividing = False → skip ✗

════════════════════════════════════════════════════════════════
ALTERNATIVE APPROACH — STRING CONVERSION:
════════════════════════════════════════════════════════════════

    A more Pythonic one-liner approach:

    def selfDividingNumbers(self, left, right):
        return [
            num for num in range(left, right + 1)
            if all(d != '0' and num % int(d) == 0 for d in str(num))
        ]

    How it works:
    ├── str(num): converts 128 → "128"
    ├── for d in str(num): iterates '1', '2', '8'
    ├── d != '0': rejects numbers with zero digit
    ├── num % int(d) == 0: checks divisibility
    └── all(): ensures EVERY digit passes

    Pros: Very concise and readable
    Cons: String conversion has slight overhead

    Both approaches are valid — the math approach avoids
    string conversion, the string approach is more Pythonic.

════════════════════════════════════════════════════════════════
WHY MODULO EXTRACTION (MATH) VS STRING:
════════════════════════════════════════════════════════════════

    MATH (% 10 and // 10):
    ├── No type conversion needed
    ├── Works directly with integers
    ├── Slightly faster (no string allocation)
    └── More "algorithmic" — good for interviews

    STRING (str(num) iteration):
    ├── More readable and Pythonic
    ├── Fewer lines of code
    ├── Requires int() conversion back for each digit
    └── More "practical" — good for production code

    For this problem, both are perfectly fine since
    the constraint is small (right ≤ 10^4).

════════════════════════════════════════════════════════════════
SINGLE-DIGIT NUMBERS (1-9):
════════════════════════════════════════════════════════════════

    Every number from 1 to 9 is always self-dividing:
    ├── Only one digit (itself)
    ├── n % n = 0 always (any number divides itself)
    ├── No digit is zero (range starts at 1)
    └── All trivially pass ✓

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    left = right = 1           → [1] ✓
    left = right = 10          → [] (contains 0) ✓
    left = 1, right = 9        → [1,2,3,4,5,6,7,8,9] ✓
    Number with repeated digits → 11: 11%1=0 ✓, 22: 22%2=0 ✓
    Number with zero in middle → 102: rejected for digit 0 ✓
    Large number 9999          → 9999%9=0 ✓ → self-dividing ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O((right - left) × d)
════════════════════════════════════════════════════════════════

    (right - left + 1) numbers to check
    Each number has at most d digits (d ≤ 5 since max is 10^4)
    Per digit: O(1) modulo operation

    For the given constraint (right ≤ 10^4):
    → At most 10,000 numbers × 5 digits = 50,000 operations
    → Very fast ✓

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(1) auxiliary
════════════════════════════════════════════════════════════════

    Only a few integer variables (temp, digit, is_self_dividing).
    The result list is required output, not extra space.

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Digit extraction (modulo 10 and integer division)
    Divisibility check (modulo operator)
    Early termination (break on first failing digit)
    Edge case handling (zero digit detection)
    Brute force with pruning (simple but efficient for small input)
"""
