# 2160. Minimum Sum of Four Digit Number After Splitting Digits
# Difficulty: Easy
# https://leetcode.com/problems/minimum-sum-of-four-digit-number-after-splitting-digits/

"""
PROBLEM:
You are given a positive four-digit integer num consisting of digits from 0 to 9.
Split num into two new integers new1 and new2 by using the digits found in num. 
Leading zeros are allowed in new1 and new2, and all the digits found in num must be used.
Return the minimum possible sum of new1 and new2.

EXAMPLES:
Input: num = 2932 → Output: 52
Explanation:
Digits: [2, 2, 3, 9].
Pairs: 29 and 23.
Sum = 29 + 23 = 52.

Input: num = 4009 → Output: 13
Explanation:
Digits: [0, 0, 4, 9].
Pairs: 04 and 09.
Sum = 4 + 9 = 13.

CONSTRAINTS:
- 1000 <= num <= 9999

MATH RULES (POSITIONAL NOTATION & GREEDY SELECTION):
Any two-digit number can be represented as 10 * tens + units.
If we split four digits into two 2-digit numbers:
Total Sum = (10 * a + c) + (10 * b + d) = 10 * (a + b) + (c + d).
Splitting into a 1-digit and a 3-digit number yields 100 * a + 10 * b + c + d, 
which introduces a weight factor of 100, strictly increasing the total sum.
Therefore, splitting evenly into two 2-digit numbers is always optimal.
To minimize 10 * (a + b) + (c + d):
- The tens positions (weight 10) must take the two smallest available digits.
- The units positions (weight 1) take the two remaining larger digits.
"""

# STEP 1: Extract all 4 digits and sort them in ascending order: d0 <= d1 <= d2 <= d3.
# STEP 2: Assign d0 and d1 to the tens places, and d2 and d3 to the units places.
# STEP 3: Compute and return 10 * (d0 + d1) + d2 + d3.

class Solution:
    def minimumSum(self, num: int) -> int:
        
        # Sort the four digits in ascending order
        digits = sorted(int(d) for d in str(num))
        
        # Multiply the two smallest digits by 10 (tens place) and add the remaining two (units place)
        return 10 * (digits[0] + digits[1]) + digits[2] + digits[3]

"""
WHY EACH PART:
- sorted(int(d) for d in str(num)): Extracts and sorts all 4 digits. Sorting 4 elements takes negligible constant time.
- 10 * (digits[0] + digits[1]) + digits[2] + digits[3]: Implements the minimized positional formula directly without needing string concats or temporary number variables.

KEY TECHNIQUE:
- Positional Weight Minimization: Reducing linear combinations by assigning the smallest coefficients to the largest algebraic weights.
- Greedy Choice Property: Sorting guarantees locally optimal placement yields the globally optimal minimum sum.

EDGE CASES:
- Leading zeros (e.g., 4009): Digits sort to [0, 0, 4, 9]. Formula yields 10*(0 + 0) + 4 + 9 = 13. Handled seamlessly.
- Identical digits (e.g., 2222): Digits sort to [2, 2, 2, 2]. 10*(2 + 2) + 2 + 2 = 44. Correct.

TIME COMPLEXITY: O(1) - The input size is strictly fixed at 4 digits. Sorting 4 items takes constant operations.
SPACE COMPLEXITY: O(1) - A list of size 4 is allocated in memory.
"""
