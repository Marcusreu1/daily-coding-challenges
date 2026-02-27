"""
368. Largest Divisible Subset
Difficulty: Medium
https://leetcode.com/problems/largest-divisible-subset/

PROBLEM:
Given a set of distinct positive integers nums, return the largest
subset answer such that every pair (answer[i], answer[j]) of elements
in this subset satisfies:
    - answer[i] % answer[j] == 0, OR
    - answer[j] % answer[i] == 0

If there are multiple solutions, return any of them.

EXAMPLES:
Input: nums = [1,2,3] → Output: [1,2] or [1,3]
    [1,2]: 2 % 1 = 0 ✓
    [1,3]: 3 % 1 = 0 ✓

Input: nums = [1,2,4,8] → Output: [1,2,4,8]
    Every larger element is divisible by all smaller ones.

CONSTRAINTS:
• 1 <= nums.length <= 1000
• 1 <= nums[i] <= 2 × 10⁹
• All integers in nums are unique

KEY INSIGHT - TRANSITIVITY:
If a | b and b | c, then a | c (a divides c).

So if we SORT the array, we only need to check if each element
is divisible by the previous element in our subset.
The transitivity property guarantees all pairs work!

APPROACH: Dynamic Programming
1. Sort the array
2. dp[i] = size of largest divisible subset ending at nums[i]
3. Track parent pointers to reconstruct the subset
"""

from typing import List


# ============================================================================
# SOLUTION 1: DP WITH PARENT TRACKING 
# ============================================================================

class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        
        if not nums:
            return []
        
        n = len(nums)
        nums.sort()                                              # Step 1: Sort
        
        # dp[i] = size of largest divisible subset ending at i
        dp = [1] * n
        parent = [-1] * n                                        # To reconstruct
        
        max_size = 1
        max_index = 0
        
        # Step 2: Fill DP table
        for i in range(1, n):
            for j in range(i):
                if nums[i] % nums[j] == 0:                       # Can extend subset
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        parent[i] = j
            
            if dp[i] > max_size:                                 # Track maximum
                max_size = dp[i]
                max_index = i
        
        # Step 3: Reconstruct the subset
        result = []
        idx = max_index
        while idx != -1:
            result.append(nums[idx])
            idx = parent[idx]
        
        return result[::-1]                                      # Reverse to get ascending order


# ============================================================================
# SOLUTION 2: DP WITH EXPLICIT SUBSET STORAGE
# ============================================================================

class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        
        if not nums:
            return []
        
        nums.sort()
        n = len(nums)
        
        # subsets[i] = largest divisible subset ending at nums[i]
        subsets = [[num] for num in nums]
        
        for i in range(1, n):
            for j in range(i):
                if nums[i] % nums[j] == 0:
                    if len(subsets[j]) + 1 > len(subsets[i]):
                        subsets[i] = subsets[j] + [nums[i]]
        
        return max(subsets, key=len)


# ============================================================================
# SOLUTION 3: OPTIMIZED WITH EARLY TERMINATION
# ============================================================================

class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        
        if len(nums) <= 1:
            return nums
        
        nums.sort()
        n = len(nums)
        
        dp = [1] * n
        parent = [-1] * n
        
        max_len = 1
        max_idx = 0
        
        for i in range(1, n):
            # Only check divisors (optimization)
            for j in range(i - 1, -1, -1):                       # Reverse for potential early gains
                if nums[i] % nums[j] == 0:
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        parent[i] = j
            
            if dp[i] > max_len:
                max_len = dp[i]
                max_idx = i
        
        # Reconstruct
        result = []
        while max_idx != -1:
            result.append(nums[max_idx])
            max_idx = parent[max_idx]
        
        return result[::-1]


# ============================================================================
# SOLUTION 4: USING DICTIONARY FOR CLEANER CODE
# ============================================================================

class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        
        if not nums:
            return []
        
        nums.sort()
        
        # dp_dict[num] = (size, previous_element)
        dp_dict = {num: (1, None) for num in nums}
        
        max_num = nums[0]
        max_size = 1
        
        for i, num in enumerate(nums):
            for j in range(i):
                prev = nums[j]
                if num % prev == 0:
                    if dp_dict[prev][0] + 1 > dp_dict[num][0]:
                        dp_dict[num] = (dp_dict[prev][0] + 1, prev)
            
            if dp_dict[num][0] > max_size:
                max_size = dp_dict[num][0]
                max_num = num
        
        # Reconstruct
        result = []
        current = max_num
        while current is not None:
            result.append(current)
            current = dp_dict[current][1]
        
        return result[::-1]


"""
HOW IT WORKS (Detailed Trace):

Example: nums = [4, 8, 10, 240]

Step 1: Sort → [4, 8, 10, 240]

Step 2: Build DP

i=0, nums[0]=4:
    dp[0] = 1, parent[0] = -1
    
i=1, nums[1]=8:
    j=0: 8 % 4 = 0 ✓
         dp[1] = dp[0] + 1 = 2
         parent[1] = 0
    
i=2, nums[2]=10:
    j=0: 10 % 4 ≠ 0
    j=1: 10 % 8 ≠ 0
    dp[2] = 1, parent[2] = -1
    
i=3, nums[3]=240:
    j=0: 240 % 4 = 0 ✓
         dp[3] = dp[0] + 1 = 2
         parent[3] = 0
    j=1: 240 % 8 = 0 ✓
         dp[3] = max(2, dp[1] + 1) = 3
         parent[3] = 1
    j=2: 240 % 10 = 0 ✓
         dp[3] = max(3, dp[2] + 1) = 3 (no change)

Final DP:
    nums:   [4,  8,  10, 240]
    dp:     [1,  2,  1,  3]
    parent: [-1, 0, -1,  1]
    
max_index = 3 (dp[3] = 3)

Reconstruct from index 3:
    idx=3: nums[3]=240, parent[3]=1
    idx=1: nums[1]=8, parent[1]=0
    idx=0: nums[0]=4, parent[0]=-1
    
Result (reversed): [4, 8, 240] ✓

WHY SORTING WORKS:
┌────────────────────────────────────────────────────────────────┐
│  After sorting: nums[i] >= nums[j] for i > j                   │
│                                                                │
│  For divisibility: if nums[i] % nums[j] == 0                  │
│  then nums[i] is a MULTIPLE of nums[j]                        │
│  (since nums[i] >= nums[j], can't be the other way)           │
│                                                                │
│  Transitivity:                                                 │
│  If we have subset [..., a, b] where b % a = 0                │
│  And c % b = 0                                                 │
│  Then c % a = 0 automatically!                                 │
│                                                                │
│  So we only check: nums[i] % nums[j] for extending subset     │
└────────────────────────────────────────────────────────────────┘

WHY THIS IS LIKE LIS (Longest Increasing Subsequence):
┌────────────────────────────────────────────────────────────────┐
│  LIS: dp[i] = longest subsequence ending at i                  │
│       where nums[i] > nums[j] for all j in subsequence        │
│                                                                │
│  This problem: dp[i] = largest divisible subset ending at i   │
│       where nums[i] % nums[j] == 0 for prev element           │
│                                                                │
│  Same DP structure, different condition!                       │
└────────────────────────────────────────────────────────────────┘

TRANSITIVITY PROOF:
┌────────────────────────────────────────────────────────────────┐
│  Given: a | b (a divides b) → b = a × k₁ for some integer k₁  │
│         b | c (b divides c) → c = b × k₂ for some integer k₂  │
│                                                                │
│  Then: c = b × k₂ = (a × k₁) × k₂ = a × (k₁ × k₂)            │
│        → a | c ✓                                               │
│                                                                │
│  Example: 2|4 (4=2×2), 4|8 (8=4×2) → 2|8 (8=2×4) ✓           │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  nums = [1]         → [1] (single element)                    │
│  nums = [2, 3, 5]   → [2] or [3] or [5] (no pairs divide)    │
│  nums = [1, 2, 3]   → [1, 2] or [1, 3] (1 divides everything)│
│  Large numbers      → Works due to % operation                 │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(n²)
├── Sorting: O(n log n)
├── DP: O(n²) - two nested loops
├── Reconstruction: O(n)
└── Total: O(n²)

SPACE COMPLEXITY: O(n)
├── dp array: O(n)
├── parent array: O(n)
├── result: O(n)
└── Total: O(n)

OPTIMIZATION NOTES:
┌────────────────────────────────────────────────────────────────┐
│  For each nums[i], we only need to check its divisors.        │
│  Could precompute divisors, but O(n²) is acceptable for       │
│  n ≤ 1000.                                                    │
│                                                                │
│  If nums[i] % nums[j] == 0, nums[j] ≤ √nums[i] or            │
│  nums[j] is a "large divisor". Can optimize but not needed.   │
└────────────────────────────────────────────────────────────────┘
CONCEPTS USED:
• Dynamic Programming
• Divisibility
• Transitivity Property
• Array Sorting
• Path Reconstruction
"""
