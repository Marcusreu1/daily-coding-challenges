# 2364. Count Number of Bad Pairs
# Difficulty: Medium
# https://leetcode.com/problems/count-number-of-bad-pairs/

"""
PROBLEM:
You are given a 0-indexed integer array nums. A pair of indices (i, j) is a bad pair if i < j and j - i != nums[j] - nums[i].
Return the total number of bad pairs in nums.

EXAMPLES:
Input: nums = [4,1,3,3] → Output: 5
Explanation: The pair (0, 1) is a bad pair since 1 - 0 != 1 - 4 (1 != -3).
The pair (0, 2) is a bad pair since 2 - 0 != 3 - 4 (2 != -1).
The pair (0, 3) is a bad pair since 3 - 0 != 3 - 4 (3 != -1).
The pair (1, 2) is a bad pair since 2 - 1 != 3 - 1 (1 != 2).
The pair (2, 3) is a bad pair since 3 - 2 != 3 - 3 (1 != 0).
There are a total of 5 bad pairs.

Input: nums = [1,2,3,4,5] → Output: 0
Explanation: There are no bad pairs, as every pair satisfies j - i == nums[j] - nums[i].

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9

MATH RULES (ALGEBRAIC REARRANGEMENT & INVERSE COMBINATORICS):
1. Algebraic Grouping: The condition for a GOOD pair is (j - i == nums[j] - nums[i]). 
   By rearranging the terms to isolate the variables of the same index on each side, we get:
   nums[i] - i == nums[j] - j.
   This mathematically transforms a relational problem (comparing i to j) into a state-matching problem. We map each element to `nums[k] - k`. Any two identical mapped values constitute a good pair.
2. Combinatorial Subtraction: The maximum number of valid pairs in any array of size N is N * (N - 1) / 2.
   Therefore: Bad Pairs = Total Pairs - Good Pairs.
   We can calculate the number of Good Pairs in a single O(N) pass using a Hash Map to track the frequencies of the transformed values.
"""

from typing import List

# STEP 1: Calculate the mathematical maximum number of total pairs possible in the array.
# STEP 2: Initialize a hash map to track frequencies of (nums[i] - i) and an accumulator for good pairs.
# STEP 3: Iterate through the array, calculating the transformed value for each element.
# STEP 4: Add the number of previously seen identical values to the good pairs tally.
# STEP 5: Increment the frequency of the current transformed value in the map.
# STEP 6: Return the mathematically deduced bad pairs (Total - Good).

class Solution:
    def countBadPairs(self, nums: List[int]) -> int:
        
        n = len(nums)
        # Total combinations of pairs in a set of size N is N * (N - 1) / 2
        total_pairs = n * (n - 1) // 2
        
        good_pairs = 0
        diff_counts = {}
        
        # Traverse the array to count occurrences of (nums[i] - i)
        for i, num in enumerate(nums):
            # Algebraic transformation
            diff = num - i
            
            # Every previously seen matching 'diff' forms exactly one good pair with the current element
            if diff in diff_counts:
                good_pairs += diff_counts[diff]
                diff_counts[diff] += 1
            else:
                diff_counts[diff] = 1
                
        # Inverse logic deduction
        return total_pairs - good_pairs

"""
WHY EACH PART:
- n * (n - 1) // 2: Pure combinations formula (nCr where r=2). Calculates the absolute ceiling of possible interactions in O(1) time.
- diff = num - i: The mathematical key to the problem. Decouples the 2D requirement of checking j against i into a 1D state validation.
- good_pairs += diff_counts[diff]: If we have seen the state 'diff' 3 times before, the current element forms exactly 3 new good pairs. Accumulating on the fly prevents the need for a secondary loop.

KEY TECHNIQUE:
- Algebraic Simplification: Rearranging inequalities/equalities to group index variables.
- Inverse Problem Solving: It's often computationally cheaper to find what ISN'T matching the criteria and subtract it from the universal set.

EDGE CASES:
- Array is perfectly sequential (e.g., [1, 2, 3]): All differences are identical. good_pairs will equal total_pairs. Returns 0 seamlessly.
- Only 1 element in array: The constraints guarantee at least 1 element. If len is 1, total_pairs is 0. Loop runs, diff_counts updates, good_pairs is 0. Returns 0 - 0 = 0. Correct.

TIME COMPLEXITY: O(N) - We iterate through the array exactly once. Hash map lookups and inserts are O(1) on average. This perfectly bypasses the O(N^2) brute-force limitation.
SPACE COMPLEXITY: O(N) - In the worst-case scenario (where every single `num - i` is unique), the hash map will store N key-value pairs.
"""
