# 171. Excel Sheet Column Number
# Difficulty: Easy
# https://leetcode.com/problems/excel-sheet-column-number/

"""
PROBLEM:
Given a string columnTitle that represents the column title as it appears
in an Excel sheet, return its corresponding column number.

EXAMPLES:
Input: columnTitle = "A"   → Output: 1
Input: columnTitle = "AB"  → Output: 28
Input: columnTitle = "ZY"  → Output: 701

MAPPING:
A → 1,  B → 2,  C → 3,  ... Z → 26
AA → 27, AB → 28, ... AZ → 52
BA → 53, ... ZZ → 702
AAA → 703 ...

CONSTRAINTS:
- 1 <= columnTitle.length <= 7
- columnTitle consists only of uppercase English letters
- columnTitle is in the range ["A", "FXSHRXW"]

KEY INSIGHT:
This is base-26 conversion where A=1, B=2, ..., Z=26 (not 0-25).
Process left to right: result = result * 26 + char_value

FORMULA:
"ABC" = A×26² + B×26¹ + C×26⁰
      = 1×676 + 2×26 + 3×1
      = 731

SOLUTION:
- Iterate through each character left to right
- Multiply accumulated result by 26 (shift left in base-26)
- Add current character's value (1-26)
"""

# STEP 1: Initialize result to 0
# STEP 2: For each character, multiply by 26 and add char value
# STEP 3: Character value = ord(char) - ord('A') + 1
# STEP 4: Return final accumulated result

class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        
        result = 0
        
        for char in columnTitle:                                                 # Process left to right
            
            value = ord(char) - ord('A') + 1                                     # A=1, B=2, ..., Z=26
            
            result = result * 26 + value                                         # Shift and add
        
        return result


"""
WHY EACH PART:
- result = 0: Starting accumulator for base conversion
- for char in columnTitle: Process each letter left to right
- ord(char) - ord('A'): Gives 0 for 'A', 1 for 'B', ..., 25 for 'Z'
- + 1: Adjusts to 1-indexed (A=1, not A=0)
- result * 26: Shifts previous digits left (like ×10 in decimal)
- + value: Adds current digit to the ones place
- return result: Final converted number

HOW IT WORKS (Example: columnTitle = "ZY"):

┌─ Iteration 1: char = 'Z' ─────────────────────────────────┐
│  value = ord('Z') - ord('A') + 1                          │
│        = 90 - 65 + 1                                      │
│        = 26                                               │
│                                                           │
│  result = 0 × 26 + 26                                     │
│         = 26                                              │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Iteration 2: char = 'Y' ─────────────────────────────────┐
│  value = ord('Y') - ord('A') + 1                          │
│        = 89 - 65 + 1                                      │
│        = 25                                               │
│                                                           │
│  result = 26 × 26 + 25                                    │
│         = 676 + 25                                        │
│         = 701                                             │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
        Return 701 ✓

HOW IT WORKS (Example: columnTitle = "ABC"):

char = 'A':  value = 1,   result = 0 × 26 + 1 = 1
char = 'B':  value = 2,   result = 1 × 26 + 2 = 28
char = 'C':  value = 3,   result = 28 × 26 + 3 = 731

Return 731 ✓

Verification: A×26² + B×26¹ + C×26⁰ = 1×676 + 2×26 + 3 = 731 ✓

WHY result * 26?
┌────────────────────────────────────────────────────────────┐
│  Similar to decimal conversion:                            │
│                                                            │
│  "123" → 0×10+1=1 → 1×10+2=12 → 12×10+3=123               │
│                                                            │
│  "AB"  → 0×26+1=1 → 1×26+2=28                             │
│                                                            │
│  Multiplying by base "shifts" existing digits left,        │
│  making room for the new digit in the ones place.          │
└────────────────────────────────────────────────────────────┘

WHY +1 IN VALUE CALCULATION?
┌────────────────────────────────────────────────────────────┐
│  ord('A') - ord('A') = 0     But Excel: A = 1              │
│  ord('B') - ord('A') = 1     But Excel: B = 2              │
│  ord('Z') - ord('A') = 25    But Excel: Z = 26             │
│                                                            │
│  Adding 1 converts from 0-indexed to 1-indexed             │
└────────────────────────────────────────────────────────────┘

COMPARISON WITH PROBLEM 168 (Inverse):
┌────────────────────────────────────────────────────────────┐
│  168: Number → Title        171: Title → Number            │
│  (Encode)                   (Decode)                       │
├────────────────────────────────────────────────────────────┤
│  n -= 1                     value = ord(c) - ord('A') + 1  │
│  remainder = n % 26         result = result * 26 + value   │
│  char = 'A' + remainder                                    │
│  n //= 26                                                  │
├────────────────────────────────────────────────────────────┤
│  Divide by 26               Multiply by 26                 │
│  Build right-to-left        Build left-to-right            │
│  Subtract to adjust         Add to adjust                  │
└────────────────────────────────────────────────────────────┘

ASCII TABLE REFERENCE:
┌────────────────────────────────────────────────────────────┐
│  Character    ord()    ord(c) - ord('A')    + 1 (Excel)   │
│  ─────────    ─────    ─────────────────    ───────────   │
│     'A'        65            0                   1         │
│     'B'        66            1                   2         │
│     'C'        67            2                   3         │
│     ...       ...          ...                 ...         │
│     'Y'        89           24                  25         │
│     'Z'        90           25                  26         │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION (using reduce):

from functools import reduce

class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        return reduce(
            lambda result, char: result * 26 + (ord(char) - ord('A') + 1),
            columnTitle,
            0
        )

ALTERNATIVE SOLUTION (using enumerate and powers):

class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        result = 0
        n = len(columnTitle)
        for i, char in enumerate(columnTitle):
            value = ord(char) - ord('A') + 1
            power = n - 1 - i                                                    # Position from right
            result += value * (26 ** power)
        return result

# "ZY": Z×26¹ + Y×26⁰ = 26×26 + 25×1 = 701

VERIFICATION TABLE:
┌──────────────┬──────────┬─────────────────────────────────┐
│    Title     │  Number  │          Calculation            │
├──────────────┼──────────┼─────────────────────────────────┤
│      A       │     1    │  0×26 + 1 = 1                   │
│      Z       │    26    │  0×26 + 26 = 26                 │
│      AA      │    27    │  0×26+1=1 → 1×26+1=27           │
│      AB      │    28    │  0×26+1=1 → 1×26+2=28           │
│      AZ      │    52    │  0×26+1=1 → 1×26+26=52          │
│      BA      │    53    │  0×26+2=2 → 2×26+1=53           │
│      ZY      │   701    │  0×26+26=26 → 26×26+25=701      │
│      ZZ      │   702    │  0×26+26=26 → 26×26+26=702      │
│      AAA     │   703    │  1 → 27 → 703                   │
└──────────────┴──────────┴─────────────────────────────────┘

EDGE CASES:
- Single letter "A": Returns 1 ✓
- Single letter "Z": Returns 26 ✓
- Two letters "AA": Returns 27 ✓
- Maximum "FXSHRXW": Returns 2147483647 (2^31-1) ✓

TIME COMPLEXITY: O(n)
- n = length of columnTitle
- Single pass through all characters
- Each operation is O(1)

SPACE COMPLEXITY: O(1)
- Only using a single integer variable
- No additional data structures

CONCEPTS USED:
- Base conversion (base-26 to base-10)
- ASCII character arithmetic
- 1-indexed number system (bijective base-26)
- Horner's method for polynomial evaluation
"""
