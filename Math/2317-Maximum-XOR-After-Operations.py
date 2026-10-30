# 2317. Maximum XOR After Operations
# Difficulty: Medium
# https://leetcode.com/problems/maximum-xor-after-operations/

"""
PROBLEM:
You are given a 0-indexed integer array nums. In one operation, select any non-negative integer x and an index i, then update nums[i] to be equal to nums[i] AND (nums[i] XOR x).
Note that AND is the bitwise AND operation and XOR is the bitwise XOR operation.
Return the maximum possible bitwise XOR of all elements of nums after applying the operation any number of times.

EXAMPLES:
Input: nums = [3,2,4,6] → Output: 7
Explanation: 
Apply the operation to nums[2] with x = 4. nums[2] becomes 4 AND (4 XOR 4) = 0.
Apply the operation to nums[3] with x = 6. nums[3] becomes 6 AND (6 XOR 6) = 0.
Now nums = [3, 2, 0, 0].
The XOR of all elements is 3 XOR 2 XOR 0 XOR 0 = 1. Wait, we want the maximum.
If we change nums to [3, 2, 4, 6] and just apply operations to isolate 1s...
Actually, the maximum XOR is the bitwise OR of all elements: 3 | 2 | 4 | 6 = 7.

Input: nums = [1,2,3,9,2] → Output: 11
Explanation: 
The bitwise OR of all elements is 1 | 2 | 3 | 9 | 2 = 11. 
We can easily apply operations to eliminate duplicate 1-bits across the array to ensure every bit position with at least one 1 has exactly one 1 remaining, yielding an XOR sum of 11.

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^8

MATH RULES (BITWISE REDUCTION & OR-EQUIVALENCE):
1. The Operation `nums[i] AND (nums[i] XOR x)`: 
   If a bit in nums[i] is 0, `0 AND (...)` is always 0. We can NEVER change a 0 to a 1.
   If a bit in nums[i] is 1, choosing x to have a 1 at that bit makes `(1 XOR 1) = 0`, so `1 AND 0 = 0`. Choosing x to have a 0 makes `(1 XOR 0) = 1`, so `1 AND 1 = 1`.
   Therefore, this operation acts strictly as a "bit eraser". We can turn any 1 into a 0, but never 0 into 1.
2. XOR Maximization:
   The XOR sum of an array has a 1 at the k-th bit if there is an ODD number of 1s at that position across all elements.
   Since we can erase 1s at will, if a bit position has ANY 1s in the array, we can erase excesses until exactly ONE 1 remains. This guarantees the final XOR will have a 1 at that position.
   If a position has NO 1s, it will remain 0.
   This "if there is at least one 1, the result is 1" logic is the exact definition of the Bitwise OR operation.
"""

from typing import List

# STEP 1: Initialize a variable to accumulate the Bitwise OR of all elements.
# STEP 2: Iterate through every number in the array.
# STEP 3: Apply the bitwise OR assignment operator (|=).
# STEP 4: Return the accumulated result.

class Solution:
    def maximumXOR(self, nums: List[int]) -> int:
        
        max_xor = 0
        
        # Traverse the array to find the global bitwise OR
        for num in nums:
            max_xor |= num
            
        return max_xor

"""
WHY EACH PART:
- max_xor |= num: Accumulates all the '1' bits that exist anywhere in the array. This effectively computes the mathematical ceiling of the XOR sum achievable via the erasure operation.

KEY TECHNIQUE:
- Bitwise Logic Reduction: Abstracting a complex simulated operation into its fundamental bit-level truth table to discover it maps perfectly to a primitive OR operation.

EDGE CASES:
- Array with all zeros (e.g., [0, 0, 0]): The OR is 0. Returns 0. Correct.
- Array with identical numbers (e.g., [7, 7, 7]): Erasing two 7s leaves one 7. The OR is 7. Returns 7. Correct.

TIME COMPLEXITY: O(N) - We iterate through the elements of the `nums` array exactly once.
SPACE COMPLEXITY: O(1) - Only a single scalar integer variable is allocated in memory.
"""
