# 1486. XOR Operation in an Array
# Difficulty: Easy
# https://leetcode.com/problems/xor-operation-in-an-array/

"""
PROBLEM:
You are given an integer `n` and an integer `start`.
Define an array `nums` where `nums[i] = start + 2 * i` (0-indexed) and `n == nums.length`.
Return the bitwise XOR of all elements of `nums`.

EXAMPLES:
Input: n = 5, start = 0
Output: 8
(Explanation: Array nums is equal to [0, 2, 4, 6, 8] where (0 ^ 2 ^ 4 ^ 6 ^ 8) = 8.
Where "^" corresponds to bitwise XOR operator.)

Input: n = 4, start = 3
Output: 8
(Explanation: Array nums is equal to [3, 5, 7, 9] where (3 ^ 5 ^ 7 ^ 9) = 8.)

CONSTRAINTS:
- 1 <= n <= 1000
- 0 <= start <= 1000
- n == nums.length

ALGORITHM LOGIC (On-the-fly Generation & Cumulative XOR):
1. We avoid the rookie mistake of actually allocating memory for an array of size `n`. 
   Since each element can be strictly derived from its index, we generate them dynamically.
2. We initialize an accumulator `ans` with 0 (because 0 is the identity element for XOR: 0 ^ x = x).
3. We loop `n` times, acting as our virtual indices `i`.
4. In each iteration, we calculate `start + 2 * i` and instantly apply the XOR operation to our accumulator.
5. This simulates the array construction and evaluation simultaneously, slashing space complexity to true O(1).

VISUALIZATION (n = 4, start = 3):
ans = 0

i = 0: val = 3 + 2(0) = 3. ans = 0 ^ 3 = 3.
i = 1: val = 3 + 2(1) = 5. ans = 3 ^ 5 = 6.
i = 2: val = 3 + 2(2) = 7. ans = 6 ^ 7 = 1.
i = 3: val = 3 + 2(3) = 9. ans = 1 ^ 9 = 8.

Loop ends. Return 8. ✓
"""

# STEP 1: Initialize the XOR accumulator to 0 (neutral element)
# STEP 2: Iterate exactly `n` times, representing the virtual array indices
# STEP 3: Mathematically generate the value for index `i` on the fly
# STEP 4: Apply bitwise XOR cumulatively
# STEP 5: Return the final evaluated accumulator

class Solution:
    def xorOperation(self, n: int, start: int) -> int:
        
        ans = 0
        
        for i in range(n):
            
            # Dynamically compute the value and XOR it with the running total
            ans ^= (start + 2 * i)
            
        return ans

"""
WHY EACH PART:
- ans = 0: Crucial starting point. If we started with any other number, it would permanently taint the bitwise operations.
- range(n): Generates the indices 0 to n-1 seamlessly.
- ans ^= ... : The compound assignment operator for XOR. It evaluates the right side of the equation entirely before combining it at the bit level with `ans`.

HOW IT WORKS (Example: n = 1, start = 7):
Loop runs exactly once (i = 0).
ans = 0 ^ (7 + 0) -> ans = 7.
Returns 7. ✓

KEY TECHNIQUE:
- Virtual Arrays / Lazy Evaluation
- Bitwise Operations (Cumulative state tracking)

EDGE CASES:
- Minimum `n` (n = 1): Loop runs once, computes `start` correctly without errors. ✓
- Large offsets: Handled perfectly. Operations remain strictly localized to integer bit manipulation, which cannot overflow in Python. ✓

TIME COMPLEXITY: O(N) - We iterate exactly `n` times. Given the constraint N <= 1000, this loop executes in less than a microsecond. 
*(Note: There is a deep mathematical O(1) solution utilizing the repetitive nature of XOR on arithmetic progressions divided by 2, but for N=1000, the O(N) simulation is the industry standard due to its absolute readability and instantaneous performance).*
SPACE COMPLEXITY: O(1) - No arrays are built. We strictly maintain a single integer variable `ans` in memory regardless of how large `n` grows.
"""
