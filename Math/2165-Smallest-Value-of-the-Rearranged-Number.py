# 2165. Smallest Value of the Rearranged Number
# Difficulty: Medium
# https://leetcode.com/problems/smallest-value-of-the-rearranged-number/

"""
PROBLEM:
You are given an integer num. Rearrange the digits of num such that its value is minimized and it does not contain any leading zeros.
Return the rearranged number with minimal value.
Note that the sign of the number does not change after rearranging the digits.

EXAMPLES:
Input: num = 310 → Output: 103
Explanation: The possible arrangements for the digits of 310 are 013, 031, 103, 130, 301, 310. 
The arrangement with the smallest value that does not contain any leading zeros is 103.

Input: num = -7605 → Output: -7650
Explanation: Some possible arrangements for the digits of -7605 are -7650, -6705, -5076, -0567.
The arrangement with the smallest value that does not contain any leading zeros is -7650.

CONSTRAINTS:
- -10^15 <= num <= 10^15

MATH RULES (GREEDY SORTING & ZERO DISPLACEMENT):
The problem requires handling positive and negative numbers with completely inverse logic.
1. Negative Numbers: To make a negative number as small as possible (furthest to the left on the number line), its absolute value must be as large as possible. Therefore, we sort the digits in purely descending order (e.g., 98760). Leading zeros are naturally impossible here because 0 is the smallest digit and will always end up at the back.
2. Positive Numbers: To make a positive number as small as possible, we sort its digits in ascending order. However, this groups all '0's at the absolute front, creating illegal leading zeros.
To fix this efficiently:
- Sort ascending (e.g., ['0', '0', '3', '5'])
- Find the first non-zero digit (which is '3' at index 2).
- Swap it with the digit at index 0. (Result: ['3', '0', '0', '5']).
This single O(1) swap perfectly constructs the optimal legal number.
"""

# STEP 1: Handle the edge case where num is 0 instantly.
# STEP 2: If the number is negative, sort its digits descending and append the negative sign.
# STEP 3: If the number is positive, sort its digits ascending.
# STEP 4: Resolve leading zeros by finding the first non-zero digit and swapping it with index 0.
# STEP 5: Join the characters, convert back to an integer, and return.

class Solution:
    def smallestNumber(self, num: int) -> int:
        
        if num == 0:
            return 0
            
        if num < 0:
            # For negative numbers, maximize the absolute value (sort descending)
            # -num converts the number to positive to extract digits cleanly
            digits = sorted(str(-num), reverse=True)
            return -int("".join(digits))
            
        else:
            # For positive numbers, minimize the value (sort ascending)
            digits = sorted(str(num))
            
            # Resolve leading zeros
            for i in range(len(digits)):
                if digits[i] != '0':
                    # Swap the first non-zero digit with the leading zero
                    digits[0], digits[i] = digits[i], digits[0]
                    break
                    
            return int("".join(digits))

"""
WHY EACH PART:
- sorted(str(-num), reverse=True): Safely bypasses the negative sign '-' during string sorting, preventing it from being treated as a character.
- digits[0], digits[i] = digits[i], digits[0]: Python's elegant tuple unpacking swaps elements in place in O(1) time without needing a temporary variable.
- break: Ensures that only the FIRST non-zero digit is swapped, preserving the ascending order of the rest of the digits.

KEY TECHNIQUE:
- Greedy Strategy: Arranging components by positional weight to deterministically construct a max/min bound.
- In-place Array Manipulation: Fixing state invalidations (leading zeros) using minimal swap operations instead of array slicing.

EDGE CASES:
- num = 0: Immediately caught and returned.
- Number with multiple zeros (e.g., 2000): Sorted is ['0', '0', '0', '2']. First non-zero is at index 3. Swap results in ['2', '0', '0', '0']. Reconstructs to 2000 perfectly.

TIME COMPLEXITY: O(D log D) - Where D is the number of digits in `num`. Since `num` fits within a 64-bit integer, D is at most 15. Sorting 15 characters takes effectively O(1) time.
SPACE COMPLEXITY: O(D) - A list of up to 15 characters is allocated in memory, which is equivalent to O(1) auxiliary space.
"""
