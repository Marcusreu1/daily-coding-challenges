# 1071. Greatest Common Divisor of Strings
# Difficulty: Easy
# https://leetcode.com/problems/greatest-common-divisor-of-strings/

"""
PROBLEM:
For two strings s and t, we say "t divides s" if and only if s = t + t + ... + t 
(i.e., t is concatenated with itself one or more times).
Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.

EXAMPLES:
Input: str1 = "ABCABC", str2 = "ABC"   → Output: "ABC"
Input: str1 = "ABABAB", str2 = "ABAB"  → Output: "AB"
Input: str1 = "LEET", str2 = "CODE"    → Output: ""

CONSTRAINTS:
- 1 <= str1.length, str2.length <= 1000
- str1 and str2 consist of English uppercase letters.

MATHEMATICAL INTUITION (THE "TRICK"):
This problem is built on two core mathematical properties:
1. The Commutative Property of Divisible Strings:
   If str1 and str2 share ANY common divisor string, then concatenating them in either 
   order MUST yield the exact same result (str1 + str2 == str2 + str1).
   If this is false, they share no common building block. Return "".
2. The Greatest Common Divisor (GCD) of Lengths:
   If we know a common divisor string exists (from step 1), the length of the LARGEST 
   common divisor string is exactly the mathematical GCD of the lengths of str1 and str2.
"""

# STEP 1: Import the math module to use the built-in gcd function.
# STEP 2: Check if str1 + str2 equals str2 + str1. If not, return "".
# STEP 3: Find the GCD of the lengths of str1 and str2.
# STEP 4: Return the prefix of str1 up to the GCD length.

import math

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        
        # Step 1: Check if they share a common repeating pattern
        if str1 + str2 != str2 + str1:
            return ""
            
        # Step 2: Calculate the GCD of their lengths
        max_length = math.gcd(len(str1), len(str2))
        
        # Step 3: Return the substring of str1 from 0 to max_length
        return str1[:max_length]

"""
WHY EACH PART:
- str1 + str2 != str2 + str1: Acts as a definitive filter. It proves whether or not the two strings are constructed from the exact same repeating base block.
- math.gcd(len(str1), len(str2)): Finds the maximum possible length of the repeating block.
- str1[:max_length]: Since the strings are made of repeating blocks, the base block must be the prefix of the string.

HOW IT WORKS (Example: str1="ABABAB", str2="ABAB"):

Initial: str1 = "ABABAB" (len 6), str2 = "ABAB" (len 4)

Condition Check:
├── str1 + str2 = "ABABABABAB"
├── str2 + str1 = "ABABABABAB"
└── They are equal! Proceed.

Math GCD:
├── len(str1) = 6
├── len(str2) = 4
└── math.gcd(6, 4) = 2

Result Extraction:
├── max_length = 2
└── str1[:2] = "AB"
return "AB" ✓

KEY TECHNIQUE:
- String Concatenation Equality: A brilliant shortcut to verify identical repeating patterns without loops.
- Euclidean Algorithm (GCD): Applying pure number theory to string manipulation.

EDGE CASES:
- No common divisor ("LEET", "CODE"): Returns "" (LEETCODE != CODELEET) ✓
- Identical strings ("ABC", "ABC"): Returns "ABC" (GCD of 3 and 3 is 3) ✓
- One string is multiple of the other ("A", "AAAAA"): Returns "A" ✓
- Share letters but different patterns ("AB", "BA"): Returns "" (ABBA != BAAB) ✓

TIME COMPLEXITY: O(N + M) - Where N and M are the lengths of str1 and str2. The concatenation and comparison take O(N + M) time. The math.gcd runs in O(log(min(N, M))) which is negligible in comparison.
SPACE COMPLEXITY: O(N + M) - To store the concatenated strings in memory during the comparison.

CONCEPTS USED:
- Number Theory (Euclidean Algorithm / GCD)
- String Manipulation
- Mathematical Proof in Code
"""
