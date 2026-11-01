# 2348. Number of Zero-Filled Subarrays
# Difficulty: Medium
# https://leetcode.com/problems/number-of-zero-filled-subarrays/

"""
PROBLEM:
Given an integer array nums, return the number of subarrays filled with 0.
A subarray is a contiguous non-empty sequence of elements within an array.

EXAMPLES:
Input: nums = [1,3,0,0,2,0,0,4] → Output: 6
Explanation: 
There are 4 occurrences of [0] as a subarray.
There are 2 occurrences of [0,0] as a subarray.
There is no occurrence of a subarray with a size more than 2 filled with 0. Therefore, we return 6.

Input: nums = [0,0,0,2,0,0] → Output: 9
Explanation:
There are 5 occurrences of [0] as a subarray.
There are 3 occurrences of [0,0] as a subarray.
There is 1 occurrence of [0,0,0] as a subarray.
Total = 5 + 3 + 1 = 9.

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

MATH RULES (TRIANGULAR NUMBERS & ITERATIVE ACCUMULATION):
A contiguous block of K zeros produces exactly K * (K + 1) / 2 subarrays.
Instead of tracking block boundaries to apply the formula at the end, we can exploit the iterative nature of the series: 1 + 2 + 3 + ... + K.
Every time we encounter a '0', the current streak of zeros increases by 1. The number of NEW subarrays created strictly by adding this specific zero to the contiguous block is exactly equal to the new streak length.
Thus, simply adding the streak length to a global total dynamically at each '0' perfectly calculates the Gaussian sum in a single O(N) pass without requiring division or nested loops.
"""

from typing import List

# STEP 1: Initialize variables to track the global total and the current contiguous zero streak.
# STEP 2: Iterate through each element in the array.
# STEP 3: If the element is 0, increment the streak and dynamically add it to the total.
# STEP 4: If the element is non-zero, reset the streak to 0.
# STEP 5: Return the accumulated total.

class Solution:
    def zeroFilledSubarray(self, nums: List[int]) -> int:
        
        total_subarrays = 0
        current_zeros = 0
        
        for num in nums:
            if num == 0:
                # The streak continues, creating 'current_zeros' new valid subarrays
                current_zeros += 1
                total_subarrays += current_zeros
            else:
                # The streak is broken, reset the counter
                current_zeros = 0
                
        return total_subarrays

"""
WHY EACH PART:
- current_zeros += 1 -> total_subarrays += current_zeros: Represents the mathematical truth that the N-th zero in a sequence forms exactly N new sub-arrays ending at that specific index.
- current_zeros = 0: Acts as an O(1) state reset. The global `total_subarrays` safely retains all previously calculated blocks.

KEY TECHNIQUE:
- Dynamic State Accumulation: Converting a block-level mathematical formula (Gauss sum) into a streaming step-by-step addition to achieve optimal O(N) time and O(1) space.

EDGE CASES:
- Array with NO zeros (e.g., [1, 2, 3]): The `if num == 0` block never triggers. Returns 0 seamlessly.
- Array with ALL zeros (e.g., [0, 0, 0]): The counter increments uninterrupted. Total resolves to 1 + 2 + 3 = 6 perfectly.

TIME COMPLEXITY: O(N) - We traverse the array exactly once, performing simple O(1) arithmetic operations per element.
SPACE COMPLEXITY: O(1) - Only two scalar integer variables are allocated in memory.
"""
