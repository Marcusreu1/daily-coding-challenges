# 908. Smallest Range I
# Difficulty: Easy
# https://leetcode.com/problems/smallest-range-i/

"""
PROBLEM:
You are given an integer array `nums` and an integer `k`.
In one operation, you can choose any index i and change nums[i] to nums[i] + x where -k <= x <= k.
You can apply this operation at most once for each index.
The score of nums is the difference between the maximum and minimum elements in nums.
Return the minimum score of nums after applying the mentioned operation at most once for each index.

EXAMPLES:
Input: nums = [1], k = 0           -> Output: 0 (Score is 1 - 1 = 0)
Input: nums = [0,10], k = 2        -> Output: 6 (Change to [2,8]. Score is 8 - 2 = 6)
Input: nums = [1,3,6], k = 3       -> Output: 0 (Change to [4,4,4]. Score is 4 - 4 = 0)

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^4
- 0 <= k <= 10^4

MATHEMATICAL REDUCTION:
To minimize the difference between the maximum and minimum values, we must:
1. Increase the minimum value as much as possible: new_min = min_val + k
2. Decrease the maximum value as much as possible: new_max = max_val - k

The new theoretical difference becomes:
new_max - new_min = (max_val - k) - (min_val + k) = max_val - min_val - 2k

If (max_val - min_val) <= 2k, the bounds can overlap, meaning we can make all elements in the array perfectly equal. The minimum possible difference is 0.

VISUALIZATION (nums = [0, 10], k = 2):
Original min = 0, Original max = 10
Difference = 10

Action:
Push min up by 2  -> 0 + 2 = 2
Push max down by 2 -> 10 - 2 = 8

New range calculation:
(10 - 0) - (2 * 2) = 10 - 4 = 6

Result: 6 ✓
"""

# STEP 1: Find the maximum value in the array
# STEP 2: Find the minimum value in the array
# STEP 3: Calculate the theoretical minimum range: (max - min) - 2 * k
# STEP 4: Return 0 if the range is negative, otherwise return the calculated range

class Solution:
    def smallestRangeI(self, nums: list[int], k: int) -> int:
        
        max_val = max(nums)                                                    # Find the largest number
        min_val = min(nums)                                                    # Find the smallest number
        
        minimum_score = (max_val - min_val) - (2 * k)                          # Calculate the shortened distance
        
        return max(0, minimum_score)                                           # Return 0 if negative, else the score

"""
WHY EACH PART:
- max(nums) and min(nums): We only care about the extremes. Elements in the middle can safely be adjusted to fit within these newly compressed bounds.
- - (2 * k): We subtract 2k because we are closing the gap from both sides simultaneously (k from the top, k from the bottom).
- max(0, minimum_score): Prevents returning a negative score. If the adjustment power (2k) is greater than the original gap, we just make all numbers identical (score = 0).

HOW IT WORKS (Example: [1,3,6], k=3):

Initial State:
├── max_val = 6
├── min_val = 1
├── k = 3

Math Logic:
├── distance = max_val - min_val = 6 - 1 = 5
├── reduction_power = 2 * 3 = 6
├── minimum_score = 5 - 6 = -1

Final Check:
└── return max(0, -1) = 0 ✓

KEY TECHNIQUE:
- Math/Greedy approach: Ignoring the entire array and focusing solely on the boundaries. By mathematically reducing the problem, we avoid simulating the adjustments for every element.

EDGE CASES:
- Array of length 1: max and min are the same. Difference is 0. max(0, 0 - 2k) returns 0. ✓
- All elements are the same: max and min are equal. Returns 0. ✓
- Large k values: Handled gracefully by the max(0, ...) wrapper. ✓

TIME COMPLEXITY: O(N) - We iterate through the array twice (internally via max() and min()), where N is the length of nums.
SPACE COMPLEXITY: O(1) - We only store a few integer variables, regardless of the input size.

CONCEPTS USED:
- Arrays
- Mathematics
- Greedy algorithms (Boundary focusing)
"""
