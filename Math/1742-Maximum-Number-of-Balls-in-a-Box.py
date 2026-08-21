# 1742. Maximum Number of Balls in a Box
# Difficulty: Easy
# https://leetcode.com/problems/maximum-number-of-balls-in-a-box/

"""
PROBLEM:
You are working in a ball factory where you have n balls numbered from lowLimit up to highLimit inclusive (i.e., n = highLimit - lowLimit + 1).
You drop each ball into a box with a number equal to the sum of the ball's digits.
For example, the ball number 321 will be dropped in the box number 3 + 2 + 1 = 6.
Return the number of balls in the box with the most balls.

EXAMPLES:
Input: lowLimit = 1, highLimit = 10 → Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 ...
Ball Count:  2 1 1 1 1 1 1 1 1 0  0  ...
Box 1 has the most number of balls with 2 balls (ball 1 and ball 10).

Input: lowLimit = 5, highLimit = 15 → Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 ...
Ball Count:  1 1 1 1 2 2 1 1 1 0  0  ...
Boxes 5 and 6 have the most number of balls with 2 balls in each.
We return 2.

CONSTRAINTS:
- 1 <= lowLimit <= highLimit <= 10^5

ALGORITHM RULES (DIGIT SUM & FREQUENCY ARRAY):
Instead of casting numbers to strings to sum their digits (which is O(k) but with high overhead), we use mathematical extraction (modulo 10 and integer division by 10).
Since the maximum possible value is 10^5, the number with the maximum digit sum in this range is 99999.
Sum of digits for 99999: 9 + 9 + 9 + 9 + 9 = 45.
This means box IDs will never exceed 45. We can use a fixed-size array of 46 elements (0 to 45) instead of a Hash Map to count the frequencies, which drastically improves memory access time.

VISUALIZATION (lowLimit = 1, highLimit = 10):
Array 'boxes' of size 46, all initialized to 0.

i = 1: sum = 1 -> boxes[1] += 1
i = 2: sum = 2 -> boxes[2] += 1
...
i = 9: sum = 9 -> boxes[9] += 1
i = 10: sum = 1 + 0 = 1 -> boxes[1] += 1

Final state of boxes array:
Index: 0  1  2  3  4  5  6  7  8  9  10 ...
Count: 0  2  1  1  1  1  1  1  1  1  0  ...

Maximum value in array: 2 ✓
"""

# STEP 1: Initialize a fixed-size array 'boxes' with zeros. A size of 46 is sufficient.
# STEP 2: Iterate through every number from lowLimit to highLimit.
# STEP 3: Mathematically extract and sum the digits of the current number.
# STEP 4: Increment the counter in the 'boxes' array at the index corresponding to the digit sum.
# STEP 5: Return the maximum value found in the 'boxes' array.

class Solution:
    def countBalls(self, lowLimit: int, highLimit: int) -> int:
        
        # Max digit sum for numbers <= 10^5 is 45 (from 99999)
        boxes = [0] * 46                                                     # Frequency array
        
        for i in range(lowLimit, highLimit + 1):
            
            # Temporary variable to process digits without mutating 'i'
            current_num = i
            digit_sum = 0
            
            # Extract and sum digits mathematically
            while current_num > 0:
                digit_sum += current_num % 10
                current_num //= 10
                
            # Drop the ball in the corresponding box
            boxes[digit_sum] += 1
            
        # Return the highest frequency
        return max(boxes)

"""
WHY EACH PART:
- [0] * 46: Bypasses the overhead of Dictionary hashing by using direct memory addressing in an array.
- range(lowLimit, highLimit + 1): Ensures we process the inclusive bounds properly.
- current_num % 10: Extracts the rightmost digit instantly.
- current_num //= 10: Removes the rightmost digit for the next iteration.

HOW IT WORKS (Example: processing ball 321):

Initial: current_num = 321, digit_sum = 0

Iteration 1:
├── current_num % 10 = 1
├── digit_sum = 0 + 1 = 1
└── current_num // 10 = 32

Iteration 2:
├── current_num % 10 = 2
├── digit_sum = 1 + 2 = 3
└── current_num // 10 = 3

Iteration 3:
├── current_num % 10 = 3
├── digit_sum = 3 + 3 = 6
└── current_num // 10 = 0

Exit: current_num is 0. 
boxes[6] is incremented by 1. ✓

KEY TECHNIQUE:
- Modulo Arithmetic for String Parsing: Bypasses the expensive conversion of int -> str -> list of chars -> int.
- Space Bound Analysis: Realizing the strict physical constraints of the problem (max sum = 45) to optimize data structures.

EDGE CASES:
- lowLimit == highLimit: The loop runs exactly once, safely dropping 1 ball and returning max = 1.
- Maximum constraints (10^5): Python executes ~100,000 modulo loops in a fraction of a second, well within execution limits.

TIME COMPLEXITY: O(N * D) - Where N is (highLimit - lowLimit + 1) and D is the number of digits (at most 5). Effectively O(N).
SPACE COMPLEXITY: O(1) - The boxes array size is strictly bound to 46, which is constant regardless of N.

CONCEPTS USED:
- Frequency Arrays
- Digit Extraction (Modulo & Floor Division)
- Optimization via Constraints Analysis
"""
