# 829. Consecutive Numbers Sum
# Difficulty: Hard
# https://leetcode.com/problems/consecutive-numbers-sum/

"""
PROBLEM:
Given an integer n, return the number of ways you can write n as the sum of consecutive positive integers.

EXAMPLES:
Input: n = 5    → Output: 2
Explanation: 5 = 5 = 2 + 3

Input: n = 9    → Output: 3
Explanation: 9 = 9 = 4 + 5 = 2 + 3 + 4

Input: n = 15   → Output: 4
Explanation: 15 = 15 = 8 + 7 = 4 + 5 + 6 = 1 + 2 + 3 + 4 + 5

CONSTRAINTS:
- 1 <= n <= 10^9

LOGIC RULES (ALGEBRAIC REDUCTION):
1. A sum of 'k' consecutive integers starting from 'x' is written as:
   x + (x + 1) + (x + 2) + ... + (x + k - 1) = n
2. Combining the terms gives:
   k * x + (k * (k - 1)) / 2 = n
3. Solving for x (the starting integer):
   x = (n - (k * (k - 1)) / 2) / k
4. For the sequence to be valid, 'x' MUST be a strictly positive integer.
   This means:
   - The numerator (n - (k * (k - 1)) / 2) must be strictly greater than 0.
   - The numerator must be perfectly divisible by k (modulo == 0).
5. We iterate through values of 'k' starting from 1 and stop as soon as the numerator drops to <= 0.

VISUALIZATION (n = 9):
Let's iterate 'k' (the number of terms in the sequence):

k = 1:
- numerator = 9 - (1 * 0) / 2 = 9
- 9 > 0? Yes.
- 9 % 1 == 0? Yes! -> Valid x = 9. Sequence: [9]. (count = 1)

k = 2:
- numerator = 9 - (2 * 1) / 2 = 8
- 8 > 0? Yes.
- 8 % 2 == 0? Yes! -> Valid x = 4. Sequence: [4, 5]. (count = 2)

k = 3:
- numerator = 9 - (3 * 2) / 2 = 6
- 6 > 0? Yes.
- 6 % 3 == 0? Yes! -> Valid x = 2. Sequence: [2, 3, 4]. (count = 3)

k = 4:
- numerator = 9 - (4 * 3) / 2 = 3
- 3 > 0? Yes.
- 3 % 4 == 0? No! -> x would be 0.75. Not an integer.

k = 5:
- numerator = 9 - (5 * 4) / 2 = -1
- -1 > 0? No! Stop iteration. 
Result: 3 valid ways. ✓
"""

# STEP 1: Initialize the counter for valid sequences and the sequence length 'k'
# STEP 2: Start an infinite loop to test increasing values of 'k'
# STEP 3: Calculate the arithmetic progression subtractor: k * (k - 1) // 2
# STEP 4: Break the loop if the numerator becomes <= 0 (x would be negative or zero)
# STEP 5: If the numerator is perfectly divisible by k, we found a valid integer x. Increment count.
# STEP 6: Return the final count.

class Solution:
    def consecutiveNumbersSum(self, n: int) -> int:
        
        valid_ways = 0
        k = 1
        
        while True:
            # Step 3: Calculate the arithmetic series sum to subtract
            sub_term = (k * (k - 1)) // 2
            numerator = n - sub_term
            
            # Step 4: x must be > 0. If numerator <= 0, x is invalid, and all future k's will also be invalid.
            if numerator <= 0:
                break
                
            # Step 5: Check if x is a perfect integer
            if numerator % k == 0:
                valid_ways += 1
                
            k += 1
            
        return valid_ways

"""
WHY EACH PART:
- (k * (k - 1)) // 2: Sum of first k-1 integers. We use integer division // to avoid converting to floats, 
  which prevents precision errors with massive numbers.
- numerator <= 0: Acts as our 'WHERE' clause to terminate the loop early. The sequence length 'k' 
  grew so large that the sum of 1+2+..+k already exceeded 'n', leaving no room for a positive start number.
- numerator % k == 0: Checks if the mathematical requirement for 'x' being a whole number is fulfilled.

HOW IT WORKS (Example dry run for n = 5):

Initial: valid_ways = 0, k = 1

Iter 1 (k=1):
├── sub_term = 0
├── num = 5 - 0 = 5
├── 5 > 0 -> Continue
├── 5 % 1 == 0 -> valid_ways = 1
└── k = 2

Iter 2 (k=2):
├── sub_term = 1
├── num = 5 - 1 = 4
├── 4 > 0 -> Continue
├── 4 % 2 == 0 -> valid_ways = 2
└── k = 3

Iter 3 (k=3):
├── sub_term = 3
├── num = 5 - 3 = 2
├── 2 > 0 -> Continue
├── 2 % 3 == 0 -> False
└── k = 4

Iter 4 (k=4):
├── sub_term = 6
├── num = 5 - 6 = -1
├── -1 <= 0 -> BREAK LOOP!

Returns valid_ways = 2. (Sequences: [5], [2,3]). ✓

EDGE CASES:
- n = 1: Loop runs for k=1 (num=1, valid), runs for k=2 (num=1-1=0, break). Returns 1. ✓
- Large n (e.g., 10^9): Loop breaks when k*(k-1)/2 >= 10^9, which happens around k ~ 45,000. 
  Extremely fast execution, completely avoiding O(N) Time Limit Exceeded. ✓

TIME COMPLEXITY: O(sqrt(N))
The loop terminates when `k * (k - 1) / 2 >= N`, which mathematically means `k` is roughly proportional 
to the square root of 2N. For N = 10^9, it runs at most ~45,000 iterations, taking sub-milliseconds.

SPACE COMPLEXITY: O(1)
We only store three scalar integers (`valid_ways`, `k`, `numerator`). Memory allocation is perfectly constant.
"""
