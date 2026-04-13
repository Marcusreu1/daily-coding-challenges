"""
553. Optimal Division
Difficulty: Medium
https://leetcode.com/problems/optimal-division/

PROBLEM:
    Given an array of positive integers, add parentheses to maximize
    the result of dividing all numbers left to right.
    Return the expression as a string.

EXAMPLES:
    Input: nums = [1000,100,10,2] → Output: "1000/(100/10/2)"
    Input: nums = [2,3,4]         → Output: "2/(3/4)"
    Input: nums = [2]             → Output: "2"

CONSTRAINTS:
    1 <= nums.length <= 10
    2 <= nums[i] <= 1000

KEY INSIGHT:
    nums[0] is ALWAYS in the numerator.
    nums[1] is ALWAYS in the denominator (unavoidable).
    All other numbers (nums[2..n-1]) CAN be moved to the numerator
    by wrapping nums[1..n-1] in one big parenthesis.

    Optimal: nums[0] / (nums[1] / nums[2] / ... / nums[n-1])
    This equals: nums[0] × nums[2] × ... × nums[n-1] / nums[1]

    Maximizes because we multiply by everything except nums[1].

CHALLENGES:
    Recognizing the mathematical pattern (not a DP problem!)
    Handling edge cases (n=1, n=2)
    Understanding WHY this grouping is always optimal

SOLUTION:
    n = 1: return the number
    n = 2: return "a/b"
    n >= 3: return "a/(b/c/d/...)"
"""


# STEP 1: Handle n = 1 (single number, no division)
# STEP 2: Handle n = 2 (simple division, no parentheses needed)
# STEP 3: For n >= 3, wrap nums[1..n-1] in parentheses
# STEP 4: Build and return the expression string


class Solution:
    def optimalDivision(self, nums: List[int]) -> str:

        n = len(nums)

        if n == 1:                                                    # Single number, nothing to divide
            return str(nums[0])

        if n == 2:                                                    # Simple division, no optimization possible
            return f"{nums[0]}/{nums[1]}"

        middle = "/".join(str(x) for x in nums[1:])                  # Join nums[1..n-1] with "/"

        return f"{nums[0]}/({middle})"                                # Wrap in parentheses after first number


"""
WHY EACH PART:
    n == 1:              No division at all → just the number itself
    n == 2:              Only one division, parentheses can't change anything
    nums[1:]:            All numbers after the first (the "denominator group")
    "/".join(...):        Connects them with "/" → "100/10/2"
    f"{nums[0]}/({middle})": Builds "1000/(100/10/2)" format
    
    We DON'T need to actually compute the result — just build the expression!


HOW IT WORKS (Example: nums = [1000, 100, 10, 2]):

    n = 4 → not 1, not 2 → go to general case

    middle:
    ├── nums[1:] = [100, 10, 2]
    ├── str each: ["100", "10", "2"]
    └── "/".join → "100/10/2"

    return f"1000/(100/10/2)" 

    Math verification:
    ├── Inside parens: 100/10/2 = 5
    ├── Full expression: 1000/5 = 200
    └── Equivalent to: 1000 × 10 × 2 / 100 = 200 ✓


HOW IT WORKS (Example: nums = [2, 3, 4]):

    n = 3 → general case

    middle:
    ├── nums[1:] = [3, 4]
    └── "/".join → "3/4"

    return "2/(3/4)" 

    Math verification:
    ├── 3/4 = 0.75
    ├── 2/0.75 = 2.666...
    ├── Equivalent to: 2 × 4 / 3 = 8/3 ≈ 2.667 ✓
    │
    ├── Compare with no parens: 2/3/4 = 0.1667
    └── Our answer is bigger ✓


HOW IT WORKS (Example: nums = [5]):

    n = 1 → return "5" 


HOW IT WORKS (Example: nums = [10, 5]):

    n = 2 → return "10/5" 


WHY THIS PATTERN IS ALWAYS OPTIMAL:
    Given: a / b / c / d / ...

    Every arrangement of parentheses produces:
        numerator   = product of some subset of {a, b, c, d, ...}
        denominator = product of the remaining numbers

    Rules that NEVER change:
        1. "a" (nums[0]) is ALWAYS in the numerator
        2. "b" (nums[1]) is ALWAYS in the denominator

    Why? Because a is the starting number (always on top)
    and b is the FIRST divisor (always divides a, no matter what).

    For c, d, e, ... we have a CHOICE:
        They can end up in numerator OR denominator
        depending on parentheses.

    To MAXIMIZE: put everything possible in the numerator!

    ┌─────────────────────────────────────┐
    │  Optimal = a × c × d × ... / b     │
    │            ↑ numerator ↑    ↑denom  │
    │                                     │
    │  Achieved by: a / (b / c / d / ...) │
    └─────────────────────────────────────┘


PROOF WITH 3 NUMBERS [a, b, c]:
    Only two options exist:

    Option 1: a / b / c = a / (b × c)
        numerator = a
        denominator = b × c

    Option 2: a / (b / c) = a × c / b
        numerator = a × c
        denominator = b

    Since c >= 2 (constraint):
        a × c / b > a / (b × c)
        Option 2 wins! 


PROOF WITH 4 NUMBERS [a, b, c, d]:
    Key options:

    a/b/c/d           = a / (bcd)            numerator: a
    a/(b/c/d)         = a × c × d / b        numerator: a × c × d  ← MAX 
    a/(b/c)/d         = a × c / (b × d)      numerator: a × c
    a/b/(c/d)         = a × d / (b × c)      numerator: a × d
    (a/b)/(c/d)       = a × d / (b × c)      numerator: a × d
    a/(b/(c/d))       = a × c / (b × d)      numerator: a × c

    a × c × d / b has the MOST in the numerator
    and the LEAST (just b) in the denominator → MAXIMUM 


HANDLING SPECIAL CASES:
    n = 1:                   Just the number, no division → "5" ✓
    n = 2:                   Single division, no choice → "a/b" ✓
    n = 3:                   "a/(b/c)" ✓
    All same numbers [2,2,2]: "2/(2/2)" = 2/1 = 2 ✓
    Large n = 10:            Still just one parenthesis pair ✓


KEY TECHNIQUE:
    Mathematical insight:    Recognize the pattern instead of brute force
    Greedy reasoning:        Maximize numerator, minimize denominator
    String building:         join() for clean expression construction
    Edge case handling:      n=1 and n=2 before general case


EDGE CASES:
    nums = [2]:              "2" ✓
    nums = [2, 3]:           "2/3" ✓
    nums = [2, 3, 4]:        "2/(3/4)" ✓
    nums = [1000,100,10,2]:  "1000/(100/10/2)" ✓
    All minimum [2,2,...,2]:  Works correctly ✓
    All maximum [1000,...]:   Works correctly ✓
    n = 10 (maximum):        One pair of parentheses ✓


TIME COMPLEXITY: O(n)
    Single pass through nums to build the string
    join() iterates through n-1 elements

SPACE COMPLEXITY: O(n)
    The result string has all n numbers
    No additional data structures needed


CONCEPTS USED:
    Mathematical reasoning (division properties)
    Greedy algorithm (maximize numerator)
    String manipulation (join, f-strings)
    Edge case analysis
    Proof by enumeration (showing pattern holds)
"""
