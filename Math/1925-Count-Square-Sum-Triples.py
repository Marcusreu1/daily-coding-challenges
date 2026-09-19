# 1925. Count Square Sum Triples
# Difficulty: Easy
# https://leetcode.com/problems/count-square-sum-triples/

"""
PROBLEM:
A square sum triple (a,b,c) is a triple where a, b, and c are integers and a^2 + b^2 = c^2.
Given an integer n, return the number of square sum triples such that 1 <= a, b, c <= n.

EXAMPLES:
Input: n = 5 → Output: 2
Explanation: The square sum triples are (3,4,5) and (4,3,5).

Input: n = 10 → Output: 4
Explanation: The square sum triples are (3,4,5), (4,3,5), (6,8,10), and (8,6,10).

CONSTRAINTS:
- 1 <= n <= 250

MATH RULES (SEARCH SPACE REDUCTION & EARLY BREAK):
A naive O(N^3) approach checking all combinations of a, b, and c is unnecessary. 
Since c is mathematically strictly defined by a and b (c = sqrt(a^2 + b^2)), we only need two loops for 'a' and 'b'.
We calculate c_squared = a^2 + b^2. 
Instead of checking if c <= n after calculating the square root, we can check if c_squared <= n^2. 
If c_squared exceeds n^2, any further larger values of 'b' will also exceed n^2, allowing us to safely `break` the inner loop early, drastically cutting down execution time.

VISUALIZATION (n = 5):
n_squared = 25

a = 3:
  b = 1: c_squared = 9 + 1 = 10. (isqrt(10)^2 != 10). Skip.
  b = 2: c_squared = 9 + 4 = 13. Skip.
  b = 3: c_squared = 9 + 9 = 18. Skip.
  b = 4: c_squared = 9 + 16 = 25. 25 <= 25. isqrt(25) = 5. 5*5 == 25. Valid! Count = 1.
  b = 5: c_squared = 9 + 25 = 34. 34 > 25. Break loop!

a = 4:
  b = 1: c_squared = 16 + 1 = 17. Skip.
  ...
  b = 3: c_squared = 16 + 9 = 25. Valid! Count = 2.
  b = 4: c_squared = 16 + 16 = 32. 32 > 25. Break loop!

Return count = 2 ✓
"""

import math

# STEP 1: Precalculate n squared to optimize bounds checking.
# STEP 2: Iterate 'a' from 1 to n - 1. Precalculate a squared.
# STEP 3: Iterate 'b' from 1 to n - 1. 
# STEP 4: Calculate the required c squared. If it exceeds n squared, break the inner loop early.
# STEP 5: Use integer square root to check if c squared is a perfect square. If true, increment count.

class Solution:
    def countTriples(self, n: int) -> int:
        
        count = 0
        n_squared = n * n
        
        # We only need to go up to n - 1 because a and b must be strictly less than c
        for a in range(1, n):
            a_squared = a * a
            
            for b in range(1, n):
                c_squared = a_squared + b * b
                
                # Early break optimization: if the sum exceeds n^2, further 'b's will too
                if c_squared > n_squared:
                    break
                    
                # Calculate the exact integer square root
                c = math.isqrt(c_squared)
                
                # Check if it was a perfect square without decimals
                if c * c == c_squared:
                    count += 1
                    
        return count

"""
WHY EACH PART:
- n_squared = n * n: Calculating this once saves potentially 60,000+ multiplications inside the loop.
- range(1, n): 'a' and 'b' can never be equal to 'n', because 'c' must be <= n, and 'c' is always strictly greater than 'a' and 'b'.
- if c_squared > n_squared: break: This is the magic line. It reduces the O(N^2) complexity to roughly O(N^2 / 2) by pruning the search tree dynamically the moment bounds are exceeded.
- math.isqrt(c_squared): Python's built-in fast integer square root. It completely eliminates floating-point precision inaccuracies (like 4.99999999).

KEY TECHNIQUE:
- Algebraic Deduction: Eliminating nested loops by relying on mathematical relationships.
- Search Space Pruning: Stopping a loop gracefully when limits are mathematically proven to be exceeded.

EDGE CASES:
- Smallest n (n = 1, 2, 3, 4): The `c_squared > n_squared` condition will quickly prune the loops. Will correctly return 0 as no triples exist below 5.

TIME COMPLEXITY: O(N^2) - The two nested loops iterate over N, but the early `break` drastically halves the actual operations. Very fast.
SPACE COMPLEXITY: O(1) - Only a few integer variables are allocated.

CONCEPTS USED:
- Pythagorean Theorem
- Early Termination / Pruning
- Integer Math Precision
"""
