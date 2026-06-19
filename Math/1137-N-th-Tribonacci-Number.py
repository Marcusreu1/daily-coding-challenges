# 1137. N-th Tribonacci Number
# Difficulty: Easy
# https://leetcode.com/problems/n-th-tribonacci-number/

"""
PROBLEM:
The Tribonacci sequence Tn is defined as follows: 
T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.
Given `n`, return the value of Tn.

EXAMPLES:
Input: n = 4
Output: 4
Explanation:
T_3 = 0 + 1 + 1 = 2
T_4 = 1 + 1 + 2 = 4

Input: n = 25
Output: 1389537

CONSTRAINTS:
- 0 <= n <= 37
- The answer is guaranteed to fit within a 32-bit integer.

ALGORITHMIC INTUITION (THE "TRICK"):
The naive approach is to use pure recursion: return tribonacci(n-1) + tribonacci(n-2) + tribonacci(n-3).
However, this leads to an O(3^n) time complexity, which causes a Time Limit Exceeded (TLE) error 
because it recalculates the same overlapping subproblems millions of times.

Instead of working top-down, we use Bottom-Up Dynamic Programming with Space Optimization.
Since we only ever need the LAST THREE numbers to calculate the next one, we don't even need 
an array. We can just maintain three variables (a, b, c) and shift them forward like a sliding window.
"""

# STEP 1: Handle base cases directly (n = 0, 1, 2) to prevent out-of-bounds errors.
# STEP 2: Initialize the first three numbers in the sequence (a=0, b=1, c=1).
# STEP 3: Loop from 3 up to n.
# STEP 4: Calculate the next number by summing a, b, and c.
# STEP 5: Shift the window forward: 'a' takes 'b's value, 'b' takes 'c's, 'c' takes the new sum.
# STEP 6: Return 'c', which holds the nth value after the loop completes.

class Solution:
    def tribonacci(self, n: int) -> int:
        
        # Step 1: Base cases
        if n == 0: return 0
        if n == 1 or n == 2: return 1
        
        # Step 2: Initialize the sliding window of 3 variables
        a = 0  # T_0
        b = 1  # T_1
        c = 1  # T_2
        
        # Step 3: Compute bottom-up iteratively
        for _ in range(3, n + 1):
            
            # Step 4: Calculate next value
            next_val = a + b + c
            
            # Step 5: Shift variables forward
            a = b
            b = c
            c = next_val
            
        # Step 6: c holds the nth value
        return c

"""
WHY EACH PART:
- Handling base cases explicitly: Prevents the loop from running or returning incorrect values if n is extremely small.
- a, b, c variables: Replaces an entire array dp[] = [0, 1, 1, ...]. We discard old values we no longer need, saving memory.
- Simultaneous assignment (a, b, c = b, c, a+b+c) can also be used in Python for elegance, but explicit steps are easier to read for beginners.

HOW IT WORKS (Example: n = 5):
Initial: a = 0, b = 1, c = 1

Iteration 1 (calculating T_3):
├── next_val = 0 + 1 + 1 = 2
├── a = 1
├── b = 1
└── c = 2

Iteration 2 (calculating T_4):
├── next_val = 1 + 1 + 2 = 4
├── a = 1
├── b = 2
└── c = 4

Iteration 3 (calculating T_5):
├── next_val = 1 + 2 + 4 = 7
├── a = 2
├── b = 4
└── c = 7

Exit Loop. Return c (7) ✓

TIME COMPLEXITY: O(N) - We run a single loop from 3 to N. Execution is instantaneous even for n=37.
SPACE COMPLEXITY: O(1) - We only allocate memory for three integer variables, regardless of N. Constant space.

CONCEPTS USED:
- Dynamic Programming (Bottom-Up)
- Sliding Window (Space Optimization)
"""
