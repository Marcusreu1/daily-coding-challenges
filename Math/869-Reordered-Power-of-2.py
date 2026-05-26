# 869. Reordered Power of 2
# Difficulty: Medium
# https://leetcode.com/problems/reordered-power-of-2/

"""
PROBLEM:
You are given an integer `n`. We reorder the digits in any order (including the original order) 
such that the leading digit is not zero.
Return `true` if and only if we can do this so that the resulting number is a power of two.

EXAMPLES:
Input: n = 1
Output: true (1 is 2^0)

Input: n = 10
Output: false (10 cannot be reordered to any power of 2. '01' has a leading zero)

Input: n = 46
Output: true (46 can be reordered to 64, which is 2^6)

CONSTRAINTS:
- 1 <= n <= 10^9

THE PERMUTATION TRAP:
A naive approach would be to generate all permutations of the digits of `n` and check if 
any of them is a power of 2. For a 10-digit number, there are 10! (3.6 million) permutations. 
This is highly inefficient and prone to Time Limit Exceeded (TLE).

REVERSE THINKING & ANAGRAM SIGNATURES:
Instead of generating millions of permutations of `n`, we generate the powers of 2.
Since `n <= 10^9`, the maximum power of 2 that can be formed within this digit limit 
is 2^29 (536,870,912). Therefore, there are ONLY 30 valid powers of 2 (from 2^0 to 2^29) 
that we ever need to care about.

If `n` can be reordered into a power of 2, it means `n` and that power of 2 are "anagrams" 
of each other—they must contain the exact same frequency of each digit. By counting the 
occurrences of each digit (creating a frequency signature), we can simply compare the 
signature of `n` against the signatures of the 30 possible powers of 2.
"""

from collections import Counter

# STEP 1: Compute the digit frequency signature of the input `n`.
# STEP 2: Iterate through all possible exponents from 0 to 29.
# STEP 3: Compute the power of 2 using bitwise shifting (1 << i).
# STEP 4: Compute the digit frequency signature of this power of 2.
# STEP 5: If the signatures match exactly, `n` can be reordered to this power of 2.
# STEP 6: If no matches are found after checking all 30 options, return False.

class Solution:
    def reorderedPowerOf2(self, n: int) -> bool:
        
        # Calculate the frequency signature of the input number
        # Example: n = 46 -> Counter({'4': 1, '6': 1})
        n_signature = Counter(str(n))
        
        # There are only 30 powers of 2 within the 10^9 limit (2^0 to 2^29)
        for i in range(30):
            
            # Generate the power of 2 using left bit shift (equivalent to 2**i)
            power_of_2 = 1 << i
            
            # Calculate the signature of the current power of 2
            power_signature = Counter(str(power_of_2))
            
            # If the frequency of all digits matches, they are anagrams
            if n_signature == power_signature:
                return True
                
        return False

"""
WHY EACH PART:
- Counter(str(n)): This standard library tool creates a dictionary-like object that counts how many times each character appears. It handles the "reordering" logic perfectly because dictionaries are unordered by nature.
- 1 << i: Bitwise left shift is the fastest computational way to calculate 2^i. (e.g., 1 << 3 is 1000 in binary, which is 8).
- range(30): Bounds our search space strictly to the constraints. 10^9 is just under 2^30 (1,073,741,824). Thus, checking beyond 2^29 is mathematically unnecessary.

HOW IT WORKS (Example: n = 46):
Initial:
├── n_signature = Counter({'4': 1, '6': 1})

Iteration 0-5:
├── power_of_2 = 1, 2, 4, 8, 16, 32
└── None of their signatures match n_signature.

Iteration 6:
├── power_of_2 = 1 << 6 = 64
├── power_signature = Counter({'6': 1, '4': 1})
├── n_signature == power_signature evaluates to True! (Order in Counter doesn't matter)
└── Returns True. ✓

KEY TECHNIQUE:
- State Space Reduction: Turning a massive permutation problem (3.6 million states) into a predefined lookup table problem (30 states).
- Hashing / Frequency Maps: Using `Counter` to prove that two sequences are permutations of each other in O(K) time, where K is the number of digits.

EDGE CASES:
- Leading zeros: Inherently handled. Because standard powers of 2 (like 64) do not have leading zeros, if `n` requires a leading zero to form the anagram, the power of 2 signature simply wouldn't match it correctly in length or digit count.

TIME COMPLEXITY: O(log^2 N). The outer loop runs exactly 30 times (constant O(1)). Inside the loop, `str()` and `Counter()` process the digits of 2^i. The number of digits in `N` is log10(N). Therefore, the time is strictly bounded and executes almost instantaneously.
SPACE COMPLEXITY: O(log N) to store the string representations and Counter dictionaries of the digits, which at most is 10 characters long. Effectively O(1) auxiliary space.

CONCEPTS USED:
- Reverse Thinking
- Hashing / Digit Frequency Counting
- Bitwise Operations
"""
