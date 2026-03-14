"""
415. Add Strings
Difficulty: Easy
https://leetcode.com/problems/add-strings/

PROBLEM:
Given two non-negative integers num1 and num2 represented as strings,
return the sum of num1 and num2 as a string.

You must NOT:
    - Use any built-in BigInteger library
    - Convert the inputs to integers directly

EXAMPLES:
Input: num1 = "11", num2 = "123"  → Output: "134"
Input: num1 = "456", num2 = "77"  → Output: "533"
Input: num1 = "0", num2 = "0"     → Output: "0"

CONSTRAINTS:
    1 <= num1.length, num2.length <= 10^4
    num1 and num2 consist of only digits
    num1 and num2 don't have leading zeros (except "0" itself)

KEY INSIGHT:
Simulate manual addition: process digits RIGHT to LEFT,
carry over when sum >= 10. Use ord(c) - ord('0') to convert
characters to digits without using int() on the whole string.

CHALLENGES:
    Strings can have different lengths
    Must handle carry propagation
    Final carry after all digits processed
    No direct int() conversion allowed

SOLUTION:
    1. Two pointers from the end of each string
    2. Add digits + carry at each position
    3. Extract digit (% 10) and new carry (// 10)
    4. Handle remaining carry at the end
    5. Reverse the built string
"""

# STEP 1: Initialize two pointers at the end of each string
# STEP 2: Process digits from right to left with carry
# STEP 3: Handle final carry
# STEP 4: Reverse and return result

class Solution:
    def addStrings(self, num1: str, num2: str) -> str:

        i = len(num1) - 1                                                # Pointer at end of num1
        j = len(num2) - 1                                                # Pointer at end of num2
        carry = 0                                                        # Carry starts at 0
        result = []                                                      # Collect digits (reversed)

        while i >= 0 or j >= 0 or carry:                                 # While there's work to do
            d1 = ord(num1[i]) - ord('0') if i >= 0 else 0               # Get digit from num1 (or 0)
            d2 = ord(num2[j]) - ord('0') if j >= 0 else 0               # Get digit from num2 (or 0)

            total = d1 + d2 + carry                                      # Sum both digits + carry
            result.append(str(total % 10))                               # Keep last digit of sum
            carry = total // 10                                          # Carry for next position

            i -= 1                                                       # Move left in num1
            j -= 1                                                       # Move left in num2

        return ''.join(reversed(result))                                 # Reverse and join into string

"""
WHY EACH PART:

    i = len(num1) - 1: Start at last digit (rightmost)
    j = len(num2) - 1: Same for num2
    carry = 0: No carry at the beginning
    result = []: List is faster than string concatenation for building
    while i >= 0 or j >= 0 or carry: Three conditions to keep going:
        ├── i >= 0: num1 still has digits
        ├── j >= 0: num2 still has digits
        └── carry: still have carry to process (handles "99" + "1" = "100")
    ord(char) - ord('0'): Convert char to digit without int()
    if i >= 0 else 0: If string exhausted, treat as 0
    total % 10: Extract the digit to write (13 → 3)
    total // 10: Extract the carry (13 → 1)
    reversed(result): We built right-to-left, need to flip

HOW IT WORKS (Example: num1 = "456", num2 = "77"):

    i=2, j=1, carry=0

    Iteration 1: i=2, j=1
    ├── d1 = ord('6')-ord('0') = 6
    ├── d2 = ord('7')-ord('0') = 7
    ├── total = 6 + 7 + 0 = 13
    ├── result = ['3'],  carry = 1
    └── i=1, j=0

    Iteration 2: i=1, j=0
    ├── d1 = ord('5')-ord('0') = 5
    ├── d2 = ord('7')-ord('0') = 7
    ├── total = 5 + 7 + 1 = 13
    ├── result = ['3','3'],  carry = 1
    └── i=0, j=-1

    Iteration 3: i=0, j=-1
    ├── d1 = ord('4')-ord('0') = 4
    ├── d2 = 0 (j < 0, num2 exhausted)
    ├── total = 4 + 0 + 1 = 5
    ├── result = ['3','3','5'],  carry = 0
    └── i=-1, j=-2

    Loop ends: i<0, j<0, carry=0
    reversed(['3','3','5']) → ['5','3','3']
    ''.join → "533" ✓

WHY "or carry" IN THE WHILE CONDITION:

    Example: "99" + "1"
    ├── i=-1, j=-1 → both strings exhausted
    ├── BUT carry = 1 still remains!
    ├── Without "or carry": returns "00" ✗
    └── With "or carry": processes carry → "100" ✓

    The carry condition handles cases where the result
    has MORE digits than either input.

WHY LIST + REVERSED INSTEAD OF STRING PREPEND:

    String prepend: result = char + result → O(n) each time → O(n²) total
    ├── Creates new string every time (strings are immutable)
    └── "3" → "33" → "533" (copies grow each time)

    List append + reverse: → O(1) each time → O(n) total
    ├── ['3'] → ['3','3'] → ['3','3','5'] (O(1) appends)
    └── reverse at end: O(n) once
    
    Much faster for large numbers!

WHY ord(c) - ord('0') WORKS:

    ASCII table has digits in consecutive positions:
    ├── ord('0') = 48
    ├── ord('1') = 49
    ├── ord('5') = 53
    └── ord('9') = 57

    ord('5') - ord('0') = 53 - 48 = 5 ✓
    ord('9') - ord('0') = 57 - 48 = 9 ✓

    This converts any digit CHARACTER to its numeric VALUE
    without using int() on the input strings.

COMPARISON WITH REAL-LIFE ADDITION:

    Paper:                     Code:
    Write rightmost digit    → total % 10
    "Carry the 1"            → total // 10
    Shorter number gets 0s   → else 0
    Final carry = new digit  → "or carry" in while

EDGE CASES:

    "0" + "0": 0+0=0, carry=0 → "0" ✓
    Same length "11" + "22": Straightforward → "33" ✓
    Different length "1" + "999": Handles naturally → "1000" ✓
    Carry propagation "999" + "1": Multiple carries → "1000" ✓
    Large numbers (10^4 digits): O(n) handles it ✓
    One number is "0": Acts as identity → returns other number ✓

TIME COMPLEXITY: O(max(n, m))
    Where n = len(num1), m = len(num2)
    We process each digit once, at most max(n,m) + 1 iterations

SPACE COMPLEXITY: O(max(n, m))
    Result list stores at most max(n,m) + 1 digits

CONCEPTS USED:
    Elementary addition algorithm (grade school math)
    Two-pointer technique (from end of strings)
    Carry propagation
    ASCII arithmetic (ord(c) - ord('0'))
    List building + reverse (vs string concatenation)
    Handling different-length inputs with default values
"""
