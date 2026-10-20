# 2221. Find Triangular Sum of an Array
# Difficulty: Medium
# https://leetcode.com/problems/find-triangular-sum-of-an-array/

"""
PROBLEM:
You are given a 0-indexed integer array nums, where nums[i] is a digit between 0 and 9 (inclusive).
The triangular sum of nums is the value of the only element present in nums after the following process terminates:
- Let nums comprise of n elements. If n == 1, end the process. Otherwise, create a new 0-indexed integer array newNums of length n - 1.
- For each index i where 0 <= i < n - 1, assign the value of newNums[i] as (nums[i] + nums[i + 1]) % 10.
- Replace the array nums with newNums.
- Repeat the entire process starting from the first step.
Return the triangular sum of nums.

EXAMPLES:
Input: nums = [1,2,3,4,5] → Output: 8
Explanation:
Row 0: [1, 2, 3, 4, 5]
Row 1: [3, 5, 7, 9]
Row 2: [8, 2, 6]
Row 3: [0, 8]
Row 4: [8]
The single remaining element is 8.

Input: nums = [5] → Output: 5
Explanation: Since there is only one element in nums, the triangular sum is 5.

CONSTRAINTS:
- 1 <= nums.length <= 1000
- 0 <= nums[i] <= 9

MATH RULES (PASCAL'S TRIANGLE & IN-PLACE REDUCTION):
1. Mathematical Relation:
   The expansion of adjacent sums mirrors Pascal's Triangle. The contribution of nums[i] to the un-modded final sum
   is defined by the binomial coefficient C(N - 1, i).
   Final Sum = Sum(C(N - 1, i) * nums[i]) % 10 for i from 0 to N - 1.

2. In-Place Simulation:
   With N <= 1000, N^2 / 2 is ~500,000 operations, which runs instantaneously.
   We can perform the reduction directly on the input array 'nums' without allocating new memory buffers, 
   reducing the auxiliary space complexity to strictly O(1).
"""

from typing import List

# STEP 1: Determine the total initial length N of the array.
# STEP 2: Outer loop reduces the active window size from N - 1 down to 1.
# STEP 3: Inner loop updates elements in-place: nums[i] = (nums[i] + nums[i + 1]) % 10.
# STEP 4: Return nums[0] after all reductions complete.

class Solution:
    def triangularSum(self, nums: List[int]) -> int:
        
        n = len(nums)
        
        # Outer loop controls the current right boundary of the active array
        for size in range(n - 1, 0, -1):
            
            # Inner loop updates adjacent pairs in-place
            for i in range(size):
                nums[i] = (nums[i] + nums[i + 1]) % 10
                
        # The single surviving value condenses at index 0
        return nums[0]

"""
WHY EACH PART:
- size in range(n - 1, 0, -1): Progressively shrinks the active array window by 1 in each pass.
- nums[i] = (nums[i] + nums[i + 1]) % 10: Overwrites index `i` safely because index `i + 1` is read before it is overwritten in the next iteration step.
- return nums[0]: Avoids secondary variable allocations by returning the condensed root directly.

KEY TECHNIQUE:
- In-Place Array Mutation: Reusing memory locations of contiguous computations to achieve O(1) space complexity.
- Pascal Reduction Simulation: Processing adjacent pairwise reductions sequentially.

EDGE CASES:
- Single element array (e.g. nums = [5]): Outer loop range(0, 0, -1) is empty. Instantly returns nums[0] = 5. Correct.
- Array with all zeros (e.g. [0, 0, 0]): Modular sums remain 0 throughout all levels. Returns 0 cleanly.

TIME COMPLEXITY: O(N^2) - Where N is the number of elements in `nums`. The total operations equal (N - 1) + (N - 2) + ... + 1 = N * (N - 1) / 2. For N = 1000, this is ~500,000 operations, running in a few milliseconds.
SPACE COMPLEXITY: O(1) - The reduction modifies the input array in-place, requiring no extra memory allocations.
"""
