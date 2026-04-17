"""
592. Fraction Addition and Subtraction
Difficulty: Medium
https://leetcode.com/problems/fraction-addition-and-subtraction/

PROBLEM:
    Given a string expression representing an expression of fraction
    addition and subtraction, return the calculation result as an
    irreducible fraction (simplest form).

EXAMPLES:
    Input: "-1/2+1/2"       → Output: "0/1"
    Input: "-1/2+1/2+1/3"   → Output: "1/3"
    Input: "1/3-1/2"        → Output: "-1/6"

CONSTRAINTS:
    The input only contains '0'-'9', '/', '+', '-'
    Each fraction has format ±numerator/denominator
    Numerator: [0, 10], Denominator: [1, 10]
    At most 10 fractions
    Result fits in 32-bit int

KEY INSIGHT:
    Parse fractions using regex, then accumulate result using
    the cross-multiplication formula:
        a/b + c/d = (a*d + c*b) / (b*d)

    Simplify with GCD after each step to keep numbers small.

CHALLENGES:
    Parsing the expression string (handling signs correctly)
    Reducing fractions with GCD
    Handling zero numerator (result "0/1")
    Keeping the sign in the numerator (not denominator)

SOLUTION:
    Use regex to extract all fractions with their signs.
    Accumulate left to right using cross multiplication.
    Simplify with GCD after each addition.
"""


# STEP 1: Extract all fractions from string using regex
# STEP 2: Initialize accumulator as 0/1
# STEP 3: For each fraction, add to accumulator using cross multiplication
# STEP 4: Simplify with GCD after each addition
# STEP 5: Return result as "numerator/denominator"


import re
from math import gcd

class Solution:
    def fractionAddition(self, expression: str) -> str:

        fractions = re.findall(r'[+-]?\d+/\d+', expression)          # Extract all fractions with signs

        num = 0                                                       # Accumulated numerator (starts at 0)
        den = 1                                                       # Accumulated denominator (starts at 1)

        for frac in fractions:                                        # Process each fraction
            parts = frac.split('/')                                   # Split "num/den"
            n = int(parts[0])                                         # Numerator (includes sign)
            d = int(parts[1])                                         # Denominator (always positive)

            num = num * d + n * den                                   # Cross multiply: a/b + c/d = (ad+cb)/(bd)
            den = den * d                                             # New denominator

            g = gcd(abs(num), abs(den))                               # GCD for simplification
            num //= g                                                 # Reduce numerator
            den //= g                                                 # Reduce denominator

        return f"{num}/{den}"                                         # Format result


"""
WHY EACH PART:
    re.findall(r'[+-]?\d+/\d+'): Matches fractions like "1/3", "-1/2", "+1/6"
    num=0, den=1:                Starting value 0/1 (additive identity)
    frac.split('/'):             Separates numerator from denominator
    int(parts[0]):               Parses numerator including sign ("+1" or "-1")
    int(parts[1]):               Parses denominator (always positive)
    num*d + n*den:               Cross multiplication formula for addition
    den*d:                       Common denominator through multiplication
    gcd(abs(num), abs(den)):     GCD works on absolute values
    num //= g, den //= g:       Simplify fraction to irreducible form
    f"{num}/{den}":              Format as required string


HOW THE REGEX WORKS:
    Pattern: [+-]?\d+/\d+

    [+-]?  → optional sign character (+ or -)
    \d+    → one or more digits (numerator)
    /      → literal slash
    \d+    → one or more digits (denominator)

    Examples:
    ├── "-1/2+1/2+1/3"  → ["-1/2", "+1/2", "+1/3"]
    ├── "1/3-1/2"       → ["1/3", "-1/2"]
    ├── "-1/2"          → ["-1/2"]
    └── "5/3+1/3"       → ["5/3", "+1/3"]

    The first fraction might not have a sign → [+-]? handles that!


HOW IT WORKS (Example: "1/3-1/2"):

    fractions = ["1/3", "-1/2"]
    num = 0, den = 1

    Process "1/3" (n=1, d=3):
    ├── num = 0*3 + 1*1 = 1
    ├── den = 1*3 = 3
    ├── gcd(1, 3) = 1
    └── result so far: 1/3

    Process "-1/2" (n=-1, d=2):
    ├── num = 1*2 + (-1)*3 = 2-3 = -1
    ├── den = 3*2 = 6
    ├── gcd(1, 6) = 1
    └── result so far: -1/6

    return "-1/6" 


HOW IT WORKS (Example: "-1/2+1/2+1/3"):

    fractions = ["-1/2", "+1/2", "+1/3"]
    num = 0, den = 1

    Process "-1/2" (n=-1, d=2):
    ├── num = 0*2 + (-1)*1 = -1
    ├── den = 1*2 = 2
    ├── gcd(1, 2) = 1
    └── result: -1/2

    Process "+1/2" (n=1, d=2):
    ├── num = -1*2 + 1*2 = -2+2 = 0
    ├── den = 2*2 = 4
    ├── gcd(0, 4) = 4
    ├── num = 0/4 = 0, den = 4/4 = 1
    └── result: 0/1

    Process "+1/3" (n=1, d=3):
    ├── num = 0*3 + 1*1 = 1
    ├── den = 1*3 = 3
    ├── gcd(1, 3) = 1
    └── result: 1/3

    return "1/3" 


WHY CROSS MULTIPLICATION WORKS:
    To add a/b + c/d:

    We need a common denominator:
        a/b = (a×d) / (b×d)
        c/d = (c×b) / (b×d)    ← same denominator now!

    Add numerators:
        (a×d + c×b) / (b×d)

    This ALWAYS works, regardless of whether b and d
    share common factors. We clean up with GCD afterward.

    ┌─────────────────────────────────┐
    │  a     c     a×d + c×b         │
    │ ─── + ─── = ───────────        │
    │  b     d       b × d           │
    │                                 │
    │  Then simplify with GCD         │
    └─────────────────────────────────┘


WHY GCD AFTER EACH STEP:
    Without simplification, numbers grow fast:

    1/2 + 1/3 = 5/6          (OK so far)
    5/6 + 1/4 = 26/24        (getting bigger)
    26/24 + 1/5 = 178/120    (growing fast!)
    
    With simplification:
    1/2 + 1/3 = 5/6
    5/6 + 1/4 = 26/24 → 13/12
    13/12 + 1/5 = 77/60      (manageable)

    Simplifying keeps numbers small → prevents overflow ✓


WHY gcd(0, x) = x WORKS PERFECTLY:
    When numerator becomes 0:
        gcd(0, 36) = 36
        0/36 → 0/36 ÷ 36 = 0/1 

    This is mathematically correct:
        gcd(0, x) = x because x divides 0 and x divides x.


WHY SIGN STAYS IN NUMERATOR:
    Python's integer division preserves sign in numerator:
        -6 // 3 = -2   (sign in numerator ✓)
        
    Denominator stays positive because:
        - Input denominators are positive (constraint)
        - Multiplying positive × positive = positive
        - GCD is always positive
        - Dividing positive by positive = positive

    So the sign naturally remains in the numerator 


HANDLING SPECIAL CASES:
    Result is 0:          "0/1" (GCD handles naturally) ✓
    Result is negative:   "-1/6" (sign in numerator) ✓
    Result is whole:      "3/1" (denominator becomes 1) ✓
    Single fraction:      Just returns it simplified ✓
    All cancel out:       Returns "0/1" ✓


KEY TECHNIQUE:
    Regex parsing:         Clean extraction of signed fractions
    Cross multiplication:  Universal fraction addition formula
    GCD reduction:         Keeps fractions in simplest form
    Accumulator pattern:   Process one fraction at a time
    Sign handling:         Naturally through integer parsing


EDGE CASES:
    "-1/2+1/2":           "0/1" ✓
    "1/3-1/2":            "-1/6" ✓
    "-1/2+1/2+1/3":       "1/3" ✓
    "0/1":                "0/1" ✓
    "1/1":                "1/1" ✓
    "-1/1":               "-1/1" ✓
    "1/2+1/2":            "1/1" ✓
    "10/1-10/1":          "0/1" ✓
    Many fractions (10):  Accumulates correctly ✓


TIME COMPLEXITY: O(n)
    Regex parsing: O(n) where n = length of expression
    Processing each fraction: O(1) arithmetic + O(log(max)) for GCD
    At most 10 fractions → effectively O(n)

SPACE COMPLEXITY: O(n)
    List of extracted fraction strings
    A few integer variables for accumulation


CONCEPTS USED:
    Regular expressions (pattern matching)
    Fraction arithmetic (cross multiplication)
    GCD for fraction reduction (Euclidean algorithm)
    Accumulator pattern (running total)
    String parsing and formatting
"""
