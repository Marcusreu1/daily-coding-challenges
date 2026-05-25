# 866. Prime Palindrome
# Difficulty: Medium
# https://leetcode.com/problems/prime-palindrome/

"""
PROBLEM:
Given an integer `n`, return the smallest prime palindrome greater than or equal to `n`.
An integer is prime if it has exactly two divisors: 1 and itself. Note that 1 is not a prime number.
An integer is a palindrome if it reads the same from left to right as it does from right to left.

EXAMPLES:
Input: n = 6
Output: 7

Input: n = 8
Output: 11

Input: n = 13
Output: 101

CONSTRAINTS:
- 1 <= n <= 10^8

MATHEMATICAL INSIGHT (The 11 Divisibility Rule):
Checking numbers one by one up to 10^8 leads to Time Limit Exceeded (TLE). 
However, Number Theory gives us a massive shortcut: 
ALL even-length palindromes (except 11) are divisible by 11, meaning they can NEVER be prime.
Proof: The alternating sum of digits of an even-length palindrome cancels itself out to 0, 
which is divisible by 11. (e.g., 1221 -> 1 - 2 + 2 - 1 = 0).

Therefore, we can completely skip checking any 2, 4, 6, or 8-digit numbers. 
Instead of checking if numbers are palindromes, we GENERATE odd-length palindromes directly 
from a "root" and check if they are prime.
"""

# STEP 1: Create an optimized helper function to check for primality.
# STEP 2: Handle the only even-length prime palindrome (11) as an explicit edge case.
# STEP 3: Iterate through root lengths from 1 to 5 (sufficient to generate up to 9-digit palindromes).
# STEP 4: Iterate through all possible roots of that length (e.g., 100 to 999).
# STEP 5: Generate an odd-length palindrome by mirroring the root.
# STEP 6: If the generated palindrome >= n, check if it is prime. Return it if true.

class Solution:
    def primePalindrome(self, n: int) -> int:
        
        # Helper function for fast primality testing
        def is_prime(num: int) -> bool:
            if num < 2: 
                return False
            if num % 2 == 0: 
                return num == 2
            # Only check odd numbers up to the square root of num
            for i in range(3, int(num**0.5) + 1, 2):
                if num % i == 0:
                    return False
            return True
        
        # Explicitly handle 11, the only even-length prime palindrome
        if 8 <= n <= 11:
            return 11
            
        # Generate odd-length palindromes using roots
        # For N = 10^8, the answer could be up to 100030001 (a 9-digit number).
        # A 9-digit palindrome is formed from a 5-digit root.
        for length in range(1, 6):
            start = 10**(length - 1)
            end = 10**length
            
            for root in range(start, end):
                s = str(root)
                # Construct odd-length palindrome by mirroring the root
                # Example: root '123' -> '123' + '21' -> '12321'
                p = int(s + s[-2::-1])
                
                # We only process if it meets the minimum threshold
                if p >= n:
                    if is_prime(p):
                        return p
        
        return -1

"""
WHY EACH PART:
- int(num**0.5) + 1: A prime factor of a number will never be greater than its square root. This reduces primality checking from O(N) to O(sqrt(N)).
- if 8 <= n <= 11: Since our generator exclusively builds ODD-length palindromes, we manually catch the case where the answer is 11.
- s[-2::-1]: String slicing to reverse the root while excluding its last character. This acts as the pivot for the odd-length palindrome.

HOW IT WORKS (Example: n = 13):
Initial check: 13 is not between 8 and 11.

Outer Loop (length = 1):
├── roots: 1 to 9 -> odd palindromes 1 to 9. 
└── None are >= 13.

Outer Loop (length = 2):
├── roots: 10 to 99
├── root = 10: s = '10'. Mirror = '1'. p = 101.
├── p >= n (101 >= 13) is True.
├── is_prime(101) is True.
└── Returns 101. ✓

KEY TECHNIQUE:
- Search Space Pruning: By exploiting the modulo 11 rule and generating palindromes from roots, we shrink the search space from ~100,000,000 checks down to merely ~10,000 generations. 

EDGE CASES:
- n = 1 or 2: Correctly handled. The loop generates `p = 2`, which is prime, returning 2.
- n = 8 to 11: Handled manually to prevent skipping 11.
- n > 10^8: Handled by generating up to 9-digit palindromes. The smallest prime palindrome above 10^8 is 100030001, which is found using a 5-digit root (10003).

TIME COMPLEXITY: O(10^5 * sqrt(N)). We generate at most 10^5 roots. Checking primality for the generated palindrome takes O(sqrt(N)) time. 
SPACE COMPLEXITY: O(1) auxiliary space, manipulating standard strings and integers.

CONCEPTS USED:
- Number Theory (Divisibility by 11)
- Primality Testing
- Search Space Optimization
- String manipulation (Reversal and concatenation)
"""
