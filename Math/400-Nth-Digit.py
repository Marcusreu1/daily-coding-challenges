"""
400. Nth Digit
Difficulty: Medium
https://leetcode.com/problems/nth-digit/

PROBLEM:
Given an integer n, return the nth digit of the infinite integer sequence:
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...]

Written as a continuous string of digits:
    "123456789101112131415161718192021..."

Return the nth digit (1-indexed) of this string.

EXAMPLES:
Input: n = 3  → Output: 3
    "12[3]456..." → 3rd digit is '3'

Input: n = 11 → Output: 0
    "1234567891[0]11..." → 11th digit is '0' (from number 10)

CONSTRAINTS:
    1 <= n <= 2^31 - 1

KEY INSIGHT:
The sequence has a predictable structure grouped by digit length:
    1-digit (1-9):       9 numbers  ×  1 = 9 digits
    2-digit (10-99):     90 numbers ×  2 = 180 digits
    3-digit (100-999):   900 numbers × 3 = 2700 digits
    k-digit:             9×10^(k-1) × k digits

We can "skip" entire groups to locate the exact digit in O(log n).

CHALLENGES:
    n can be up to 2×10^9 — can't generate the sequence
    Must use math to jump directly to the answer
    Off-by-one errors with 1-indexed vs 0-indexed

SOLUTION:
    1. Subtract digit groups until n falls within current group
    2. Calculate which number within that group
    3. Extract which digit within that number
"""

# STEP 1: Skip complete digit groups to find the right group
# STEP 2: Find which number within the group
# STEP 3: Find which digit within that number

class Solution:
    def findNthDigit(self, n: int) -> int:

        digits = 1                                                       # Current digit length (1, 2, 3...)
        count = 9                                                        # Numbers in this group (9, 90, 900...)
        start = 1                                                        # First number in group (1, 10, 100...)

        while n > digits * count:                                        # Skip entire digit groups
            n -= digits * count                                          # Subtract this group's total digits
            digits += 1                                                  # Move to next digit length
            count *= 10                                                  # 10x more numbers in next group
            start *= 10                                                  # Next group starts at next power of 10

        number = start + (n - 1) // digits                               # Which number in this group
        digit_idx = (n - 1) % digits                                     # Which digit in that number (0-indexed)

        return int(str(number)[digit_idx])                               # Extract and return the digit

"""
WHY EACH PART:

    digits = 1: Start checking 1-digit numbers first
    count = 9: There are 9 one-digit numbers (1-9)
    start = 1: First 1-digit number is 1
    while n > digits * count: If n exceeds this group, skip it entirely
    n -= digits * count: Remove all digits consumed by this group
    digits += 1, count *= 10, start *= 10: Move to next group
    (n-1) // digits: 0-indexed position → which number (offset from start)
    (n-1) % digits: 0-indexed position → which digit within the number
    int(str(number)[digit_idx]): Convert number to string, pick the digit

HOW IT WORKS (Example: n = 11):

    STEP 1 - Find the group:
    ├── digits=1, count=9, start=1
    ├── 11 > 1×9 = 9? YES → skip group 1
    ├── n = 11 - 9 = 2
    ├── digits=2, count=90, start=10
    ├── 2 > 2×90 = 180? NO → we're in group 2
    └── n = 2, digits = 2, start = 10

    STEP 2 - Find the number:
    ├── number = 10 + (2-1) // 2 = 10 + 0 = 10
    └── We're looking at the number 10

    STEP 3 - Find the digit:
    ├── digit_idx = (2-1) % 2 = 1
    ├── str(10)[1] = '0'
    └── Result: 0 ✓

HOW IT WORKS (Example: n = 15):

    Sequence: 1 2 3 4 5 6 7 8 9 1 0 1 1 1 2
    Position: 1 2 3 4 5 6 7 8 9 . . . . . 15

    STEP 1 - Find the group:
    ├── digits=1, count=9: 15 > 9? YES → n = 15-9 = 6
    ├── digits=2, count=90: 6 > 180? NO → group 2
    └── n = 6, digits = 2, start = 10

    STEP 2 - Find the number:
    ├── number = 10 + (6-1) // 2 = 10 + 2 = 12
    └── We're looking at number 12

    STEP 3 - Find the digit:
    ├── digit_idx = (6-1) % 2 = 1
    ├── str(12)[1] = '2'
    └── Result: 2 ✓

WHY (n-1) AND NOT n:

    Without -1 (WRONG):
    ├── n=2, digits=2: number = 10 + 2//2 = 11
    └── But digit 2 of group is still in "10" ✗

    With -1 (CORRECT):
    ├── n=2, digits=2: number = 10 + 1//2 = 10
    └── digit_idx = 1%2 = 1 → "10"[1] = '0' ✓

    The -1 converts from 1-indexed to 0-indexed for division/modulo

DIGIT GROUP STRUCTURE:

    Group 1: numbers 1-9      → 9×1    = 9 digits      (cumulative: 9)
    Group 2: numbers 10-99    → 90×2   = 180 digits    (cumulative: 189)
    Group 3: numbers 100-999  → 900×3  = 2700 digits   (cumulative: 2889)
    Group 4: numbers 1000-9999→ 9000×4 = 36000 digits  (cumulative: 38889)

    General: Group k has 9 × 10^(k-1) numbers, each with k digits

EDGE CASES:

    n = 1: First digit → '1' ✓
    n = 9: Last 1-digit → '9' ✓
    n = 10: First digit of 10 → '1' ✓
    n = 11: Second digit of 10 → '0' ✓
    n = 189: Last digit of 99 → '9' ✓
    n = 190: First digit of 100 → '1' ✓
    Large n (2^31): Only ~10 digit groups → fast ✓

TIME COMPLEXITY: O(log n)
    The while loop runs at most O(log₁₀ n) times (~10 iterations max)
    Each iteration is O(1)

SPACE COMPLEXITY: O(1)
    Only a few variables: digits, count, start, number, digit_idx

CONCEPTS USED:
    Mathematical pattern recognition
    Digit grouping by number length
    Integer division and modulo for positioning
    1-indexed to 0-indexed conversion
    String indexing for digit extraction
"""
