# 1837. Sum of Digits in Base K
# Difficulty: Easy
# https://leetcode.com/problems/sum-of-digits-in-base-k/

"""
PROBLEM:
Given an integer n (in base 10) and a base k, return the sum of the digits of n after converting n from base 10 to base k.
After converting, each digit should be interpreted as a base 10 number, and the sum should be returned in base 10.

EXAMPLES:
Input: n = 34, k = 6 → Output: 9
Explanation: 34 (base 10) expressed in base 6 is 54. 5 + 4 = 9.

Input: n = 10, k = 10 → Output: 1
Explanation: n is already in base 10. 1 + 0 = 1.

CONSTRAINTS:
- 1 <= n <= 100
- 2 <= k <= 10

MATH RULES (BASE CONVERSION):
To convert a number from base 10 to any base 'k', we repeatedly divide the number by 'k'.
The remainder of this division (n % k) gives us the least significant digit in the new base.
The quotient (n // k) gives us the remaining number to process.
Since the problem only asks for the SUM of these digits, we do not need to construct the actual converted string. We can just add the remainders to an accumulator as we calculate them.

VISUALIZATION (n = 34, k = 6):
Initial: total_sum = 0, n = 34

Step 1:
- Digit = 34 % 6 = 4
- total_sum = 0 + 4 = 4
- n = 34 // 6 = 5

Step 2:
- Digit = 5 % 6 = 5
- total_sum = 4 + 5 = 9
- n = 5 // 6 = 0

Exit loop because n is 0.
Result: 9 ✓
"""

# STEP 1: Initialize a variable to accumulate the sum of the digits.
# STEP 2: Use a while loop that runs as long as n is strictly greater than 0.
# STEP 3: In each iteration, extract the current base-k digit using modulo k and add it to the sum.
# STEP 4: Remove the extracted digit from n by performing floor division by k.
# STEP 5: Return the accumulated sum.

class Solution:
    def sumBase(self, n: int, k: int) -> int:
        
        total_sum = 0
        
        # Continuously extract digits until the number is fully broken down
        while n > 0:
            
            # Extract the least significant digit in base k
            digit = n % k
            total_sum += digit
            
            # Shift the number down by one power of k
            n //= k
            
        return total_sum

"""
WHY EACH PART:
- n % k: Extracts the mathematical value of the digit without needing string formatting libraries like bin() or hex().
- total_sum += digit: Applies the core requirement of the problem dynamically on the fly.
- n //= k: Shrinks the number logarithmically, ensuring the while loop terminates efficiently.

HOW IT WORKS (Example: n = 42, k = 2):

Initial: total_sum = 0, n = 42

Iteration 1:
├── 42 % 2 = 0
├── total_sum = 0 + 0 = 0
└── n = 42 // 2 = 21

Iteration 2:
├── 21 % 2 = 1
├── total_sum = 0 + 1 = 1
└── n = 21 // 2 = 10

Iteration 3:
├── 10 % 2 = 0
├── total_sum = 1 + 0 = 1
└── n = 10 // 2 = 5

Iteration 4:
├── 5 % 2 = 1
├── total_sum = 1 + 1 = 2
└── n = 5 // 2 = 2

Iteration 5:
├── 2 % 2 = 0
├── total_sum = 2 + 0 = 2
└── n = 2 // 2 = 1

Iteration 6:
├── 1 % 2 = 1
├── total_sum = 2 + 1 = 3
└── n = 1 // 2 = 0

Exit: Loop finishes

Return 3 ✓ (42 in base 2 is 101010, sum of digits is 1+0+1+0+1+0 = 3).

KEY TECHNIQUE:
- Modulo Arithmetic: Using mathematical operations to evaluate a state in a different numeric base directly in memory.
- O(1) Space Accumulation: Calculating the answer without allocating arrays or strings.

EDGE CASES:
- n < k: The loop will run exactly once. The modulo returns n, and the division returns 0. Works perfectly.
- k = 10: Extracts base 10 digits as expected, skipping any base conversion overhead.

TIME COMPLEXITY: O(log_k n) - The number of iterations is strictly proportional to how many times n can be divided by k.
SPACE COMPLEXITY: O(1) - The algorithm uses a single integer for the accumulator.

CONCEPTS USED:
- Number Systems (Base Conversion)
- Modulo Arithmetic
- Iterative Reduction
"""
