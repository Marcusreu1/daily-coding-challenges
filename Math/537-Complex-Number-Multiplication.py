"""
537. Complex Number Multiplication
Difficulty: Medium
https://leetcode.com/problems/complex-number-multiplication/

PROBLEM:
    Given two complex numbers num1 and num2 as strings in "a+bi" format,
    return their multiplication result as a string in the same format.

    Note: i² = -1 by definition.

EXAMPLES:
    Input: num1 = "1+1i", num2 = "1+1i"  → Output: "0+2i"
    Input: num1 = "1+-1i", num2 = "1+-1i" → Output: "0+-2i"

CONSTRAINTS:
    num1, num2 are valid complex numbers in "a+bi" format
    a and b are integers in range [-100, 100]

KEY INSIGHT:
    (a + bi)(c + di) = (ac - bd) + (ad + bc)i

    This is just the FOIL expansion with the rule i² = -1.
    Parse the strings to extract a, b, c, d → apply formula → format result.

CHALLENGES:
    Parsing the string correctly (handling negative numbers like "1+-3i")
    Remembering that i² = -1 (gives the "-bd" in the real part)
    Output format must match exactly: "real+imagi"

SOLUTION:
    Parse both strings to extract (a, b) and (c, d).
    Apply the complex multiplication formula.
    Format and return the result string.
"""


# STEP 1: Parse num1 to extract a (real) and b (imaginary)
# STEP 2: Parse num2 to extract c (real) and d (imaginary)
# STEP 3: Apply formula: real = ac - bd, imag = ad + bc
# STEP 4: Format result as "real+imagi"


class Solution:
    def complexNumberMultiply(self, num1: str, num2: str) -> str:

        a, b = map(int, num1[:-1].split("+"))                        # Parse "a+bi" → remove "i", split by "+"
        c, d = map(int, num2[:-1].split("+"))                        # Same parsing for second number

        real = a * c - b * d                                          # Real part: ac - bd
        imag = a * d + b * c                                          # Imaginary part: ad + bc

        return f"{real}+{imag}i"                                      # Format: "real+imagi"


"""
WHY EACH PART:
    num1[:-1]:           Removes the trailing "i" → "1+1i" becomes "1+1"
    .split("+"):         Splits "1+1" into ["1", "1"] or "-1+-3" into ["-1", "-3"]
    map(int, ...):       Converts string parts to integers
    a*c - b*d:           Real part of complex multiplication (FOIL + i²=-1)
    a*d + b*c:           Imaginary part of complex multiplication
    f"{real}+{imag}i":   Reconstructs the output in required format


HOW IT WORKS (Example: num1 = "1+1i", num2 = "1+1i"):

    Parsing num1:
    ├── "1+1i"[:-1] = "1+1"
    ├── "1+1".split("+") = ["1", "1"]
    └── a = 1, b = 1

    Parsing num2:
    ├── "1+1i"[:-1] = "1+1"
    ├── "1+1".split("+") = ["1", "1"]
    └── c = 1, d = 1

    Formula:
    ├── real = 1×1 - 1×1 = 0
    ├── imag = 1×1 + 1×1 = 2
    └── return "0+2i" 


HOW IT WORKS (Example: num1 = "1+-1i", num2 = "1+-1i"):

    Parsing num1:
    ├── "1+-1i"[:-1] = "1+-1"
    ├── "1+-1".split("+") = ["1", "-1"]
    └── a = 1, b = -1

    Parsing num2:
    ├── "1+-1i"[:-1] = "1+-1"
    ├── "1+-1".split("+") = ["1", "-1"]
    └── c = 1, d = -1

    Formula:
    ├── real = 1×1 - (-1)×(-1) = 1 - 1 = 0
    ├── imag = 1×(-1) + (-1)×1 = -1 - 1 = -2
    └── return "0+-2i" 


WHY THE FOIL FORMULA WORKS:
    (a + bi)(c + di)
    
    F irst: a × c   = ac
    O uter: a × di  = adi
    I nner: bi × c  = bci
    L ast:  bi × di = bdi²

    Sum: ac + adi + bci + bdi²
                          ↓
         ac + adi + bci + bd(-1)     ← because i² = -1

         = (ac - bd) + (ad + bc)i
           ↑─ real ─↑   ↑─ imag ─↑


WHY PARSING WITH [:-1] AND split("+") WORKS:
    The format is always "a+bi":

    "3+4i"   → [:-1] → "3+4"   → split("+") → ["3", "4"]     ✓
    "-3+4i"  → [:-1] → "-3+4"  → split("+") → ["-3", "4"]    ✓
    "3+-4i"  → [:-1] → "3+-4"  → split("+") → ["3", "-4"]    ✓
    "-3+-4i" → [:-1] → "-3+-4" → split("+") → ["-3", "-4"]   ✓
    "0+0i"   → [:-1] → "0+0"   → split("+") → ["0", "0"]     ✓

    The negative sign stays ATTACHED to the number.
    split("+") never breaks a negative number because the format
    guarantees the "+" is the separator between real and imaginary.


WHY OUTPUT FORMAT INCLUDES "+" EVEN WITH NEGATIVES:
    The problem expects the exact format "real+imagi":

    Result (0, -2) → "0+-2i"   NOT "0-2i"
    
    This looks unusual but matches the problem's specification.
    The "+" is always present as a separator, and the negative
    sign is part of the imaginary number itself.


HANDLING SPECIAL CASES:
    Both zero: "0+0i" × "0+0i" = "0+0i"              ✓
    Pure real: "3+0i" × "2+0i" = "6+0i"              ✓
    Pure imag: "0+2i" × "0+3i" = "-6+0i" (2i×3i=6i²=-6) ✓
    Negatives: "-1+-1i" × "-1+-1i" = "0+2i"          ✓
    One × zero: "5+3i" × "0+0i" = "0+0i"             ✓


KEY TECHNIQUE:
    String parsing:      [:-1] removes trailing character, split separates parts
    FOIL expansion:      Standard algebraic multiplication
    i² = -1 rule:        Converts i² terms into real number contributions
    Format string:       f-string for clean output construction


EDGE CASES:
    "0+0i" × "0+0i":    "0+0i" ✓
    "1+0i" × "1+0i":    "1+0i" (purely real) ✓
    "0+1i" × "0+1i":    "-1+0i" (i² = -1) ✓
    "-100+-100i" × "-100+-100i": Handles max values ✓
    "1+0i" × "0+1i":    "0+1i" (identity × i) ✓


TIME COMPLEXITY: O(n)
    Parsing strings: O(n) where n = string length
    Multiplication: O(1) — just 4 multiplications and 2 additions
    Overall dominated by string operations

SPACE COMPLEXITY: O(1)
    Only a few integer variables (a, b, c, d, real, imag)
    Output string is O(n) but that's required by the problem


CONCEPTS USED:
    Complex number arithmetic
    FOIL method (distributive property)
    String parsing (slicing + splitting)
    Mathematical identity (i² = -1)
    String formatting (f-strings)
"""
