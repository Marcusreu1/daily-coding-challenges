# 268. Missing Number
# Difficulty: Easy
# https://leetcode.com/problems/missing-number/

"""
PROBLEM:
Given an array nums containing n distinct numbers in the range [0, n],
return the only number in the range that is missing from the array.

EXAMPLES:
Input: nums = [3,0,1]          → Output: 2
Input: nums = [0,1]            → Output: 2
Input: nums = [9,6,4,2,3,5,7,0,1] → Output: 8

CONSTRAINTS:
- n == nums.length
- 1 <= n <= 10^4
- 0 <= nums[i] <= n
- All numbers in nums are unique

KEY INSIGHT (Multiple approaches):

1. GAUSS FORMULA (Sum):
   Expected sum = n(n+1)/2
   Missing = expected - actual sum

2. XOR:
   XOR all indices (0 to n) with all values
   Pairs cancel out, missing number remains

Both are O(n) time and O(1) space!

SOLUTION:
We'll implement the XOR approach as it avoids potential overflow issues.
"""

# STEP 1: Initialize result with n (the index we won't iterate over)
# STEP 2: XOR each index with its corresponding value
# STEP 3: The remaining value is the missing number

from typing import List

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        
        n = len(nums)
        result = n                                                               # Start with n (won't be an index)
        
        for i in range(n):
            result ^= i ^ nums[i]                                                # XOR index and value
        
        return result


"""
WHY EACH PART:
- n = len(nums): Array has n elements, range is [0, n]
- result = n: Initialize with n because we only loop 0 to n-1
- result ^= i ^ nums[i]: XOR current index and value into result
- return result: After all XORs, only the missing number remains

HOW IT WORKS (Example: nums = [3, 0, 1]):

┌─ Initial ─────────────────────────────────────────────────┐
│  n = 3, result = 3                                        │
│  We will XOR: indices (0,1,2) + values (3,0,1) + n (3)   │
└───────────────────────────────────────────────────────────┘

┌─ i = 0 ───────────────────────────────────────────────────┐
│  result = result ^ i ^ nums[i]                            │
│         = 3 ^ 0 ^ 3                                       │
│         = 0                                               │
│                                                           │
│  Binary: 011 ^ 000 ^ 011 = 000                           │
└───────────────────────────────────────────────────────────┘

┌─ i = 1 ───────────────────────────────────────────────────┐
│  result = result ^ i ^ nums[i]                            │
│         = 0 ^ 1 ^ 0                                       │
│         = 1                                               │
│                                                           │
│  Binary: 000 ^ 001 ^ 000 = 001                           │
└───────────────────────────────────────────────────────────┘

┌─ i = 2 ───────────────────────────────────────────────────┐
│  result = result ^ i ^ nums[i]                            │
│         = 1 ^ 2 ^ 1                                       │
│         = 2                                               │
│                                                           │
│  Binary: 001 ^ 010 ^ 001 = 010                           │
└───────────────────────────────────────────────────────────┘

┌─ Result ──────────────────────────────────────────────────┐
│  return 2 ✓                                               │
└───────────────────────────────────────────────────────────┘

WHY XOR WORKS:
┌────────────────────────────────────────────────────────────┐
│  After all XORs, we've XOR'd:                              │
│  • Every index from 0 to n-1                               │
│  • The value n (initial result)                            │
│  • Every value in nums                                     │
│                                                            │
│  So we've XOR'd: 0,1,2,...,n and nums[0],nums[1],...      │
│                                                            │
│  Since nums contains all of 0 to n EXCEPT one number:     │
│  • Numbers that appear TWICE (in both) cancel: a^a = 0    │
│  • The MISSING number appears only ONCE → it remains!     │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION 1 (Gauss Sum Formula):

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        expected_sum = n * (n + 1) // 2                                          # Gauss formula
        actual_sum = sum(nums)
        return expected_sum - actual_sum

# Example: nums = [3, 0, 1], n = 3
# expected = 3 * 4 / 2 = 6
# actual = 3 + 0 + 1 = 4
# missing = 6 - 4 = 2 ✓

ALTERNATIVE SOLUTION 2 (HashSet):

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        num_set = set(nums)
        n = len(nums)
        
        for i in range(n + 1):                                                   # Check 0 to n
            if i not in num_set:
                return i

# Time: O(n), Space: O(n)

ALTERNATIVE SOLUTION 3 (Sort):

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        nums.sort()
        
        for i, num in enumerate(nums):
            if i != num:                                                         # Expected i, got num
                return i
        
        return len(nums)                                                         # Missing is n

# Time: O(n log n), Space: O(1) or O(n) depending on sort

ALTERNATIVE SOLUTION 4 (Index as Hash):

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        
        # Use cyclic sort concept
        for i in range(n):
            while nums[i] < n and nums[i] != i:
                # Swap nums[i] to its correct position
                correct = nums[i]
                nums[i], nums[correct] = nums[correct], nums[i]
        
        # Find where index != value
        for i in range(n):
            if nums[i] != i:
                return i
        
        return n

# Time: O(n), Space: O(1), but modifies input

XOR PROPERTIES EXPLAINED:
┌────────────────────────────────────────────────────────────┐
│  XOR Truth Table:                                          │
│  ┌─────┬─────┬───────┐                                     │
│  │  A  │  B  │ A ^ B │                                     │
│  ├─────┼─────┼───────┤                                     │
│  │  0  │  0  │   0   │                                     │
│  │  0  │  1  │   1   │                                     │
│  │  1  │  0  │   1   │                                     │
│  │  1  │  1  │   0   │                                     │
│  └─────┴─────┴───────┘                                     │
│                                                            │
│  Key Properties:                                           │
│  • a ^ a = 0   (self-cancellation)                        │
│  • a ^ 0 = a   (identity)                                 │
│  • a ^ b = b ^ a   (commutative)                          │
│  • (a ^ b) ^ c = a ^ (b ^ c)   (associative)              │
│                                                            │
│  These properties let us find the "lonely" number!        │
└────────────────────────────────────────────────────────────┘

GAUSS FORMULA HISTORY:
┌────────────────────────────────────────────────────────────┐
│  Legend says young Gauss (age 7) quickly solved:           │
│  1 + 2 + 3 + ... + 100 = ?                                │
│                                                            │
│  He paired numbers:                                        │
│  (1 + 100) + (2 + 99) + (3 + 98) + ... = 101 × 50 = 5050 │
│                                                            │
│  General formula:                                          │
│  1 + 2 + ... + n = n × (n + 1) / 2                        │
│                                                            │
│  Including 0:                                              │
│  0 + 1 + 2 + ... + n = n × (n + 1) / 2  (same!)          │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- nums = [0]: n=1, range [0,1], missing 1 ✓
- nums = [1]: n=1, range [0,1], missing 0 ✓
- nums = [0,1]: n=2, range [0,1,2], missing 2 ✓
- nums = [0,1,2,...,n-1]: missing n ✓
- nums = [1,2,3,...,n]: missing 0 ✓

VERIFICATION TABLE:
┌─────────────────────────┬───────────────────┬─────────────┐
│         nums            │    Calculation    │   Missing   │
├─────────────────────────┼───────────────────┼─────────────┤
│        [0]              │  1-0 = 1          │      1      │
│        [1]              │  1-1 = 0          │      0      │
│       [0,1]             │  3-1 = 2          │      2      │
│      [3,0,1]            │  6-4 = 2          │      2      │
│     [0,1,3,4]           │  10-8 = 2         │      2      │
│  [9,6,4,2,3,5,7,0,1]    │  45-37 = 8        │      8      │
└─────────────────────────┴───────────────────┴─────────────┘

TIME COMPLEXITY: O(n)
- Single pass through the array
- Each operation is O(1)

SPACE COMPLEXITY: O(1)
- Only using a single integer variable
- No additional data structures

CONCEPTS USED:
- XOR bit manipulation
- Gauss summation formula
- Finding missing element in range
- Pairing/cancellation technique
"""
