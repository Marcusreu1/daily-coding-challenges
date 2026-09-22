# 1952. Three Divisors
# Difficulty: Easy
# https://leetcode.com/problems/three-divisors/

"""
PROBLEM:
Given an integer n, return true if n has exactly three positive divisors. Otherwise, return false.
An integer m is a divisor of n if there exists an integer k such that n = k * m.

EXAMPLES:
Input: n = 2 → Output: false
Explanation: 2 has only two divisors: 1 and 2.

Input: n = 4 → Output: true
Explanation: 4 has exactly three divisors: 1, 2, and 4.

Input: n = 9 → Output: true
Explanation: 9 has exactly three divisors: 1, 3, and 9.

CONSTRAINTS:
- 1 <= n <= 10^4

MATH RULES (SQUARES OF PRIMES):
A number typically has an even number of divisors because they appear in pairs (e.g., for 12: 1x12, 2x6, 3x4).
The ONLY way a number can have an ODD number of divisors is if it is a perfect square (one of the pairs is a number multiplied by itself).
To have EXACTLY THREE divisors, those divisors must be:
1. The number 1.
2. The square root of the number.
3. The number itself.
For no other divisors to exist, the square root must not be divisible by anything else. 
Conclusion: A number has exactly 3 divisors IF AND ONLY IF it is the square of a prime number. (e.g., 2^2=4, 3^2=9, 5^2=25, 7^2=49).

VISUALIZATION (n = 25):
Step 1: Is it a perfect square? sqrt(25) = 5. 5 * 5 == 25. (Yes).
Step 2: Is the root (5) a prime number? Divisors of 5 are 1 and 5. (Yes).
Result: True ✓ (Divisors of 25 are exactly 1, 5, 25).
"""

import math

# STEP 1: Handle base cases. Numbers less than 4 (1, 2, 3) cannot have 3 divisors.
# STEP 2: Calculate the exact integer square root of n.
# STEP 3: If squaring the root does not equal n, it is not a perfect square, return False.
# STEP 4: Check if the square root itself is a prime number.
# STEP 5: If the root is divisible by any number, return False. Otherwise, return True.

class Solution:
    def isThree(self, n: int) -> bool:
        
        # Base case: Smallest number with 3 divisors is 4 (2^2)
        if n < 4:
            return False
            
        # Get the integer square root
        root = math.isqrt(n)
        
        # Check if 'n' is a perfect square
        if root * root != n:
            return False
            
        # Verify if the 'root' is a prime number
        # We only need to check up to the square root of the 'root'
        limit = math.isqrt(root)
        for i in range(2, limit + 1):
            if root % i == 0:
                return False
                
        # If it's a perfect square and the root is prime, it has exactly 3 divisors
        return True

"""
WHY EACH PART:
- n < 4: Acts as an immediate filter to prevent evaluating numbers like 1, 2, and 3 which naturally fail the condition.
- math.isqrt(n): Python's fast integer square root algorithm natively avoids floating-point inaccuracies.
- range(2, math.isqrt(root) + 1): When checking if a number is prime, we mathematically only need to test divisors up to its square root. This makes the prime check incredibly fast.

KEY TECHNIQUE:
- Mathematical Reduction: Transforming a linear O(N) counting problem into an O(sqrt(sqrt(N))) property verification problem. 

EDGE CASES:
- n = 1: Bypassed correctly by the `n < 4` check (returns False).
- n is a square of a non-prime (e.g., 16): root is 4. 4 is divisible by 2 in the prime-check loop. Returns False. (16 has 5 divisors: 1, 2, 4, 8, 16).

TIME COMPLEXITY: O(N^(1/4)) - The integer square root takes O(1) time. The prime-checking loop runs up to the square root of the root, meaning it runs proportional to N^(1/4). For N=10000, it takes a maximum of 3 loop iterations. Astonishingly fast.
SPACE COMPLEXITY: O(1) - Only integer variables are used.

CONCEPTS USED:
- Number Theory (Prime Numbers, Perfect Squares)
- Divisibility Rules
- Search Space Optimization
"""
