"""
738. Monotone Increasing Digits
Difficulty: Medium
https://leetcode.com/problems/monotone-increasing-digits/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

An integer has monotone increasing digits if each pair of adjacent
digits satisfies: d[i] <= d[i+1] (non-decreasing from left to right).

Given a non-negative integer n, return the largest number that is
less than or equal to n AND has monotone increasing digits.

EXAMPLES:

    Input: n = 10    → Output: 9
    Input: n = 1234  → Output: 1234 (already monotone)
    Input: n = 332   → Output: 299

CONSTRAINTS:

    0 <= n <= 10^9

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

When a digit is GREATER than the next digit (violation), we:
    1. DECREASE that digit by 1
    2. Set ALL digits to the RIGHT to 9 (maximize the result)

We scan RIGHT TO LEFT so that decreasing a digit can cascade
properly if it creates a new violation with the digit before it.

Example: 332 → detect 3>2 → [3,2,9] → detect 3>2 → [2,9,9] → 299

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. CASCADE EFFECT: Fixing one violation can create another
2. DIRECTION: Must scan right-to-left to handle cascades
3. MAXIMIZING: After fixing, fill right side with 9s (not 0s)
4. TRACKING: Need to mark WHERE to start filling 9s

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Convert number to list of digit characters
STEP 2: Scan right to left — when digits[i-1] > digits[i]:
        → Decrease digits[i-1] by 1
        → Mark position i as the "fill 9s from here" point
STEP 3: Set all digits from mark position to end as '9'
STEP 4: Convert back to integer
"""


class Solution:
    def monotoneIncreasingDigits(self, n: int) -> int:

        digits = list(str(n))                                                     # Convert to list of char digits
        mark = len(digits)                                                        # Position from which to fill 9s

        # ── Scan right to left for violations ──
        for i in range(len(digits) - 1, 0, -1):                                  # From last digit back to second
            if digits[i - 1] > digits[i]:                                         # Violation: left digit > right digit
                digits[i - 1] = str(int(digits[i - 1]) - 1)                       # Decrease the left digit by 1
                mark = i                                                          # Mark: everything from i onward → 9

        # ── Fill 9s from mark to end ──
        for i in range(mark, len(digits)):                                        # From mark position to the end
            digits[i] = '9'                                                       # Set to '9' to maximize result

        return int(''.join(digits))                                               # Join and convert back to integer


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

digits = list(str(n)):
    Convert integer to list of characters so we can modify
    individual digits. "332" → ['3', '3', '2']

mark = len(digits):
    Initialize mark to beyond the last digit (meaning "no 9-fill needed").
    If no violation is found, mark stays here and nothing gets filled.

for i in range(len(digits) - 1, 0, -1):
    Traverse from the RIGHTMOST digit back to the SECOND digit.
    Right-to-left is crucial because fixing a violation at position i
    might cause a NEW violation at position i-1, which we'll catch
    in the next iteration.

digits[i - 1] > digits[i]:
    This detects a violation of the monotone increasing property.
    The left digit is strictly greater than the right digit.

digits[i - 1] = str(int(digits[i - 1]) - 1):
    Decrease the violating digit by 1. This is the minimum change
    needed to potentially fix the violation.
    Example: '3' → int('3') - 1 = 2 → str(2) = '2'

mark = i:
    Record that everything from position i onward should become 9.
    If multiple violations cascade, mark keeps moving LEFT to the
    earliest position, which is correct.

for i in range(mark, len(digits)): digits[i] = '9':
    Fill all positions from mark to end with '9'.
    This maximizes the result after reducing a digit.

int(''.join(digits)):
    Join the character list back into a string and convert to int.
    The int() also naturally handles leading zeros (e.g., "09" → 9).

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 332):
════════════════════════════════════════════════════════════════

    digits = ['3', '3', '2'], mark = 3

    i=2: digits[1]='3' > digits[2]='2' → VIOLATION
    ├── digits[1] = '3'-1 = '2' → ['3', '2', '2']
    └── mark = 2

    i=1: digits[0]='3' > digits[1]='2' → VIOLATION (cascade!)
    ├── digits[0] = '3'-1 = '2' → ['2', '2', '2']
    └── mark = 1

    Fill 9s from position 1:
    ['2', '9', '9'] → 299 ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 1332):
════════════════════════════════════════════════════════════════

    digits = ['1', '3', '3', '2'], mark = 4

    i=3: digits[2]='3' > digits[3]='2' → VIOLATION
    ├── digits[2] = '2' → ['1', '3', '2', '2']
    └── mark = 3

    i=2: digits[1]='3' > digits[2]='2' → VIOLATION (cascade!)
    ├── digits[1] = '2' → ['1', '2', '2', '2']
    └── mark = 2

    i=1: digits[0]='1' ≤ digits[1]='2' → OK ✓

    Fill 9s from position 2:
    ['1', '2', '9', '9'] → 1299 ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 10):
════════════════════════════════════════════════════════════════

    digits = ['1', '0'], mark = 2

    i=1: digits[0]='1' > digits[1]='0' → VIOLATION
    ├── digits[0] = '0' → ['0', '0']
    └── mark = 1

    Fill 9s from position 1:
    ['0', '9'] → int("09") = 9 ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 1234, already monotone):
════════════════════════════════════════════════════════════════

    digits = ['1', '2', '3', '4'], mark = 4

    i=3: '3' ≤ '4' ✓
    i=2: '2' ≤ '3' ✓
    i=1: '1' ≤ '2' ✓

    No violations → mark stays at 4 → no 9-fill
    Result: 1234 ✓

════════════════════════════════════════════════════════════════
WHY RIGHT-TO-LEFT (NOT LEFT-TO-RIGHT):
════════════════════════════════════════════════════════════════

    Example: n = 333222

    LEFT-TO-RIGHT (WRONG):
    ├── Compare 3,3 → OK
    ├── Compare 3,3 → OK
    ├── Compare 3,2 → Fix! → [3,3,2,222] → oops, 3>2 now!
    └── Would need MULTIPLE passes to fix cascades

    RIGHT-TO-LEFT (CORRECT):
    ├── i=5: '2' ≤ '2' → OK
    ├── i=4: '2' ≤ '2' → OK
    ├── i=3: '3' > '2' → Fix → [3,3,2,222], mark=3
    ├── i=2: '3' > '2' → Fix → [3,2,2,222], mark=2
    ├── i=1: '3' > '2' → Fix → [2,2,2,222], mark=1
    └── Fill 9s from mark=1 → [2,9,9,999] → 299999 ✓

    Single pass handles ALL cascades because each fix propagates
    leftward, and we're already moving left!

════════════════════════════════════════════════════════════════
WHY FILLING WITH 9 IS OPTIMAL:
════════════════════════════════════════════════════════════════

    When we decrease digit at position p:
    ├── We've made the number SMALLER than n (guaranteed ≤ n)
    ├── Everything LEFT of p is already monotone increasing
    ├── d[p] was decreased → d[p] ≤ 9 → transition to 9 is valid
    ├── 9 → 9 → 9 is monotone (9 ≤ 9) ✓
    └── 9 is the LARGEST digit → maximizes the result

    Example for n = 332:
    ├── After fixing: [2, _, _]
    ├── Fill with 9:  [2, 9, 9] = 299 ← MAXIMUM possible
    ├── Fill with 0:  [2, 0, 0] = 200 ← valid but NOT maximum
    └── 9s give us the biggest number that's still ≤ n ✓

════════════════════════════════════════════════════════════════
WHY mark TRACKS THE EARLIEST POSITION:
════════════════════════════════════════════════════════════════

    As we cascade left, mark keeps updating to earlier positions:

    n = 4321:
    ├── i=3: 2>1 → mark=3 → [4,3,1,_]
    ├── i=2: 3>1 → mark=2 → [4,2,_,_]
    ├── i=1: 4>2 → mark=1 → [3,_,_,_]
    └── Fill from mark=1: [3,9,9,9] → 3999

    Each cascade pushes mark further left. At the end, we fill
    9s from the EARLIEST affected position, which is correct
    because everything from there was disrupted by cascading fixes.

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    n = 0              → 0 (no digits to check) ✓
    n = 9              → 9 (single digit, always monotone) ✓
    n = 10             → 9 (1 > 0, reduce to 09 = 9) ✓
    n = 1234           → 1234 (already monotone) ✓
    n = 4321           → 3999 (full cascade) ✓
    n = 1111           → 1111 (all equal, monotone) ✓
    n = 1000000000     → 999999999 (10^9 → 9 nines) ✓
    n = 999999999      → 999999999 (all 9s, monotone) ✓
    n = 120            → 119 (1≤2 OK, 2>0 fix) ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(d)
════════════════════════════════════════════════════════════════

    d = number of digits in n (at most 10 for n ≤ 10^9)
    First pass (right to left): O(d)
    Second pass (fill 9s): O(d)
    Total: O(d) → effectively O(1) since d ≤ 10

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(d)
════════════════════════════════════════════════════════════════

    Character list of digits: O(d)
    Since d ≤ 10, this is effectively O(1).

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Greedy algorithm (maximize by filling 9s after reducing)
    Right-to-left traversal (handle cascading violations in one pass)
    Digit manipulation (string ↔ integer conversion)
    Monotone sequence property (non-decreasing order)
    Cascade detection (one fix can trigger another)
"""
