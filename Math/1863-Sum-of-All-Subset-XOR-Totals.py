# 1863. Sum of All Subset XOR Totals
# Difficulty: Easy
# https://leetcode.com/problems/sum-of-all-subset-xor-totals/

"""
PROBLEM:
The XOR total of an array is defined as the bitwise XOR of all its elements, or 0 if the array is empty.
Given an array nums, return the sum of all XOR totals for every subset of nums.
A subset of an array is a selection of elements (possibly none) of the array.

EXAMPLES:
Input: nums = [1,3] → Output: 6
Explanation: The 4 subsets of [1,3] are:
- The empty subset has an XOR total of 0.
- [1] has an XOR total of 1.
- [3] has an XOR total of 3.
- [1,3] has an XOR total of 1 XOR 3 = 2.
0 + 1 + 3 + 2 = 6

Input: nums = [5,1,6] → Output: 28
Explanation: The 8 subsets of [5,1,6] are:
- Empty: 0
- [5]: 5
- [1]: 1
- [6]: 6
- [5,1]: 5 ^ 1 = 4
- [5,6]: 5 ^ 6 = 3
- [1,6]: 1 ^ 6 = 7
- [5,1,6]: 5 ^ 1 ^ 6 = 2
0 + 5 + 1 + 6 + 4 + 3 + 7 + 2 = 28

CONSTRAINTS:
- 1 <= nums.length <= 12
- 1 <= nums[i] <= 20

MATH RULES (BITWISE COMBINATORICS):
Generating all subsets and calculating their XOR sums takes O(2^N) time. We can optimize this to O(N) using bitwise properties.
Look at each bit position independently. If a bit is set (1) in AT LEAST ONE element of the array, it will be set in EXACTLY HALF of all possible subsets.
The total number of subsets is 2^n. Half of that is 2^(n-1).
Therefore, any bit that appears anywhere in the array will contribute its value multiplied by 2^(n-1) to the final sum.
To find out which bits appear at least once across all numbers, we can simply apply the Bitwise OR (|) to all elements in the array, and then multiply the result by 2^(n-1).

VISUALIZATION (nums = [1, 3]):
Binary of 1: 01
Binary of 3: 11
Total elements (n) = 2. Subsets half multiplier = 2^(2-1) = 2^1 = 2.

Step 1 (Find active bits using OR):
01 | 11 = 11 (which is 3 in decimal).

Step 2 (Multiply by 2^(n-1)):
3 * 2^1 = 3 * 2 = 6.

Result: 6 ✓
"""

from typing import List

# STEP 1: Initialize a variable to accumulate the bitwise OR of all numbers.
# STEP 2: Iterate through the array and apply the OR operator to merge all bits.
# STEP 3: Shift the merged bits to the left by (n - 1) places.
# STEP 4: Return the shifted value as the mathematically proven sum.

class Solution:
    def subsetXORSum(self, nums: List[int]) -> int:
        
        active_bits = 0
        
        # Merge all bits to see which ones are set in at least one number
        for num in nums:
            active_bits |= num
            
        # Multiply the active bits mask by 2^(n-1) using a left bit shift
        result = active_bits << (len(nums) - 1)
        
        return result

"""
WHY EACH PART:
- active_bits |= num: The Bitwise OR operator perfectly maps every unique bit present in the entire array into a single integer.
- << (len(nums) - 1): Left shifting an integer by X is mathematically identical to multiplying it by 2^X. It bypasses slow exponentiation functions.

HOW IT WORKS (Example: nums = [5, 1, 6]):

Initial: active_bits = 0, n = 3. 2^(3-1) -> Shift by 2.

Iteration 1 (num = 5, binary 101):
├── active_bits = 000 | 101 = 101 (5)

Iteration 2 (num = 1, binary 001):
├── active_bits = 101 | 001 = 101 (5)

Iteration 3 (num = 6, binary 110):
├── active_bits = 101 | 110 = 111 (7)

Exit loop.

Calculation:
├── active_bits = 7
├── result = 7 << 2 (which means 7 * 2^2 -> 7 * 4)
└── result = 28

Return 28 ✓

KEY TECHNIQUE:
- Combinatorics Optimization: Transforming an O(2^N) backtracking problem into an O(N) mathematical property problem.
- Bit Manipulation: Leveraging the independence of bit columns to evaluate systemic outcomes instantly.

EDGE CASES:
- n = 1 (e.g., nums = [5]): Loop sets active_bits to 5. Shift is 1 - 1 = 0. 5 << 0 = 5. Correct, subsets are [] and [5], XORs are 0 and 5, sum is 5. ✓
- All numbers are the same (e.g., [2, 2]): OR merges them to 2. Shift by 1. 2 << 1 = 4. Subsets: [], [2], [2], [2,2]->0. Sum = 4. ✓

TIME COMPLEXITY: O(N) - We traverse the array of length N exactly once.
SPACE COMPLEXITY: O(1) - Only one integer variable is allocated.

CONCEPTS USED:
- Bitwise Logic (OR, Left Shift)
- Combinatorics Mathematics
- Subsets and Probabilities
"""
