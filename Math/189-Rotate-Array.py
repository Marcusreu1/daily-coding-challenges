# 189. Rotate Array
# Difficulty: Medium
# https://leetcode.com/problems/rotate-array/

"""
PROBLEM:
Given an integer array nums, rotate the array to the right by k steps,
where k is non-negative.

EXAMPLES:
Input: nums = [1,2,3,4,5,6,7], k = 3 → Output: [5,6,7,1,2,3,4]
Input: nums = [-1,-100,3,99], k = 2  → Output: [3,99,-1,-100]

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -2^31 <= nums[i] <= 2^31 - 1
- 0 <= k <= 10^5

KEY INSIGHT:
Rotating right by k = moving last k elements to the front.
[A | B] → [B | A] can be achieved with THREE REVERSALS:
1. Reverse entire array: [rev(B) | rev(A)]
2. Reverse first k: [B | rev(A)]
3. Reverse last n-k: [B | A]

CHALLENGES:
1. In-place modification (O(1) space required)
2. Handle k >= n (use k % n)

SOLUTION:
Triple reversal technique - elegant O(n) time, O(1) space solution.
"""

# STEP 1: Handle k >= n by taking modulo
# STEP 2: Reverse entire array
# STEP 3: Reverse first k elements
# STEP 4: Reverse remaining n-k elements

from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        
        n = len(nums)
        k = k % n                                                                # Handle k >= n
        
        if k == 0:                                                               # No rotation needed
            return
        
        def reverse(left: int, right: int) -> None:                              # Helper to reverse subarray
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]                # Swap elements
                left += 1
                right -= 1
        
        reverse(0, n - 1)                                                        # Step 1: Reverse all
        reverse(0, k - 1)                                                        # Step 2: Reverse first k
        reverse(k, n - 1)                                                        # Step 3: Reverse rest


"""
WHY EACH PART:
- n = len(nums): Store length for repeated use
- k = k % n: Rotating n times = no change, so reduce k
- k == 0 check: Early exit if no rotation needed
- reverse helper: Reusable function for in-place subarray reversal
- left < right: Continue until pointers meet/cross
- swap with tuple: Python's elegant way to swap without temp variable
- reverse(0, n-1): Reverse entire array
- reverse(0, k-1): Reverse first k elements (indices 0 to k-1)
- reverse(k, n-1): Reverse last n-k elements (indices k to n-1)

HOW IT WORKS (Example: nums = [1,2,3,4,5,6,7], k = 3):

SETUP:
├── n = 7
├── k = 3 % 7 = 3
└── k != 0, proceed

┌─ reverse(0, 6) - Reverse ALL ─────────────────────────────┐
│  [1, 2, 3, 4, 5, 6, 7]                                    │
│   L                 R    swap → [7, 2, 3, 4, 5, 6, 1]     │
│      L           R       swap → [7, 6, 3, 4, 5, 2, 1]     │
│         L     R          swap → [7, 6, 5, 4, 3, 2, 1]     │
│            LR            L >= R, stop                     │
│                                                           │
│  Result: [7, 6, 5, 4, 3, 2, 1]                            │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ reverse(0, 2) - Reverse first k=3 ───────────────────────┐
│  [7, 6, 5, 4, 3, 2, 1]                                    │
│   L     R                swap → [5, 6, 7, 4, 3, 2, 1]     │
│      LR                  L >= R, stop                     │
│                                                           │
│  Result: [5, 6, 7, 4, 3, 2, 1]                            │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ reverse(3, 6) - Reverse last n-k=4 ──────────────────────┐
│  [5, 6, 7, 4, 3, 2, 1]                                    │
│            L        R    swap → [5, 6, 7, 1, 3, 2, 4]     │
│               L  R       swap → [5, 6, 7, 1, 2, 3, 4]     │
│                 LR       L >= R, stop                     │
│                                                           │
│  Result: [5, 6, 7, 1, 2, 3, 4] ✓                          │
└───────────────────────────────────────────────────────────┘

WHY TRIPLE REVERSAL WORKS:
┌────────────────────────────────────────────────────────────┐
│  Original: [A | B]  where A = [1,2,3,4], B = [5,6,7]       │
│  Goal:     [B | A]                                         │
│                                                            │
│  Step 1: reverse([A|B]) = [rev(B)|rev(A)]                  │
│          [1,2,3,4|5,6,7] → [7,6,5|4,3,2,1]                 │
│                                                            │
│  Step 2: reverse first k of [rev(B)|rev(A)]                │
│          [7,6,5|4,3,2,1] → [5,6,7|4,3,2,1]                 │
│          Now B is correct!                                 │
│                                                            │
│  Step 3: reverse last n-k                                  │
│          [5,6,7|4,3,2,1] → [5,6,7|1,2,3,4]                 │
│          Now A is correct!                                 │
│                                                            │
│  Final: [B | A] = [5,6,7,1,2,3,4] ✓                        │
└────────────────────────────────────────────────────────────┘

WHY k = k % n?
┌────────────────────────────────────────────────────────────┐
│  n = 4, original = [1, 2, 3, 4]                            │
│                                                            │
│  k = 4: rotate 4 = [1, 2, 3, 4] (back to original)         │
│  k = 5: rotate 5 = rotate 1 = [4, 1, 2, 3]                 │
│  k = 8: rotate 8 = rotate 0 = [1, 2, 3, 4]                 │
│                                                            │
│  k % n eliminates full rotations, keeping only effective k │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION 1 (Extra Array - O(n) space):

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n
        rotated = [0] * n
        
        for i in range(n):
            rotated[(i + k) % n] = nums[i]                                       # New position
        
        for i in range(n):
            nums[i] = rotated[i]                                                 # Copy back

ALTERNATIVE SOLUTION 2 (Python slicing - creates new list):

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        k = k % len(nums)
        nums[:] = nums[-k:] + nums[:-k]                                          # Slice and concatenate

# Note: nums[:] = ... modifies in-place (required by problem)
# nums = ... would just reassign the variable (wrong!)

VISUAL: Why reverse works (think of it as flipping):
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  [1, 2, 3, 4, 5, 6, 7]   Original                          │
│                                                            │
│  Imagine cutting and flipping:                             │
│                                                            │
│  Flip ALL:    [7, 6, 5, 4, 3, 2, 1]                        │
│                ─────── ───────────                         │
│                 want    want to                            │
│                 this    flip this                          │
│                                                            │
│  Flip first 3: [5, 6, 7, 4, 3, 2, 1]                       │
│                 ─────── (correct!)                         │
│                                                            │
│  Flip last 4:  [5, 6, 7, 1, 2, 3, 4]                       │
│                          ───────────(correct!)             │
│                                                            │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- k = 0: No rotation needed → returns same array ✓
- k = n: Full rotation → returns same array ✓
- k > n: k = k % n handles this ✓
- n = 1: Single element, no change ✓
- k = 1: Move last element to front ✓

TIME COMPLEXITY: O(n)
- Each of three reversals is O(n/2) at most
- Total: O(n) operations

SPACE COMPLEXITY: O(1)
- Only using a few pointer variables
- Modifications done in-place
- No additional arrays needed

CONCEPTS USED:
- In-place array manipulation
- Two-pointer technique (for reversal)
- Modular arithmetic (k % n)
- Array reversal as primitive operation
- Mathematical insight (three reversals = rotation)
"""
