"""
462. Minimum Moves to Equal Array Elements II
Difficulty: Medium
https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/

PROBLEM:
Given an integer array nums of size n, return the minimum number of
moves required to make all array elements equal. In one move, you
can increment or decrement an element by 1.

EXAMPLES:
Input: nums = [1,2,3]      → Output: 2
    Target = 2 (median): |1-2| + |2-2| + |3-2| = 1+0+1 = 2

Input: nums = [1,10,2,9]   → Output: 16
    Sorted: [1,2,9,10] → pairs: (1,10)=9, (2,9)=7 → 9+7 = 16

CONSTRAINTS:
    n == nums.length
    1 <= n <= 10^5
    -10^9 <= nums[i] <= 10^9

KEY INSIGHT:
The optimal target is the MEDIAN of the array. The median minimizes
the sum of absolute deviations. Equivalently, we can pair the smallest
with the largest, second smallest with second largest, etc., and sum
the differences.

CHALLENGES:
    Proving median is optimal (not mean or mode)
    Understanding why pairing extremes works
    Handling even vs odd length arrays

WHY MEDIAN IS OPTIMAL:
    At the median, there are equal elements on each side.
    Moving target left → closer to left half BUT farther from right half.
    With equal counts on each side, any move away from median
    loses at least as much as it gains → median is optimal.

PAIRING TRICK:
    For sorted array, pair (nums[0], nums[n-1]), (nums[1], nums[n-2])...
    Each pair contributes AT LEAST nums[right] - nums[left] moves.
    The median as target achieves this lower bound for ALL pairs.

SOLUTION:
    1. Sort the array
    2. Use two pointers: pair smallest with largest
    3. Sum the differences of each pair
"""

# STEP 1: Sort the array
# STEP 2: Pair extremes with two pointers
# STEP 3: Sum the differences

class Solution:
    def minMoves2(self, nums: List[int]) -> int:

        nums.sort()                                                      # Sort to pair extremes

        left = 0                                                         # Pointer to smallest
        right = len(nums) - 1                                            # Pointer to largest
        moves = 0                                                        # Total moves counter

        while left < right:                                              # Until pointers meet
            moves += nums[right] - nums[left]                            # Difference of this pair
            left += 1                                                    # Move inward
            right -= 1                                                   # Move inward

        return moves

"""
WHY EACH PART:

    nums.sort(): Need sorted order to pair smallest with largest
    left = 0, right = n-1: Two pointers starting from extremes
    moves = 0: Accumulate total moves
    while left < right: Process pairs until pointers meet (or cross)
    nums[right] - nums[left]: Minimum moves for this pair
    left += 1, right -= 1: Move to next inner pair

HOW IT WORKS (Example: nums = [1, 2, 3]):

    Sorted: [1, 2, 3]

    Iteration 1: left=0, right=2
    ├── nums[2] - nums[0] = 3 - 1 = 2
    ├── moves = 2
    └── left=1, right=1

    left == right → STOP (middle element pairs with itself = 0)

    Result: 2 ✓

HOW IT WORKS (Example: nums = [1, 10, 2, 9]):

    Sorted: [1, 2, 9, 10]

    Iteration 1: left=0, right=3
    ├── nums[3] - nums[0] = 10 - 1 = 9
    ├── moves = 9
    └── left=1, right=2

    Iteration 2: left=1, right=2
    ├── nums[2] - nums[1] = 9 - 2 = 7
    ├── moves = 9 + 7 = 16
    └── left=2, right=1

    left > right → STOP

    Result: 16 ✓

WHY PAIRING EXTREMES WORKS:

    Sorted: [1, 2, 9, 10],  any target t between 2 and 9:

    Pair (1, 10):
    ├── |1-t| + |10-t| = (t-1) + (10-t) = 9
    └── Always 9, regardless of t (as long as 1 ≤ t ≤ 10) ✓

    Pair (2, 9):
    ├── |2-t| + |9-t| = (t-2) + (9-t) = 7
    └── Always 7, regardless of t (as long as 2 ≤ t ≤ 9) ✓

    Total: 9 + 7 = 16 (constant for any t in [2, 9])

    The MEDIAN is always between all pairs, so it achieves
    the minimum for every pair simultaneously ✓

WHY NOT THE MEAN (average):

    nums = [1, 0, 0, 8, 6]

    Mean = 3.0:  |1-3|+|0-3|+|0-3|+|8-3|+|6-3| = 2+3+3+5+3 = 16
    Median = 1:  |1-1|+|0-1|+|0-1|+|8-1|+|6-1| = 0+1+1+7+5 = 14 ✓

    The mean minimizes sum of SQUARED differences.
    The median minimizes sum of ABSOLUTE differences.
    This problem asks for absolute → MEDIAN wins.

COMPARISON WITH PROBLEM 453:

    Problem 453 (increment n-1 = decrement 1):
    ├── Can only go DOWN (effectively)
    ├── Optimal target = MINIMUM
    └── Formula: sum - n × min

    Problem 462 (increment/decrement 1):
    ├── Can go UP or DOWN
    ├── Optimal target = MEDIAN
    └── Formula: Σ|nums[i] - median| = sum of pair differences

ALTERNATIVE: EXPLICIT MEDIAN APPROACH:

    def minMoves2(self, nums):
        nums.sort()
        median = nums[len(nums) // 2]
        return sum(abs(num - median) for num in nums)

    Works correctly but the pairing approach is more elegant
    and doesn't need to handle even/odd length separately.

WHY ODD/EVEN LENGTH DOESN'T MATTER:

    Odd [1, 2, 9]:
    ├── Pair (1, 9) = 8
    ├── Middle element 2 pairs with itself = 0
    └── Total: 8 ✓ (left meets right, loop stops)

    Even [1, 2, 9, 10]:
    ├── Pair (1, 10) = 9
    ├── Pair (2, 9) = 7
    └── Total: 16 ✓ (left crosses right, loop stops)

    Both handled naturally by the two-pointer approach ✓

EDGE CASES:

    Single element [5]: No pairs → 0 moves ✓
    Two elements [1,10]: One pair → 10-1 = 9 ✓
    Already equal [3,3,3]: All pairs = 0 → 0 ✓
    Negative numbers [-5,0,5]: Pair (-5,5)=10 → 10 ✓
    All negatives [-10,-3,-1]: Pair (-10,-1)=9 → 9 ✓
    Large values (10^9): Differences fit in integer → works ✓
    Even length: Two medians both optimal ✓
    Odd length: Unique median → optimal ✓

TIME COMPLEXITY: O(n log n)
    O(n log n) for sorting
    O(n) for the two-pointer pass
    Dominated by sorting

SPACE COMPLEXITY: O(1)
    Sorting in-place (or O(n) depending on sort implementation)
    Only a few variables: left, right, moves

CONCEPTS USED:
    Median minimizes sum of absolute deviations
    Two-pointer technique on sorted array
    Pairing extremes (smallest with largest)
    Mathematical proof via triangle inequality
    Comparison: mean (squares) vs median (absolutes)
"""
