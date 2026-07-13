# 1317. Convert Integer to the Sum of Two No-Zero Integers
# Difficulty: Easy
# https://leetcode.com/problems/convert-integer-to-the-sum-of-two-no-zero-integers/

"""
PROBLEM:
Given an integer n, return a list of two integers [a, b] where:
- a and b are No-Zero integers (they don't contain any '0' in their decimal representation).
- a + b = n
If there are multiple valid answers, you can return any of them.

EXAMPLES:
Input: n = 2
Output: [1, 1]
(Explanation: 1 + 1 = 2. Neither 1 nor 1 contains a zero. A valid answer.)

Input: n = 11
Output: [2, 9]
(Explanation: 2 + 9 = 11. Neither contains a zero. [3, 8], [4, 7], etc., are also valid.)

Input: n = 10000
Output: [1, 9999]
(Explanation: 1 + 9999 = 10000. No zeros used in these integers.)

CONSTRAINTS:
- 2 <= n <= 10^4

ALGORITHM LOGIC (Linear Search & String Validation):
1. Given the small constraint (n <= 10000), an O(N) linear scan is perfectly optimal.
2. We iterate a variable `a` from 1 up to n-1.
3. For each `a`, its counterpart `b` must strictly be `n - a`.
4. We cast both `a` and `b` to strings and check if the character '0' exists inside them.
5. The very first pair that passes the `not in` check is returned immediately, breaking the loop.

VISUALIZATION (n = 11):
Iteration 1:
a = 1, b = 11 - 1 = 10
Is '0' in "1"? No.
Is '0' in "10"? Yes. (Fails)

Iteration 2:
a = 2, b = 11 - 2 = 9
Is '0' in "2"? No.
Is '0' in "9"? No. (Passes!)
Return [2, 9] ✓
"""

# STEP 1: Loop `a` from 1 up to n-1 (since b must be at least 1)
# STEP 2: Calculate `b` as `n - a`
# STEP 3: Cast both numbers to strings and verify '0' is not present in either
# STEP 4: Return [a, b] immediately upon finding the first valid pair

class Solution:
    def getNoZeroIntegers(self, n: int) -> list[int]:
        
        for a in range(1, n):                                        # Iterate from 1 to n-1
            
            b = n - a                                                # Deduce the counterpart mathematically
            
            if '0' not in str(a) and '0' not in str(b):              # Validate the No-Zero condition
                return [a, b]                                        # Early exit with the valid pair

"""
WHY EACH PART:
- range(1, n): We start at 1 because 0 is inherently a "zero integer". We stop at n-1 to ensure `b` is also at least 1.
- b = n - a: Reduces a complex two-pointer combination problem into a deterministic single-variable loop.
- '0' not in str(): Python's internal substring search (implemented in C) is incredibly fast. Converting to string and checking is much faster here than mathematically modulo-dividing every number by 10.
- return [a, b] inside the loop: This acts as an early exit constraint. Since the problem accepts *any* valid answer, stopping at the very first one saves processing time.

HOW IT WORKS (Example: n = 10):
a = 1, b = 9. 
'0' in "1"? False. '0' in "9"? False.
Both are False, meaning no zeroes exist.
Returns [1, 9]. ✓

KEY TECHNIQUE:
- Brute Force: Knowing when to use it based on constraint boundaries. 10^4 iterations take ~0.001 seconds in modern CPU architecture.
- String conversion for digit inspection.

EDGE CASES:
- n = 2: The smallest possible input. Loop runs exactly once (a=1, b=1). Both pass. Returns [1, 1]. ✓
- n = 1010: Skips multiple numbers containing zero (like 10 and 1000) and gracefully lands on [11, 999]. ✓

TIME COMPLEXITY: O(N) - In the absolute worst case, we might scan almost all numbers up to N before finding a valid pair. Converting a number up to 10^4 to a string takes O(1) time (since it's max 5 characters).
SPACE COMPLEXITY: O(1) - We only allocate a few pointer variables and transient string representations.

CONCEPTS USED:
- Linear Search
- Substring searching
- Math (Complements)
"""
