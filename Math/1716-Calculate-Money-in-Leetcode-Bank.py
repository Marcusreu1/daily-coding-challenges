# 1716. Calculate Money in Leetcode Bank
# Difficulty: Easy
# https://leetcode.com/problems/calculate-money-in-leetcode-bank/

"""
PROBLEM:
Hercy wants to save money for his first car. He puts money in the Leetcode bank every day.
He starts by putting in $1 on Monday, the first day. Every day from Tuesday to Sunday, he will put in $1 more than the day before. 
On every subsequent Monday, he will put in $1 more than the previous Monday.
Given n, return the total amount of money he will have in the Leetcode bank at the end of the nth day.

EXAMPLES:
Input: n = 4 → Output: 10
Explanation: After the 4th day, the total is 1 + 2 + 3 + 4 = 10.

Input: n = 10 → Output: 37
Explanation: After the 10th day, the total is (1 + 2 + 3 + 4 + 5 + 6 + 7) + (2 + 3 + 4) = 37. Notice that on the 2nd Monday, Hercy only puts in $2.

CONSTRAINTS:
- 1 <= n <= 1000

MATH RULES (ARITHMETIC PROGRESSION):
Instead of simulating the days with a loop O(n), we can use the sum formula for an arithmetic progression to achieve O(1).
Formula for the sum of an arithmetic sequence: S = (n / 2) * [2*a + (n - 1)*d]

1. Full Weeks:
   - Week 1 sum: 28
   - Week 2 sum: 35
   - Week 3 sum: 42
   - This is an arithmetic progression with a = 28, d = 7, and n = full_weeks.

2. Remaining Days:
   - The starting amount on the remaining Monday is exactly (full_weeks + 1).
   - This is another arithmetic progression with a = full_weeks + 1, d = 1, and n = remaining_days.

VISUALIZATION (n=10):
weeks = 10 // 7 = 1 full week
days = 10 % 7 = 3 remaining days

Weeks Sum:
a = 28, d = 7, n = 1
Sum = (1 / 2) * [2*28 + (1 - 1)*7] = 28

Days Sum:
a = 1 + 1 = 2, d = 1, n = 3
Sum = (3 / 2) * [2*2 + (3 - 1)*1] = (3 / 2) * [4 + 2] = 3 * 3 = 9

Total = 28 + 9 = 37 ✓
"""

# STEP 1: Calculate the number of full weeks and the remaining days using division and modulo.
# STEP 2: Calculate the total money saved during the full weeks using the AP formula.
# STEP 3: Calculate the total money saved during the extra remaining days using the AP formula.
# STEP 4: Return the sum of both calculations.

class Solution:
    def totalMoney(self, n: int) -> int:
        
        # Calculate full weeks and remaining odd days
        weeks = n // 7
        days = n % 7
        
        # Sum of the full weeks: AP with a=28, d=7, n=weeks
        weeks_sum = (weeks * (2 * 28 + (weeks - 1) * 7)) // 2
        
        # Sum of the remaining days: AP with a=(weeks + 1), d=1, n=days
        days_sum = (days * (2 * (weeks + 1) + (days - 1))) // 2
        
        # Return total savings
        return weeks_sum + days_sum

"""
WHY EACH PART:
- weeks = n // 7: Extracts exactly how many 7-day cycles fit into the given days.
- days = n % 7: Extracts the leftover days that don't make up a full week.
- integer division (//) instead of normal division (/): We use // 2 in the progression formula to ensure the result stays as an integer type without float conversion.

HOW IT WORKS (Example: n = 20):

Initial: n = 20

Execution:
├── weeks = 20 // 7 = 2
├── days = 20 % 7 = 6
├── weeks_sum = (2 * (56 + 7)) // 2 = (2 * 63) // 2 = 63
├── days_sum = (6 * (2 * (2 + 1) + 5)) // 2 = (6 * (6 + 5)) // 2 = (6 * 11) // 2 = 33
└── result = 63 + 33 = 96

Return 96 ✓

KEY TECHNIQUE:
- Math / Arithmetic Progressions: Bypassing simulation algorithms entirely by evaluating the state of the problem mathematically. 
- O(1) Optimization: Any purely formula-based approach drops iteration overhead.

EDGE CASES:
- n < 7: 'weeks' will be 0. The weeks_sum evaluates cleanly to 0, and days_sum calculates the direct sum of the first 'n' days.
- Very large n: Since no loops are used, the calculation remains instant regardless of how large n gets.

TIME COMPLEXITY: O(1) - The answer is calculated through constant-time mathematical formulas.
SPACE COMPLEXITY: O(1) - Only a few integer variables are allocated.

CONCEPTS USED:
- Arithmetic Progressions (Series Sum)
- Modulo and Floor Division
- Mathematical Simulation
"""
