# 2028. Find Missing Observations
# Difficulty: Medium
# https://leetcode.com/problems/find-missing-observations/

"""
PROBLEM:
You have observations of n + m 6-sided dice rolls with each face numbered from 1 to 6. n of the observations went missing, and you only have the observations of m rolls. Fortunately, you have also calculated the exact average (mean) value of the n + m rolls.
You are given an integer array rolls of length m where rolls[i] is the value of the ith observation. You are also given the two integers mean and n.
Return an array of length n containing the missing observations such that the average value of the n + m rolls is exactly mean. If there are multiple valid answers, return any of them. If no such array exists, return an empty array.

EXAMPLES:
Input: rolls = [3,2,4,3], mean = 4, n = 2 → Output: [6,6]
Explanation: The mean of all n + m rolls is (3 + 2 + 4 + 3 + 6 + 6) / 6 = 24 / 6 = 4.

Input: rolls = [1,5,6], mean = 3, n = 4 → Output: [2,3,2,2]
Explanation: The mean of all n + m rolls is (1 + 5 + 6 + 2 + 3 + 2 + 2) / 7 = 21 / 7 = 3.

Input: rolls = [1,2,3,4], mean = 6, n = 4 → Output: []
Explanation: It is impossible for the mean to be 6 no matter what the 4 missing rolls are, since reaching that sum would require dice values greater than 6.

CONSTRAINTS:
- m == rolls.length
- 1 <= n, m <= 10^5
- 1 <= rolls[i], mean <= 6

MATH RULES (REVERSE AVERAGING & FAIR DISTRIBUTION):
Average is defined as Sum / Count. Therefore, the required total sum of all dice is simply Mean * (n + m).
We can find the required sum for the missing dice by subtracting the sum of the known rolls from the total sum.
Missing Sum = Total Sum - Observed Sum.

Once we have the Missing Sum, we must verify if it's possible to construct it with 'n' 6-sided dice. 
The absolute minimum sum 'n' dice can make is n (all 1s). The absolute maximum is 6*n (all 6s). If the Missing Sum falls outside this boundary, it's impossible.

If possible, we distribute the Missing Sum evenly across the 'n' dice using modular arithmetic:
- The base value for every die is: Missing Sum // n
- The remainder (leftover points) is: Missing Sum % n
We simply add 1 to the base value for 'remainder' number of dice, and keep the base value for the rest.

VISUALIZATION (rolls = [1,5,6], mean = 3, n = 4):
m = 3. Total dice = 4 + 3 = 7.
Total target sum = 3 * 7 = 21.
Observed sum = 1 + 5 + 6 = 12.
Missing sum = 21 - 12 = 9.

Validity check: n=4 <= 9 <= 6*4=24. Valid!
Base value = 9 // 4 = 2.
Remainder = 9 % 4 = 1.

Result: 1 die will be (2+1 = 3), and 3 dice will be (2).
Array: [3, 2, 2, 2] ✓
"""

from typing import List

# STEP 1: Calculate the total sum required to achieve the given mean.
# STEP 2: Calculate the sum of the missing observations algebraically.
# STEP 3: Verify if the required missing sum can physically be rolled with 'n' 6-sided dice.
# STEP 4: Calculate the uniform base value for the dice and the modulo remainder.
# STEP 5: Construct and return the array by distributing the remainder evenly.

class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        
        m = len(rolls)
        total_sum_required = mean * (n + m)
        observed_sum = sum(rolls)
        missing_sum = total_sum_required - observed_sum
        
        # Verify physical boundaries: 
        # - Minimum sum is 'n' (all 1s)
        # - Maximum sum is '6 * n' (all 6s)
        if missing_sum < n or missing_sum > 6 * n:
            return []
            
        # Distribute the required sum as evenly as possible
        base_value = missing_sum // n
        remainder = missing_sum % n
        
        # 'remainder' dice get base_value + 1 to absorb the modulo. 
        # The remaining (n - remainder) dice just get the base_value.
        result = [base_value + 1] * remainder + [base_value] * (n - remainder)
        
        return result

"""
WHY EACH PART:
- missing_sum < n or missing_sum > 6 * n: Acts as the absolute mathematical gatekeeper. It prevents logic errors like trying to assign dice with value 7 or 0.
- base_value = missing_sum // n: Finds the integer floor distribution securely without using floats.
- [base_value + 1] * remainder + [base_value] * (n - remainder): Python's list multiplication allows us to build the complete array in a highly optimized C-level operation, avoiding manual for-loops.

KEY TECHNIQUE:
- Algebraic Inversion: Working backwards from an expected result (mean) to find hidden variables.
- Greedy Distribution: Using division and modulo to flatten values evenly in O(1) logical steps.

EDGE CASES:
- Perfect division (e.g., missing_sum = 12, n = 4): base=3, remainder=0. Array becomes [3]*0 + [3]*4 = [3, 3, 3, 3]. Perfect safety.
- Impossible high mean (e.g., mean = 6, but rolls sum is too low): Handled flawlessly by the boundary `missing_sum > 6 * n` check, returning [].

TIME COMPLEXITY: O(m + n) - We traverse the observed rolls once to sum them O(m), and then we instantiate the resulting array of length n in O(n).
SPACE COMPLEXITY: O(1) auxiliary space - The logic uses scalar math variables. The O(n) space is strictly for the output required by the problem.

CONCEPTS USED:
- Statistics & Averages
- Array Generation
- Modular Arithmetic
"""
