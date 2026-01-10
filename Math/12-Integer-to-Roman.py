# 12. Integer to Roman
# Difficulty: Medium
# https://leetcode.com/problems/integer-to-roman/

"""
PROBLEM:
Given an integer, convert it to a Roman numeral.

ROMAN NUMERAL RULES:
- Basic symbols: I(1), V(5), X(10), L(50), C(100), D(500), M(1000)
- Subtraction cases: IV(4), IX(9), XL(40), XC(90), CD(400), CM(900)
- Symbols are placed from largest to smallest, left to right
- Maximum 3 consecutive repetitions of same symbol

EXAMPLES:
Input: num = 3749  → Output: "MMMDCCXLIX"
       3000 + 500 + 200 + 40 + 9 = MMM + D + CC + XL + IX

Input: num = 58    → Output: "LVIII"
       50 + 5 + 3 = L + V + III

Input: num = 1994  → Output: "MCMXCIV"
       1000 + 900 + 90 + 4 = M + CM + XC + IV

CONSTRAINTS:
- 1 <= num <= 3999
"""

# STEP 1: Create value-symbol mapping (largest to smallest)
# STEP 2: Include special subtraction cases (4, 9, 40, 90, 400, 900)
# STEP 3: For each value, while it fits in num, append symbol and subtract
# STEP 4: Return accumulated result string

class Solution:
    def intToRoman(self, num: int) -> str:
        
        valores = [                                                              # Value-symbol pairs
            (1000, "M"),                                                          # Thousands
            (900, "CM"),                                                          # 900 (special case)
            (500, "D"),                                                           # Five hundreds
            (400, "CD"),                                                          # 400 (special case)
            (100, "C"),                                                           # Hundreds
            (90, "XC"),                                                           # 90 (special case)
            (50, "L"),                                                            # Fifty
            (40, "XL"),                                                           # 40 (special case)
            (10, "X"),                                                            # Tens
            (9, "IX"),                                                            # 9 (special case)
            (5, "V"),                                                             # Five
            (4, "IV"),                                                            # 4 (special case)
            (1, "I")                                                              # Ones
        ]
        
        resultado = ""                                                           # Build result string
        
        for valor, simbolo in valores:                                           # Iterate largest to smallest
            while num >= valor:                                                  # While value fits
                resultado += simbolo                                             # Append symbol
                num -= valor                                                     # Subtract value
        
        return resultado                                                         # Return Roman numeral

"""
WHY EACH PART:
- valores list: Contains ALL possible values including subtraction cases
- Ordered largest to smallest: Greedy approach - always take biggest value first
- Tuples (valor, simbolo): Keeps number-symbol pairs together
- while num >= valor: May need same symbol multiple times (e.g., MMM for 3000)
- resultado += simbolo: String concatenation builds Roman numeral left to right
- num -= valor: Reduce remaining value after using a symbol

HOW IT WORKS (Example: num = 1994):
Initial: num = 1994, resultado = ""

valor=1000, simbolo="M":
├── 1994 >= 1000? Yes → resultado="M", num=994
└── 994 >= 1000? No → next value

valor=900, simbolo="CM":
├── 994 >= 900? Yes → resultado="MCM", num=94
└── 94 >= 900? No → next value

valor=500,400,100,90: all skip (94 < all of them... wait)

valor=90, simbolo="XC":
├── 94 >= 90? Yes → resultado="MCMXC", num=4
└── 4 >= 90? No → next value

valor=50,40,10,9,5: all skip (4 < all of them)

valor=4, simbolo="IV":
├── 4 >= 4? Yes → resultado="MCMXCIV", num=0
└── 0 >= 4? No → next value

valor=1: 0 >= 1? No → next value (done)

Return: "MCMXCIV" ✓

KEY TECHNIQUE:
- Greedy algorithm: Always take the largest value that fits
- Include subtraction cases: Treat 4,9,40,90,400,900 as atomic units
- Ordered list: Ensures we try larger values before smaller ones
- While loop: Handles repeated symbols (MMM, CCC, XXX, III)

ALTERNATIVE APPROACH (Separate lists):
class Solution:
    def intToRoman(self, num: int) -> str:
        valores = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        simbolos = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        
        resultado = ""
        for i in range(len(valores)):
            while num >= valores[i]:
                resultado += simbolos[i]
                num -= valores[i]
        return resultado

# Same logic, different data structure

EDGE CASES:
- Minimum (num=1): Returns "I" ✓
- Maximum (num=3999): Returns "MMMCMXCIX" ✓
- All subtraction cases (num=1994): Returns "MCMXCIV" ✓
- Round thousands (num=3000): Returns "MMM" ✓
- Single digit (num=8): Returns "VIII" ✓
- Contains 4 (num=4): Returns "IV" ✓
- Contains 9 (num=9): Returns "IX" ✓
- Contains 40 (num=40): Returns "XL" ✓
- Contains 90 (num=90): Returns "XC" ✓
- Contains 400 (num=400): Returns "CD" ✓
- Contains 900 (num=900): Returns "CM" ✓

TIME COMPLEXITY: O(1) - Maximum ~15 total iterations (bounded by num <= 3999)
SPACE COMPLEXITY: O(1) - Fixed size lookup table, output at most 15 characters

CONCEPTS USED:
- Greedy algorithm
- Value-symbol mapping with tuples
- Ordered iteration (largest to smallest)
- While loop for repeated values
- String concatenation
- Mathematical subtraction cases in Roman numerals
"""
