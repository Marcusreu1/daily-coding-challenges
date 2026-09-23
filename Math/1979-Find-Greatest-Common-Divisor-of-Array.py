# 1979. Find Greatest Common Divisor of Array
# Difficulty: Easy
# https://leetcode.com/problems/find-greatest-common-divisor-of-array/

"""
PROBLEM:
Given an integer array nums, return the greatest common divisor of the smallest number and largest number in nums.
The greatest common divisor of two numbers is the largest positive integer that evenly divides both numbers.

EXAMPLES:
Input: nums = [2,5,6,9,10] → Output: 2
Explanation:
The smallest number in nums is 2.
The largest number in nums is 10.
The greatest common divisor of 2 and 10 is 2.

Input: nums = [7,5,6,8,3] → Output: 1
Explanation:
The smallest number in nums is 3.
The largest number in nums is 8.
The greatest common divisor of 3 and 8 is 1.

Input: nums = [3,3] → Output: 3
Explanation:
The smallest number in nums is 3.
The largest number in nums is 3.
The greatest common divisor of 3 and 3 is 3.

CONSTRAINTS:
- 2 <= nums.length <= 1000
- 1 <= nums[i] <= 1000

MATH RULES (EUCLIDEAN ALGORITHM):
To find the Greatest Common Divisor (GCD) without checking every number in a loop, we rely on the Euclidean Algorithm.
The principle states that gcd(a, b) = gcd(b, a % b).
By repeatedly applying the modulo operator until the remainder is 0, the last non-zero divisor is mathematically proven to be the GCD.
Python's built-in `math.gcd(a, b)` function implements this exact algorithm at the C-level, making it extremely fast (O(log(min(a, b)))).

VISUALIZATION (nums = [8, 5, 6, 12, 3]):
Step 1: Find extremes
  smallest = 3
  largest = 12

Step 2: Calculate GCD using Euclidean logic mathematically:
  a = 12, b = 3
  12 % 3 = 0.
  Since remainder is 0, the GCD is 3.

Result: 3 ✓
"""

import math
from typing import List

# STEP 1: Find the smallest element in the array using the built-in min() function.
# STEP 2: Find the largest element in the array using the built-in max() function.
# STEP 3: Return the calculated Greatest Common Divisor using the optimized math.gcd() function.

class Solution:
    def findGCD(self, nums: List[int]) -> int:
        
        # O(N) operations to find the extremes
        smallest = min(nums)
        largest = max(nums)
        
        # O(log(min(smallest, largest))) operation using the Euclidean algorithm
        return math.gcd(smallest, largest)

"""
WHY EACH PART:
- min(nums) / max(nums): Python's native implementations are written in C, making them significantly faster than writing a manual `for` loop to find the minimum and maximum values.
- math.gcd(): Encapsulates the Euclidean Algorithm perfectly, avoiding the need to write the standard `while b: a, b = b, a % b` logic manually.

KEY TECHNIQUE:
- Array Traversal: Finding bounding values (min/max) linearly.
- Euclidean Algorithm: Using Number Theory to bypass O(N) naive looping for common divisors.

EDGE CASES:
- Array where all elements are the same (e.g., [3, 3, 3]): min and max will both be 3. math.gcd(3, 3) returns 3 correctly.
- Co-prime numbers (e.g., smallest is 3, largest is 8): math.gcd(3, 8) evaluates to 1, which perfectly aligns with the mathematical definition of co-primes.

TIME COMPLEXITY: O(N) - Traversing the array to find the minimum and maximum takes O(N) time. The GCD calculation takes O(log(min_val)) which is practically instantaneous and treated as O(1) in this context.
SPACE COMPLEXITY: O(1) - Only scalar integer variables are used. No extra space is allocated.

CONCEPTS USED:
- Number Theory
- Euclidean Algorithm
- Array Min/Max bounds
"""
