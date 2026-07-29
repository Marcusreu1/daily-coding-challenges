# 1447. Simplified Fractions
# Difficulty: Medium
# https://leetcode.com/problems/simplified-fractions/

"""
PROBLEM:
Given an integer `n`, return a list of all simplified fractions between 0 and 1 (exclusive) 
such that the denominator is less than or equal to `n`. You can return the answer in any order.

EXAMPLES:
Input: n = 2
Output: ["1/2"]
(Explanation: "1/2" is the only valid fraction with a denominator <= 2 that lies between 0 and 1.)

Input: n = 3
Output: ["1/2","1/3","2/3"]

Input: n = 4
Output: ["1/2","1/3","1/4","2/3","3/4"]
(Explanation: "2/4" is not a simplified fraction because it can be simplified to "1/2".)

CONSTRAINTS:
- 1 <= n <= 100

ALGORITHM LOGIC (Combinatorics & Greatest Common Divisor):
1. A fraction a/b is strictly between 0 and 1 if 0 < a < b.
2. A fraction a/b is in its most simplified (irreducible) form if and only if `a` and `b` are coprime.
3. Two integers are coprime if their Greatest Common Divisor (GCD) is exactly 1.
4. We iterate through all possible denominators from 2 to `n`.
5. For each denominator, we iterate through all valid numerators from 1 to `denominator - 1`.
6. Using the highly optimized Euclidean algorithm via `math.gcd()`, we verify if the pair is coprime.
7. If `gcd(numerator, denominator) == 1`, we format the string and append it to our results list.

VISUALIZATION (n = 4):
denom = 2:
  num = 1: gcd(1, 2) == 1. Add "1/2" ✓

denom = 3:
  num = 1: gcd(1, 3) == 1. Add "1/3" ✓
  num = 2: gcd(2, 3) == 1. Add "2/3" ✓

denom = 4:
  num = 1: gcd(1, 4) == 1. Add "1/4" ✓
  num = 2: gcd(2, 4) == 2. (Not 1!). Discard "2/4" 
  num = 3: gcd(3, 4) == 1. Add "3/4" ✓

Result: ["1/2", "1/3", "2/3", "1/4", "3/4"] ✓
"""

import math

# STEP 1: Initialize the results list
# STEP 2: Iterate over possible denominators starting from 2 up to n
# STEP 3: Iterate over possible numerators from 1 up to (denominator - 1)
# STEP 4: Check if the numerator and denominator are coprime using math.gcd
# STEP 5: Format as a string and append if they are coprime

class Solution:
    def simplifiedFractions(self, n: int) -> list[str]:
        
        ans = []
        
        # Denominator bounds: lowest possible is 2 to keep fraction < 1
        for denominator in range(2, n + 1):
            
            # Numerator bounds: must be at least 1, and strictly less than denominator
            for numerator in range(1, denominator):
                
                # Check for irreducible fraction property
                if math.gcd(numerator, denominator) == 1:
                    
                    # Construct string dynamically
                    ans.append(f"{numerator}/{denominator}")
                    
        return ans

"""
WHY EACH PART:
- range(2, n + 1): Starting at 2 prevents division by 0 and handles the < 1 constraint naturally.
- range(1, denominator): Ensures the fraction is strictly greater than 0 and strictly less than 1.
- math.gcd(num, den) == 1: Replaces the need for a Hash Set tracking evaluated float divisions (which is prone to floating-point errors). GCD guarantees exact, integer-level mathematical truth.
- f"{num}/{den}": Python's f-strings are the most memory-efficient and readable way to concatenate integers into string formats.

HOW IT WORKS (Example: num = 3, den = 6):
Algorithm tests `math.gcd(3, 6)`.
The GCD is 3.
3 != 1.
The algorithm skips adding "3/6" (which correctly prevents duplicating the "1/2" we already added). ✓

KEY TECHNIQUE:
- Mathematics (Number Theory - Coprimes)
- Euclidean Algorithm
- Combinatorial nested loops

EDGE CASES:
- n = 1: The outer loop `range(2, 2)` does not execute. Returns `[]`, which is correct because no fraction >0 and <1 exists with denominator 1. ✓
- Consecutive numbers (e.g. 2/3, 3/4): Consecutive integers are ALWAYS coprime by mathematical definition. `math.gcd` correctly returns 1 for all of them. ✓

TIME COMPLEXITY: O(N^2 * log(N)) - The nested loops generate exactly (N * (N-1)) / 2 pairs, which is O(N^2). For each pair, `math.gcd` executes in O(log(min(numerator, denominator))) time. Since N <= 100, this is extremely fast, executing in less than ~60,000 minimal operations.
SPACE COMPLEXITY: O(N^2) - The length of the output list grows proportionally to the number of valid irreducible fractions (which mathematically correlates to the sequence of Euler's totient functions sum, bounded loosely by O(N^2)).
"""
