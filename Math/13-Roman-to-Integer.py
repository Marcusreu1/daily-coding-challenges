# 13. Roman to Integer
# Difficulty: Easy
# https://leetcode.com/problems/roman-to-integer/

"""
PROBLEM:
Given a Roman numeral string, convert it to an integer.

ROMAN NUMERAL VALUES:
Symbol  Value
I       1
V       5
X       10
L       50
C       100
D       500
M       1000

SUBTRACTION CASES:
- I before V or X → subtract I (IV=4, IX=9)
- X before L or C → subtract X (XL=40, XC=90)
- C before D or M → subtract C (CD=400, CM=900)

EXAMPLES:
Input: s = "III"      → Output: 3     (1+1+1)
Input: s = "LVIII"    → Output: 58    (50+5+1+1+1)
Input: s = "MCMXCIV"  → Output: 1994  (1000+900+90+4)

CONSTRAINTS:
- 1 <= s.length <= 15
- s contains only: I, V, X, L, C, D, M
- Input is valid Roman numeral in range [1, 3999]

KEY INSIGHT:
If current symbol value < next symbol value → SUBTRACT
Otherwise → ADD
"""

# STEP 1: Create symbol-to-value dictionary
# STEP 2: Initialize result to 0
# STEP 3: Iterate through each character
# STEP 4: If current value < next value → subtract (subtraction case)
# STEP 5: Otherwise → add
# STEP 6: Return result

class Solution:
    def romanToInt(self, s: str) -> int:
        
        valores = {                                                              # Symbol to value mapping
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        
        resultado = 0                                                            # Accumulated result
        
        for i in range(len(s)):                                                  # Iterate through string
            valor_actual = valores[s[i]]                                         # Get current symbol value
            
            if i + 1 < len(s) and valor_actual < valores[s[i + 1]]:              # If next exists and is larger
                resultado -= valor_actual                                        # Subtract (subtraction case)
            else:
                resultado += valor_actual                                        # Add (normal case)
        
        return resultado                                                         # Return final integer

"""
WHY EACH PART:
- valores dict: O(1) lookup for symbol values
- for i in range(len(s)): Need index to check next character
- valores[s[i]]: Get numeric value of current Roman symbol
- i + 1 < len(s): Bounds check - ensure next character exists
- valor_actual < valores[s[i + 1]]: Detect subtraction case (I before V, etc.)
- resultado -= valor_actual: Subtract for cases like IV, IX, XL, XC, CD, CM
- resultado += valor_actual: Add for normal cases or last character

HOW IT WORKS (Example: s = "MCMXCIV"):

Position: 0   1   2   3   4   5   6
Symbol:   M   C   M   X   C   I   V
Value:   1000 100 1000 10  100  1   5

i=0: M(1000) vs C(100)  → 1000 >= 100 → ADD +1000  → result = 1000
i=1: C(100) vs M(1000)  → 100 < 1000  → SUB -100   → result = 900
i=2: M(1000) vs X(10)   → 1000 >= 10  → ADD +1000  → result = 1900
i=3: X(10) vs C(100)    → 10 < 100    → SUB -10    → result = 1890
i=4: C(100) vs I(1)     → 100 >= 1    → ADD +100   → result = 1990
i=5: I(1) vs V(5)       → 1 < 5       → SUB -1     → result = 1989
i=6: V(5) - last        → no next     → ADD +5     → result = 1994

Return: 1994 ✓

Breakdown:
M    = +1000
CM   = -100 + 1000 = 900
XC   = -10 + 100 = 90
IV   = -1 + 5 = 4
Total = 1000 + 900 + 90 + 4 = 1994

KEY TECHNIQUE:
- Compare current with next: Determines add or subtract
- Single pass: Process each character exactly once
- Dictionary lookup: O(1) value retrieval
- Subtraction pattern: Smaller before larger means subtract

EDGE CASES:
- Single character (s="V"): Returns 5 ✓
- All same (s="III"): Returns 3 (1+1+1) ✓
- Subtraction at start (s="IV"): Returns 4 ✓
- Subtraction at end (s="XIV"): Returns 14 ✓
- Multiple subtractions (s="MCMXCIV"): Returns 1994 ✓
- Maximum (s="MMMCMXCIX"): Returns 3999 ✓
- Minimum (s="I"): Returns 1 ✓
- No subtractions (s="MDCLXVI"): Returns 1666 ✓

TIME COMPLEXITY: O(n) - Single pass through string, n ≤ 15
SPACE COMPLEXITY: O(1) - Fixed size dictionary (7 entries), few variables

CONCEPTS USED:
- Dictionary for O(1) lookup
- String indexing and traversal
- Comparison with next element
- Conditional addition/subtraction
- Roman numeral subtraction rules
- Bounds checking (i + 1 < len(s))
"""
