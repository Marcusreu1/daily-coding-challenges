# 1390. Four Divisors
# Difficulty: Medium
# https://leetcode.com/problems/four-divisors/

"""
PROBLEM:
Given an integer array `nums`, return the sum of divisors of the integers in that array 
that have exactly four divisors. If there is no such integer in the array, return 0.

EXAMPLES:
Input: nums = [21,4,7]
Output: 32
(Explanation: 
21 has 4 divisors: 1, 3, 7, 21. (Sum = 32)
4 has 3 divisors: 1, 2, 4.
7 has 2 divisors: 1, 7.
The answer is the sum of divisors of 21 only.)

Input: nums = [21,21]
Output: 64
(Explanation: Both 21s have exactly four divisors. 32 + 32 = 64)

Input: nums = [1,2,3,4,5]
Output: 0
(Explanation: No numbers have exactly four divisors.)

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- 1 <= nums[i] <= 10^5

ALGORITHM LOGIC (Square Root Divisor Counting & Early Exit):
1. For each number, we only need to scan for divisors up to its square root (sqrt(N)).
2. Every time we find a divisor `i`, its paired divisor is automatically `N // i`.
3. We add both divisors to a local sum and increase the divisor count by 2 
   (ensuring we handle exact square roots carefully so we don't count the same number twice).
4. If at any point the divisor count exceeds 4, we strictly abort the check for that number using a `break` statement. This is a massive optimization.
5. If the count is exactly 4 after the inner loop finishes, we add the local sum to the global total.

VISUALIZATION (num = 21):
Limit = isqrt(21) = 4

i = 1: 21 % 1 == 0. Found [1, 21].
current_sum = 22, div_count = 2

i = 2: 21 % 2 != 0. Ignore.

i = 3: 21 % 3 == 0. Found [3, 7].
current_sum = 32, div_count = 4

i = 4: 21 % 4 != 0. Ignore.

Loop ends. div_count == 4? Yes! Add 32 to total_sum. ✓
"""

import math

# STEP 1: Initialize the global accumulator for valid divisor sums
# STEP 2: Loop through each integer in the `nums` array
# STEP 3: Find divisors strictly up to the integer square root of the number
# STEP 4: Sum pairs of divisors and increment the counter
# STEP 5: Apply early exit (break) if the count exceeds 4 to save computational time
# STEP 6: If exactly 4 divisors were found, commit the local sum to the global total

class Solution:
    def sumFourDivisors(self, nums: list[int]) -> int:
        
        total_sum = 0
        
        for num in nums:
            current_sum = 0
            div_count = 0
            
            # The mathematical boundary for distinct divisor pairs
            limit = math.isqrt(num)
            
            for i in range(1, limit + 1):
                
                if num % i == 0:                                     # We found a valid divisor
                    
                    current_sum += i
                    div_count += 1
                    
                    if i != num // i:                                # Check for the paired divisor (avoiding perfect square duplicates)
                        current_sum += (num // i)
                        div_count += 1
                        
                    if div_count > 4:                                # Early exit optimization: Invalidates the number immediately
                        break
            
            if div_count == 4:                                       # Strictly check for the 'exactly 4' condition
                total_sum += current_sum
                
        return total_sum

"""
WHY EACH PART:
- limit = math.isqrt(num): Limits the iterations drastically. For 10^5, it loops at most 316 times instead of 100,000 times.
- if i != num // i: Prevents adding the root twice for perfect squares (like 4, 9, 16). For `num = 4`, `i = 2`, `4 // 2 = 2`. The `if` prevents `2` from being counted as two different divisors.
- if div_count > 4: break: Without this, highly composite numbers (like 720720) would force the loop to process all their pairs wastefully when we already know they are disqualified.
- if div_count == 4: Ensures we drop numbers with 1, 2, or 3 divisors (like prime numbers or small squares).

HOW IT WORKS (Example: num = 8):
limit = isqrt(8) = 2.
i = 1: Divisors [1, 8]. count = 2, sum = 9.
i = 2: Divisors [2, 4]. count = 4, sum = 15.
End loop. count == 4. Total sum += 15. ✓

KEY TECHNIQUE:
- Square Root Mathematical Boundary
- Short-Circuiting (Poda de procesamiento)
- Coupled state tracking (counting and summing simultaneously)

EDGE CASES:
- num = 1: isqrt(1) = 1. i=1. count=1. Does not trigger `div_count == 4`. Returns 0. ✓
- Prime numbers (e.g., 7): Only divisible by 1 and itself. Count will be 2. Discarded. ✓

TIME COMPLEXITY: O(N * sqrt(M)) - Where N is the length of the `nums` array and M is the maximum value in `nums` (10^5). In the absolute worst case, we run the inner loop 316 times for 10,000 numbers, which is roughly 3 million operations. This executes seamlessly well within the time limit.
SPACE COMPLEXITY: O(1) - No extra scaling arrays are used. We only track a few integer variables in memory.
"""
