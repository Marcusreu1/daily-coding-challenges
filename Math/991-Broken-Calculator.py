# 991. Broken Calculator
# Difficulty: Medium
# https://leetcode.com/problems/broken-calculator/

"""
PROBLEM:
There is a broken calculator that has the integer `startValue` on its display initially. In one operation, you can:
1. Multiply the number on display by 2.
2. Subtract 1 from the number on display.
Given two integers `startValue` and `target`, return the minimum number of operations needed to display `target`.

EXAMPLES:
Input: startValue = 2, target = 3
Output: 2 (Multiply by 2 to get 4, subtract 1 to get 3).

Input: startValue = 5, target = 8
Output: 2 (Subtract 1 to get 4, multiply by 2 to get 8).

Input: startValue = 3, target = 10
Output: 3 (Multiply by 2 to get 6, subtract 1 to get 5, multiply by 2 to get 10).

CONSTRAINTS:
- 1 <= startValue, target <= 10^9

MATHEMATICAL REDUCTION:
Working forwards from `startValue` to `target` creates a massive branching decision tree (should I subtract or multiply?).
However, working backwards from `target` to `startValue` creates a deterministic path.
The reverse operations are:
1. Divide by 2 (only valid if the number is even).
2. Add 1.

Greedy Backward Logic:
- If `target` is ODD, we cannot divide by 2. We MUST add 1.
- If `target` is EVEN and strictly greater than `startValue`, the fastest way to reduce the gap is to divide by 2.
- If `target` falls below `startValue`, we can only add 1 repeatedly. The remaining operations are simply `startValue - target`.

VISUALIZATION (startValue = 3, target = 10):
Working backwards from 10 to 3.

Target = 10 (Even):
├── Target is even, divide by 2.
├── Target becomes 5.
└── Operations = 1

Target = 5 (Odd):
├── Target is odd, add 1.
├── Target becomes 6.
└── Operations = 2

Target = 6 (Even):
├── Target is even, divide by 2.
├── Target becomes 3.
└── Operations = 3

Target = 3:
├── Target == startValue. Loop breaks.
├── Remaining operations: startValue - target = 3 - 3 = 0.
└── Total operations = 3 + 0 = 3.

Result: 3 ✓
"""

# STEP 1: Initialize an operations counter.
# STEP 2: Loop backwards while the target is strictly greater than the startValue.
# STEP 3: If target is even, divide it by 2 to greedily shrink the gap.
# STEP 4: If target is odd, add 1 to make it even for the next division.
# STEP 5: Increment operations count for each step taken.
# STEP 6: Once target <= startValue, add the remaining linear difference to the operations counter.

class Solution:
    def brokenCalc(self, startValue: int, target: int) -> int:
        
        ops = 0                                                                # Track total operations
        
        while target > startValue:                                             # Work backwards until target is no longer greater
            
            if target % 2 == 0:                                                # If the target is even
                target //= 2                                                   # Reverse of multiply by 2
            else:                                                              # If the target is odd
                target += 1                                                    # Reverse of subtract 1
                
            ops += 1                                                           # Increment operation count
            
        return ops + (startValue - target)                                     # Add the remaining linear steps

"""
WHY EACH PART:
- while target > startValue: As long as the target is larger, it makes mathematical sense to attempt halving it. Halving shrinks distances exponentially.
- target //= 2: Using integer division securely halves the number without converting it to a float.
- target += 1: Forces an odd number to become even so it can be halved in the very next loop iteration.
- ops + (startValue - target): Once the target dips below the startValue, the only reverse operation available is addition (+1). Instead of simulating this in a loop, we calculate the remaining steps instantly using simple subtraction.

HOW IT WORKS (Example: startValue = 5, target = 8):

Initial: startValue = 5, target = 8, ops = 0

Iteration 1:
├── target (8) > startValue (5) -> True
├── target % 2 == 0 (8 is even) -> True
├── target = 8 // 2 = 4
└── ops = 1

Iteration 2:
├── target (4) > startValue (5) -> False (Loop terminates)

Final Return:
├── ops = 1
├── startValue - target = 5 - 4 = 1
└── return 1 + 1 = 2 ✓

KEY TECHNIQUE:
- Reverse Engineering / Greedy Algorithm. Changing the perspective from "building up" to "breaking down" eliminates the branching factor entirely, turning an exponential problem into a logarithmic one.

EDGE CASES:
- startValue == target: Loop doesn't execute. Returns 0 + (5 - 5) = 0. ✓
- startValue > target: Loop doesn't execute. Returns linear difference. (e.g., 10 to 5 requires five -1 operations). ✓

TIME COMPLEXITY: O(log(target)) - At worst, we divide the target by 2 in every other step. This gives logarithmic time complexity, making it incredibly fast even for bounds up to 10^9.
SPACE COMPLEXITY: O(1) - Only two integer variables (`ops` and `target`) are manipulated, regardless of the input sizes.

CONCEPTS USED:
- Math
- Greedy Algorithms
"""
