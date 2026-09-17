# 1922. Count Good Numbers
# Difficulty: Medium
# https://leetcode.com/problems/count-good-numbers/

"""
PROBLEM:
A digit string is good if the digits (0-indexed) at even indices are even and the digits at odd indices are prime (2, 3, 5, or 7).
- For example, "2582" is good because the digits (2 and 8) at even positions are even and the digits (5 and 2) at odd positions are prime. However, "3245" is not good because 3 is at an even index but is not even.
Given an integer n, return the total number of good digit strings of length n. Since the answer may be large, return it modulo 10^9 + 7.

EXAMPLES:
Input: n = 1 → Output: 5
Explanation: The good numbers of length 1 are "0", "2", "4", "6", "8".

Input: n = 4 → Output: 400
Explanation: 
Even indices (0, 2): 5 choices each.
Odd indices (1, 3): 4 choices each.
Total = 5 * 4 * 5 * 4 = 400.

Input: n = 50 → Output: 564908303

CONSTRAINTS:
- 1 <= n <= 10^15

MATH RULES (COMBINATORICS & MODULAR EXPONENTIATION):
Even digits (0, 2, 4, 6, 8) give us 5 choices.
Prime digits (2, 3, 5, 7) give us 4 choices.

For a string of length 'n':
- The number of odd indices is n // 2.
- The number of even indices is n // 2 + (n % 2), which is equivalent to n - odd_indices.

Total combinations = (5^even_indices) * (4^odd_indices).
Because n can be up to 10^15, normal exponentiation results in Time Limit Exceeded (TLE). We must use Binary Exponentiation, which runs in O(log n) time.
Python's built-in `pow(base, exp, mod)` function handles this under the hood with extreme efficiency.

VISUALIZATION (n = 5):
Indices: 0 (Even), 1 (Odd), 2 (Even), 3 (Odd), 4 (Even)
Choices: 5, 4, 5, 4, 5

Calculations:
odd_indices = 5 // 2 = 2
even_indices = 5 - 2 = 3

Result: (5^3 * 4^2) % MOD
Result = (125 * 16) % MOD = 2000 ✓
"""

# STEP 1: Define the modulo constant.
# STEP 2: Calculate the exact number of even and odd indices for a string of length n.
# STEP 3: Use binary exponentiation (pow) to calculate the choices for even and odd positions modulo 10^9 + 7.
# STEP 4: Multiply the results, apply the modulo one last time, and return.

class Solution:
    def countGoodNumbers(self, n: int) -> int:
        
        MOD = 10**9 + 7
        
        # In 0-indexed strings, even indices always appear first.
        # Thus, odd indices take exactly half (floor division).
        odd_indices_count = n // 2
        even_indices_count = n - odd_indices_count
        
        # Calculate permutations using modular exponentiation (O(log N))
        even_choices = pow(5, even_indices_count, MOD)
        odd_choices = pow(4, odd_indices_count, MOD)
        
        # Combine the choices using the rule of product
        total_good_numbers = (even_choices * odd_choices) % MOD
        
        return total_good_numbers

"""
WHY EACH PART:
- odd_indices_count = n // 2: Maps logically to alternating sequences. For n=5, 5//2=2. 
- even_indices_count = n - odd_indices_count: Prevents needing conditional modulo arithmetic (like n % 2 == 1) by simply taking the remainder of n.
- pow(5, even_indices_count, MOD): Performs (5^even) % MOD in O(log N) time instead of O(N) time. Essential for preventing TLE when n = 10^15.

KEY TECHNIQUE:
- Combinatorial Rule of Product: Breaking down permutation patterns into distinct mathematical counts.
- Binary Exponentiation: Leveraging mathematical algorithms to handle exponential scale operations logarithmically.

EDGE CASES:
- n = 1: odd_indices = 0, even_indices = 1. pow(4, 0) = 1. pow(5, 1) = 5. Result: 5. Handled perfectly.
- Massive numbers (n = 10^15): Resolved almost instantly via logarithmic division of the exponent inside Python's C-backend.

TIME COMPLEXITY: O(log n) - The pow() function with three arguments uses the square-and-multiply algorithm, which halves the exponent at each step.
SPACE COMPLEXITY: O(1) - Only integer variables are created.
"""
