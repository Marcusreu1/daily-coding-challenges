# 1006. Clumsy Factorial
# Difficulty: Medium
# https://leetcode.com/problems/clumsy-factorial/

"""
PROBLEM:
Normally, the factorial of a positive integer n is the product of all positive integers 
less than or equal to n. We design a "clumsy factorial" using the operations in this 
strict order: multiplication (*), division (/), addition (+), and subtraction (-).
For example, clumsy(10) = 10 * 9 / 8 + 7 - 6 * 5 / 4 + 3 - 2 * 1.
The division is integer division and truncates toward zero. Return the clumsy factorial of n.

EXAMPLES:
Input: n = 4
Output: 7
Explanation: 7 = 4 * 3 / 2 + 1

Input: n = 10
Output: 12
Explanation: 12 = 10 * 9 / 8 + 7 - 6 * 5 / 4 + 3 - 2 * 1

CONSTRAINTS:
- 1 <= n <= 10000

ALGORITHMIC INTUITION (THE "TRICK"):
The core problem is the Order of Operations (PEMDAS). We cannot simply evaluate the 
expression from left to right because multiplication and division take precedence 
over addition and subtraction.
To solve any mathematical expression evaluation problem in Computer Science, the 
ideal data structure is a Stack.

1. We use a Stack to temporarily store the numbers.
2. If the operation is `*` or `/`, we pop the last number from the stack, apply 
   the operation with the current number, and push the result back onto the stack.
3. If the operation is `+`, we push the current number onto the stack.
4. If the operation is `-`, we push the NEGATIVE of the current number onto the stack.
5. At the end, since all multiplications and divisions have been resolved and collapsed, 
   we simply sum all the remaining elements in the stack.
"""

# STEP 1: Create the stack and insert the first number (n).
# STEP 2: Define the cycle of operations and an index counter to rotate them.
# STEP 3: Iterate from n-1 down to 1.
# STEP 4: Collapse multiplications and divisions immediately using the top of the stack.
# STEP 5: Be careful with negative division in Python (use int() instead of //).
# STEP 6: Add and subtract by pushing positive or negative values to the stack.
# STEP 7: Return the total sum of the stack.

class Solution:
    def clumsy(self, n: int) -> int:
        
        stack = [n]
        operations = ['*', '/', '+', '-']
        op_idx = 0
        
        for i in range(n - 1, 0, -1):
            op = operations[op_idx % 4]
            
            if op == '*':
                # Pop the top, multiply, and push back
                stack.append(stack.pop() * i)
                
            elif op == '/':
                # TRICK: int() truncates toward zero, crucial for negative numbers in Python
                stack.append(int(stack.pop() / i))
                
            elif op == '+':
                stack.append(i)
                
            elif op == '-':
                stack.append(-i)
                
            # Move to the next operation
            op_idx += 1
            
        return sum(stack)

"""
WHY EACH PART:
- op_idx % 4: This is the perfect mathematical way to create an infinite cycle through a static array of 4 elements.
- int(stack.pop() / i): In Python, integer division `//` truncates toward negative infinity (e.g., -3 // 2 = -2). The problem requires truncating toward ZERO. Using float division with `int()` achieves exactly this (e.g., int(-3 / 2) = -1).
- stack.append(-i): Transforms subtraction into an addition of negative numbers, allowing us to simply run sum(stack) at the end.

HOW IT WORKS (Example: n = 4):
Initial Stack: stack = [4]

Iteration 1 (i = 3, op = '*'):
├── stack.pop() = 4
├── 4 * 3 = 12
└── stack = [12]

Iteration 2 (i = 2, op = '/'):
├── stack.pop() = 12
├── 12 / 2 = 6
└── stack = [6]

Iteration 3 (i = 1, op = '+'):
├── We push 1 directly
└── stack = [6, 1]

End of loop.
Final Sum: sum([6, 1]) = 7. ✓

TIME COMPLEXITY: O(N) - We iterate through the numbers exactly once.
SPACE COMPLEXITY: O(N) - In the worst case, the stack will store N/2 elements.

CONCEPTS USED:
- Stack Data Structure
- Expression Evaluation / AST
- Modular Arithmetic (Cycles)
"""
