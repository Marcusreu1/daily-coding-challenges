# 2119. A Number After a Double Reversal
# Difficulty: Easy
# https://leetcode.com/problems/a-number-after-a-double-reversal/

"""
PROBLEM:
Reversing an integer means to reverse all its digits.
For example, reversing 2021 gives 1202. Reversing 12300 gives 321 as the leading zeros are not retained.
Given an integer num, reverse num to get reversed1, then reverse reversed1 to get reversed2. 
Return true if reversed2 equals num. Otherwise return false.

EXAMPLES:
Input: num = 526 → Output: true
Explanation: Reverse num to get 625, then reverse 625 to get 526, which equals num.

Input: num = 1800 → Output: false
Explanation: Reverse num to get 81, then reverse 81 to get 18, which does not equal num.

Input: num = 0 → Output: true
Explanation: Reverse num to get 0, then reverse 0 to get 0, which equals num.

CONSTRAINTS:
- 0 <= num <= 10^6

MATH RULES (INFORMATION LOSS & MODULO ARITHMETIC):
Simulating the reversals by converting integers to strings and back is highly inefficient (O(N) time and space).
Instead, we analyze the invariant: A number will only change after a double reversal if information is lost during the first reversal.
Information is ONLY lost when a number generates leading zeros in the first reversal, because standard integers cannot hold leading zeros.
A number will generate a leading zero upon reversal if and only if it ends with a trailing zero (e.g., 120 -> 21).
Therefore, any number ending in 0 (where num % 10 == 0) will return False.
The only mathematical exception to this rule is the number 0 itself, which remains 0 after infinite reversals.
"""

# STEP 1: Check if the number is exactly 0. If so, it perfectly survives a double reversal.
# STEP 2: Use modulo 10 to extract the last digit. If it is NOT 0, the number will survive.
# STEP 3: Return the evaluation of these logical conditions directly.

class Solution:
    def isSameAfterReversals(self, num: int) -> bool:
        
        # A number survives if it is 0, OR if its last digit is not 0.
        return num == 0 or num % 10 != 0

"""
WHY EACH PART:
- num == 0: The explicit edge case. 0 reversed is 0.
- num % 10 != 0: The modulo operator is the fastest way to extract the tail of an integer. If the remainder of dividing by 10 is not 0, the number does not end in 0.
- or: Short-circuit logical operator. If num == 0 is True, Python skips the modulo calculation entirely, returning True instantly.

KEY TECHNIQUE:
- O(1) Mathematical Deduction: Bypassing simulation algorithms by identifying the terminal conditions of the system.

EDGE CASES:
- num = 0: Correctly caught by `num == 0`, returning True.
- Single digit numbers (1-9): 5 % 10 = 5. 5 != 0 is True. Returns True safely.
- Massive numbers ending in zero (e.g., 1000000): 1000000 % 10 = 0. 0 != 0 is False. Returns False instantly without building giant strings in memory.

TIME COMPLEXITY: O(1) - The modulo operation and logical comparisons take constant time. It executes in a fraction of a millisecond.
SPACE COMPLEXITY: O(1) - No extra variables, arrays, or strings are allocated in memory.
"""
