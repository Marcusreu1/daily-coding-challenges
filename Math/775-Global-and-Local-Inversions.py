"""
775. Global and Local Inversions
Difficulty: Medium
https://leetcode.com/problems/global-and-local-inversions/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

You are given an integer array nums, which is a permutation of
the numbers from 0 to n - 1.

A global inversion is a pair (i, j) such that:

    i < j and nums[i] > nums[j]

A local inversion is a pair (i, i + 1) such that:

    nums[i] > nums[i + 1]

Return True if the number of global inversions is equal to the
number of local inversions. Otherwise, return False.

EXAMPLES:

    Input: nums = [1, 0, 2]
    Output: True

    Explanation:
        Global inversions:
            (0, 1): nums[0] = 1 > nums[1] = 0

        Local inversions:
            (0, 1): nums[0] = 1 > nums[1] = 0

        Both counts are 1.

    Input: nums = [1, 2, 0]
    Output: False

    Explanation:
        Global inversions:
            (0, 2): nums[0] = 1 > nums[2] = 0
            (1, 2): nums[1] = 2 > nums[2] = 0

        Local inversions:
            (1, 2): nums[1] = 2 > nums[2] = 0

        Global count = 2, local count = 1.

CONSTRAINTS:

    1 <= nums.length <= 10^5
    0 <= nums[i] < nums.length
    All nums[i] are unique
    nums is a permutation of [0, 1, ..., n - 1]

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

Every local inversion is automatically a global inversion.

Therefore:

    local inversions ⊆ global inversions

So global inversions are always greater than or equal to
local inversions.

For both counts to be equal, there must be NO global inversion
that is not local.

That means there cannot be an inversion between elements whose
indices are more than 1 apart.

For a permutation of [0, 1, ..., n - 1], this condition is equivalent to:

    abs(nums[i] - i) <= 1

for every index i.

In other words, each value can be at most one position away from
its sorted position.

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. Understanding that local inversions are a subset of global inversions
2. Avoiding brute force O(n²) global inversion counting
3. Recognizing the displacement condition abs(nums[i] - i) <= 1
4. Proving that moving more than one position creates a non-local inversion

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Iterate through every index i
STEP 2: Check how far nums[i] is from its sorted position i
STEP 3: If abs(nums[i] - i) > 1, return False
STEP 4: If every element passes, return True

WHY THIS WORKS:
    In the sorted permutation, value x belongs at index x.
    If a value is displaced by more than 1 position, it must have
    crossed over at least one non-adjacent element, creating a
    global inversion that is not local.
"""

from typing import List


class Solution:
    def isIdealPermutation(self, nums: List[int]) -> bool:

        for i, value in enumerate(nums):                                          # Check each value and its index
            if abs(value - i) > 1:                                                # Too far from sorted position
                return False                                                     # Non-local global inversion exists

        return True                                                              # All inversions are local


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

for i, value in enumerate(nums):
    We need both the current index i and the value stored there.
    Since nums is a permutation of [0, ..., n-1], value should
    ideally be located at index value.

abs(value - i):
    Measures how far the value is from its sorted position.

    Example:
        nums = [1, 0, 2]

        i=0, value=1 → abs(1-0)=1
        i=1, value=0 → abs(0-1)=1
        i=2, value=2 → abs(2-2)=0

    Every value is at most 1 position away.

if abs(value - i) > 1:
    If a value moved more than one position, it must have crossed
    over a non-adjacent element. That creates a global inversion
    that is not local, so the counts cannot be equal.

return False:
    As soon as we find one invalid displacement, we can stop.
    One non-local global inversion is enough to make the answer False.

return True:
    If every value is at most one position away from its sorted index,
    then every global inversion must be local.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: nums = [1, 0, 2]):
════════════════════════════════════════════════════════════════

    Index:   0  1  2
    nums:   [1, 0, 2]

    i=0:
    ├── value = 1
    ├── abs(1 - 0) = 1
    └── Valid ✓

    i=1:
    ├── value = 0
    ├── abs(0 - 1) = 1
    └── Valid ✓

    i=2:
    ├── value = 2
    ├── abs(2 - 2) = 0
    └── Valid ✓

    No value is more than 1 position away.
    Return True ✓

    Inversions:
    ├── Global: (0,1)
    ├── Local:  (0,1)
    └── Counts are equal.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: nums = [1, 2, 0]):
════════════════════════════════════════════════════════════════

    Index:   0  1  2
    nums:   [1, 2, 0]

    i=0:
    ├── value = 1
    ├── abs(1 - 0) = 1
    └── Valid ✓

    i=1:
    ├── value = 2
    ├── abs(2 - 1) = 1
    └── Valid ✓

    i=2:
    ├── value = 0
    ├── abs(0 - 2) = 2
    └── Invalid ✗

    Return False.

    Why?
    ├── nums[0] = 1 > nums[2] = 0 → global inversion
    ├── But indices 0 and 2 are not adjacent
    └── Therefore, this inversion is not local.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: nums = [0, 2, 1, 3]):
════════════════════════════════════════════════════════════════

    Index:   0  1  2  3
    nums:   [0, 2, 1, 3]

    i=0:
    ├── value = 0
    ├── abs(0 - 0) = 0
    └── Valid ✓

    i=1:
    ├── value = 2
    ├── abs(2 - 1) = 1
    └── Valid ✓

    i=2:
    ├── value = 1
    ├── abs(1 - 2) = 1
    └── Valid ✓

    i=3:
    ├── value = 3
    ├── abs(3 - 3) = 0
    └── Valid ✓

    Return True.

    Inversions:
    ├── Global: (1,2), because 2 > 1
    ├── Local:  (1,2), because they are adjacent
    └── Counts are equal.

════════════════════════════════════════════════════════════════
WHY LOCAL INVERSIONS ARE ALWAYS GLOBAL INVERSIONS:
════════════════════════════════════════════════════════════════

    A local inversion has the form:

        nums[i] > nums[i + 1]

    A global inversion has the form:

        i < j and nums[i] > nums[j]

    If we choose j = i + 1, then:

        i < i + 1
        nums[i] > nums[i + 1]

    So every local inversion satisfies the definition of a
    global inversion.

    Therefore:
        local inversions are included inside global inversions.

    This means the only possible problem is having extra global
    inversions that are not local.

════════════════════════════════════════════════════════════════
WHY abs(nums[i] - i) > 1 MEANS FALSE:
════════════════════════════════════════════════════════════════

    Since nums is a permutation, value x belongs at index x in
    the sorted array:

        Sorted: [0, 1, 2, 3, 4, ...]

    If value x is at index i and abs(x - i) > 1, then x has moved
    more than one position away from where it belongs.

    That movement cannot be explained by only one adjacent swap.
    It means x crossed over at least one non-adjacent element.

    Crossing over a non-adjacent element creates a global inversion
    that is not local.

    Therefore:
        abs(nums[i] - i) > 1 → return False.

════════════════════════════════════════════════════════════════
ALTERNATIVE APPROACH: PREFIX MAX
════════════════════════════════════════════════════════════════

    Another valid way to solve the problem is to directly check
    for non-local global inversions.

    A non-local inversion exists if:

        nums[i] > nums[j] where j >= i + 2

    We can scan from left to right and keep the maximum value seen
    up to index i - 2.

    If max(nums[0 ... i-2]) > nums[i], then nums[i] forms a
    non-local global inversion with some earlier element.

    Code:

        def isIdealPermutation(self, nums):
            prefix_max = nums[0]

            for i in range(2, len(nums)):
                prefix_max = max(prefix_max, nums[i - 2])
                if prefix_max > nums[i]:
                    return False

            return True

    This is also O(n), but the displacement solution is simpler.

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    nums = [0]              → True, no inversions ✓
    nums = [1, 0]           → True, one local/global inversion ✓
    nums = [0, 1, 2]        → True, sorted array has zero inversions ✓
    nums = [1, 0, 2]        → True, only local inversion ✓
    nums = [1, 2, 0]        → False, has non-local inversion ✓
    nums = [2, 0, 1]        → False, value 2 is too far left ✓
    nums = [0, 2, 1, 3]     → True, one adjacent swap only ✓
    nums = [3, 2, 1, 0]     → False, many non-local inversions ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(n)
════════════════════════════════════════════════════════════════

    We scan the array once.
    Each index does O(1) work.

    Total: O(n)

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(1)
════════════════════════════════════════════════════════════════

    We only use a few variables.
    No additional data structures are needed.

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Permutation properties
    Global inversions
    Local inversions
    Greedy observation
    Index-value displacement
    Mathematical proof by contradiction
    One-pass array scanning
"""
