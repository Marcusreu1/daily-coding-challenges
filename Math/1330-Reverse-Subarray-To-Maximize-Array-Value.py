# 1330. Reverse Subarray To Maximize Array Value
# Difficulty: Hard
# https://leetcode.com/problems/reverse-subarray-to-maximize-array-value/

"""
PROBLEM:
You are given an integer array `nums`. The value of this array is defined as the sum of 
|nums[i] - nums[i + 1]| for all 0 <= i < nums.length - 1.
You are allowed to select any subarray of the given array and reverse it. You can perform 
this operation only once.
Find maximum possible value of the final array.

EXAMPLES:
Input: nums = [2,3,1,5,4]
Output: 10
(Explanation: The starting value is |2-3| + |3-1| + |1-5| + |5-4| = 1 + 2 + 4 + 1 = 8.
By reversing the subarray [3,1,5], the array becomes [2,5,1,3,4].
The new value is |2-5| + |5-1| + |1-3| + |3-4| = 3 + 4 + 2 + 1 = 10.)

Input: nums = [2,4,9,24,2,1,10]
Output: 68

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -10^5 <= nums[i] <= 10^5

ALGORITHM LOGIC (Boundary Delta Optimization):
1. Reversing a subarray [L, R] does NOT change the internal distances. It only breaks two links 
   (at L-1 and R+1) and creates two new links.
2. The change in value (delta) for an internal reverse is:
   Delta = |nums[R] - nums[L-1]| + |nums[R+1] - nums[L]| - |nums[L] - nums[L-1]| - |nums[R+1] - nums[R]|
3. Mathematically, the maximum possible delta for two independent adjacent pairs (a, b) and (c, d) is:
   Max Delta = 2 * (min(c, d) - max(a, b))
4. To maximize this in O(N) time, we need to find the absolute maximum of min(c,d) across all pairs, 
   and the absolute minimum of max(a,b) across all pairs.
5. We also must check prefix reversals (L=0) and suffix reversals (R=n-1), as they only break one link.

VISUALIZATION (nums = [2, 3, 1, 5, 4]):
Base value: |2-3| + |3-1| + |1-5| + |5-4| = 8

Pairs:
(2,3) -> min=2, max=3
(3,1) -> min=1, max=3
(1,5) -> min=1, max=5
(5,4) -> min=4, max=5

Global max of mins (max_min) = max(2, 1, 1, 4) = 4
Global min of maxs (min_max) = min(3, 3, 5, 5) = 3
Max Internal Gain = max(0, 2 * (4 - 3)) = 2

Check Prefix/Suffix gains (e.g., reversing [0..3]):
Original link |5-4| becomes |2-4|. Gain: |2-4| - |5-4| = 2 - 1 = 1.
Max Boundary Gain = 1.

Final Answer = Base (8) + Max Gain (2) = 10. ✓
"""

import math

# STEP 1: Calculate the base value of the array and initialize tracking variables
# STEP 2: Iterate through the array to find the global max_min and min_max for internal pairs
# STEP 3: Simultaneously calculate potential gains for prefix and suffix reversals
# STEP 4: Calculate the max internal gain using the math formula: 2 * (max_min - min_max)
# STEP 5: Return the base value plus the highest gain found among internal, prefix, or suffix reversals

class Solution:
    def maxValueAfterReverse(self, nums: list[int]) -> int:
        
        n = len(nums)
        base_value = 0
        
        max_min = -math.inf                                          # To find the highest minimum of any pair
        min_max = math.inf                                           # To find the lowest maximum of any pair
        
        boundary_gain = 0                                            # To track max gain from prefix or suffix reversals
        
        for i in range(n - 1):
            
            a = nums[i]
            b = nums[i + 1]
            diff = abs(a - b)
            
            base_value += diff                                       # Accumulate original array value
            
            max_min = max(max_min, min(a, b))                        # Update global max of minimums
            min_max = min(min_max, max(a, b))                        # Update global min of maximums
            
            # Check Prefix reversal gain: Reversing from 0 to i
            prefix_gain = abs(nums[0] - b) - diff
            
            # Check Suffix reversal gain: Reversing from i+1 to n-1
            suffix_gain = abs(nums[-1] - a) - diff
            
            # Keep the highest boundary gain found
            boundary_gain = max(boundary_gain, prefix_gain, suffix_gain)
            
        # Calculate max internal gain using the disjoint intervals formula
        internal_gain = max(0, 2 * (max_min - min_max))
        
        # Return base + the absolute best gain possible
        return base_value + max(boundary_gain, internal_gain)

"""
WHY EACH PART:
- max_min = -math.inf and min_max = math.inf: Setting these to extreme opposites ensures that the very first pair evaluated will safely overwrite them and establish the baseline.
- base_value += diff: We need the original sum to add our final delta to it.
- prefix_gain = abs(nums[0] - b) - diff: If we reverse from index 0 to `i`, the new link is formed between the old start (nums[0]) and the element right after our reversed block (`b`). We subtract the broken link (`diff`) to get the net gain.
- max(0, 2 * (max_min - min_max)): If the intervals overlap, `max_min - min_max` will be negative. A negative gain means reversing makes the array worse, so we default to 0 (no gain).

HOW IT WORKS (Math trick breakdown):
If we have pair A (1, 5) and pair B (5, 9).
Pair A spans [1, 5]. Pair B spans [5, 9].
max_min = 5. min_max = 5. 
2 * (5 - 5) = 0 gain. (They touch, no empty space).

If we have pair A (1, 3) and pair B (7, 9).
Pair A spans [1, 3]. Pair B spans [7, 9].
max_min = 7. min_max = 3.
2 * (7 - 3) = 8 gain! 
Because reversing the block between them forces 1 to connect to 9 (distance 8) and 3 to connect to 7 (distance 4). Original distances were 2 and 2. Net gain is exactly 8.

KEY TECHNIQUE:
- Mathematical Abstraction: Breaking down the absolute value function into a geometric interval problem reduces an O(N^2) double-loop search into an elegant O(N) single-pass scan.

EDGE CASES:
- Already optimal array (e.g., [1, 2, 3, 4, 5]): Gains will be 0 or negative. Formula maxes out at 0, returns the base value. ✓
- Array of length 2: Internal loop processes 1 pair. Gains evaluate to 0. Works perfectly. ✓

TIME COMPLEXITY: O(N) - We iterate through the array of length N exactly one time. All max/min checks inside the loop are O(1).
SPACE COMPLEXITY: O(1) - We only store a few integer variables to track the base value, maximums, and minimums. No extra arrays or data structures are created.

CONCEPTS USED:
- Advanced Math / Geometry (Interval Overlaps)
- Absolute Value Manipulation
- Greedy Scanning
- Prefix and Suffix Evaluation
"""
