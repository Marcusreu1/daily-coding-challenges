# 2396. Strictly Palindromic Number
# Difficulty: Medium
# https://leetcode.com/problems/strictly-palindromic-number/

"""
PROBLEM:
An integer n is strictly palindromic if, for every base b between 2 and n - 2 (inclusive), the string representation of the integer n in base b is palindromic.
Given an integer n, return true if n is strictly palindromic and false otherwise.
A string is palindromic if it reads the same forward and backward.

EXAMPLES:
Input: n = 9 → Output: false
Explanation: In base 2: 9 = 1001 (base 2), which is palindromic.
In base 3: 9 = 100 (base 3), which is not palindromic.
Therefore, 9 is not strictly palindromic so we return false.

Input: n = 4 → Output: false
Explanation: We only consider base 2: 4 = 100 (base 2), which is not palindromic.
Therefore, we return false.

CONSTRAINTS:
- 4 <= n <= 10^5

MATH RULES (UNIVERSAL COUNTEREXAMPLE PROOF):
A naive solution converts `n` into every base from 2 to n - 2 and checks for palindromes in O(N log N) time.
However, we can prove mathematically that NO strictly palindromic number exists for any n >= 4 by examining the upper-bound base b = n - 2:
1. For n = 4: The only base to check is b = 4 - 2 = 2. In base 2, 4 is represented as "100", which is not a palindrome.
2. For any n >= 5: The base b = n - 2 is at least 3, meaning the digit '2' is a valid single digit in base b.
   Algebraically, we can always rewrite n as:
   n = 1 * (n - 2)^1 + 2 * (n - 2)^0
   Thus, for EVERY integer n >= 5, its exact representation in base (n - 2) is "12".
Since "12" is never palindromic, the condition fails universally at base (n - 2) for all valid inputs.
"""

# STEP 1: Bypass all base conversion simulations using the mathematical proof for base (n - 2).
# STEP 2: Return False directly in constant time.

class Solution:
    def isStrictlyPalindromic(self, n: int) -> bool:
        
        # Mathematically proven: for n = 4, base 2 is "100"; for all n >= 5, base (n - 2) is always "12".
        return False

"""
WHY EACH PART:
- return False: Directly outputs the proven mathematical invariant, eliminating O(N log N) base-conversion loops and string reversals.

KEY TECHNIQUE:
- Constructive Mathematical Proof (Counterexample): Identifying an invariant failure condition at the boundary (b = n - 2) that collapses the entire problem space to a constant boolean truth value.

EDGE CASES:
- Minimum constraint (n = 4): Base 2 yields "100". False holds.
- Maximum constraint (n = 10^5): Base 99998 yields "12". False holds instantaneously without timeout risk.

TIME COMPLEXITY: O(1) - Executes in a single CPU instruction regardless of the magnitude of `n`.
SPACE COMPLEXITY: O(1) - Zero memory allocations required.
"""
