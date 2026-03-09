"""
396. Rotate Function
Difficulty: Medium
https://leetcode.com/problems/rotate-function/

PROBLEM:
Given an integer array nums of length n.
Assume arrk to be an array obtained by rotating nums by k positions clock-wise.
We define the "rotation function" F on nums as:

    F(k) = 0 * arrk[0] + 1 * arrk[1] + ... + (n-1) * arrk[n-1]

Return the maximum value of F(0), F(1), ..., F(n-1).

EXAMPLES:
Input: nums = [4,3,2,6] → Output: 26
    F(0) = 0×4 + 1×3 + 2×2 + 3×6 = 0 + 3 + 4 + 18  = 25
    F(1) = 0×6 + 1×4 + 2×3 + 3×2 = 0 + 4 + 6 + 6   = 16
    F(2) = 0×2 + 1×6 + 2×4 + 3×3 = 0 + 6 + 8 + 9   = 23
    F(3) = 0×3 + 1×2 + 2×6 + 3×4 = 0 + 2 + 12 + 12 = 26
    max = 26

Input: nums = [100] → Output: 0

CONSTRAINTS:
    n == nums.length
    1 <= n <= 10^5
    -100 <= nums[i] <= 100

KEY INSIGHT:
Instead of recalculating each F(k) from scratch in O(n), we can derive
F(k) from F(k-1) in O(1) using a mathematical recurrence:

    F(k) = F(k-1) + totalSum - n × nums[n - k]

CHALLENGES:
    Brute force O(n²) is too slow for n = 10^5
    Need to discover the recurrence relation between F(k) and F(k-1)
    Identifying WHICH element "wraps around" at each rotation step

MATHEMATICAL DERIVATION:
When rotating one more position (from rotation k-1 to rotation k):
    - The LAST element of arr(k-1) wraps around to position 0
      → Its coefficient drops from (n-1) to 0:  change = -(n-1)
    - Every OTHER element shifts right by 1 position
      → Each of their coefficients increases by 1:  change = +1 each

    F(k) - F(k-1) = (+1) × (n-1 elements) + (-(n-1)) × (wrapping element)
                   = (totalSum - wrapping_el) - (n-1) × wrapping_el
                   = totalSum - n × wrapping_el

    The wrapping element at step k is: nums[n - k]

    Therefore: F(k) = F(k-1) + totalSum - n × nums[n - k]

SOLUTION:
    1. Calculate totalSum and F(0)
    2. Use the recurrence to get F(1), F(2), ..., F(n-1) in O(1) each
    3. Track the maximum across all F(k)
"""

# STEP 1: Precompute totalSum and F(0)
# STEP 2: Iterate k from 1 to n-1, applying the recurrence
# STEP 3: Track and return the maximum F(k)

class Solution:
    def maxRotateFunction(self, nums: List[int]) -> int:

        n = len(nums)
        total_sum = sum(nums)                                            # Sum of all elements (constant)

        f = sum(i * nums[i] for i in range(n))                          # Calculate F(0) directly

        max_val = f                                                      # Initialize max with F(0)

        for k in range(1, n):                                            # Compute F(1) through F(n-1)
            f = f + total_sum - n * nums[n - k]                          # O(1) recurrence relation
            max_val = max(max_val, f)                                    # Update maximum

        return max_val

"""
WHY EACH PART:

    total_sum = sum(nums): Precomputed once, reused in every recurrence step
    f = sum(i * nums[i]): F(0) is our starting point, calculated directly
    max_val = f: F(0) could be the answer, start tracking from here
    for k in range(1, n): Already have F(0), need F(1) through F(n-1)
    f = f + total_sum - n * nums[n-k]: The O(1) magic — recurrence relation
    max_val = max(max_val, f): Greedily keep the best F(k) found so far

HOW IT WORKS (Example: nums = [4, 3, 2, 6]):

    n = 4,  total_sum = 4+3+2+6 = 15

    F(0) = 0×4 + 1×3 + 2×2 + 3×6 = 25
    max_val = 25

    k=1: wrapping element = nums[4-1] = nums[3] = 6
    ├── F(1) = 25 + 15 - 4×6 = 25 + 15 - 24 = 16
    └── max_val = max(25, 16) = 25

    k=2: wrapping element = nums[4-2] = nums[2] = 2
    ├── F(2) = 16 + 15 - 4×2 = 16 + 15 - 8 = 23
    └── max_val = max(25, 23) = 25

    k=3: wrapping element = nums[4-3] = nums[1] = 3
    ├── F(3) = 23 + 15 - 4×3 = 23 + 15 - 12 = 26
    └── max_val = max(25, 26) = 26

    Result: 26 ✓

WHY THE RECURRENCE WORKS (Visual proof):

    Rotation arr0 → arr1:  [4, 3, 2, 6] → [6, 4, 3, 2]

    Element 4: coefficient 0 → 1  (+1)
    Element 3: coefficient 1 → 2  (+1)
    Element 2: coefficient 2 → 3  (+1)
    Element 6: coefficient 3 → 0  (-(n-1) = -3)  ← wraps around!

    Change = +1 +1 +1 -3
           = (4 + 3 + 2) - 3×6
           = (4+3+2+6) - 6 - 3×6
           = totalSum - 4×6
           = totalSum - n × nums[n-1]
           = 15 - 24 = -9

    F(1) = F(0) + (-9) = 25 - 9 = 16 ✓

BRUTE FORCE vs OPTIMIZED:

    Brute Force:
        For each k: rotate array + compute F(k) → O(n) per rotation
        Total: O(n²) → TOO SLOW for n = 10^5 ✗

    Optimized (this solution):
        Compute F(0) once: O(n)
        Each subsequent F(k) in O(1) via recurrence
        Total: O(n) ✓

WHY nums[n - k] IS THE WRAPPING ELEMENT:

    k=1: last element of arr0 = nums[n-1] = nums[4-1] = 6  ✓
    k=2: last element of arr1 = nums[n-2] = nums[4-2] = 2  ✓
    k=3: last element of arr2 = nums[n-3] = nums[4-3] = 3  ✓

    Pattern: the element at position n-k in the ORIGINAL array
    is always the one that wraps from coefficient (n-1) → 0

EDGE CASES:

    Single element [100]: F(0) = 0×100 = 0 → Returns 0 ✓
    Two elements: Computes F(0) and F(1), picks max ✓
    All same values: All F(k) equal → Returns any ✓
    Negative values: Recurrence handles naturally ✓
    All negative: Correctly picks least negative F(k) ✓
    Large n (10^5): O(n) handles it efficiently ✓

TIME COMPLEXITY: O(n)
    O(n) to compute sum and F(0)
    O(n) to iterate k = 1 to n-1 with O(1) per step

SPACE COMPLEXITY: O(1)
    Only a few variables: total_sum, f, max_val

CONCEPTS USED:
    Mathematical recurrence relations
    Array rotation properties
    Optimization from O(n²) to O(n)
    Precomputation (totalSum)
    Greedy maximum tracking
"""
