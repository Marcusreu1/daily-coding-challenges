# 2177. Find Three Consecutive Integers That Sum to a Given Number
# Difficulty: Medium
# https://leetcode.com/problems/find-three-consecutive-integers-that-sum-to-a-given-number/

"""
PROBLEM:
Given an integer num, return three consecutive integers (as a sorted array) that sum to num. 
If num cannot be expressed as the sum of three consecutive integers, return an empty array.

EXAMPLES:
Input: num = 33 → Output: [10,11,12]
Explanation: 33 can be expressed as 10 + 11 + 12 = 33.
10, 11, and 12 are 3 consecutive integers, so we return [10, 11, 12].

Input: num = 4 → Output: []
Explanation: There is no way to express 4 as the sum of 3 consecutive integers.

CONSTRAINTS:
- 0 <= num <= 10^15

MATH RULES (ALGEBRAIC REDUCTION):
Instead of searching for the numbers iteratively, we can prove the solution mathematically.
Let the three consecutive integers be represented relative to the middle integer 'x':
(x - 1), x, and (x + 1).
The sum of these three integers is: (x - 1) + x + (x + 1) = 3x.
This algebraic proof guarantees two invariant laws:
1. The target 'num' MUST be perfectly divisible by 3 (num % 3 == 0) to have a valid solution.
2. If it is divisible, the middle integer 'x' is exactly equal to num / 3.

VISUALIZATION (num = 33):
Step 1: Check divisibility. 33 % 3 == 0. (Valid).
Step 2: Find the middle element. x = 33 / 3 = 11.
Step 3: Calculate neighbors. 
  Left = 11 - 1 = 10
  Right = 11 + 1 = 12
Result: [10, 11, 12] ✓
"""

from typing import List

# STEP 1: Check if the number is perfectly divisible by 3 using the modulo operator.
# STEP 2: If it's not divisible, mathematically no consecutive integers can form it; return an empty array.
# STEP 3: If it is divisible, find the middle integer by performing integer division by 3.
# STEP 4: Return the array containing the middle integer and its immediate neighbors.

class Solution:
    def sumOfThree(self, num: int) -> List[int]:
        
        # Invariant 1: The sum of any 3 consecutive integers is always a multiple of 3.
        if num % 3 != 0:
            return []
            
        # Invariant 2: The middle integer is exactly exactly one third of the sum.
        mid = num // 3
        
        # Reconstruct the sequence mathematically.
        return [mid - 1, mid, mid + 1]

"""
WHY EACH PART:
- num % 3 != 0: Acts as a mathematical short-circuit. Instantly drops impossible targets (like 4, 5, 7, 8) in a fraction of a millisecond.
- num // 3: Uses Python's integer floor division. This avoids floating-point conversion issues, ensuring 'mid' stays as a pure integer type, even for inputs up to 10^15.

KEY TECHNIQUE:
- Algebraic Reduction: Converting a search problem or sliding window algorithm into a static algebraic formula to drop complexity from O(N) to O(1).

EDGE CASES:
- num = 0: 0 % 3 == 0. mid = 0 // 3 = 0. Returns [-1, 0, 1]. Exactly correct, as -1 + 0 + 1 = 0.
- Massive numbers (e.g., 10^15): Solved instantly since math formulas operate in constant time, avoiding Time Limit Exceeded (TLE) errors standard loops would hit.

TIME COMPLEXITY: O(1) - The algorithm performs a single modulo operation, one division, and an array instantiation. Execution time is instantaneous and entirely independent of the input size.
SPACE COMPLEXITY: O(1) - Only a single scalar integer variable ('mid') and an array of 3 integers are allocated in memory.
"""
