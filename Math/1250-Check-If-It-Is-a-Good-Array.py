# 1250. Check If It Is a Good Array
# Difficulty: Hard
# https://leetcode.com/problems/check-if-it-is-a-good-array/

"""
PROBLEM:
Given an array nums of positive integers. Your task is to select some subset of nums, 
multiply each element by an integer and add all these numbers. 
The array is said to be good if you can obtain a sum of 1 from the array by any 
possible subset and multiplicand. Return True if the array is good, otherwise return False.

EXAMPLES:
Input: nums = [12,5,7,23]    → Output: True
(Explanation: Pick 5 and 7. 5*3 + 7*(-2) = 15 - 14 = 1)

Input: nums = [29,6,10]      → Output: True
(Explanation: Pick 29, 6 and 10. 29*1 + 6*(-3) + 10*(-1) = 29 - 18 - 10 = 1)

Input: nums = [3,6]          → Output: False
(Explanation: The GCD of 3 and 6 is 3. Any linear combination of them will be a multiple of 3. 
You can never reach 1.)

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9

ALGORITHM LOGIC (Bézout's Identity):
1. According to Bézout's Identity, the smallest positive integer that can be expressed as 
   a linear combination (ax + by) of two integers 'a' and 'b' is their Greatest Common Divisor (GCD).
2. The problem asks if we can reach exactly 1. This means the GCD of our chosen subset MUST be 1.
3. Adding more numbers to a subset can only DECREASE or MAINTAIN the overall GCD. It can never increase it.
4. Therefore, to maximize our chances of getting a GCD of 1, we should just calculate the GCD of the ENTIRE array.
5. If the GCD of the entire array is 1, return True. Otherwise, return False.

VISUALIZATION (nums = [12, 5, 7, 23]):

Iter  | Num | Operation       | current_gcd | Target Reached?
-------------------------------------------------------------
Init  | 12  | Start           |     12      |       No
  1   |  5  | GCD(12, 5)      |      1      |  YES! (12 and 5 are coprime)
 
We can early return True at index 1 without even checking 7 and 23.
"""

import math

# STEP 1: Initialize current_gcd with the first element of the array
# STEP 2: Iterate through the rest of the array
# STEP 3: Update current_gcd with the GCD of itself and the current number
# STEP 4: Early exit - if current_gcd becomes 1, return True immediately
# STEP 5: If the loop finishes and current_gcd is not 1, return False

class Solution:
    def isGoodArray(self, nums: list[int]) -> bool:
        
        current_gcd = nums[0]                                        # Start with the first number
        
        if current_gcd == 1:                                         # Edge case: If the first number is 1
            return True
            
        for i in range(1, len(nums)):                                # Loop through the rest of the numbers
            
            current_gcd = math.gcd(current_gcd, nums[i])             # Calculate new GCD cumulatively
            
            if current_gcd == 1:                                     # If we hit 1, we found a coprime subset
                return True
                
        return current_gcd == 1                                      # Return True if final GCD is 1, else False

"""
WHY EACH PART:
- import math: Python's built-in math module has a highly optimized GCD function using the Euclidean algorithm.
- current_gcd = nums[0]: We need a baseline to start comparing. The GCD of a single number is the number itself.
- if current_gcd == 1: (Inside the loop) This is a crucial performance optimization. Since GCD can never grow, once it hits 1, it will stay 1 forever. No need to process the remaining thousands of numbers.
- return current_gcd == 1: If the loop completes without hitting 1, this safely evaluates to False (e.g., if all numbers were multiples of 2, the final GCD would be >= 2).

HOW IT WORKS (Example: nums = [6, 10, 15]):
Index 0: current_gcd = 6
Index 1: math.gcd(6, 10) = 2. current_gcd becomes 2. (Not 1 yet)
Index 2: math.gcd(2, 15) = 1. current_gcd becomes 1. 
Hit condition! Return True. ✓
(Explanation: 6, 10, and 15 don't share a common divisor across all three. 6 and 10 share 2. 10 and 15 share 5. 6 and 15 share 3. But together, their GCD is 1).

KEY TECHNIQUE:
- Mathematics (Number Theory): Recognizing that "linear combinations of a subset" directly translates to Bézout's Identity.
- Cumulative Reduction: Using an accumulator variable to track a property (GCD) that shrinks monotonically.

EDGE CASES:
- Array with one element ([1]): Returns True. ✓
- Array with one element ([5]): Returns False. ✓
- Array containing a 1 anywhere ([100, 200, 1, 300]): Reaches the 1, becomes 1, returns True early. ✓
- Large numbers with no common divisor ([2147483647, 2147483646]): Returns True efficiently. ✓

TIME COMPLEXITY: O(N * log(min(A, B))) - Where N is the length of the array, and log(min(A, B)) is the time complexity of the Euclidean algorithm for GCD. Because of the early exit, it often runs in O(1) best-case time.
SPACE COMPLEXITY: O(1) - We only use a single variable `current_gcd` regardless of the input size.

CONCEPTS USED:
- Bézout's Identity
- Greatest Common Divisor (GCD)
- Early Exit / Pruning
- Euclidean Algorithm (under the hood of math.gcd)
"""
