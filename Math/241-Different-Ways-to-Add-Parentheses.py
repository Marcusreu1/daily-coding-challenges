# 241. Different Ways to Add Parentheses
# Difficulty: Medium
# https://leetcode.com/problems/different-ways-to-add-parentheses/

"""
PROBLEM:
Given a string expression of numbers and operators (+, -, *), return all
possible results from computing all the different possible ways to group
numbers and operators. You may return the answer in any order.

EXAMPLES:
Input: expression = "2-1-1"
Output: [0, 2]
Explanation: (2-1)-1 = 0, 2-(1-1) = 2

Input: expression = "2*3-4*5"
Output: [-34, -14, -10, -10, 10]

CONSTRAINTS:
- 1 <= expression.length <= 20
- expression consists of digits and operators '+', '-', '*'
- All integer values in input are in range [0, 99]
- The integer values do not have leading zeros

KEY INSIGHT:
Use DIVIDE AND CONQUER. For each operator, split the expression into
left and right parts, recursively compute all results for each part,
then combine every left result with every right result using the operator.

BASE CASE:
If expression has no operators, it's just a number - return [number]

RECURSION:
For each operator at position i:
  left_results = solve(expression[0:i])
  right_results = solve(expression[i+1:])
  for each left in left_results:
      for each right in right_results:
          results.append(left operator right)

OPTIMIZATION:
Use memoization to avoid recomputing same subexpressions.
"""

# STEP 1: Check memo for cached result
# STEP 2: Try splitting at each operator
# STEP 3: Recursively solve left and right parts
# STEP 4: Combine all pairs of results
# STEP 5: If no operators found, parse as number (base case)

from typing import List
from functools import lru_cache

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        
        memo = {}                                                                # Cache for subproblems
        
        def compute(expr: str) -> List[int]:
            
            if expr in memo:                                                     # Return cached result
                return memo[expr]
            
            results = []
            
            for i, char in enumerate(expr):                                      # Find each operator
                
                if char in '+-*':                                                # Split at this operator
                    
                    left_part = expr[:i]                                         # Expression left of operator
                    right_part = expr[i+1:]                                      # Expression right of operator
                    
                    left_results = compute(left_part)                            # All results from left
                    right_results = compute(right_part)                          # All results from right
                    
                    for left in left_results:                                    # Combine every pair
                        for right in right_results:
                            
                            if char == '+':
                                results.append(left + right)
                            elif char == '-':
                                results.append(left - right)
                            else:                                                # char == '*'
                                results.append(left * right)
            
            if not results:                                                      # No operators found = just a number
                results.append(int(expr))
            
            memo[expr] = results                                                 # Cache before returning
            return results
        
        return compute(expression)


"""
WHY EACH PART:
- memo = {}: Dictionary to cache results for subexpressions
- if expr in memo: Return already computed results (memoization)
- for i, char in enumerate(expr): Iterate to find operators
- if char in '+-*': We found an operator to split on
- expr[:i]: Left subexpression (before operator)
- expr[i+1:]: Right subexpression (after operator)
- compute(left_part): Recursively get all results from left
- compute(right_part): Recursively get all results from right
- for left... for right...: Cartesian product of all combinations
- if not results: No operators were found → base case, parse number
- memo[expr] = results: Save result before returning

HOW IT WORKS (Example: "2-1-1"):

┌─ compute("2-1-1") ────────────────────────────────────────┐
│                                                           │
│  i=0: '2' not operator                                    │
│  i=1: '-' IS operator                                     │
│      ├── left = "2"                                       │
│      ├── right = "1-1"                                    │
│      ├── compute("2") = [2]        (base case)            │
│      ├── compute("1-1"):                                  │
│      │       ├── i=1: '-' IS operator                     │
│      │       ├── left = "1" → [1]                         │
│      │       ├── right = "1" → [1]                        │
│      │       └── 1 - 1 = 0 → [0]                          │
│      └── 2 - 0 = 2                                        │
│                                                           │
│  i=2: '1' not operator                                    │
│  i=3: '-' IS operator                                     │
│      ├── left = "2-1"                                     │
│      ├── right = "1"                                      │
│      ├── compute("2-1"):                                  │
│      │       ├── i=1: '-' IS operator                     │
│      │       ├── left = "2" → [2]                         │
│      │       ├── right = "1" → [1]                        │
│      │       └── 2 - 1 = 1 → [1]                          │
│      ├── compute("1") = [1]        (base case)            │
│      └── 1 - 1 = 0                                        │
│                                                           │
│  i=4: '1' not operator                                    │
│                                                           │
│  results = [2, 0]                                         │
└───────────────────────────────────────────────────────────┘

HOW IT WORKS (Example: "2*3-4*5"):

Split by '*' at pos 1:  "2" * "3-4*5"
    [2] * compute("3-4*5")
    
Split by '-' at pos 3:  "2*3" - "4*5"
    compute("2*3") - compute("4*5")
    [6] - [20] = [-14]
    
Split by '*' at pos 5:  "2*3-4" * "5"
    compute("2*3-4") * [5]

Each split generates different groupings!

VISUAL: Tree of all groupings for "2*3-4*5"

                        "2*3-4*5"
              ______________|______________
             /              |              \
         "2"*"3-4*5"   "2*3"-"4*5"    "2*3-4"*"5"
            /               |               \
           /                |                \
    2*[...,-17,...]    [6]-[20]      [...,2,-2,...]*5
          |                |                |
       -34,...           -14           10,-10,...

DIVIDE AND CONQUER PATTERN:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  1. DIVIDE: Split expression at each operator              │
│                                                            │
│     "a + b * c"                                            │
│         ↓                                                  │
│     Split at '+': "a" + "b*c"                              │
│     Split at '*': "a+b" * "c"                              │
│                                                            │
│  2. CONQUER: Recursively solve subproblems                 │
│                                                            │
│     solve("a") → [a_value]                                 │
│     solve("b*c") → [all possible results]                  │
│                                                            │
│  3. COMBINE: Apply operator to all pairs                   │
│                                                            │
│     for each left_result:                                  │
│         for each right_result:                             │
│             result = left_result OP right_result           │
│                                                            │
└────────────────────────────────────────────────────────────┘

WHY MEMOIZATION HELPS:
┌────────────────────────────────────────────────────────────┐
│  Expression: "1+2+3+4"                                     │
│                                                            │
│  Without memo:                                             │
│  "1+2" computed when processing:                           │
│    • "1+2" + "3+4"                                         │
│    • "1+2+3" + "4" (internally computes "1+2")            │
│                                                            │
│  With memo:                                                │
│  "1+2" computed once, then retrieved from cache            │
│                                                            │
│  Saves significant time for longer expressions!            │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION (iterative with eval - not recommended but interesting):

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        # Parse tokens
        tokens = []
        num = ''
        for char in expression:
            if char in '+-*':
                tokens.append(int(num))
                tokens.append(char)
                num = ''
            else:
                num += char
        tokens.append(int(num))
        
        # tokens = [num, op, num, op, num, ...]
        n = len(tokens) // 2 + 1  # number of operands
        
        # dp[i][j] = all results for tokens[2*i:2*j+1]
        # ... (complex DP setup)

CATALAN NUMBERS CONNECTION:
┌────────────────────────────────────────────────────────────┐
│  The number of ways to fully parenthesize n operands       │
│  equals the (n-1)th Catalan number:                        │
│                                                            │
│  C(n) = C(2n, n) / (n + 1)                                 │
│                                                            │
│  n=1: C(0) = 1    → "a" (1 way)                            │
│  n=2: C(1) = 1    → "(a+b)" (1 way)                        │
│  n=3: C(2) = 2    → "((a+b)+c)" or "(a+(b+c))"            │
│  n=4: C(3) = 5    → 5 different ways                       │
│  n=5: C(4) = 14   → 14 different ways                      │
│                                                            │
│  This grows as O(4^n / n^1.5) - exponential!              │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- Single number "11": Returns [11] ✓
- Two operands "1+2": Returns [3] ✓
- All same operators "1+2+3": Returns [6, 6] (actually same) ✓
- All multiplications "2*3*4": Returns [24] (all same) ✓
- Mixed operators: Handles correctly ✓
- Multi-digit numbers "10*20": Handles correctly ✓

VERIFICATION TABLE:
┌─────────────────┬─────────────────────────────────────────┐
│   Expression    │              Results                    │
├─────────────────┼─────────────────────────────────────────┤
│      "2"        │  [2]                                    │
│     "1+1"       │  [2]                                    │
│    "2-1-1"      │  [0, 2]                                 │
│    "2*2*2"      │  [8] (only one unique result)           │
│   "2*3-4*5"     │  [-34, -14, -10, -10, 10]               │
│   "1+2+3+4"     │  [10, 10, 10, 10, 10] (5 ways, same)    │
└─────────────────┴─────────────────────────────────────────┘

TIME COMPLEXITY: O(C(n) × n)
- C(n) = Catalan number ≈ 4^n / n^1.5
- n operators mean n+1 operands
- Exponential in number of operators
- Memoization helps avoid redundant work

SPACE COMPLEXITY: O(C(n) × n)
- Memo stores results for all subexpressions
- Each result list can have up to C(n) elements
- Recursion depth up to O(n)

CONCEPTS USED:
- Divide and Conquer
- Recursion with memoization
- Cartesian product of results
- Expression parsing
- Catalan numbers (mathematical background)
"""
