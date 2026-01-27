# 150. Evaluate Reverse Polish Notation
# Difficulty: Medium
# https://leetcode.com/problems/evaluate-reverse-polish-notation/

"""
PROBLEM:
You are given an array of strings 'tokens' that represents an arithmetic
expression in Reverse Polish Notation (RPN). Evaluate the expression and
return an integer that represents the value.

EXAMPLES:
Input: ["2","1","+","3","*"]  → Output: 9  → (2 + 1) * 3
Input: ["4","13","5","/","+"] → Output: 6  → 4 + (13 / 5)
Input: ["10","6","9","3","+","-11","*","/","*","17","+","5","+"] → Output: 22

CONSTRAINTS:
- 1 <= tokens.length <= 10^4
- tokens[i] is an operator (+, -, *, /) OR an integer in [-200, 200]
- Division truncates toward zero (not floor division!)

KEY INSIGHT:
Use a STACK - numbers get pushed, operators pop two and push result.
RPN was literally designed to be evaluated with a stack!

CHALLENGES:
1. Operand order: second pop is LEFT operand (a - b, not b - a)
2. Division truncation: int(a/b) truncates toward 0, not // which floors

SOLUTION:
- Iterate through tokens left to right
- Number → push to stack
- Operator → pop b, pop a, compute a○b, push result
- Return the single remaining element
"""

# STEP 1: Initialize stack and define operators
# STEP 2: Process each token left to right
# STEP 3: If number → push; if operator → pop, compute, push
# STEP 4: Return final result (last element in stack)

from typing import List

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        
        stack = []                                                               # Holds operands during evaluation
        operators = {'+', '-', '*', '/'}                                         # Set for O(1) lookup
        
        for token in tokens:                                                     # Process left to right
            
            if token in operators:                                               # It's an operator
                b = stack.pop()                                                  # Right operand (popped first!)
                a = stack.pop()                                                  # Left operand (popped second!)
                
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                else:                                                            # token == '/'
                    result = int(a / b)                                          # Truncate toward zero!
                
                stack.append(result)                                             # Push result for next operation
            
            else:                                                                # It's a number
                stack.append(int(token))                                         # Convert string → int and push
        
        return stack[0]                                                          # Single element remains = answer


"""
WHY EACH PART:
- stack = []: LIFO structure perfect for nested operations
- operators set: O(1) membership check vs O(n) for list
- b = pop() FIRST: Last pushed = right operand in expression
- a = pop() SECOND: Second to last = left operand
- int(a / b): True division then truncate (NOT floor division //)
- stack.append(result): Result becomes operand for future operations
- return stack[0]: Valid RPN always leaves exactly one number

HOW IT WORKS (Example: ["2","1","+","3","*"]):

Anchor = "2":
├── Is "2" an operator? No
└── Push 2 → stack = [2]

Anchor = "1":
├── Is "1" an operator? No
└── Push 1 → stack = [2, 1]

Anchor = "+":
├── Is "+" an operator? Yes
├── b = pop() = 1
├── a = pop() = 2
├── result = 2 + 1 = 3
└── Push 3 → stack = [3]

Anchor = "3":
├── Is "3" an operator? No
└── Push 3 → stack = [3, 3]

Anchor = "*":
├── Is "*" an operator? Yes
├── b = pop() = 3
├── a = pop() = 3
├── result = 3 * 3 = 9
└── Push 9 → stack = [9]

Final: stack[0] = 9 ✓

WHY int(a/b) NOT a//b:
┌─────────────────────────────────────────────────────────┐
│  -7 / 2 in different systems:                           │
│                                                         │
│  Floor division (//):  -7 // 2 = -4  (toward -∞)   ✗    │
│  True + truncate:   int(-7/2) = -3  (toward 0)     ✓    │
│                                                         │
│  The problem explicitly says "truncate toward zero"     │
└─────────────────────────────────────────────────────────┘

WHY STACK IS PERFECT FOR RPN:
Infix:  ((2 + 3) * (4 - 1))  → Needs parentheses & precedence
RPN:    2 3 + 4 1 - *        → Just left-to-right with stack

[2] → [2,3] → [5] → [5,4] → [5,4,1] → [5,3] → [15]

The stack naturally handles the "most recent operands" concept!

EDGE CASES:
- Single number ["42"]: Returns 42 ✓
- Negative numbers ["-5","3","+"]: Returns -2 ✓
- Negative division ["-7","2","/"]: Returns -3 (toward 0) ✓
- Large expressions: Stack handles naturally ✓

TIME COMPLEXITY: O(n)
- Single pass through all n tokens
- Each operation (push/pop/arithmetic) is O(1)

SPACE COMPLEXITY: O(n)
- Stack holds at most (n+1)/2 numbers
- Worst case: all numbers first, then all operators

CONCEPTS USED:
- Stack (LIFO) data structure
- Reverse Polish Notation (postfix evaluation)
- Integer truncation vs floor division
- String to integer conversion
"""
