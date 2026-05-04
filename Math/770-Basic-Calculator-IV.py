"""
770. Basic Calculator IV
Difficulty: Hard
https://leetcode.com/problems/basic-calculator-iv/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

Given an expression string with variables, numbers, +, -, *, and
parentheses, plus an evaluation map that assigns values to some
variables, simplify the expression by:

    1. Substituting known variables with their integer values
    2. Evaluating all possible arithmetic
    3. Returning the simplified polynomial as a list of string tokens

EXAMPLES:

    Input: expression = "e + 8 - a + 5"
           evalvars = ["e"], evalints = [1]
    Output: ["-1*a", "14"]

    Input: expression = "(e + 8) * (e - 8)"
           evalvars = [], evalints = []
    Output: ["1*e*e", "-64"]

    Input: expression = "a * b * c + b * a * c * 4"
           evalvars = [], evalints = []
    Output: ["5*a*b*c"]

    Input: expression = "7 - 7"
           evalvars = [], evalints = []
    Output: []

OUTPUT FORMAT:
    - Variables within a term sorted lexicographically ("a*b*c" not "b*a*c")
    - Terms sorted by degree descending, then lexicographically
    - Coefficient placed left with '*' separator ("3*a*b")
    - Coefficient of 1 is still printed ("1*e*e")
    - Terms with coefficient 0 are excluded
    - Constants (degree 0) appear last

CONSTRAINTS:

    1 <= expression.length <= 250
    expression has '+', '-', '*', '(', ')', lowercase letters, digits, spaces
    0 <= evalvars.length <= 100
    Expression is always valid

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

Represent polynomials as: dict[tuple_of_sorted_variables → coefficient]

    3*a*b + 2*a + 5  →  {('a','b'): 3, ('a',): 2, (): 5}
    variable 'e'     →  {('e',): 1}
    number 8         →  {(): 8}

Sorted tuples ensure a*b and b*a map to the same key ('a','b').
Then define add, subtract, multiply on these polynomial dicts.
Parse the expression with a recursive descent parser that respects
operator precedence: parentheses > multiplication > addition/subtraction.

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. POLYNOMIAL REPRESENTATION: Need a clean data structure for symbolic terms
2. OPERATOR PRECEDENCE: Parentheses > * > +/- must be respected
3. MULTIPLICATION: Distributing terms correctly (FOIL-like expansion)
4. VARIABLE SUBSTITUTION: Replacing known variables before evaluation
5. OUTPUT FORMATTING: Complex sorting and formatting rules
6. COMBINING LIKE TERMS: Merging same variable products across operations

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Build evaluation map for variable substitution
STEP 2: Tokenize the expression string
STEP 3: Parse using recursive descent (expr → term → factor)
STEP 4: Each parse function returns a polynomial (dict)
STEP 5: Format the resulting polynomial according to output rules

GRAMMAR FOR PARSING:
    expr   → term (('+' | '-') term)*       ← lowest precedence
    term   → factor ('*' factor)*           ← medium precedence
    factor → '(' expr ')' | atom            ← highest precedence
    atom   → variable | number
"""

from collections import defaultdict


class Solution:
    def basicCalculatorIV(self, expression: str, evalvars: list, evalints: list) -> list:

        eval_map = dict(zip(evalvars, evalints))                                  # Variable → value mapping

        # ═══════════════════════════════════════════
        # POLYNOMIAL OPERATIONS
        # ═══════════════════════════════════════════
        # Poly = {term_tuple: coefficient}
        # term_tuple = sorted tuple of variable names
        # () = constant, ('a',) = a, ('a','b') = a*b

        def poly_add(p1: dict, p2: dict) -> dict:
            """Add two polynomials: combine coefficients of like terms."""
            result = defaultdict(int)
            for term, coeff in p1.items():                                        # Add all terms from p1
                result[term] += coeff
            for term, coeff in p2.items():                                        # Add all terms from p2
                result[term] += coeff
            return {k: v for k, v in result.items() if v != 0}                    # Filter out zero-coefficient terms

        def poly_sub(p1: dict, p2: dict) -> dict:
            """Subtract two polynomials: p1 - p2."""
            result = defaultdict(int)
            for term, coeff in p1.items():                                        # Add all terms from p1
                result[term] += coeff
            for term, coeff in p2.items():                                        # Subtract all terms from p2
                result[term] -= coeff
            return {k: v for k, v in result.items() if v != 0}                    # Filter out zeros

        def poly_mul(p1: dict, p2: dict) -> dict:
            """Multiply two polynomials: distribute every term × every term."""
            result = defaultdict(int)
            for t1, c1 in p1.items():                                             # For each term in p1
                for t2, c2 in p2.items():                                         # For each term in p2
                    combined = tuple(sorted(t1 + t2))                             # Merge and sort variables
                    result[combined] += c1 * c2                                   # Multiply coefficients
            return {k: v for k, v in result.items() if v != 0}                    # Filter out zeros

        def make_poly(token: str) -> dict:
            """Convert a single token into a polynomial."""
            if token in eval_map:                                                 # Known variable → substitute value
                return {(): eval_map[token]}
            elif token.isalpha():                                                 # Free variable → term with coeff 1
                return {(token,): 1}
            else:                                                                 # Number → constant term
                return {(): int(token)}

        # ═══════════════════════════════════════════
        # TOKENIZER
        # ═══════════════════════════════════════════

        def tokenize(expr: str) -> list:
            """Break expression string into a list of tokens."""
            tokens = []
            i = 0
            while i < len(expr):
                if expr[i] == ' ':                                                # Skip whitespace
                    i += 1
                elif expr[i] in '()+-*':                                          # Operator or parenthesis
                    tokens.append(expr[i])
                    i += 1
                else:                                                             # Alphanumeric: variable or number
                    j = i
                    while j < len(expr) and expr[j].isalnum():                    # Consume full token
                        j += 1
                    tokens.append(expr[i:j])
                    i = j
            return tokens

        # ═══════════════════════════════════════════
        # RECURSIVE DESCENT PARSER
        # ═══════════════════════════════════════════

        tokens = tokenize(expression)
        self.pos = 0                                                              # Current token index

        def parse_expr() -> dict:
            """Parse: expr → term (('+' | '-') term)*"""
            result = parse_term()                                                 # Parse first term
            while self.pos < len(tokens) and tokens[self.pos] in ('+', '-'):      # While + or -
                op = tokens[self.pos]                                             # Save operator
                self.pos += 1                                                     # Consume operator
                right = parse_term()                                              # Parse next term
                if op == '+':
                    result = poly_add(result, right)                              # Add polynomials
                else:
                    result = poly_sub(result, right)                              # Subtract polynomials
            return result

        def parse_term() -> dict:
            """Parse: term → factor ('*' factor)*"""
            result = parse_factor()                                               # Parse first factor
            while self.pos < len(tokens) and tokens[self.pos] == '*':             # While *
                self.pos += 1                                                     # Consume '*'
                right = parse_factor()                                            # Parse next factor
                result = poly_mul(result, right)                                  # Multiply polynomials
            return result

        def parse_factor() -> dict:
            """Parse: factor → '(' expr ')' | atom"""
            if tokens[self.pos] == '(':                                           # Parenthesized sub-expression
                self.pos += 1                                                     # Consume '('
                result = parse_expr()                                             # Recursively parse inner expr
                self.pos += 1                                                     # Consume ')'
                return result
            else:                                                                 # Atom: variable or number
                token = tokens[self.pos]
                self.pos += 1                                                     # Consume token
                return make_poly(token)                                           # Convert to polynomial

        # ═══════════════════════════════════════════
        # EXECUTE AND FORMAT
        # ═══════════════════════════════════════════

        poly = parse_expr()                                                       # Evaluate entire expression
        poly = {k: v for k, v in poly.items() if v != 0}

        # Sort: highest degree first, then lexicographically
        sorted_terms = sorted(poly.keys(), key=lambda t: (-len(t), t))

        result = []
        for term in sorted_terms:
            coeff = poly[term]
            if term:                                                              # Has variables
                result.append('*'.join([str(coeff)] + list(term)))                # "coeff*var1*var2*..."
            else:                                                                 # Constant term
                result.append(str(coeff))                                         # Just the number
        return result


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

eval_map = dict(zip(evalvars, evalints)):
    Creates a lookup dictionary for variable substitution.
    ["e"] + [1] → {"e": 1}

POLYNOMIAL REPRESENTATION {tuple: int}:
    The tuple contains SORTED variable names.
    Sorting ensures a*b and b*a both become ('a','b').
    The empty tuple () represents a constant (no variables).
    This naturally handles "like terms" — same tuple = same term.

tuple(sorted(t1 + t2)):
    When multiplying terms, concatenate variable tuples and sort.
    ('a',) * ('b','c') → ('a') + ('b','c') → ('a','b','c')
    This gives canonical form for the product term.

{k: v for k, v in result.items() if v != 0}:
    After any operation, remove terms with coefficient 0.
    This keeps the polynomial clean and handles cancellation.
    Example: a - a → {('a',): 1-1=0} → filtered to {}

make_poly(token):
    Converts an atomic token into a single-term polynomial:
    - Known variable ("e" with e=1) → {(): 1}       (substituted!)
    - Free variable ("a")          → {('a',): 1}    (kept symbolic)
    - Number ("8")                 → {(): 8}         (constant)

TOKENIZER:
    Handles all cases regardless of whitespace:
    "(e + 8)" → ["(", "e", "+", "8", ")"]
    Operators/parens are single-char tokens.
    Alphanumeric sequences are consumed as full tokens.

RECURSIVE DESCENT PARSER:
    Three functions, one per precedence level:
    - parse_expr: handles + and - (lowest precedence)
    - parse_term: handles * (medium precedence)
    - parse_factor: handles () and atoms (highest precedence)

    The nesting naturally enforces precedence:
    parse_expr calls parse_term (so * binds tighter than +/-)
    parse_term calls parse_factor (so () binds tighter than *)

self.pos:
    Shared mutable position counter across all parse functions.
    Each function consumes tokens and advances pos.

sorted(poly.keys(), key=lambda t: (-len(t), t)):
    Primary sort: degree DESCENDING (-len gives highest first)
    Secondary sort: lexicographic ASCENDING (tuple comparison)
    This matches the required output ordering.

'*'.join([str(coeff)] + list(term)):
    Formats "3*a*b*c" from coefficient 3 and term ('a','b','c').
    For constants (empty term), just str(coeff) → "-64".

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: "e + 8 - a + 5", e=1):
════════════════════════════════════════════════════════════════

    eval_map = {"e": 1}
    tokens = ["e", "+", "8", "-", "a", "+", "5"]

    parse_expr:
    ├── parse_term → parse_factor → "e" → eval_map → {(): 1}
    ├── "+", parse_term → "8" → {(): 8}
    ├── poly_add: {(): 1+8} = {(): 9}
    ├── "-", parse_term → "a" → {('a',): 1}
    ├── poly_sub: {(): 9, ('a',): -1}
    ├── "+", parse_term → "5" → {(): 5}
    └── poly_add: {(): 14, ('a',): -1}

    Sort: ('a',) degree=1 first, () degree=0 second
    Format: ["-1*a", "14"] ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: "(e + 8) * (e - 8)", no substitutions):
════════════════════════════════════════════════════════════════

    tokens = ["(", "e", "+", "8", ")", "*", "(", "e", "-", "8", ")"]

    parse_expr → parse_term:
    ├── parse_factor → "(" → parse_expr:
    │   ├── "e" → {('e',): 1}
    │   ├── "+" → "8" → {(): 8}
    │   └── poly_add: {('e',): 1, (): 8}         ← (e + 8)
    ├── "*"
    ├── parse_factor → "(" → parse_expr:
    │   ├── "e" → {('e',): 1}
    │   ├── "-" → "8" → {(): 8}
    │   └── poly_sub: {('e',): 1, (): -8}        ← (e - 8)
    └── poly_mul:
        ├── ('e',)×('e',) = ('e','e'): 1×1 = 1
        ├── ('e',)×()     = ('e',): 1×(-8) = -8
        ├── ()×('e',)     = ('e',): 8×1 = +8
        ├── ()×()         = (): 8×(-8) = -64
        ├── ('e',) total: -8+8 = 0 → filtered out!
        └── Result: {('e','e'): 1, (): -64}

    Format: ["1*e*e", "-64"] ✓   (e² - 64, difference of squares!)

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: "a * b * c + b * a * c * 4"):
════════════════════════════════════════════════════════════════

    parse_expr:
    ├── parse_term: a * b * c
    │   ├── {('a',):1} × {('b',):1} = {('a','b'):1}
    │   └── {('a','b'):1} × {('c',):1} = {('a','b','c'):1}
    ├── "+"
    ├── parse_term: b * a * c * 4
    │   ├── {('b',):1} × {('a',):1} = {('a','b'):1}
    │   ├── × {('c',):1} = {('a','b','c'):1}
    │   └── × {():4} = {('a','b','c'):4}
    └── poly_add: {('a','b','c'): 1+4} = {('a','b','c'): 5}

    Note: b*a*c and a*b*c BOTH produce ('a','b','c') due to sorting!
    Format: ["5*a*b*c"] ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: "7 - 7"):
════════════════════════════════════════════════════════════════

    parse_expr:
    ├── "7" → {(): 7}
    ├── "-"
    ├── "7" → {(): 7}
    └── poly_sub: {(): 7-7} = {(): 0} → filtered → {}

    Empty dict → [] ✓

════════════════════════════════════════════════════════════════
WHY RECURSIVE DESCENT FOR PARSING:
════════════════════════════════════════════════════════════════

    Alternative approaches:
    ├── Stack-based (Shunting Yard): Works, but more complex with polynomials
    ├── eval() with regex: Clever but hard to explain / debug
    └── Recursive descent: Clean, maps directly to the grammar ✓

    The grammar has 3 precedence levels:
        expr  (+ -)  →  calls term
        term  (*)    →  calls factor
        factor (())  →  calls expr (recursion!)

    This nesting naturally handles precedence:
        "1 + 2 * 3" → parse_expr:
        ├── parse_term → parse_factor → 1 (no *, returns {():1})
        ├── "+"
        └── parse_term:
            ├── parse_factor → 2
            ├── "*"
            ├── parse_factor → 3
            └── poly_mul: {(): 6}
        poly_add: {(): 7}  →  ["7"] ✓  (* evaluated before +)

════════════════════════════════════════════════════════════════
WHY SORTED TUPLES AS KEYS:
════════════════════════════════════════════════════════════════

    Problem: a*b and b*a are the SAME term, need same dict key.

    Without sorting:
    ├── a*b → ('a','b')
    ├── b*a → ('b','a')
    └── Different keys! Cannot combine like terms! ✗

    With sorting:
    ├── a*b → sorted('a','b') → ('a','b')
    ├── b*a → sorted('b','a') → ('a','b')
    └── Same key! Like terms automatically combine! ✓

    Also handles higher degrees:
    ├── c*a*b → sorted → ('a','b','c')
    ├── b*c*a → sorted → ('a','b','c')
    └── All orderings of same variables → same key ✓

════════════════════════════════════════════════════════════════
WHY FILTER ZERO COEFFICIENTS:
════════════════════════════════════════════════════════════════

    Operations can produce zero coefficients through cancellation:

    (e+8) * (e-8):
    ├── +8e from () × ('e',)
    ├── -8e from ('e',) × ()
    └── Total ('e',) coefficient: +8 + (-8) = 0

    If we don't filter: {('e',): 0} would produce "0*e" in output!
    Filtering after each operation keeps polynomials clean.

════════════════════════════════════════════════════════════════
OUTPUT SORTING EXPLAINED:
════════════════════════════════════════════════════════════════

    key=lambda t: (-len(t), t)

    -len(t): Higher degree terms first
        ('a','a','b','c') degree 4 → -4
        ('a','b')         degree 2 → -2
        ()                degree 0 →  0

    t: Lexicographic tiebreaker within same degree
        ('a','a','b') < ('a','b','c') → 'a' comes first

    Example ordering:
        ["-2*a*a*a",      degree 3
         "3*a*a*b",       degree 3 (a*a*b > a*a*a lexicographically)
         "3*b*b",         degree 2
         "4*a",           degree 1
         "5*c",           degree 1 (c > a)
         "-6"]            degree 0

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    "7 - 7"                      → [] (everything cancels) ✓
    "0"                          → [] (zero coefficient) ✓
    "e + 8 - a + 5" with e=1    → ["-1*a", "14"] ✓
    "(e + 8) * (e - 8)"         → ["1*e*e", "-64"] ✓
    All variables substituted    → single constant or [] ✓
    No variables substituted     → fully symbolic result ✓
    Multi-letter variables       → "temperature" handled by isalpha() ✓
    Deeply nested parentheses    → recursion handles naturally ✓
    Single variable "a"          → ["1*a"] (coeff 1 printed) ✓
    Single number "5"            → ["5"] ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(n × m² × k log k)
════════════════════════════════════════════════════════════════

    n = length of expression (tokenization + parsing)
    m = max number of terms in any intermediate polynomial
    k = max degree of any term (for sorting variables in tuple)

    Tokenization: O(n)
    Parsing: O(n) tokens processed
    Each multiplication: O(m² × k log k) — all pairs × sorting
    Formatting: O(m × k) for joining strings

    In practice, with expression length ≤ 250, this is very fast.

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(m × k)
════════════════════════════════════════════════════════════════

    m = total number of distinct terms in the polynomial
    k = max tuple length (max degree)
    Token list: O(n)
    Intermediate polynomials: O(m × k)
    Recursion depth: O(n) in worst case (deeply nested parens)

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Polynomial representation (dict with tuple keys)
    Recursive descent parsing (grammar-driven expression evaluation)
    Operator precedence (encode via function nesting)
    Symbolic computation (manipulating expressions with unknowns)
    Like-term combination (matching via sorted tuple keys)
    Canonical forms (sorted variables ensure uniqueness)
    Distributive property (polynomial multiplication)
    Hash map operations (defaultdict for accumulation)
"""
