"""
628. Maximum Product of Three Numbers
Difficulty: Easy
https://leetcode.com/problems/maximum-product-of-three-numbers/

PROBLEM:
    Given an integer array nums, find three numbers whose product
    is maximum and return the maximum product.

EXAMPLES:
    Input: nums = [1,2,3]           → Output: 6
    Input: nums = [1,2,3,4]         → Output: 24
    Input: nums = [-1,-2,-3]        → Output: -6
    Input: nums = [-100,-99,1,2,3]  → Output: 29700

CONSTRAINTS:
    3 <= nums.length <= 10^4
    -1000 <= nums[i] <= 1000

KEY INSIGHT:
    The maximum product of 3 numbers comes from one of TWO cases:
        1. Three LARGEST numbers (last 3 in sorted array)
        2. Two most NEGATIVE × the LARGEST (first 2 × last in sorted)

    negative × negative = positive → can produce a huge product!

    Result = max(nums[-1]×nums[-2]×nums[-3], nums[0]×nums[1]×nums[-1])

CHALLENGES:
    Recognizing that two negatives can produce a larger product
    Not just blindly taking the 3 largest
    Handling all-negative arrays correctly

SOLUTION:
    Sort the array.
    Compare the two candidate products.
    Return the maximum.
"""


# STEP 1: Sort the array
# STEP 2: Compute candidate 1: three largest (last 3)
# STEP 3: Compute candidate 2: two smallest × largest (first 2 × last)
# STEP 4: Return the maximum of both candidates


class Solution:
    def maximumProduct(self, nums: List[int]) -> int:

        nums.sort()                                                   # Sort ascending

        candidate1 = nums[-1] * nums[-2] * nums[-3]                  # Three largest numbers
        candidate2 = nums[0] * nums[1] * nums[-1]                    # Two most negative × largest

        return max(candidate1, candidate2)                            # Best of both options


"""
WHY EACH PART:
    nums.sort():          Puts smallest (most negative) first, largest last
    nums[-1]*[-2]*[-3]:   Three largest → maximizes if all positive or mix
    nums[0]*[1]*[-1]:     Two most negative × largest → neg×neg=pos, could be huge
    max(c1, c2):          Only one of these two can be the answer — pick the bigger


HOW IT WORKS (Example: nums = [1, 2, 3, 4]):

    sorted = [1, 2, 3, 4]

    candidate1 = 4 × 3 × 2 = 24
    candidate2 = 1 × 2 × 4 = 8

    max(24, 8) = 24 


HOW IT WORKS (Example: nums = [-100, -99, 1, 2, 3]):

    sorted = [-100, -99, 1, 2, 3]

    candidate1 = 3 × 2 × 1 = 6
    candidate2 = (-100) × (-99) × 3 = 29700

    max(6, 29700) = 29700 

    Key: (-100) × (-99) = 9900 (positive!)
         9900 × 3 = 29700


HOW IT WORKS (Example: nums = [-5, -4, -3, -2, -1]):

    sorted = [-5, -4, -3, -2, -1]

    candidate1 = (-1) × (-2) × (-3) = -6
    candidate2 = (-5) × (-4) × (-1) = -20

    max(-6, -20) = -6 

    When all negative, we want the three CLOSEST to zero
    (least negative), which is candidate1.


HOW IT WORKS (Example: nums = [-5, -4, 0, 0, 3]):

    sorted = [-5, -4, 0, 0, 3]

    candidate1 = 3 × 0 × 0 = 0
    candidate2 = (-5) × (-4) × 3 = 60

    max(0, 60) = 60 


WHY ONLY TWO CANDIDATES:
    For product of 3 numbers to be maximized, consider ALL sign combos:

    (+)(+)(+) = (+) → want 3 largest positives → candidate1
    (-)(-)(-) = (-) → always negative, worst case
    (+)(+)(-) = (-) → always negative
    (-)(-)(+) = (+) → want 2 most negative × largest positive → candidate2

    Only two combos give positive results!

    And candidate1 handles the "all negative" case too
    (picks the three least negative = closest to zero).

    ┌─────────────────────────────────────────────────┐
    │  candidate1 = best "three big positives" combo  │
    │  candidate2 = best "two negatives × positive"   │
    │                                                 │
    │  Every other combo loses to one of these two.   │
    └─────────────────────────────────────────────────┘


WHY NOT nums[0] × nums[1] × nums[2] (three smallest)?
    Three most negative numbers:
        (-100) × (-99) × (-98) = -970200 (NEGATIVE)

    This can NEVER be the maximum product (unless we must
    pick negatives, and candidate1 already handles that
    by picking the three closest to zero).


WHY NOT nums[0] × nums[-2] × nums[-1] (one negative × two largest)?
    (-100) × 3 × 4 = -1200 (NEGATIVE)

    One negative always makes the product negative.
    Never optimal. 


ALTERNATIVE: O(n) SINGLE-PASS APPROACH:
    Instead of sorting, find the 5 key values in one pass:

    max1 >= max2 >= max3   (three largest)
    min1 <= min2           (two smallest)

    class Solution:
        def maximumProduct(self, nums):
            max1 = max2 = max3 = float('-inf')
            min1 = min2 = float('inf')

            for n in nums:
                if n >= max1:
                    max3, max2, max1 = max2, max1, n
                elif n >= max2:
                    max3, max2 = max2, n
                elif n >= max3:
                    max3 = n

                if n <= min1:
                    min2, min1 = min1, n
                elif n <= min2:
                    min2 = n

            return max(max1*max2*max3, min1*min2*max1)

    Time: O(n), Space: O(1)
    Same logic, no sorting needed!


HANDLING SPECIAL CASES:
    All positive:          candidate1 wins (3 largest) ✓
    All negative:          candidate1 wins (3 least negative) ✓
    Mix with negatives:    candidate2 may win ✓
    Contains zeros:        Handled naturally ✓
    Exactly 3 elements:    Both candidates use all 3 → same result ✓
    Two large negatives:   candidate2 captures this ✓


KEY TECHNIQUE:
    Sort and select:        Simple O(n log n) approach
    Two-candidate strategy: Only 2 combos can be optimal
    Negative × negative:    Recognizing this creates large positives
    Edge analysis:          Only extremes of sorted array matter


EDGE CASES:
    [1, 2, 3]:              6 (only option) ✓
    [-1, -2, -3]:           -6 (least negative product) ✓
    [-1000, -999, 1]:       999000 (neg × neg × pos) ✓
    [0, 0, 0]:              0 ✓
    [-1, 0, 1]:             0 (best possible) ✓
    [1000, 1000, 1000]:     10^9 ✓
    [-1000, -1000, 1000]:   10^9 ✓


TIME COMPLEXITY: O(n log n)
    Sorting dominates
    Two product calculations: O(1)
    (O(n) possible with single-pass approach)

SPACE COMPLEXITY: O(1)
    In-place sort (or constant extra variables for O(n) approach)
    Only two candidate variables


CONCEPTS USED:
    Sorting for extremes identification
    Sign analysis in multiplication
    Two-candidate optimization
    Negative number properties (neg × neg = pos)
    Greedy selection (only extremes matter)
"""
