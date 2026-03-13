"""
412. Fizz Buzz
Difficulty: Easy
https://leetcode.com/problems/fizz-buzz/

PROBLEM:
Given an integer n, return a string array answer (1-indexed) where:
    answer[i] == "FizzBuzz" if i is divisible by 3 and 5
    answer[i] == "Fizz"     if i is divisible by 3
    answer[i] == "Buzz"     if i is divisible by 5
    answer[i] == str(i)     if none of the above

EXAMPLES:
Input: n = 3  → Output: ["1","2","Fizz"]
Input: n = 5  → Output: ["1","2","Fizz","4","Buzz"]
Input: n = 15 → Output: ["1","2","Fizz","4","Buzz","Fizz","7","8",
                          "Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]

CONSTRAINTS:
    1 <= n <= 10^4

KEY INSIGHT:
Use string CONCATENATION instead of nested if/elif.
Build the string piece by piece: add "Fizz" if %3, add "Buzz" if %5.
If string is still empty, use the number itself.

CHALLENGES:
    Order of conditions matters in if/elif approach
    "FizzBuzz" must appear for numbers divisible by BOTH 3 and 5
    Concatenation approach avoids the ordering trap entirely

SOLUTION:
    1. Iterate from 1 to n
    2. Build string: "Fizz" if %3, + "Buzz" if %5
    3. If empty string, use str(i)
    4. Append to result
"""

# STEP 1: Iterate from 1 to n
# STEP 2: Build string by concatenation
# STEP 3: Default to str(i) if string is empty
# STEP 4: Collect results

class Solution:
    def fizzBuzz(self, n: int) -> List[str]:

        result = []                                                      # Final answer list

        for i in range(1, n + 1):                                        # 1-indexed: 1 to n
            s = ""                                                       # Start with empty string

            if i % 3 == 0:                                               # Divisible by 3?
                s += "Fizz"                                              # Add "Fizz"

            if i % 5 == 0:                                               # Divisible by 5?
                s += "Buzz"                                              # Add "Buzz"

            if not s:                                                    # Still empty? Not divisible by 3 or 5
                s = str(i)                                               # Use the number itself

            result.append(s)                                             # Add to answer

        return result

"""
WHY EACH PART:

    result = []: Collect all answers in order
    for i in range(1, n+1): Problem is 1-indexed (starts at 1, not 0)
    s = "": Fresh string for each number
    if i % 3 == 0: s += "Fizz": Adds "Fizz" component
    if i % 5 == 0: s += "Buzz": Adds "Buzz" component (NOT elif!)
    if not s: s = str(i): Empty string is falsy in Python
    result.append(s): Build the answer list

HOW IT WORKS (Example: n = 15, showing key numbers):

    i=1:  s = "" → no %3, no %5 → s = "1"
    i=2:  s = "" → no %3, no %5 → s = "2"

    i=3:  s = "" → %3 ✓ → s = "Fizz"
    ├── %5? NO → stays "Fizz"
    └── not empty → "Fizz" ✓

    i=5:  s = "" → %3? NO
    ├── %5 ✓ → s = "Buzz"
    └── not empty → "Buzz" ✓

    i=15: s = "" → %3 ✓ → s = "Fizz"
    ├── %5 ✓ → s = "Fizz" + "Buzz" = "FizzBuzz"
    └── not empty → "FizzBuzz" ✓

    Result: ["1","2","Fizz","4","Buzz","Fizz","7","8",
             "Fizz","Buzz","11","Fizz","13","14","FizzBuzz"] ✓

WHY CONCATENATION IS BETTER THAN IF/ELIF:

    if/elif approach (careful ordering needed):
    ├── Must check "both 3 and 5" FIRST
    ├── Easy to get wrong order → bug
    └── Adding new rules requires restructuring ALL conditions

    Concatenation approach (this solution):
    ├── Each condition is INDEPENDENT (if, not elif)
    ├── Order doesn't matter for correctness
    ├── "FizzBuzz" builds naturally: "Fizz" + "Buzz"
    └── Adding new rules = just add one more if ✓

    Example: if we add "divisible by 7 → Jazz":
        if i % 3 == 0: s += "Fizz"
        if i % 5 == 0: s += "Buzz"
        if i % 7 == 0: s += "Jazz"     ← just add this line!
        # 105 → "FizzBuzzJazz" automatically ✓

WHY "if" AND NOT "elif" FOR BUZZ:

    elif: "if Fizz, SKIP Buzz check" → 15 becomes just "Fizz" ✗
    if:   "check Buzz INDEPENDENTLY" → 15 becomes "FizzBuzz" ✓

    The two checks are NOT mutually exclusive,
    so they must be separate if statements.

WHY "if not s" WORKS:

    In Python, empty string "" is FALSY:
    ├── not "" → True  (string is empty, use number)
    └── not "Fizz" → False (string has content, keep it)

    This is equivalent to: if len(s) == 0

PATTERN OF FIZZBUZZ (repeats every 15 numbers):

    1  2  Fizz  4  Buzz  Fizz  7  8  Fizz  Buzz  11  Fizz  13  14  FizzBuzz
    ↑                                                                   ↑
    Cycle start                                                    Cycle end

    The pattern repeats because LCM(3,5) = 15

EDGE CASES:

    n = 1: Just ["1"] ✓
    n = 3: ["1","2","Fizz"] ✓
    n = 15: Full cycle including "FizzBuzz" ✓
    n = 10^4: Simple loop handles it easily ✓
    Multiples of 15: Always "FizzBuzz" ✓
    Prime numbers > 5: Always just the number ✓

TIME COMPLEXITY: O(n)
    Single pass from 1 to n
    Each iteration does constant work (modulo + concatenation)

SPACE COMPLEXITY: O(n)
    The result list stores n strings
    (O(1) extra space if we exclude the output)

CONCEPTS USED:
    Modulo operator for divisibility
    String concatenation for building results
    Falsy values in Python (empty string)
    Scalable condition design (independent checks)
    1-indexed iteration
"""
