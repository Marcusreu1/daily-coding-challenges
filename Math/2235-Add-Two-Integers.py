# 2235. Add Two Integers
# Difficulty: Easy
# https://leetcode.com/problems/add-two-integers/

"""
PROBLEM:
Given two integers num1 and num2, return the sum of the two integers.

EXAMPLES:
Input: num1 = 12, num2 = 5 → Output: 17
Explanation: num1 is 12, num2 is 5, and their sum is 12 + 5 = 17.

Input: num1 = -10, num2 = 4 → Output: -6
Explanation: num1 + num2 = -6.

CONSTRAINTS:
- -100 <= num1, num2 <= 100

MATH RULES (ALU CONSTANT TIME OPERATION):
This is the foundational "Hello World" algorithm of LeetCode, designed primarily to verify the compiler, test cases, and runtime environment of the platform.
Under the hood, the '+' operator translates directly to a low-level Assembly ADD instruction executed by the CPU's Arithmetic Logic Unit (ALU). 
It requires zero dynamic memory allocations and executes deterministically in a single clock cycle.
"""

# STEP 1: Add num1 and num2 using the native addition operator.
# STEP 2: Return the evaluated sum.

class Solution:
    def sum(self, num1: int, num2: int) -> int:
        
        # CPU-level integer addition
        return num1 + num2

"""
WHY EACH PART:
- num1 + num2: The native Python arithmetic operator resolves integer addition intrinsically.

KEY TECHNIQUE:
- Hardware-level Arithmetic: Trusting the CPU architecture to resolve scalar algebraic operations in pure O(1) time without algorithmic overhead.

EDGE CASES:
- Negative integers (e.g., -100 + 50): Handled natively by Two's Complement representation at the hardware level. Returns -50 correctly.
- Zero bounds (e.g., 0 + 0): Evaluates to 0 seamlessly.

TIME COMPLEXITY: O(1) - Single operation.
SPACE COMPLEXITY: O(1) - No extra variables or space utilized.
"""
