# 1822. Sign of the Product of an Array
# Difficulty: Easy
# https://leetcode.com/problems/sign-of-the-product-of-an-array/

"""
PROBLEM:
There is a function signFunc(x) that returns:
- 1 if x is positive.
- -1 if x is negative.
- 0 if x is equal to 0.
You are given an integer array nums. Let product be the product of all values in the array nums.
Return signFunc(product).

EXAMPLES:
Input: nums = [-1,-2,-3,-4,3,2,1] → Output: 1
Explanation: The product of all values in the array is 144, and signFunc(144) = 1.

Input: nums = [1,5,0,2,-3] → Output: 0
Explanation: The product of all values in the array is 0, and signFunc(0) = 0.

Input: nums = [-1,1,-1,1,-1] → Output: -1
Explanation: The product of all values in the array is -1, and signFunc(-1) = -1.

CONSTRAINTS:
- 1 <= nums.length <= 1000
- -100 <= nums[i] <= 100

MATH RULES (SIGN PARITY & SHORT-CIRCUIT):
Calculating the actual product of up to 1000 numbers is a massive computational waste and causes Integer Overflow in strictly-typed languages (like Java/C++). 
Instead of tracking the product, we only track the mathematical SIGN.
1. Any number multiplied by 0 is 0. If we encounter a 0, we immediately halt and return 0.
2. Positive numbers do not change the sign of a product (Positive * Positive = Positive, Negative * Positive = Negative). We can ignore them.
3. Negative numbers flip the sign. If we track the sign starting at 1, every time we encounter a negative number, we multiply our tracker by -1.

VISUALIZATION (nums = [-1, 2, -3]):
Initial: sign = 1

i=0, num = -1:
  - num < 0, so sign = sign * -1 -> 1 * -1 = -1

i=1, num = 2:
  - num is positive. Ignore. sign remains -1.

i=2, num = -3:
  - num < 0, so sign = sign * -1 -> -1 * -1 = 1

Exit loop. Return sign (1) ✓
"""

from typing import List

# STEP 1: Initialize a sign tracker to 1 (positive).
# STEP 2: Iterate through every number in the array.
# STEP 3: If the number is 0, immediately return 0 (short-circuit).
# STEP 4: If the number is less than 0, multiply the sign tracker by -1 to flip it.
# STEP 5: Return the final evaluated sign.

class Solution:
    def arraySign(self, nums: List[int]) -> int:
        
        sign = 1
        
        for num in nums:
            # Short-circuit logic: a single zero makes the entire product zero
            if num == 0:
                return 0
                
            # Flip the sign tracker for every negative number encountered
            if num < 0:
                sign *= -1
                
        return sign

"""
WHY EACH PART:
- sign = 1: The neutral starting point for multiplication logic.
- if num == 0: return 0: A massive O(1) time-saver if a zero happens to be near the beginning of a huge array.
- sign *= -1: Efficiently toggles the state between 1 and -1 without needing boolean flags or counting parity manually.

KEY TECHNIQUE:
- State Tracking (Parity): Bypassing heavy arithmetic operations by extracting the only mathematical property that matters (the sign).
- Short-circuit Evaluation: Stopping a loop early when the absolute final result is already guaranteed.

EDGE CASES:
- Array with all positive numbers: The loop runs, the 'if' conditions are never met, and it cleanly returns 1.
- Array with a single 0 at index 0: Immediately returns 0 in O(1) time without checking the rest.

TIME COMPLEXITY: O(N) - In the worst-case scenario (no zeros), we evaluate every number in the array exactly once.
SPACE COMPLEXITY: O(1) - We only allocate a single integer variable ('sign') regardless of the array's size.

CONCEPTS USED:
- Parity logic
- Short-circuiting
- Array traversal
"""
