# 1759. Count Number of Homogenous Substrings
# Difficulty: Medium
# https://leetcode.com/problems/count-number-of-homogenous-substrings/

"""
PROBLEM:
Given a string s, return the number of homogenous substrings of s. Since the answer may be too large, return it modulo 10^9 + 7.
A string is homogenous if all the characters of the string are the same.
A substring is a contiguous sequence of characters within a string.

EXAMPLES:
Input: s = "abbcccaa" → Output: 13
Explanation: The homogenous substrings are listed as below:
"a"   appears 3 times.
"aa"  appears 1 time.
"b"   appears 2 times.
"bb"  appears 1 time.
"c"   appears 3 times.
"cc"  appears 2 times.
"ccc" appears 1 time.
Total = 3 + 1 + 2 + 1 + 3 + 2 + 1 = 13.

Input: s = "xy" → Output: 2
Explanation: The homogenous substrings are "x" and "y".

Input: s = "zzzzz" → Output: 15

CONSTRAINTS:
- 1 <= s.length <= 10^5
- s consists of lowercase English letters.

MATH RULES (CONTINUOUS COUNTING):
If we have a block of identical consecutive characters of length L, the total number of homogenous substrings is the sum of integers from 1 to L (Gauss Summation).
Instead of calculating the full length L and applying L * (L + 1) / 2 at the end of each block, we can just maintain a 'streak' counter.
If the current character matches the previous one, we increment the streak. If it doesn't, we reset the streak to 1. 
In every step, we add the current streak to our total. This builds the sum (1 + 2 + 3 ... + L) dynamically.

VISUALIZATION (s = "abbc"):
Initial: total = 0, streak = 0, prev = ""

i=0, char='a': doesn't match prev. streak = 1. total = 0 + 1 = 1. prev = 'a'
i=1, char='b': doesn't match prev. streak = 1. total = 1 + 1 = 2. prev = 'b'
i=2, char='b': matches prev. streak = 2. total = 2 + 2 = 4. prev = 'b'
i=3, char='c': doesn't match prev. streak = 1. total = 4 + 1 = 5. prev = 'c'

Result: 5 ✓
"""

# STEP 1: Initialize the total sum, the current streak counter, and the modulo constant.
# STEP 2: Keep track of the previously seen character.
# STEP 3: Iterate through each character in the string.
# STEP 4: Increment the streak if it matches the previous character, otherwise reset it to 1.
# STEP 5: Add the current streak to the total sum.
# STEP 6: Return the total modulo 10^9 + 7.

class Solution:
    def countHomogenous(self, s: str) -> int:
        
        MOD = 10**9 + 7
        total_substrings = 0
        current_streak = 0
        prev_char = ""
        
        for char in s:
            
            # Check if the homogenous sequence continues
            if char == prev_char:
                current_streak += 1
            else:
                # Sequence broken, reset streak and update tracking character
                current_streak = 1
                prev_char = char
                
            # Add the current mathematical streak to the total
            total_substrings += current_streak
            
        # Return the final count with modulo applied
        return total_substrings % MOD

"""
WHY EACH PART:
- current_streak += 1: Keeps building the mathematical sequence (1, 2, 3...) as long as the letters are identical.
- current_streak = 1: Resets the sequence whenever a new letter appears.
- total_substrings += current_streak: By adding the streak at every single step, we perfectly replicate the (L * (L + 1)) // 2 formula without needing to look ahead or manage index bounds manually.
- % MOD: Prevents the return value from overflowing beyond the accepted constraints of competitive programming environments.

HOW IT WORKS (Example: s = "aaa"):

Initial: total = 0, streak = 0, prev = ""

Iteration 1 (char = 'a'):
├── char != prev -> streak = 1, prev = 'a'
└── total = 0 + 1 = 1

Iteration 2 (char = 'a'):
├── char == prev -> streak = 1 + 1 = 2
└── total = 1 + 2 = 3

Iteration 3 (char = 'a'):
├── char == prev -> streak = 2 + 1 = 3
└── total = 3 + 3 = 6

Exit: Loop finishes

return 6 % 1000000007 = 6 ✓

KEY TECHNIQUE:
- Dynamic Summation: Calculating the combinations of substrings on the fly by adding the expanding length of the sequence directly to the accumulator.
- Single Pass (O(N)): Avoiding nested loops by carrying state (prev_char and current_streak) forward.

EDGE CASES:
- String with all unique characters (e.g., "abcdef"): The streak resets to 1 on every step. Total equals the length of the string.
- String with all identical characters (e.g., "zzzzz"): The streak grows continuously up to N, perfectly replicating the Gauss sum.

TIME COMPLEXITY: O(n) - We iterate through the string exactly once. Checking and adding takes O(1) time.
SPACE COMPLEXITY: O(1) - We only store a few variables (streak, total, prev_char), requiring constant extra space regardless of string length.

CONCEPTS USED:
- String Traversal
- Mathematical Summation (Combinatorics)
- Modulo Arithmetic
- State Tracking
"""
