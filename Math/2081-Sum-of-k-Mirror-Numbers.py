# 2081. Sum of k-Mirror Numbers
# Difficulty: Hard
# https://leetcode.com/problems/sum-of-k-mirror-numbers/

"""
PROBLEM:
A k-mirror number is a positive integer without leading zeros that reads the same both forward and backward in base-10, as well as in base-k.
Given two integers k and n, return the sum of the first n k-mirror numbers.

EXAMPLES:
Input: k = 2, n = 5 → Output: 25
Explanation: The first 5 k-mirror numbers in base-10 are 1, 3, 5, 7, and 9.
Their representations in base-2 are 1, 11, 101, 111, and 1001, which are all palindromes.
Sum = 1 + 3 + 5 + 7 + 9 = 25.

Input: k = 3, n = 7 → Output: 499
Explanation: The first 7 k-mirror numbers in base-10 are 1, 2, 4, 8, 121, 151, and 212.
Their representations in base-3 are 1, 2, 11, 22, 11111, 12121, and 21212.
Sum = 499.

CONSTRAINTS:
- 2 <= k <= 9
- 1 <= n <= 30

MATH RULES (GENERATIVE PRUNING & BASE CONVERSION):
Checking every number iteratively (1, 2, 3...) to see if it is a palindrome is O(N) where N can grow into the billions. This leads to Time Limit Exceeded (TLE).
Instead of checking numbers, we GENERATE base-10 palindromes strictly in ascending order.
For any given length 'L', a palindrome is symmetrically dictated by its left half (the seed).
- If L = 4, seeds range from 10 to 99. (e.g., seed 12 -> palindrome 1221).
- If L = 5, seeds range from 100 to 999. Since L is odd, the last digit of the seed is the center and is not duplicated (e.g., seed 123 -> palindrome 12321).
This combinatorial approach drops the time complexity from checking O(10^L) numbers down to strictly generating O(10^(L/2)) valid numbers.
For each generated base-10 palindrome, we mathematically convert it to an array of base-k digits and check for symmetry.

VISUALIZATION (Generating Palindromes of Length 3):
Length = 3 (Odd)
Half Length = 2 -> Seed range: 10 to 99.

Iteration 1: Seed = 10.
- Since length is odd, the last digit (0) is the center. 
- Temp becomes 1. 
- Mirror logic: val = 10 * 10 + 1 = 101.
Check base-k palindrome for 101.

Iteration 2: Seed = 11.
- Temp becomes 1.
- Mirror logic: val = 11 * 10 + 1 = 111.
Check base-k palindrome for 111.
"""

# STEP 1: Define a helper function to efficiently evaluate if an integer is a palindrome in a given base k.
# STEP 2: Initialize variables for the total sum, the count of discovered numbers, and the current length of base-10 palindromes being generated.
# STEP 3: Generate the left-half seeds for the current length and mathematically mirror them to construct pure base-10 palindromes.
# STEP 4: Test the generated palindrome using the helper function. If it passes, add it to the sum.
# STEP 5: Stop and return the sum once we have found exactly n k-mirror numbers.

class Solution:
    def kMirror(self, k: int, n: int) -> int:
        
        # Helper function to check base-k palindrome symmetry
        def is_k_palindrome(num: int, base: int) -> bool:
            digits = []
            while num > 0:
                digits.append(num % base)
                num //= base
                
            # A list is equivalent to its reverse if it's a palindrome
            return digits == digits[::-1]
            
        total_sum = 0
        found = 0
        length = 1
        
        # Keep searching expanding lengths until 'n' numbers are found
        while found < n:
            
            # The length of the seed controls the magnitude of the palindrome
            half_len = (length + 1) // 2
            
            # Smallest and largest seed for the current half length
            start = 10**(half_len - 1)
            end = 10**half_len
            
            # Iterate strictly over valid seeds
            for seed in range(start, end):
                
                # Construct the palindrome mathematically to avoid string manipulation latency
                temp = seed
                val = seed
                
                # Odd length means the last digit of the seed sits exactly in the center
                if length % 2 != 0:
                    temp //= 10
                    
                # Append the reversed digits of temp to val
                while temp > 0:
                    val = val * 10 + (temp % 10)
                    temp //= 10
                    
                # Check the dual-palindrome requirement
                if is_k_palindrome(val, k):
                    total_sum += val
                    found += 1
                    
                    # Return immediately when the quota is met
                    if found == n:
                        return total_sum
                        
            # Move to the next magnitude of base-10 palindromes
            length += 1
            
        return total_sum

"""
WHY EACH PART:
- digits.append(num % base): Extracts base-k digits in O(log_k(num)) time. Mathematically optimal.
- 10**(half_len - 1): Automatically prevents leading zeros! Because the seed always starts at 1, 10, 100, etc., the first digit is never 0, guaranteeing the mirrored last digit is never 0.
- val = val * 10 + (temp % 10): Generates the palindrome purely through integer arithmetic. This is significantly faster than using str(seed) + str(seed)[::-1].

KEY TECHNIQUE:
- Generative Algorithms: Instead of blindly traversing a search space (filtering), explicitly construct only the target states to skip billions of invalid iterations.

EDGE CASES:
- Small n, large gaps (e.g., n=30): The algorithm scales smoothly, expanding string lengths without choking memory, as the maximum required number fits comfortably in standard 64-bit bounds.

TIME COMPLEXITY: O(K * log_k(N)) - Where K is the total number of base-10 palindromes generated until 'n' valid targets are found. Generating each palindrome takes O(L) where L is the number of digits, and checking takes O(log_k(V)) where V is the value. 
SPACE COMPLEXITY: O(log_k(N)) - Space is entirely minimal. We only allocate a temporary array to hold the digits of the number converted to base-k, which is infinitesimally small.
"""
