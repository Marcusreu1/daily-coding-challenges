# 2048. Next Greater Numerically Balanced Number
# Difficulty: Medium
# https://leetcode.com/problems/next-greater-numerically-balanced-number/

"""
PROBLEM:
An integer x is numerically balanced if for every digit d in the number x, there are exactly d occurrences of that digit in x.
Given an integer n, return the smallest numerically balanced number strictly greater than n.

EXAMPLES:
Input: n = 1 → Output: 22
Explanation: 22 is balanced since 2 appears exactly 2 times. It is the smallest balanced number strictly greater than 1.

Input: n = 1000 → Output: 1333
Explanation: 1333 is balanced (1 appears once, 3 appears three times).

Input: n = 3000 → Output: 3133
Explanation: 3133 is balanced.

CONSTRAINTS:
- 0 <= n <= 10^6

MATH RULES (SEARCH SPACE BOUNDING & EARLY PRUNING):
Since n <= 10^6, the absolute largest output we will ever generate is the smallest balanced 7-digit number.
A 7-digit balanced number requires its constituent digits' frequencies to sum to 7. The optimal smallest combination is one '1', two '2's, and four '4's.
Sorted ascending, the absolute maximum answer is 1,224,444.
A brute force search from n+1 up to 1,224,444 is perfectly optimal for O(1) space if the validation function is heavily optimized.

To optimize the validation, we avoid expensive string conversions and use mathematical modulo operations.
We implement Early Stopping (Pruning):
1. '0' can never exist in a balanced number (it must appear 0 times, but its presence means it appeared at least once).
2. If the current count of a digit exceeds its numerical value while parsing, the number is instantly invalid.
"""

# STEP 1: Define a highly optimized helper function to check if a number is numerically balanced.
# STEP 2: Use integer math (modulo 10 and floor division) to extract and tally digits.
# STEP 3: Implement early stopping conditions (presence of 0, or count exceeding the digit's value).
# STEP 4: After tallying, verify that all present digits meet the exact frequency requirement.
# STEP 5: In the main function, start searching from n + 1 indefinitely until the helper returns True.

class Solution:
    def nextBeautifulNumber(self, n: int) -> int:
        
        # Helper function to validate numerical balance
        def is_balanced(num: int) -> bool:
            # Array to store frequencies of digits 0-9
            counts = [0] * 10
            
            temp = num
            # Phase 1: Extract digits and prune impossible numbers instantly
            while temp > 0:
                digit = temp % 10
                
                # A balanced number can never contain the digit 0
                if digit == 0:
                    return False
                    
                counts[digit] += 1
                
                # Early Pruning: If a digit appears more times than its value, it's invalid
                if counts[digit] > digit:
                    return False
                    
                temp //= 10
                
            # Phase 2: Verify all present digits have the exact required frequency
            for i in range(1, 10):
                if counts[i] > 0 and counts[i] != i:
                    return False
                    
            return True
            
        # STEP 5: Search for the next valid number starting at n + 1
        current = n + 1
        while True:
            if is_balanced(current):
                return current
            current += 1

"""
WHY EACH PART:
- counts = [0] * 10: Fixed-size array is massively faster than importing Counter or creating Hash Maps for single digits.
- temp % 10 / temp //= 10: Pure mathematical extraction avoids string memory allocation and string-to-int parsing latency.
- if counts[digit] > digit: The most powerful optimization. If the number is 44444..., it fails the moment the fifth '4' is read, saving computation cycles.

KEY TECHNIQUE:
- Search Space Bounding: Knowing the maximum possible answer ensures our while loop isn't a hazard.
- Fast Mathematical Validation: Using early breaks and avoiding string conversions inside heavy loops.

EDGE CASES:
- n = 0: current starts at 1, fails. current = 2, fails. ... current = 22 -> Valid! Returns 22.
- Worst-case maximum n = 1,000,000: Loop cleanly executes up to 1,224,444 and returns safely.

TIME COMPLEXITY: O(M) - Where M is the distance between `n` and the next balanced number. In the worst case, M is roughly 224,000. Inside the loop, checking takes at most 7 basic integer operations. It executes virtually instantly.
SPACE COMPLEXITY: O(1) - Only integer variables and an array of 10 integers are allocated.
"""
