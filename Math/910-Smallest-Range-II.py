# 910. Smallest Range II
# Difficulty: Medium
# https://leetcode.com/problems/smallest-range-ii/

"""
PROBLEM:
You are given an integer array `nums` and an integer `k`.
For each index i where 0 <= i < nums.length, change nums[i] to be either nums[i] + k or nums[i] - k.
The score of nums is the difference between the maximum and minimum elements in nums.
Return the minimum score of nums after changing the values at each index.

EXAMPLES:
Input: nums = [1], k = 0           -> Output: 0 (Score is 1 - 1 = 0)
Input: nums = [0,10], k = 2        -> Output: 6 (Change to [2, 8]. Score is 8 - 2 = 6)
Input: nums = [1,3,6], k = 3       -> Output: 3 (Change to [4, 6, 3]. Score is 6 - 3 = 3)

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^4
- 0 <= k <= 10^4

MATHEMATICAL REDUCTION:
If we sort the array, the optimal strategy to minimize the range is to increase the smaller numbers (left side) and decrease the larger numbers (right side).
Imagine a split point `i`. For all elements from 0 to i, we add k. For all elements from i+1 to the end, we subtract k.
After splitting at index `i`:
- The new maximum will be either the elevated end of the left part (nums[i] + k) or the lowered end of the right part (nums[-1] - k).
- The new minimum will be either the elevated start of the left part (nums[0] + k) or the lowered start of the right part (nums[i+1] - k).
We iterate through all possible split points and track the minimum possible difference.

VISUALIZATION (nums = [1, 3, 6], k = 3):
Sorted nums: [1, 3, 6]
Initial worst-case score: 6 - 1 = 5 (If we add 3 to all or subtract 3 from all)

Split at index 0 (Left: [1], Right: [3, 6]):
Add 3 to Left: [4]
Sub 3 to Right: [0, 3]
- new_max = max(1+3, 6-3) = max(4, 3) = 4
- new_min = min(1+3, 3-3) = min(4, 0) = 0
- Difference = 4 - 0 = 4 (Min score so far: 4)

Split at index 1 (Left: [1, 3], Right: [6]):
Add 3 to Left: [4, 6]
Sub 3 to Right: [3]
- new_max = max(3+3, 6-3) = max(6, 3) = 6
- new_min = min(1+3, 6-3) = min(4, 3) = 3
- Difference = 6 - 3 = 3 (Min score so far: 3)

Result: 3 ✓
"""

# STEP 1: Sort the array so we can cleanly divide small numbers from large numbers
# STEP 2: Initialize the result with the initial difference (case where all go up or all go down)
# STEP 3: Iterate through every possible split point (from 0 to n-2)
# STEP 4: Calculate the potential new maximum and new minimum for the current split
# STEP 5: Update the result with the smallest difference found

class Solution:
    def smallestRangeII(self, nums: list[int], k: int) -> int:
        
        nums.sort()                                                            # Sort array in ascending order
        
        n = len(nums)
        min_score = nums[-1] - nums[0]                                         # Baseline score (no relative change)
        
        for i in range(n - 1):                                                 # Try splitting between i and i+1
            
            # The new max is either the highest elevated number, or the highest lowered number
            highest_elevated = nums[i] + k
            highest_lowered = nums[-1] - k
            new_max = max(highest_elevated, highest_lowered)
            
            # The new min is either the lowest elevated number, or the lowest lowered number
            lowest_elevated = nums[0] + k
            lowest_lowered = nums[i+1] - k
            new_min = min(lowest_elevated, lowest_lowered)
            
            # Update the minimum score found
            min_score = min(min_score, new_max - new_min)
            
        return min_score                                                       # Return the absolute minimum range

"""
WHY EACH PART:
- nums.sort(): Crucial step. It allows us to safely assume that splitting the array logically separates "smaller" from "larger" values.
- min_score = nums[-1] - nums[0]: Our fallback. If k is so small (or so large) that changing directions makes things worse, keeping everyone moving in the same direction maintains the original range.
- range(n - 1): We stop at n-2 because our split requires at least one element on the right side (i+1).
- max(highest_elevated, highest_lowered) / min(...): Instead of scanning the whole modified array in O(N) time per split, we use O(1) math to find the extremes by looking only at the boundaries of the split.

HOW IT WORKS (Example: [0, 10], k = 2):

Initial State:
├── nums = [0, 10] (already sorted)
├── min_score = 10 - 0 = 10

Iteration 1 (i = 0):
├── Split point between 0 and 10
├── new_max = max(0 + 2, 10 - 2) = max(2, 8) = 8
├── new_min = min(0 + 2, 10 - 2) = min(2, 8) = 2
├── current_diff = 8 - 2 = 6
└── min_score = min(10, 6) = 6

Exit loop.
return 6 ✓

KEY TECHNIQUE:
- Array Sorting + Linear Scan (Pivot). By sorting the array, we reduce the problem to finding a single pivot point where all elements to the left increase, and all elements to the right decrease. Finding the max and min of the new array takes O(1) time per pivot.

EDGE CASES:
- Array of length 1: Loop doesn't execute. Returns nums[0] - nums[0] = 0. ✓
- k is very large: The crossing of boundaries will make the split diff large, so it falls back to the initial difference. ✓
- All elements are the same: Baseline is 0, any split yields an equal or greater diff, returns 0. ✓

TIME COMPLEXITY: O(N log N) - Sorting the array takes O(N log N) time. The single pass through the array takes O(N) time. Overall time is dominated by sorting.
SPACE COMPLEXITY: O(1) or O(N) - Depending on the sorting algorithm used by Python (Timsort takes O(N) space in the worst case).
CONCEPTS USED:
- Arrays
- Sorting
- Greedy algorithms (Pivot splitting)
"""
