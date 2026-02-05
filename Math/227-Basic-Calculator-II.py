# 227. Basic Calculator II
# Difficulty: Medium
# https://leetcode.com/problems/basic-calculator-ii/

"""
PROBLEM:
Given a string s which represents an expression, evaluate this expression
and return its value. The integer division should truncate toward zero.

VALID CHARACTERS:
- Digits: '0' to '9'
- Operators: '+', '-', '*', '/'
- Spaces: ' '
- NO parentheses in this problem

EXAMPLES:
Input: s = "3+2*2"     → Output: 7
Input: s = " 3/2 "     → Output: 1
Input: s = " 3+5 / 2 " → Output: 5

CONSTRAINTS:
- 1 <= s.length <= 3 × 10^5
- s consists of integers and operators (+, -, *, /) separated by spaces
- s represents a valid expression
- All integers fit in 32-bit signed integer range
- No division by zero

KEY INSIGHT:
Use a stack to handle operator precedence:
- For + and -: push number to stack (defer calculation)
- For * and /: operate immediately with stack top (high precedence)
- At end: sum all values in stack

CHALLENGES:
1. Operator precedence: * and / before + and -
2. Multi-digit numbers: "123" needs to be built digit by digit
3. Division truncation: toward zero, not floor

SOLUTION:
Track "previous operator". When we finish reading a number,
apply the previous operator to decide what to do with it.
"""

# STEP 1: Initialize stack, current number, and previous operator
# STEP 2: Process each character (and handle end of string)
# STEP 3: For digits: build multi-digit number
# STEP 4: For operators: apply previous operator, update prev_op
# STEP 5: Return sum of stack

class Solution:
    def calculate(self, s: str) -> int:
        
        stack = []
        num = 0
        prev_op = '+'                                                            # Assume '+' before first number
        
        for i, char in enumerate(s):
            
            if char.isdigit():                                                   # Build multi-digit number
                num = num * 10 + int(char)
            
            # Process when we hit an operator OR end of string
            if char in '+-*/' or i == len(s) - 1:
                
                if prev_op == '+':                                               # Addition: push positive
                    stack.append(num)
                
                elif prev_op == '-':                                             # Subtraction: push negative
                    stack.append(-num)
                
                elif prev_op == '*':                                             # Multiplication: immediate
                    stack.append(stack.pop() * num)
                
                elif prev_op == '/':                                             # Division: immediate, truncate to 0
                    stack.append(int(stack.pop() / num))
                
                prev_op = char                                                   # Update operator for next number
                num = 0                                                          # Reset number
        
        return sum(stack)                                                        # Sum all values in stack


"""
WHY EACH PART:
- stack = []: Stores values to be summed at the end
- num = 0: Builds multi-digit numbers
- prev_op = '+': First number treated as "+num" (pushed as positive)
- char.isdigit(): Check if building a number
- num * 10 + int(char): Shift left and add digit (1 → 12 → 123)
- i == len(s) - 1: Process last number even without trailing operator
- prev_op == '+': Push positive number to stack
- prev_op == '-': Push negative number (will be added at end)
- prev_op == '*': Pop, multiply, push (immediate evaluation)
- prev_op == '/': Pop, divide with truncation, push
- int(stack.pop() / num): Truncates toward zero (not floor!)
- sum(stack): All * and / done; now just sum remaining values

HOW IT WORKS (Example: "3+2*2"):

┌─ Initial State ───────────────────────────────────────────┐
│  stack = [], num = 0, prev_op = '+'                       │
└───────────────────────────────────────────────────────────┘

┌─ i=0, char='3' ───────────────────────────────────────────┐
│  isdigit? Yes → num = 0×10 + 3 = 3                        │
│  is operator? No                                          │
└───────────────────────────────────────────────────────────┘

┌─ i=1, char='+' ───────────────────────────────────────────┐
│  isdigit? No                                              │
│  is operator? Yes                                         │
│  prev_op = '+' → push 3                                   │
│  stack = [3]                                              │
│  prev_op = '+', num = 0                                   │
└───────────────────────────────────────────────────────────┘

┌─ i=2, char='2' ───────────────────────────────────────────┐
│  isdigit? Yes → num = 0×10 + 2 = 2                        │
│  is operator? No                                          │
└───────────────────────────────────────────────────────────┘

┌─ i=3, char='*' ───────────────────────────────────────────┐
│  isdigit? No                                              │
│  is operator? Yes                                         │
│  prev_op = '+' → push 2                                   │
│  stack = [3, 2]                                           │
│  prev_op = '*', num = 0                                   │
└───────────────────────────────────────────────────────────┘

┌─ i=4, char='2' (LAST character) ──────────────────────────┐
│  isdigit? Yes → num = 0×10 + 2 = 2                        │
│  i == len(s)-1? Yes → process!                            │
│  prev_op = '*' → pop 2, calculate 2*2=4, push 4           │
│  stack = [3, 4]                                           │
└───────────────────────────────────────────────────────────┘

┌─ Return ──────────────────────────────────────────────────┐
│  sum([3, 4]) = 7 ✓                                        │
└───────────────────────────────────────────────────────────┘

HOW IT WORKS (Example: "14-3/2"):

i=0, '1': num = 1
i=1, '4': num = 14
i=2, '-': prev_op='+' → push 14, stack=[14], prev_op='-'
i=3, '3': num = 3
i=4, '/': prev_op='-' → push -3, stack=[14,-3], prev_op='/'
i=5, '2': num = 2, LAST char!
          prev_op='/' → pop -3, int(-3/2)=-1, push -1
          stack = [14, -1]

Return: sum([14, -1]) = 13 ✓

WHY STACK APPROACH WORKS:
┌────────────────────────────────────────────────────────────┐
│  Expression: "2 + 3 * 4 - 5"                               │
│                                                            │
│  Step by step:                                             │
│  • See 2, prev_op='+': push +2      stack=[2]              │
│  • See 3, prev_op='+': push +3      stack=[2,3]            │
│  • See 4, prev_op='*': pop 3, 3*4=12, push 12              │
│                                     stack=[2,12]           │
│  • See 5, prev_op='-': push -5      stack=[2,12,-5]        │
│                                                            │
│  sum([2, 12, -5]) = 9                                      │
│                                                            │
│  Verify: 2 + (3*4) - 5 = 2 + 12 - 5 = 9 ✓                 │
│                                                            │
│  The stack "defers" + and - until all * and / are done!   │
└────────────────────────────────────────────────────────────┘

WHY int(a/b) NOT a//b:
┌────────────────────────────────────────────────────────────┐
│  Problem says: "truncate toward zero"                      │
│                                                            │
│  -7 / 2:                                                   │
│  • Floor (//):    -7 // 2 = -4    (toward -∞)   ✗         │
│  • Truncate:   int(-7 / 2) = -3   (toward 0)    ✓         │
│                                                            │
│  7 / 2:                                                    │
│  • Both give 3 (same when positive)                        │
└────────────────────────────────────────────────────────────┘

HANDLING SPACES:
┌────────────────────────────────────────────────────────────┐
│  Spaces are implicitly skipped!                            │
│                                                            │
│  " 3 + 2 "                                                 │
│   ^ not digit, not operator → does nothing                 │
│                                                            │
│  The only condition that matters:                          │
│  • isdigit() → build number                                │
│  • in '+-*/' → process                                     │
│  • i == len(s)-1 → process last number                     │
│                                                            │
│  Spaces don't match any condition (except possibly last)   │
│  But if last char is space, num=0, no harm done            │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION (explicit space handling):

class Solution:
    def calculate(self, s: str) -> int:
        s = s.replace(' ', '')                                                   # Remove all spaces first
        
        stack = []
        num = 0
        prev_op = '+'
        
        for i, char in enumerate(s):
            if char.isdigit():
                num = num * 10 + int(char)
            
            if char in '+-*/' or i == len(s) - 1:
                if prev_op == '+':
                    stack.append(num)
                elif prev_op == '-':
                    stack.append(-num)
                elif prev_op == '*':
                    stack.append(stack.pop() * num)
                elif prev_op == '/':
                    stack.append(int(stack.pop() / num))
                
                prev_op = char
                num = 0
        
        return sum(stack)

ALTERNATIVE SOLUTION (without stack, two-pass idea in one pass):

class Solution:
    def calculate(self, s: str) -> int:
        result = 0                                                               # Final result
        last_num = 0                                                             # Last number (for * /)
        num = 0
        prev_op = '+'
        
        for i, char in enumerate(s):
            if char.isdigit():
                num = num * 10 + int(char)
            
            if char in '+-*/' or i == len(s) - 1:
                if prev_op == '+':
                    result += last_num
                    last_num = num
                elif prev_op == '-':
                    result += last_num
                    last_num = -num
                elif prev_op == '*':
                    last_num = last_num * num
                elif prev_op == '/':
                    last_num = int(last_num / num)
                
                prev_op = char
                num = 0
        
        return result + last_num

COMPARISON WITH PROBLEM 224:
┌────────────────────────────────────────────────────────────┐
│                224                  │        227           │
├─────────────────────────────────────┼──────────────────────┤
│  Operators: + -                     │  Operators: + - * /  │
│  Has: ( )                           │  No parentheses      │
│  Stack stores: (result, sign)       │  Stack stores: nums  │
│  Push on '('                        │  Push on + -         │
│  Pop on ')'                         │  Pop+calc on * /     │
│  Precedence via nesting             │  Precedence via stack│
└─────────────────────────────────────┴──────────────────────┘

EDGE CASES:
- Single number: "42" → 42 ✓
- All additions: "1+2+3" → 6 ✓
- All multiplications: "2*3*4" → 24 ✓
- Division truncation: " 3/2 " → 1 ✓
- Negative result: "1-5" → -4 ✓
- Complex: "1+2*3-4/2" → 1+6-2 = 5 ✓
- Spaces everywhere: " 1 + 2 " → 3 ✓

TIME COMPLEXITY: O(n)
- Single pass through the string
- Each character processed once
- Stack operations are O(1)
- Final sum is O(n) worst case

SPACE COMPLEXITY: O(n)
- Stack can have up to n/2 numbers
- Example: "1+2+3+4+5" → stack = [1,2,3,4,5]

CONCEPTS USED:
- Stack for deferred operations
- Operator precedence handling
- Multi-digit number parsing
- Truncation toward zero
- Previous operator tracking pattern
"""
