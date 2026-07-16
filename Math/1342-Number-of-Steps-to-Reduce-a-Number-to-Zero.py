# 1342. Number of Steps to Reduce a Number to Zero
# Difficulty: Easy
# https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/

"""
PROBLEM:
Given an integer `num`, return the number of steps to reduce it to zero.
In one step, if the current number is even, you have to divide it by 2, 
otherwise, you have to subtract 1 from it.

EXAMPLES:
Input: num = 14
Output: 6
(Explanation: 
Step 1) 14 is even; divide by 2 and obtain 7. 
Step 2) 7 is odd; subtract 1 and obtain 6.
Step 3) 6 is even; divide by 2 and obtain 3. 
Step 4) 3 is odd; subtract 1 and obtain 2. 
Step 5) 2 is even; divide by 2 and obtain 1. 
Step 6) 1 is odd; subtract 1 and obtain 0.)

Input: num = 8
Output: 4
(Explanation: 
Step 1) 8 is even; divide by 2 and obtain 4. 
Step 2) 4 is even; divide by 2 and obtain 2. 
Step 3) 2 is even; divide by 2 and obtain 1. 
Step 4) 1 is odd; subtract 1 and obtain 0.)

CONSTRAINTS:
- 0 <= num <= 10^6

ALGORITHM LOGIC (Simulation & Parity Checking):
1. This problem is a textbook case for Simulation. We don't need a complex mathematical shortcut; 
   we just need to execute the exact rules given until the exit condition is met.
2. We use a while loop that continues as long as `num` is strictly greater than 0.
3. We check for parity using the modulo operator (`num % 2 == 0`).
4. If it evaluates to True (Even), we divide by 2.
5. If it evaluates to False (Odd), we subtract 1.
6. After applying the rule, we increment our step counter.

VISUALIZATION (num = 14):
Init: num = 14, steps = 0

Iter 1: 14 % 2 == 0 (Even) -> num = 7, steps = 1
Iter 2: 7 % 2 != 0  (Odd)  -> num = 6, steps = 2
Iter 3: 6 % 2 == 0  (Even) -> num = 3, steps = 3
Iter 4: 3 % 2 != 0  (Odd)  -> num = 2, steps = 4
Iter 5: 2 % 2 == 0  (Even) -> num = 1, steps = 5
Iter 6: 1 % 2 != 0  (Odd)  -> num = 0, steps = 6

Loop breaks (num is 0). Return 6. ✓
"""

# STEP 1: Initialize a step counter to 0
# STEP 2: Loop while `num` is strictly greater than 0
# STEP 3: Use an if/else block to check if the number is even (num % 2 == 0)
# STEP 4: If even, divide `num` by 2 using integer division (//)
# STEP 5: If odd, subtract 1 from `num`
# STEP 6: Increment the step counter by 1 at the end of each iteration
# STEP 7: Return the final step count

class Solution:
    def numberOfSteps(self, num: int) -> int:
        
        steps = 0                                                    # Counter for total operations
        
        while num > 0:                                               # Condition to keep reducing
            
            if num % 2 == 0:                                         # Parity check: Even
                num //= 2                                            # Apply Rule 1: Divide by 2
            else:                                                    # Parity check: Odd
                num -= 1                                             # Apply Rule 2: Subtract 1
                
            steps += 1                                               # Record the step taken
            
        return steps                                                 # Return total steps

"""
WHY EACH PART:
- while num > 0: Ensures we don't fall into negative numbers or an infinite loop. It stops exactly when we hit the target 0.
- num //= 2: We use integer division (`//`) instead of standard division (`/`) because standard division in Python converts the result into a float (e.g., 14 / 2 = 7.0). Staying in integer types is safer and faster.
- steps += 1: Placed outside the if/else block because, regardless of which mathematical operation we performed, exactly one valid "step" was consumed.

HOW IT WORKS (Example: num = 0):
While 0 > 0 evaluates to False immediately.
The loop never executes.
Returns steps = 0. ✓

KEY TECHNIQUE:
- Pure Simulation: Translating human-readable rules into iterative computer logic without deviation.
- Compound Assignment Operators (`//=`, `-=`, `+=`): Pythonic shorthand for modifying a variable in place.

EDGE CASES:
- num = 0: As seen above, loop doesn't trigger, returns 0 steps automatically. ✓
- Very large number (num = 10^6): The division by 2 causes the number to shrink exponentially (logarithmically), so even a million is reduced to 0 in roughly 20-30 steps. ✓

TIME COMPLEXITY: O(log N) - Where N is the value of `num`. Every time the number is even, it gets halved. In the worst case (an odd number), we subtract 1, which guarantees the next number is even and will be halved. Halving repeatedly is the definition of logarithmic time.
SPACE COMPLEXITY: O(1) - We only store one extra integer variable (`steps`). No arrays or scaling data structures are created.

CONCEPTS USED:
- Simulation
- While Loops
- Modulo Arithmetic (Parity)
- Time Complexity (Logarithmic growth)
"""
