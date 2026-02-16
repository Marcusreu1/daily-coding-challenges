# 282. Expression Add Operators
# Difficulty: Hard
# https://leetcode.com/problems/expression-add-operators/

"""
PROBLEM:
Given a string num containing only digits and an integer target, return all
possibilities to insert the binary operators '+', '-', and/or '*' between
the digits of num so that the resultant expression evaluates to the target.

Note that operands in the returned expressions should not contain leading zeros.

EXAMPLES:
Input: num = "123", target = 6 → Output: ["1*2*3","1+2+3"]
Input: num = "232", target = 8 → Output: ["2*3+2","2+3*2"]
Input: num = "3456237490", target = 9191 → Output: []

CONSTRAINTS:
- 1 <= num.length <= 10
- num consists of only digits
- -2³¹ <= target <= 2³¹ - 1

KEY INSIGHT:
Use backtracking to try all combinations of operators and multi-digit numbers.
The tricky part is handling multiplication precedence.

CHALLENGE: Multiplication Precedence
When we see "2 + 3 * 4", we've already computed "2 + 3 = 5".
To correctly apply *, we need to:
1. "Undo" the previous addition: 5 - 3 = 2
2. Apply multiplication: 3 * 4 = 12
3. Add back: 2 + 12 = 14

SOLUTION:
Track 'prev' (previous operand) so we can undo when we see multiplication.
- For '+': result = result + curr, prev = curr
- For '-': result = result - curr, prev = -curr
- For '*': result = result - prev + (prev * curr), prev = prev * curr
"""

# STEP 1: Initialize result list and start backtracking
# STEP 2: For each position, try all possible number lengths
# STEP 3: Skip numbers with leading zeros (except "0" itself)
# STEP 4: Apply each operator (+, -, *) and recurse
# STEP 5: When reaching end, check if result equals target

from typing import List

class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        
        results = []
        n = len(num)
        
        def backtrack(idx: int, expr: str, result: int, prev: int):
            """
            idx: current position in num
            expr: expression built so far
            result: current evaluation result
            prev: previous operand (for handling multiplication)
            """
            
            if idx == n:                                                         # Reached end of string
                if result == target:
                    results.append(expr)
                return
            
            for i in range(idx, n):                                              # Try all substring lengths
                
                # Skip numbers with leading zeros (except "0" itself)
                if i > idx and num[idx] == '0':
                    break
                
                curr_str = num[idx:i+1]                                          # Current number as string
                curr = int(curr_str)                                             # Current number as int
                
                if idx == 0:                                                     # First number, no operator
                    backtrack(i + 1, curr_str, curr, curr)
                else:
                    # Try addition
                    backtrack(i + 1, expr + '+' + curr_str, result + curr, curr)
                    
                    # Try subtraction
                    backtrack(i + 1, expr + '-' + curr_str, result - curr, -curr)
                    
                    # Try multiplication (need to undo previous operation)
                    backtrack(i + 1, expr + '*' + curr_str, 
                              result - prev + prev * curr, prev * curr)
        
        backtrack(0, "", 0, 0)
        return results


"""
WHY EACH PART:
- results = []: Collect all valid expressions
- n = len(num): Length of input string
- idx: Current position in the string
- expr: Expression string being built
- result: Running evaluation of the expression
- prev: Previous operand (crucial for multiplication)
- if idx == n: Base case - reached end of string
- result == target: Check if current expression evaluates to target
- for i in range(idx, n): Try numbers of length 1, 2, 3, ...
- if i > idx and num[idx] == '0': break: Skip leading zeros
- idx == 0: First number has no operator before it
- result + curr: Addition is straightforward
- result - curr, prev = -curr: For subtraction, prev is negative
- result - prev + prev * curr: Undo prev, apply multiplication
- prev * curr: New prev for chained multiplications

HOW IT WORKS (Example: num = "123", target = 6):

┌─ Initial Call ────────────────────────────────────────────┐
│  backtrack(0, "", 0, 0)                                   │
│  First number - try "1", "12", "123"                      │
└───────────────────────────────────────────────────────────┘

┌─ Try "1" as first number ─────────────────────────────────┐
│  backtrack(1, "1", 1, 1)                                  │
│                                                           │
│  Try "+2": backtrack(2, "1+2", 3, 2)                      │
│    Try "+3": backtrack(3, "1+2+3", 6, 3)                  │
│      idx==3, result==6==target ✓ → add "1+2+3"           │
│    Try "-3": backtrack(3, "1+2-3", 0, -3)                 │
│      idx==3, result==0≠6 ✗                               │
│    Try "*3": backtrack(3, "1+2*3", 3-2+2*3=7, 6)         │
│      idx==3, result==7≠6 ✗                               │
│                                                           │
│  Try "-2": backtrack(2, "1-2", -1, -2)                    │
│    ... (no path reaches 6)                               │
│                                                           │
│  Try "*2": backtrack(2, "1*2", 2, 2)                      │
│    Try "+3": backtrack(3, "1*2+3", 5, 3)                  │
│      idx==3, result==5≠6 ✗                               │
│    Try "-3": backtrack(3, "1*2-3", -1, -3)               │
│      idx==3, result==-1≠6 ✗                              │
│    Try "*3": backtrack(3, "1*2*3", 2-2+2*3=6, 6)         │
│      idx==3, result==6==target ✓ → add "1*2*3"           │
└───────────────────────────────────────────────────────────┘

┌─ Try "12" as first number ────────────────────────────────┐
│  backtrack(2, "12", 12, 12)                               │
│    Try "+3": backtrack(3, "12+3", 15, 3) → 15≠6 ✗        │
│    Try "-3": backtrack(3, "12-3", 9, -3) → 9≠6 ✗         │
│    Try "*3": backtrack(3, "12*3", 36, 36) → 36≠6 ✗       │
└───────────────────────────────────────────────────────────┘

┌─ Try "123" as first number ───────────────────────────────┐
│  backtrack(3, "123", 123, 123)                            │
│  idx==3, result==123≠6 ✗                                 │
└───────────────────────────────────────────────────────────┘

Final result: ["1+2+3", "1*2*3"]

MULTIPLICATION PRECEDENCE DETAILED:
┌────────────────────────────────────────────────────────────┐
│  Expression: "2 + 3 * 4"                                   │
│                                                            │
│  Step 1: Process "2"                                       │
│    result = 2, prev = 2                                    │
│                                                            │
│  Step 2: Process "+ 3"                                     │
│    result = 2 + 3 = 5                                      │
│    prev = 3                                                │
│                                                            │
│  Step 3: Process "* 4"                                     │
│    We have: result=5, prev=3, curr=4                       │
│                                                            │
│    Wrong way: 5 * 4 = 20 ✗                                │
│                                                            │
│    Correct way:                                            │
│    result = result - prev + (prev * curr)                  │
│           = 5 - 3 + (3 * 4)                                │
│           = 2 + 12                                         │
│           = 14 ✓                                           │
│                                                            │
│    New prev = prev * curr = 3 * 4 = 12                    │
│    (for chained multiplications like "2+3*4*5")           │
└────────────────────────────────────────────────────────────┘

WHY prev = -curr FOR SUBTRACTION:
┌────────────────────────────────────────────────────────────┐
│  Expression: "5 - 3 * 2"                                   │
│                                                            │
│  Step 1: Process "5"                                       │
│    result = 5, prev = 5                                    │
│                                                            │
│  Step 2: Process "- 3"                                     │
│    result = 5 - 3 = 2                                      │
│    prev = -3  (negative!)                                  │
│                                                            │
│  Step 3: Process "* 2"                                     │
│    result = result - prev + (prev * curr)                  │
│           = 2 - (-3) + ((-3) * 2)                          │
│           = 2 + 3 - 6                                      │
│           = -1                                             │
│                                                            │
│  Check: 5 - (3 * 2) = 5 - 6 = -1 ✓                        │
│                                                            │
│  By storing prev as negative, the formula works for both  │
│  addition and subtraction cases!                          │
└────────────────────────────────────────────────────────────┘

LEADING ZEROS HANDLING:
┌────────────────────────────────────────────────────────────┐
│  num = "105"                                               │
│                                                            │
│  At idx=1 (digit '0'):                                     │
│  • Try "0" only (i=1): valid                              │
│  • Try "05" (i=2): i > idx and num[idx]=='0' → break!    │
│                                                            │
│  This prevents expressions like "1*05" or "1+05"          │
│  But allows "1*0+5" (where 0 is a standalone number)      │
└────────────────────────────────────────────────────────────┘
EDGE CASES:
- num = "0", target = 0: Returns ["0"] ✓
- num = "00", target = 0: Returns ["0+0", "0-0", "0*0"] ✓
- num = "3456237490", target = 9191: Returns [] ✓
- num = "1", target = 1: Returns ["1"] ✓
- Negative target: Handled by subtraction ✓
- Overflow: Need to be careful with very large numbers

VERIFICATION TABLE:
┌─────────────┬────────┬────────────────────────────────────┐
│    num      │ target │            Output                  │
├─────────────┼────────┼────────────────────────────────────┤
│   "123"     │   6    │ ["1+2+3", "1*2*3"]                 │
│   "232"     │   8    │ ["2+3*2", "2*3+2"]                 │
│   "105"     │   5    │ ["1*0+5", "10-5"]                  │
│   "00"      │   0    │ ["0+0", "0-0", "0*0"]              │
│   "123"     │   123  │ ["123"]                            │
└─────────────┴────────┴────────────────────────────────────┘

TIME COMPLEXITY: O(4^n × n)
- At each position (n-1 of them), we have up to 4 choices
  (3 operators + option to extend current number)
- Building expression string takes O(n)
- Total: O(4^n × n)

SPACE COMPLEXITY: O(n)
- Recursion depth is at most n
- Expression string length is O(n)
- Not counting output space

CONCEPTS USED:
- Backtracking
- Expression evaluation
- Operator precedence handling
- String manipulation
- Avoiding leading zeros
- Tracking previous operand for multiplication
"""
