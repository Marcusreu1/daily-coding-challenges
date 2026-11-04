# 2455. Average Value of Even Numbers That Are Divisible by Three
# Difficulty: Easy
# https://leetcode.com/problems/average-value-of-even-numbers-that-are-divisible-by-three/

"""
PROBLEM:
Given an integer array nums of positive integers, return the average value of all even integers that are divisible by 3.
Note that the average of n elements is the sum of the n elements divided by n and rounded down to the nearest integer.
If there are no such elements, return 0.

EXAMPLES:
Input: nums = [1,3,6,10,12,15] → Output: 9
Explanation: 6 and 12 are even numbers that are divisible by 3. (6 + 12) / 2 = 9.

Input: nums = [1,2,4,7,10] → Output: 0
Explanation: There is no single number that satisfies both conditions, so return 0.

CONSTRAINTS:
- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 1000

MATH RULES (LEAST COMMON MULTIPLE OPTIMIZATION):
A naive approach would evaluate two separate modulo conditions per iteration: (num % 2 == 0) and (num % 3 == 0).
By applying the Least Common Multiple (LCM) theorem from number theory, we know that if a number is divisible by 2 coprime integers, it must be exactly divisible by their product (2 * 3 = 6).
Therefore, any "even number divisible by 3" is mathematically just a "multiple of 6". 
This abstraction collapses the conditional branching into a single, faster operation: (num % 6 == 0).
"""

from typing import List

# STEP 1: Initialize accumulators for the total sum and the valid element count.
# STEP 2: Iterate linearly through the array.
# STEP 3: Apply the LCM optimization to filter multiples of 6.
# STEP 4: Add passing values to the sum and increment the counter.
# STEP 5: Return the integer average safely, guarding against division by zero.

class Solution:
    def averageValue(self, nums: List[int]) -> int:
        
        total_sum = 0
        count = 0
        
        for num in nums:
            # Single condition applying LCM(2, 3) = 6
            if num % 6 == 0:
                total_sum += num
                count += 1
                
        # Safe integer division return using a ternary operator
        return total_sum // count if count > 0 else 0

"""
WHY EACH PART:
- num % 6 == 0: Halves the ALU branching computations by merging the conditions geometrically.
- total_sum // count: Python's floor division operator ensures the average is automatically rounded down to an integer, matching the problem requirements without needing the math.floor() library.
- if count > 0 else 0: Essential guard clause to prevent ZeroDivisionError in arrays where no elements match the filter.

KEY TECHNIQUE:
- Arithmetic Reduction: Simplifying multi-conditional logic using properties of prime factorization.
- Single Pass Aggregation: Calculating sums and counts simultaneously without allocating secondary arrays to store valid numbers.

EDGE CASES:
- Empty result set (e.g., [1, 2, 4, 5]): The condition is never met, count remains 0, ternary safely catches and returns 0.
- Array with zeros (if constraint allowed 0): 0 % 6 == 0 is True, adding 0 to sum and 1 to count, correctly factoring 0 into the average mathematically.

TIME COMPLEXITY: O(N) - Where N is the length of the array. The array is traversed exactly once.
SPACE COMPLEXITY: O(1) - Only two scalar integer variables are tracked in memory.
"""
