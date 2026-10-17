# 2178. Maximum Split of Positive Even Integers
# Difficulty: Medium
# https://leetcode.com/problems/maximum-split-of-positive-even-integers/

"""
PROBLEM:
You are given an integer finalSum. Split it into a sum of a maximum number of unique positive even integers.
- For example, given finalSum = 12, the following splits are valid (unique positive even integers summing to finalSum): (12), (2 + 10), (2 + 4 + 6), and (4 + 8). Among them, (2 + 4 + 6) contains the maximum number of integers.
Return a list of integers that represent a valid split containing a maximum number of integers. If no valid split exists for finalSum, return an empty list.

EXAMPLES:
Input: finalSum = 12 → Output: [2,4,6]
Explanation: 2 + 4 + 6 = 12. All are unique positive even integers. It's impossible to split 12 into 4 or more even integers.

Input: finalSum = 7 → Output: []
Explanation: There are no valid splits since the sum of any even integers is always even.

Input: finalSum = 28 → Output: [2,4,6,16]
Explanation: 
Greedy extraction: 2, then 4, then 6, then 8...
28 - 2 = 26
26 - 4 = 22
22 - 6 = 16
16 - 8 = 8. 
Wait, if we take 8, remaining is 8. The next number needs to be 10, which is > 8. 
So we stop at 6. The remaining total is 16. We dump 16 into the last valid state, or just append it.
Actually, the sequence is 2, 4, 6, and the remainder is 16. 
List = [2, 4, 6, 16].

CONSTRAINTS:
- 1 <= finalSum <= 10^10

MATH RULES (PARITY & GREEDY OPTIMIZATION):
1. Parity Check: The sum of exclusively even numbers must mathematically be even. Therefore, any odd finalSum immediately returns an empty array.
2. Greedy Choice: To maximize the count of integers, we must build the sum using the absolute smallest unique even integers available in ascending order (2, 4, 6, 8...).
3. Leftover Dump: We continue subtracting the next ascending even integer until the remaining finalSum is smaller than the NEXT required even integer. When this happens, we simply add the entire remaining finalSum to the last integer we added to our list. Since the remainder is positive and even, adding it to the last element strictly increases its value, guaranteeing it will never collide with any previous elements and keeping all numbers unique.
"""

from typing import List

# STEP 1: Immediately reject any odd numbers as they violate the fundamental laws of parity.
# STEP 2: Initialize the result list and a counter starting at the smallest positive even number (2).
# STEP 3: Greedily subtract the smallest available even numbers from finalSum and add them to the list.
# STEP 4: When the remaining finalSum is too small to form a new unique even number, dump it into the last element of the list.
# STEP 5: Return the maximally split list.

class Solution:
    def maximumEvenSplit(self, finalSum: int) -> List[int]:
        
        # Fundamental parity check
        if finalSum % 2 != 0:
            return []
            
        res = []
        current_even = 2
        
        # Greedily take the smallest even numbers to maximize the length of the split
        while finalSum >= current_even:
            res.append(current_even)
            finalSum -= current_even
            current_even += 2
            
        # If there's any leftover sum that couldn't form a new unique number,
        # dump it into the last element to guarantee uniqueness and reach the exact target.
        if finalSum > 0:
            res[-1] += finalSum
            
        return res

"""
WHY EACH PART:
- finalSum % 2 != 0: Eliminates impossible edge cases in O(1) time without executing the loop.
- while finalSum >= current_even: Prevents the algorithm from subtracting a number that would leave a remainder smaller than the next required number, which would eventually lead to duplicate numbers.
- res[-1] += finalSum: The mathematical masterstroke. Because the list was strictly increasing (2, 4, 6...), adding any positive number to the last element ensures it remains strictly greater than the second-to-last element, effortlessly preserving the "unique" rule.

KEY TECHNIQUE:
- Greedy Algorithm: Making the locally optimal choice (taking the smallest possible pieces) to find the globally optimal solution (maximum number of pieces).

EDGE CASES:
- finalSum = 2: Parity passes. Loop runs once (appends 2, finalSum becomes 0). Returns [2]. Correct.
- finalSum is massive (10^10): Solved cleanly and quickly due to the mathematical scaling of the progression.

TIME COMPLEXITY: O(sqrt(N)) - Where N is finalSum. The sum of the first k even numbers is roughly k^2. Therefore, to reach a sum of N, the while loop will only execute about sqrt(N) times. For N = 10^10, the loop runs merely ~100,000 times, executing in milliseconds.
SPACE COMPLEXITY: O(sqrt(N)) - The space required for the output array scales directly with the number of elements found, which is proportional to sqrt(finalSum).
"""
