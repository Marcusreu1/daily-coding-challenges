"""
640. Solve the Equation
Difficulty: Medium
https://leetcode.com/problems/solve-the-equation/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

Given a string equation representing a linear equation with variable 'x',
solve it and return the result as a string:

    - Exactly one solution  → "x=value"
    - Infinite solutions    → "Infinite solutions"
    - No solution           → "No solution"

The equation contains only '+', '-', 'x', and digits.
'x' always has a coefficient (explicit or implicit: x = 1x, -x = -1x).

EXAMPLES:

    Input: "x+5-3+x=6+x-2"  → Output: "x=2"
    Input: "x=x"             → Output: "Infinite solutions"
    Input: "2x=x"            → Output: "x=0"
    Input: "x=x+2"           → Output: "No solution"

CONSTRAINTS:

    3 <= equation.length <= 1000
    equation has exactly one '='
    Only '+', '-', 'x', digits [0-9]
    No leading zeros
    Each term is either a constant integer or coefficient*x

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

Every linear equation reduces to the form: ax = b

    If a ≠ 0         → x = b / a          (unique solution)
    If a = 0, b = 0  → 0 = 0              (infinite solutions)
    If a = 0, b ≠ 0  → 0 = b              (no solution)

The main challenge is PARSING the string correctly to extract
coefficients and constants from each side.

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. PARSING: Extracting coefficients and constants from a raw string
2. SIGNS: Handling '+' and '-' correctly (including at the start)
3. IMPLICIT COEFFICIENTS: "x" = 1x, "-x" = -1x, "+x" = 1x
4. SPLITTING TERMS: "x+5-3+x" → ["x", "+5", "-3", "+x"]

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Split equation by '=' into left and right sides
STEP 2: Parse each side → extract (x_coefficient, constant)
STEP 3: Rearrange to form ax = b
STEP 4: Classify result (unique, infinite, or no solution)

PARSING STRATEGY:
    Use regex to extract each "term" with its sign:
    "x+5-3+x" → ["x", "+5", "-3", "+x"]

    Each term:
    - Contains 'x' → it's a coefficient (extract number before x)
    - No 'x'       → it's a constant (convert to int)
"""

import re


class Solution:
    def solveEquation(self, equation: str) -> str:

        def parse(side: str) -> tuple:
            """
            Parses one side of the equation and returns (x_coeff, constant).
            Example: "x+5-3+x" → coeff=2, const=2
            """
            coeff = 0                                                             # Accumulated coefficient of x
            const = 0                                                             # Accumulated constant
            tokens = re.findall(r'[+-]?[^+-]+', side)                             # Split into signed terms

            for token in tokens:                                                  # Process each term
                if 'x' in token:                                                  # Term with x
                    token = token.replace('x', '')                                # Remove 'x' to get coefficient
                    if token == '' or token == '+':                                # "x" or "+x" → coefficient is 1
                        coeff += 1
                    elif token == '-':                                            # "-x" → coefficient is -1
                        coeff -= 1
                    else:                                                         # "3x", "-2x", "+5x" → convert to int
                        coeff += int(token)
                else:                                                             # Constant term
                    const += int(token)                                           # Add as integer

            return coeff, const

        # ── STEP 1: Split by '=' ──
        left_side, right_side = equation.split('=')

        # ── STEP 2: Parse each side ──
        left_coeff, left_const = parse(left_side)                                # Coeff and constant from left
        right_coeff, right_const = parse(right_side)                             # Coeff and constant from right

        # ── STEP 3: Rearrange to ax = b ──
        # left_coeff * x + left_const = right_coeff * x + right_const
        # (left_coeff - right_coeff) * x = right_const - left_const
        a = left_coeff - right_coeff                                             # Net coefficient of x
        b = right_const - left_const                                             # Net constant

        # ── STEP 4: Classify and solve ──
        if a == 0:                                                                # x disappears from equation
            if b == 0:                                                            # 0 = 0 → always true
                return "Infinite solutions"
            else:                                                                 # 0 = b → impossible
                return "No solution"
        else:                                                                     # ax = b → x = b/a
            return f"x={b // a}"


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

re.findall(r'[+-]?[^+-]+', side):
    Regex that captures each "term" with its sign.
    [+-]?     → optional sign at the beginning
    [^+-]+    → one or more characters that are NOT + or -
    Result: "x+5-3+x" → ["x", "+5", "-3", "+x"]

token.replace('x', ''):
    Removes 'x' so we're left with just the numeric coefficient.
    "3x" → "3", "-2x" → "-2", "x" → "", "-x" → "-"

Implicit coefficient cases:
    "" or "+"  → coefficient is 1 (bare x = 1x)
    "-"        → coefficient is -1 (-x = -1x)
    other      → convert to int normally

a = left_coeff - right_coeff:
    Moves all x terms to the left side.
    If left has 2x and right has 1x → net = 1x

b = right_const - left_const:
    Moves all constants to the right side.
    If left has 5 and right has 4 → net = 4 - 5 = -1

b // a:
    Integer division because the problem guarantees integer solutions.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: "x+5-3+x=6+x-2"):
════════════════════════════════════════════════════════════════

STEP 1 - Split by '=':
    left_side  = "x+5-3+x"
    right_side = "6+x-2"

STEP 2 - Parse left "x+5-3+x":
    tokens = ["x", "+5", "-3", "+x"]
    ├── "x"  → has 'x' → remove x → "" → coeff += 1   → coeff=1, const=0
    ├── "+5" → no 'x'  → const += 5                    → coeff=1, const=5
    ├── "-3" → no 'x'  → const += (-3)                 → coeff=1, const=2
    └── "+x" → has 'x' → remove x → "+" → coeff += 1  → coeff=2, const=2
    Result: (coeff=2, const=2)

STEP 2 - Parse right "6+x-2":
    tokens = ["6", "+x", "-2"]
    ├── "6"  → no 'x'  → const += 6                    → coeff=0, const=6
    ├── "+x" → has 'x' → remove x → "+" → coeff += 1  → coeff=1, const=6
    └── "-2" → no 'x'  → const += (-2)                 → coeff=1, const=4
    Result: (coeff=1, const=4)

STEP 3 - Rearrange:
    2x + 2 = 1x + 4
    a = 2 - 1 = 1        (net x coefficient)
    b = 4 - 2 = 2        (net constant)
    → 1x = 2

STEP 4 - Solve:
    a ≠ 0 → x = 2 // 1 = 2
    Return "x=2" ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: "x=x"):
════════════════════════════════════════════════════════════════

    left:  (coeff=1, const=0)
    right: (coeff=1, const=0)
    a = 1 - 1 = 0
    b = 0 - 0 = 0
    → a == 0 AND b == 0 → "Infinite solutions" ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: "x=x+2"):
════════════════════════════════════════════════════════════════

    left:  (coeff=1, const=0)
    right: (coeff=1, const=2)
    a = 1 - 1 = 0
    b = 2 - 0 = 2
    → a == 0 AND b ≠ 0 → "No solution" ✓
    (Equivalent to 0x = 2, i.e. 0 = 2... impossible)

════════════════════════════════════════════════════════════════
WHY USE REGEX FOR PARSING:
════════════════════════════════════════════════════════════════

Without regex we'd need a manual character-by-character parser,
handling signs, multi-digit numbers, and 'x' placement manually.

    Manual: ~20 lines of error-prone code
    Regex:  1 clean line that splits perfectly by terms

    re.findall(r'[+-]?[^+-]+', "x+5-3+x")
    → ["x", "+5", "-3", "+x"]

Each token already comes with its sign attached, ready to process.

════════════════════════════════════════════════════════════════
THE 3 CASES OF A LINEAR EQUATION (ax = b):
════════════════════════════════════════════════════════════════

    CASE 1: a ≠ 0
    ├── There is exactly ONE solution
    ├── x = b / a
    └── Example: 2x = 4 → x = 2

    CASE 2: a = 0, b = 0
    ├── Equation reduces to 0 = 0
    ├── True for ANY value of x
    └── Example: x = x → 0x = 0 → "Infinite solutions"

    CASE 3: a = 0, b ≠ 0
    ├── Equation reduces to 0 = b (with b ≠ 0)
    ├── IMPOSSIBLE, contradiction
    └── Example: x = x+2 → 0x = 2 → "No solution"

════════════════════════════════════════════════════════════════
HANDLING SPECIAL CASES:
════════════════════════════════════════════════════════════════

    Implicit coefficient "x":
        replace('x','') → "" → detected as coeff = 1 ✓

    Implicit coefficient "-x":
        replace('x','') → "-" → detected as coeff = -1 ✓

    Explicit zero "0x":
        replace('x','') → "0" → int("0") = 0 → coeff += 0 ✓

    Multi-digit "123x":
        replace('x','') → "123" → int("123") = 123 ✓

    Negative sign at start "-x+5":
        regex captures ["-x", "+5"] → works correctly ✓

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    "x=x"              → Infinite solutions ✓
    "x=x+2"            → No solution ✓
    "2x=x"             → x=0 ✓
    "0x=0"              → Infinite solutions ✓
    "0x=5"              → No solution ✓
    "-x=-1"             → x=1 ✓
    "x+5-3+x=6+x-2"   → x=2 ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(n)
════════════════════════════════════════════════════════════════

    n = length of the equation string
    Regex scan: O(n)
    Token processing: O(n) total
    Everything else: O(1)

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(n)
════════════════════════════════════════════════════════════════

    Token list from regex: O(n) worst case
    Auxiliary variables: O(1)

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    String parsing (decomposing expression into terms)
    Regular expressions (capturing signed patterns)
    Basic linear algebra (solving ax = b)
    Equation classification (unique, infinite, no solution)
    Edge case handling (implicit coefficients)
"""
