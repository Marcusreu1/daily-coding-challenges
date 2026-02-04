# 224. Basic Calculator
# Difficulty: Hard
# https://leetcode.com/problems/basic-calculator/

"""
PROBLEM:
Given a string s representing a valid expression, implement a basic calculator
to evaluate it, and return the result of the evaluation.

VALID CHARACTERS:
- Digits: '0' to '9'
- Operators: '+', '-'
- Parentheses: '(', ')'
- Spaces: ' '

EXAMPLES:
Input: s = "1 + 1"                    → Output: 2
Input: s = " 2-1 + 2 "                → Output: 3
Input: s = "(1+(4+5+2)-3)+(6+8)"      → Output: 23
Input: s = "-(2+3)"                   → Output: -5

CONSTRAINTS:
- 1 <= s.length <= 3 × 10^5
- s consists of digits, '+', '-', '(', ')', and ' '
- s represents a valid expression
- '+' is NOT used as unary operator (no "+1")
- '-' CAN be used as unary operator ("-1", "-(1+2)")
- No two consecutive operators
- Every number is valid (fits in 32-bit integer)

KEY INSIGHT:
Use a STACK to handle parentheses. When we see '(':
- Save current (result, sign) to stack
- Reset result and sign for evaluating inside parentheses
When we see ')':
- Pop from stack and combine: prev_result + prev_sign × current_result

CHALLENGES:
1. Multi-digit numbers: "123" → build digit by digit
2. Negative expressions: "-(1+2)" → sign applies to entire parenthesis
3. Nested parentheses: Handled naturally by stack

SOLUTION:
Iterate through string, use stack for parentheses, track current
result, sign, and number being built.
"""

# STEP 1: Initialize result, sign, current number, and stack
# STEP 2: Process each character
# STEP 3: Handle digits (build multi-digit numbers)
# STEP 4: Handle operators (apply current number, update sign)
# STEP 5: Handle parentheses (push/pop from stack)
# STEP 6: Apply any remaining number and return result

class Solution:
    def calculate(self, s: str) -> int:
        
        result = 0                                                               # Running total
        sign = 1                                                                 # Current sign: +1 or -1
        num = 0                                                                  # Number being built
        stack = []                                                               # Stack for parentheses
        
        for char in s:
            
            if char.isdigit():                                                   # Build multi-digit number
                num = num * 10 + int(char)
            
            elif char == '+':                                                    # Apply number, set sign +
                result += sign * num
                num = 0
                sign = 1
            
            elif char == '-':                                                    # Apply number, set sign -
                result += sign * num
                num = 0
                sign = -1
            
            elif char == '(':                                                    # Save state, reset
                stack.append(result)                                             # Save current result
                stack.append(sign)                                               # Save current sign
                result = 0                                                       # Reset for inside parens
                sign = 1
            
            elif char == ')':                                                    # Combine with saved state
                result += sign * num                                             # Apply pending number
                num = 0
                result *= stack.pop()                                            # Multiply by saved sign
                result += stack.pop()                                            # Add saved result
            
            # Spaces are ignored (no else clause needed)
        
        result += sign * num                                                     # Apply last number
        
        return result


"""
WHY EACH PART:
- result = 0: Accumulates the total of current scope
- sign = 1: +1 for positive, -1 for negative (next number's sign)
- num = 0: Builds multi-digit numbers digit by digit
- stack = []: Stores (result, sign) when entering parentheses
- char.isdigit(): Check if character is 0-9
- num * 10 + int(char): Shift left and add new digit (builds 1→12→123)
- result += sign * num: Apply the number with its sign to result
- num = 0: Reset after applying
- sign = 1 or -1: Update sign for next number
- stack.append(result), stack.append(sign): Save state before '('
- result *= stack.pop(): Apply sign that was before '('
- result += stack.pop(): Add result that was before '('

HOW IT WORKS (Example: "(1+(4+5+2)-3)+(6+8)"):

┌─ Initial State ───────────────────────────────────────────┐
│  result = 0, sign = 1, num = 0, stack = []                │
└───────────────────────────────────────────────────────────┘

┌─ char = '(' ──────────────────────────────────────────────┐
│  Push result (0) and sign (1) to stack                    │
│  Reset: result = 0, sign = 1                              │
│  stack = [0, 1]                                           │
└───────────────────────────────────────────────────────────┘

┌─ char = '1' ──────────────────────────────────────────────┐
│  num = 0 × 10 + 1 = 1                                     │
└───────────────────────────────────────────────────────────┘

┌─ char = '+' ──────────────────────────────────────────────┐
│  result = 0 + 1 × 1 = 1                                   │
│  num = 0, sign = 1                                        │
└───────────────────────────────────────────────────────────┘

┌─ char = '(' ──────────────────────────────────────────────┐
│  Push result (1) and sign (1) to stack                    │
│  Reset: result = 0, sign = 1                              │
│  stack = [0, 1, 1, 1]                                     │
└───────────────────────────────────────────────────────────┘

┌─ chars = '4', '+', '5', '+', '2' ─────────────────────────┐
│  Process: result = 0 + 4 = 4                              │
│  Process: result = 4 + 5 = 9                              │
│  Process: result = 9 + 2 = 11                             │
│  (After '2': num = 2, not yet applied)                    │
└───────────────────────────────────────────────────────────┘

┌─ char = ')' ──────────────────────────────────────────────┐
│  Apply pending: result = 11 + 1 × (num was already 0)     │
│  Wait, let me recalculate...                              │
│  Actually at ')': result += sign × num = 9 + 1×2 = 11     │
│  Pop sign (1): result = 11 × 1 = 11                       │
│  Pop result (1): result = 1 + 11 = 12                     │
│  stack = [0, 1]                                           │
└───────────────────────────────────────────────────────────┘

┌─ char = '-' ──────────────────────────────────────────────┐
│  result = 12 + 1 × 0 = 12  (num was 0)                    │
│  sign = -1                                                │
└───────────────────────────────────────────────────────────┘

┌─ char = '3' ──────────────────────────────────────────────┐
│  num = 3                                                  │
└───────────────────────────────────────────────────────────┘

┌─ char = ')' ──────────────────────────────────────────────┐
│  Apply: result = 12 + (-1) × 3 = 9                        │
│  Pop sign (1): result = 9 × 1 = 9                         │
│  Pop result (0): result = 0 + 9 = 9                       │
│  stack = []                                               │
└───────────────────────────────────────────────────────────┘

┌─ char = '+' ──────────────────────────────────────────────┐
│  result = 9, sign = 1, num = 0                            │
└───────────────────────────────────────────────────────────┘

┌─ char = '(' ──────────────────────────────────────────────┐
│  Push 9, 1 to stack                                       │
│  Reset: result = 0, sign = 1                              │
│  stack = [9, 1]                                           │
└───────────────────────────────────────────────────────────┘

┌─ chars = '6', '+', '8', ')' ──────────────────────────────┐
│  Process 6: result = 6                                    │
│  Process +: sign = 1                                      │
│  Process 8: num = 8                                       │
│  Process ): result = 6 + 1×8 = 14                         │
│             result = 14 × 1 = 14 (pop sign)               │
│             result = 9 + 14 = 23 (pop result)             │
└───────────────────────────────────────────────────────────┘

┌─ Final ───────────────────────────────────────────────────┐
│  result += sign × num = 23 + 1 × 0 = 23                   │
│  Return 23 ✓                                              │
└───────────────────────────────────────────────────────────┘

WHY STACK STORES (result, sign) SEPARATELY:
┌────────────────────────────────────────────────────────────┐
│  We push result FIRST, then sign:                          │
│  stack.append(result)                                      │
│  stack.append(sign)                                        │
│                                                            │
│  So when popping, sign comes FIRST, then result:          │
│  sign = stack.pop()      ← Last in, first out             │
│  prev_result = stack.pop()                                │
│                                                            │
│  result = prev_result + sign × current_result              │
└────────────────────────────────────────────────────────────┘

HANDLING "-(2+3)":
┌────────────────────────────────────────────────────────────┐
│  char '-': sign = -1, result = 0                           │
│  char '(': push(0), push(-1), reset result=0, sign=1       │
│            stack = [0, -1]                                 │
│  char '2': num = 2                                         │
│  char '+': result = 0 + 1×2 = 2, sign = 1                  │
│  char '3': num = 3                                         │
│  char ')': result = 2 + 1×3 = 5                            │
│            result = 5 × (-1) = -5  (pop sign)              │
│            result = 0 + (-5) = -5  (pop result)            │
│                                                            │
│  Final: -5 ✓                                               │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- Single number: "42" → 42 ✓
- Negative start: "-1" → -1 ✓
- Multiple spaces: "  1  +  2  " → 3 ✓
- Nested parens: "((1+2))" → 3 ✓
- Negative parens: "-(-(1+2))" → 3 ✓
- Large numbers: "2147483647" → 2147483647 ✓

TIME COMPLEXITY: O(n)
- Single pass through the string
- Each character processed once
- Stack operations are O(1)

SPACE COMPLEXITY: O(n)
- Stack can grow up to O(n) for deeply nested parentheses
- Example worst case: "(((((...)))))"

CONCEPTS USED:
- Stack for nested structure handling
- Sign tracking for operator precedence
- Building multi-digit numbers
- State save/restore pattern
"""
