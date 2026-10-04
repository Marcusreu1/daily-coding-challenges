# 2110. Number of Smooth Descent Periods of a Stock
# Difficulty: Medium
# https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/

"""
PROBLEM:
You are given an integer array prices representing the daily price of a stock.
A smooth descent period of a stock consists of one or more contiguous days such that the price on each day is lower than the price on the preceding day by exactly 1. 
The first day of the period is exempted from this rule.
Return the number of smooth descent periods.

EXAMPLES:
Input: prices = [3,2,1,4] → Output: 7
Explanation: There are 7 smooth descent periods:
[3], [2], [1], [4], [3,2], [2,1], and [3,2,1]
Note that a period with one day is a smooth descent period by the definition.

Input: prices = [8,6,7,7] → Output: 4
Explanation: There are 4 smooth descent periods: [8], [6], [7], and [7].
No two contiguous days have a price difference of exactly 1.

CONSTRAINTS:
- 1 <= prices.length <= 10^5
- 1 <= prices[i] <= 10^5

MATH RULES (DYNAMIC ACCUMULATION & COMBINATORICS):
Instead of finding the total length of a strictly decreasing subarray 'L' and applying Gauss's formula (L * (L + 1) / 2) at the end, we can count the combinations on the fly.
If the current day continues a smooth descent, the number of NEW valid subarrays ending strictly on this day is exactly equal to the current streak length.
If the streak breaks, the current streak resets to 1 (since a single day is a valid period of length 1).
We just maintain a running counter of the current streak and add it to our total periods every single day.

VISUALIZATION (prices = [3, 2, 1, 4]):
Day 0 (Price 3): Streak = 1. Total = 1. (Subarray: [3])
Day 1 (Price 2): 2 == 3 - 1. Streak = 2. Total = 1 + 2 = 3. (New Subarrays: [2], [3,2])
Day 2 (Price 1): 1 == 2 - 1. Streak = 3. Total = 3 + 3 = 6. (New Subarrays: [1], [2,1], [3,2,1])
Day 3 (Price 4): 4 != 1 - 1. Streak resets to 1. Total = 6 + 1 = 7. (New Subarray: [4])

Result: 7 ✓
"""

from typing import List

# STEP 1: Initialize the total combinations and the current streak starting with the first day.
# STEP 2: Iterate through the array starting from the second day (index 1).
# STEP 3: If the current price is exactly 1 less than the previous day's price, increment the streak.
# STEP 4: If the pattern breaks, reset the streak to 1.
# STEP 5: Add the current streak to the total periods. Return the total at the end.

class Solution:
    def getDescentPeriods(self, prices: List[int]) -> int:
        
        # Start with 1 because the first element (index 0) is inherently a period of length 1
        total_periods = 1
        current_streak = 1
        
        # O(N) Traversal starting from day 2
        for i in range(1, len(prices)):
            
            # Check the mathematical condition for a smooth descent
            if prices[i] == prices[i - 1] - 1:
                current_streak += 1
            else:
                # The descent breaks, reset the streak
                current_streak = 1
                
            # Accumulate the new sub-combinations formed ending at this specific day
            total_periods += current_streak
            
        return total_periods

"""
WHY EACH PART:
- range(1, len(prices)): Starting at index 1 prevents index-out-of-bounds errors when checking `prices[i - 1]`.
- current_streak = 1 (on reset): A streak never drops to 0 because every individual number represents a valid subarray of length 1 according to the problem rules.
- total_periods += current_streak: The core combinatorics engine. It seamlessly bypasses complex nested loops by relying on the mathematical property that a sequence of length N introduces exactly N new contiguous subsequences ending at its tail.

KEY TECHNIQUE:
- On-the-fly Combinatorics (Dynamic Accumulation): Translating a localized contiguous condition into a global combination count instantly.
- State Tracking: Managing minimal state (just one streak variable) to determine the mathematical weight of the current iteration.

EDGE CASES:
- Array of length 1 (e.g., [5]): Loop does not execute. Returns total_periods = 1. Correct.
- Array with identical consecutive numbers (e.g., [4, 4]): The mathematical condition `4 == 4 - 1` fails. Streak resets. Returns 2. Correct.

TIME COMPLEXITY: O(N) - We iterate through the 'prices' array exactly once.
SPACE COMPLEXITY: O(1) - Only two integer scalar variables are allocated regardless of the input size.
"""
