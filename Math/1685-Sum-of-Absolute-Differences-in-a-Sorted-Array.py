# 1685. Sum of Absolute Differences in a Sorted Array
# Difficulty: Medium
# https://leetcode.com/problems/sum-of-absolute-differences-in-a-sorted-array/

"""
PROBLEM:
You are given an integer array nums sorted in non-decreasing order.
Build and return an integer array result with the same length as nums such that result[i] is equal to the sum of absolute differences between nums[i] and all the other elements in the array.

EXAMPLES:
Input: nums = [2,3,5] → Output: [4,3,5]
Explanation:
For nums[0]=2: |2-2| + |2-3| + |2-5| = 0 + 1 + 3 = 4.
For nums[1]=3: |3-2| + |3-3| + |3-5| = 1 + 0 + 2 = 3.
For nums[2]=5: |5-2| + |5-3| + |5-5| = 3 + 2 + 0 = 5.

CONSTRAINTS:
- 2 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^4
- nums is sorted in non-decreasing order.

MATH RULES (PREFIX SUM & ABSOLUTE DIFFERENCES):
Because the array is sorted, for any element at index 'i':
1. All elements to its left are <= nums[i].
   Absolute diff formula for left elements: (nums[i] * left_count) - left_sum
2. All elements to its right are >= nums[i].
   Absolute diff formula for right elements: right_sum - (nums[i] * right_count)

VISUALIZATION (nums = [2, 3, 5]):
Total sum = 10
Initial left_sum = 0

i = 0, num = 2:
  left_count = 0, right_count = 2
  right_sum = 10 - 0 - 2 = 8
  left_total = (2 * 0) - 0 = 0
  right_total = 8 - (2 * 2) = 4
  result[0] = 0 + 4 = 4
  left_sum updates to: 0 + 2 = 2

i = 1, num = 3:
  left_count = 1, right_count = 1
  right_sum = 10 - 2 - 3 = 5
  left_total = (3 * 1) - 2 = 1
  right_total = 5 - (3 * 1) = 2
  result[1] = 1 + 2 = 3
  left_sum updates to: 2 + 3 = 5

Result: [4, 3, 5] ✓
"""

from typing import List

# STEP 1: Calculate the total sum of the array and initialize left_sum to 0.
# STEP 2: Iterate through the array using index and value.
# STEP 3: Dynamically calculate the right_sum.
# STEP 4: Apply the mathematical grouping formulas for left and right elements.
# STEP 5: Append the calculated sum to the result list and update left_sum.

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        
        n = len(nums)                                                        # Total number of elements
        total_sum = sum(nums)                                                # O(n) precalculation of the total sum
        
        left_sum = 0                                                         # Running sum of elements to the left
        result = []                                                          # Array to store the final answers
        
        for i in range(n):                                                   # Iterate through the array
            
            # Calculate elements to the right dynamically in O(1)
            right_sum = total_sum - left_sum - nums[i]
            
            # Counts of elements on both sides
            left_count = i
            right_count = n - 1 - i
            
            # Apply mathematical simplification for sorted arrays
            left_total = (nums[i] * left_count) - left_sum
            right_total = right_sum - (nums[i] * right_count)
            
            # Combine both parts and add to the result
            result.append(left_total + right_total)
            
            # Update left_sum for the next iteration
            left_sum += nums[i]
            
        return result

"""
WHY EACH PART:
- sum(nums): Precomputing the sum prevents recalculating right-side sums from scratch, reducing time complexity.
- right_sum = total_sum - left_sum - nums[i]: We can deduce the sum of the right side instantly using variables we already track.
- left_count = i: The index exactly represents how many items are to the left.
- right_count = n - 1 - i: Total elements minus the ones on the left minus the current element itself.
- (nums[i] * left_count) - left_sum: Groups the differences. Since nums[i] is greater than all left elements, we can multiply it by the count and subtract the sum of those elements.

KEY TECHNIQUE:
- Prefix Sums & Math simplification: Bypassing the O(n^2) nested loop limitation by leveraging the sorted nature of the array to compute absolute differences mathematically in O(1) per element.

EDGE CASES:
- Elements with the same value (e.g., [2, 2, 2]): The formulas still hold perfectly, as the difference will naturally resolve to 0.
- Massive arrays (length 10^5): O(n) complexity guarantees it will run well within the time limit.

TIME COMPLEXITY: O(n) - One pass to get the total sum, and one pass to calculate the differences.
SPACE COMPLEXITY: O(n) - Used for the output array (or O(1) auxiliary space if we exclude the returned array).

CONCEPTS USED:
- Prefix Sums
- Array traversal
- Mathematical Combinations (Grouping properties)
"""
