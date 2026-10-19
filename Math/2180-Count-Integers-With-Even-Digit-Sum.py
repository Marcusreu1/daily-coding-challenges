# 2180. Count Integers With Even Digit Sum
# Difficulty: Easy
# https://leetcode.com/problems/count-integers-with-even-digit-sum/

"""
PROBLEM:
Given a positive integer num, return the number of positive integers less than or equal to num whose digit sums are even.
The digit sum of a positive integer is the sum of all its digits.

EXAMPLES:
Input: num = 4 → Output: 2
Explanation:
The only integers less than or equal to 4 whose digit sums are even are 2 and 4.    

Input: num = 30 → Output: 14
Explanation:
The 14 integers less than or equal to 30 whose digit sums are even are
2, 4, 6, 8, 11, 13, 15, 17, 19, 20, 22, 24, 26, and 28.

CONSTRAINTS:
- 1 <= num <= 1000

MATH RULES (CONSECUTIVE PAIRS PARITY):
A brute-force loop from 1 to `num` checking the digit sum of every single number takes O(N * log(N)) time.
Instead, we can use a mathematical invariant:
If we group numbers starting from 0 into pairs: (0, 1), (2, 3), (4, 5), (10, 11)...
Every pair shares the exact same prefix digits. The only difference is the final digit, where one is even and the other is odd.
Therefore, exactly ONE number in EVERY pair will have an even digit sum, and the other will have an odd digit sum.
This implies exactly half the numbers in any complete range have an even digit sum.

We can condense the entire problem into an O(1) mathematical formula based on the digit sum of the limit `num` itself:
1. If the sum of the digits of `num` is EVEN, the exact count of valid numbers is `num // 2`.
2. If the sum of the digits of `num` is ODD, the exact count of valid numbers is `(num - 1) // 2`.
"""

# STEP 1: Calculate the sum of the digits of the given boundary number `num`.
# STEP 2: Use integer math to extract digits (modulo 10 and floor division).
# STEP 3: Apply the O(1) parity formula based on whether the calculated digit sum is even or odd.

class Solution:
    def countEven(self, num: int) -> int:
        
        # Calculate the sum of the digits of `num`
        temp = num
        digit_sum = 0
        
        while temp > 0:
            digit_sum += temp % 10
            temp //= 10
            
        # O(1) Mathematical Resolution based on Consecutive Pairs Parity
        if digit_sum % 2 == 0:
            return num // 2
        else:
            return (num - 1) // 2

"""
WHY EACH PART:
- temp % 10: Extracts the last digit cleanly without slow string conversions.
- temp //= 10: Shaves off the last digit to process the next one.
- num // 2 vs (num - 1) // 2: Completely bypasses the need to iterate through the sequence. It calculates the combinatorial pairs directly.

KEY TECHNIQUE:
- Mathematical Reduction: Realizing that an alternating pattern (even, odd, even, odd digit sums) allows dividing the search space by 2 globally.
- State Abstraction: We don't care about the numbers inside the range, we only care about the boundary condition (`num` itself).

EDGE CASES:
- num = 1 (Odd digit sum): digit_sum is 1. (1 - 1) // 2 = 0. Correct.
- num = 2 (Even digit sum): digit_sum is 2. 2 // 2 = 1. Correct (only the number 2).
- num = 1000 (Odd digit sum): digit_sum is 1. (1000 - 1) // 2 = 499. Correct.

TIME COMPLEXITY: O(log_10(num)) - The while loop only executes proportional to the number of digits in `num`. Since `num` <= 1000, it runs a maximum of 4 times, effectively executing in O(1) instantaneous time.
SPACE COMPLEXITY: O(1) - Only scalar integer variables are used.
"""
