# 168. Excel Sheet Column Title
# Difficulty: Easy
# https://leetcode.com/problems/excel-sheet-column-title/

"""
PROBLEM:
Given an integer columnNumber, return its corresponding column title
as it appears in an Excel sheet.

EXAMPLES:
Input: columnNumber = 1   → Output: "A"
Input: columnNumber = 28  → Output: "AB"
Input: columnNumber = 701 → Output: "ZY"

MAPPING:
A → 1,  B → 2,  C → 3,  ... Z → 26
AA → 27, AB → 28, ... AZ → 52
BA → 53, ... ZZ → 702
AAA → 703 ...

CONSTRAINTS:
- 1 <= columnNumber <= 2^31 - 1

KEY INSIGHT:
This is NOT standard base-26! It's "bijective base-26" (1-indexed).
Standard: digits 0-25, Excel: digits 1-26 (no zero!)

TRICK: Subtract 1 before each modulo/division operation.
This converts from 1-indexed (A=1) to 0-indexed (A=0).

CHALLENGES:
1. No "zero" digit - Z is 26, not 0
2. 26 → "Z" (not "A0"), 27 → "AA" (not "A1")

SOLUTION:
- Subtract 1 to convert to 0-indexed
- Get remainder (0-25) → map to 'A'-'Z'
- Divide to get remaining number
- Reverse the result (built backwards)
"""

# STEP 1: Initialize result list
# STEP 2: While number > 0: subtract 1, get digit, divide
# STEP 3: Convert digit index to character
# STEP 4: Reverse and join result

class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        
        result = []
        
        while columnNumber > 0:
            
            columnNumber -= 1                                                    # Convert to 0-indexed
            
            remainder = columnNumber % 26                                        # Get current digit (0-25)
            
            char = chr(ord('A') + remainder)                                     # Convert to letter (A-Z)
            
            result.append(char)                                                  # Add to result
            
            columnNumber //= 26                                                  # Move to next digit
        
        return ''.join(reversed(result))                                         # Reverse (built right-to-left)


"""
WHY EACH PART:
- result = []: List to build characters (more efficient than string concat)
- columnNumber > 0: Continue until fully converted
- columnNumber -= 1: CRITICAL! Converts 1-26 system to 0-25 system
- columnNumber % 26: Gets rightmost digit (0-25)
- chr(ord('A') + remainder): Maps 0→'A', 1→'B', ..., 25→'Z'
- result.append(char): Build result right-to-left
- columnNumber //= 26: Remove rightmost digit, process next
- reversed(result): We built backwards, need to reverse

HOW IT WORKS (Example: columnNumber = 701):

┌─ Iteration 1 ─────────────────────────────────────────────┐
│  columnNumber = 701                                       │
│  columnNumber -= 1  →  700                                │
│  remainder = 700 % 26 = 24                                │
│  char = chr(65 + 24) = chr(89) = 'Y'                      │
│  result = ['Y']                                           │
│  columnNumber = 700 // 26 = 26                            │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Iteration 2 ─────────────────────────────────────────────┐
│  columnNumber = 26                                        │
│  columnNumber -= 1  →  25                                 │
│  remainder = 25 % 26 = 25                                 │
│  char = chr(65 + 25) = chr(90) = 'Z'                      │
│  result = ['Y', 'Z']                                      │
│  columnNumber = 25 // 26 = 0                              │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Loop Ends ───────────────────────────────────────────────┐
│  columnNumber = 0  →  exit while loop                     │
│  reversed(['Y', 'Z']) = ['Z', 'Y']                        │
│  ''.join(['Z', 'Y']) = "ZY" ✓                             │
└───────────────────────────────────────────────────────────┘

WHY SUBTRACT 1?
┌────────────────────────────────────────────────────────────┐
│  Without -1:                  With -1:                     │
│                                                            │
│  n=26: 26 % 26 = 0 → 'A' ✗    n=26: 25 % 26 = 25 → 'Z' ✓  │
│  n=52: 52 % 26 = 0 → 'A' ✗    n=52: 51 % 26 = 25 → 'Z' ✓  │
│                                                            │
│  The -1 shifts: 1-26 → 0-25                                │
│  So 'Z' (26) maps to index 25, not 0                       │
└────────────────────────────────────────────────────────────┘

BIJECTIVE BASE-26 vs STANDARD BASE-26:
┌────────────────────────────────────────────────────────────┐
│  Standard Base-26:        Bijective Base-26 (Excel):       │
│                                                            │
│  Digits: 0,1,2,...,25     Digits: A,B,C,...,Z (1-26)       │
│  Has zero: 0,10,20...     No zero: A, AA, AAA...           │
│                                                            │
│  26 = 1×26 + 0 = "10"     26 = "Z"                         │
│  27 = 1×26 + 1 = "11"     27 = "AA"                        │
│  52 = 2×26 + 0 = "20"     52 = "AZ"                        │
│  53 = 2×26 + 1 = "21"     53 = "BA"                        │
└────────────────────────────────────────────────────────────┘

ASCII CONVERSION:
┌────────────────────────────────────────────────────────────┐
│  ord('A') = 65                                             │
│  chr(65) = 'A'                                             │
│                                                            │
│  chr(ord('A') + 0)  = chr(65) = 'A'                        │
│  chr(ord('A') + 1)  = chr(66) = 'B'                        │
│  chr(ord('A') + 25) = chr(90) = 'Z'                        │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- columnNumber = 1: Returns "A" ✓
- columnNumber = 26: Returns "Z" (not "A0") ✓
- columnNumber = 27: Returns "AA" ✓
- columnNumber = 52: Returns "AZ" ✓
- columnNumber = 702: Returns "ZZ" ✓
- columnNumber = 703: Returns "AAA" ✓

VERIFICATION TABLE:
┌──────────────┬──────────┬─────────────────────────────────┐
│    Number    │  Title   │          Calculation            │
├──────────────┼──────────┼─────────────────────────────────┤
│      1       │    A     │  (1-1)%26=0 → A                 │
│      26      │    Z     │  (26-1)%26=25 → Z               │
│      27      │    AA    │  26%26=0→A, 0→A                 │
│      28      │    AB    │  27%26=1→B, 1-1=0→A             │
│      701     │    ZY    │  700%26=24→Y, 26-1=25→Z         │
│      702     │    ZZ    │  701%26=25→Z, 26-1=25→Z         │
└──────────────┴──────────┴─────────────────────────────────┘

TIME COMPLEXITY: O(log₂₆(n))
- Each iteration divides by 26
- Number of digits in base-26 representation

SPACE COMPLEXITY: O(log₂₆(n))
- Result list stores each character
- Maximum ~7 characters for 2^31

CONCEPTS USED:
- Bijective numeration (base without zero)
- Modular arithmetic
- ASCII character conversion
- Number base conversion with offset
"""
