# 2169. Count Operations to Obtain Zero
# Difficulty: Easy
# https://leetcode.com/problems/count-operations-to-obtain-zero/

"""
PROBLEM:
You are given two non-negative integers num1 and num2.
In one operation, if num1 >= num2, you must subtract num2 from num1, otherwise subtract num1 from num2.
- For example, if num1 = 5 and num2 = 4, subtract num2 from num1, thus obtaining num1 = 1 and num2 = 4. 
- However, if num1 = 4 and num2 = 5, after one operation, num1 = 4 and num2 = 1.
Return the number of operations required to make either num1 = 0 or num2 = 0.

EXAMPLES:
Input: num1 = 2, num2 = 3 → Output: 3
Explanation: 
- Operation 1: num1 = 2, num2 = 3. Since num1 < num2, we subtract num1 from num2 and get num1 = 2, num2 = 3 - 2 = 1.
- Operation 2: num1 = 2, num2 = 1. Since num1 > num2, we subtract num2 from num1. num1 = 2 - 1 = 1, num2 = 1.
- Operation 3: num1 = 1, num2 = 1. Since num1 == num2, we subtract num2 from num1. num1 = 1 - 1 = 0, num2 = 1.
With num1 = 0, we stop. Total operations = 3.

Input: num1 = 10, num2 = 10 → Output: 1
Explanation: 
- Operation 1: num1 = 10, num2 = 10. num1 >= num2, so num1 = 10 - 10 = 0.
Total operations = 1.

CONSTRAINTS:
- 0 <= num1, num2 <= 10^5

MATH RULES (EUCLIDEAN ACCELERATION & DIVISION AS REPEATED SUBTRACTION):
Naively simulating subtractions one by one yields O(max(num1, num2)) time complexity. If num1 = 10^5 and num2 = 1, the program executes 100,000 steps.
In mathematics, integer division (A // B) represents exactly how many times B can be subtracted from A.
The modulo operator (A % B) represents exactly what is left of A after subtracting B as many times as possible.
Therefore, we can bypass individual subtractions entirely by adding (A // B) to our operation count and updating A to (A % B) in a single O(1) step.
This perfectly mirrors the Euclidean Algorithm for finding the Greatest Common Divisor, reducing the complexity to logarithmic time.
"""

# STEP 1: Initialize an operations counter.
# STEP 2: Loop as long as neither number has reached zero.
# STEP 3: Instead of subtracting once, use integer division to count how many subtractions can happen consecutively.
# STEP 4: Use the modulo operator to instantly jump to the state after all those subtractions are completed.
# STEP 5: Return the accumulated operations.

class Solution:
    def countOperations(self, num1: int, num2: int) -> int:
        
        operations = 0
        
        while num1 > 0 and num2 > 0:
            if num1 >= num2:
                # Count how many times num2 can be subtracted from num1
                operations += num1 // num2
                # Update num1 to the remainder
                num1 %= num2
            else:
                # Count how many times num1 can be subtracted from num2
                operations += num2 // num1
                # Update num2 to the remainder
                num2 %= num1
                
        return operations

"""
WHY EACH PART:
- num1 > 0 and num2 > 0: The terminal condition. If either becomes 0, the process halts. Handles the edge case where input starts at 0 gracefully.
- operations += num1 // num2: The core mathematical jump. Replaces a slow `while num1 >= num2: num1 -= num2` loop with a single O(1) arithmetic calculation.
- num1 %= num2: Truncates the number to its remainder, perfectly mirroring the Euclidean state transition.

KEY TECHNIQUE:
- Euclidean Algorithm Optimization: Converting a subtraction-based simulation into a division-based state machine.
- O(1) Block Processing: Processing identical consecutive operations in a single mathematical step.

EDGE CASES:
- One of the numbers is initially 0 (e.g., num1 = 0, num2 = 5): The `while` loop condition fails immediately. Returns 0 operations perfectly.
- Numbers are identical (e.g., num1 = 10, num2 = 10): 10 // 10 adds 1 operation. 10 % 10 turns num1 into 0. Loop breaks. Returns 1. Perfectly handled.

TIME COMPLEXITY: O(log(min(num1, num2))) - Due to the modulo operation, at least one of the numbers is halved at each step, making the reduction logarithmic rather than linear.
SPACE COMPLEXITY: O(1) - Only scalar integer variables are allocated in memory.
"""
