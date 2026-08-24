# 1780. Check if Number is a Sum of Powers of Three
# Difficulty: Medium
# https://leetcode.com/problems/check-if-number-is-a-sum-of-powers-of-three/

"""
PROBLEM:
Given an integer n, return true if it is possible to represent n as the sum of distinct powers of three. Otherwise, return false.
An integer y is a power of three if there exists an integer x such that y == 3^x.

EXAMPLES:
Input: n = 12 → Output: true
Explanation: 12 = 3^1 + 3^2 (3 + 9 = 12). All powers are distinct.

Input: n = 91 → Output: true
Explanation: 91 = 3^0 + 3^2 + 3^4 (1 + 9 + 81 = 91). All powers are distinct.

Input: n = 21 → Output: false
Explanation: To get 21, we would need 3^2 + 3^2 + 3^1. Since 3^2 is used twice, it is not possible to represent it with distinct powers of three.

CONSTRAINTS:
- 1 <= n <= 10^7

MATH RULES (BASE 3 / TERNARY REPRESENTATION):
Any number can be represented in base 3 (ternary) using the digits 0, 1, and 2.
If a number can be formed by a sum of DISTINCT powers of three, its ternary representation must contain ONLY 0s and 1s.
- '1' means the power of 3 at that position is used once.
- '0' means the power of 3 at that position is not used.
- '2' means the power of 3 at that position must be used twice, which directly violates the distinct rule.
Therefore, if we repeatedly divide the number by 3, the remainder (modulo 3) must never be 2.

VISUALIZATION (n = 21):
Initial: n = 21

Step 1: 21 % 3 = 0. Remainder is 0. (Valid).
        n = 21 // 3 = 7
Step 2: 7 % 3 = 1. Remainder is 1. (Valid).
        n = 7 // 3 = 2
Step 3: 2 % 3 = 2. Remainder is 2. (Invalid!)
Result: False ✓
"""

# STEP 1: Loop while the number is greater than 0.
# STEP 2: Extract the last digit of the number's base-3 representation using modulo 3.
# STEP 3: If the extracted digit is 2, the number requires a duplicate power of three. Return False.
# STEP 4: Remove the processed digit by applying floor division by 3.
# STEP 5: If the loop finishes without finding a 2, return True.

class Solution:
    def checkPowersOfThree(self, n: int) -> bool:
        
        while n > 0:
            
            # Extract the current ternary digit
            remainder = n % 3
            
            # If the digit is 2, it's impossible to form the sum with distinct powers
            if remainder == 2:
                return False
                
            # Shift the number down by one power of 3
            n //= 3
            
        # If we broke down the entire number without seeing a 2, it's valid
        return True

"""
WHY EACH PART:
- n % 3: Extracts the least significant digit of the number in base 3.
- remainder == 2: The critical check. It acts as an immediate short-circuit to return False.
- n //= 3: Shifts the digits in base 3 to the right, discarding the one we just processed so we can examine the next one.

HOW IT WORKS (Example: n = 12):

Initial: n = 12

Iteration 1:
├── remainder = 12 % 3 = 0
├── check: 0 == 2 -> False
└── n = 12 // 3 = 4

Iteration 2:
├── remainder = 4 % 3 = 1
├── check: 1 == 2 -> False
└── n = 4 // 3 = 1

Iteration 3:
├── remainder = 1 % 3 = 1
├── check: 1 == 2 -> False
└── n = 1 // 3 = 0

Exit: n is 0.

Return True ✓

KEY TECHNIQUE:
- Base Conversion Logic: Using modulo and division to analyze a number's structural properties in a non-decimal numeric base without converting it to a string.

EDGE CASES:
- n = 1: 1 % 3 = 1. n becomes 0. Returns True. (3^0 = 1). ✓
- Maximum constraint (10^7): Evaluates in approximately 15 iterations since log3(10^7) is roughly 14.6. Extemely efficient.

TIME COMPLEXITY: O(log_3 n) - The number is divided by 3 in every iteration. The loop runs logarithmically proportional to n.
SPACE COMPLEXITY: O(1) - The algorithm evaluates in-place without any extra space structures.

CONCEPTS USED:
- Number Systems (Ternary / Base 3)
- Modulo Arithmetic
- Iterative Evaluation
"""
