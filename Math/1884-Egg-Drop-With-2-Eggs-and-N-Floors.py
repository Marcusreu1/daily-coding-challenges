# 1884. Egg Drop With 2 Eggs and N Floors
# Difficulty: Medium
# https://leetcode.com/problems/egg-drop-with-2-eggs-and-n-floors/

"""
PROBLEM:
You are given two identical eggs and you have access to a building with n floors labeled from 1 to n.
You know that there exists a floor f where 0 <= f <= n such that any egg dropped at a floor strictly higher than f will break, and any egg dropped at or below floor f will not break.
In each move, you may take an unbroken egg and drop it from any floor x (where 1 <= x <= n). If the egg breaks, you can no longer use it. However, if the egg does not break, you may reuse it in future moves.
Return the minimum number of moves that you need to determine with certainty what the value of f is.

EXAMPLES:
Input: n = 2 → Output: 2
Explanation: We can drop the first egg from floor 1. If it breaks, we know f = 0.
If it does not break, drop the egg from floor 2. If it breaks, we know f = 1.
If it does not break, we know f = 2.
It takes a maximum of 2 moves to determine f.

Input: n = 100 → Output: 14
Explanation: One optimal strategy is:
- Drop the 1st egg at floor 14. If it breaks, we have 1 egg left to check 13 floors (1 + 13 = 14 drops max).
- If it doesn't break, drop the 1st egg at floor 27 (14 + 13). If it breaks, check floors 15 to 26 (2 + 12 = 14 drops max).
- If it doesn't break, drop at 39 (27 + 12), and so on.
We can cover up to 105 floors with 14 drops.

CONSTRAINTS:
- 1 <= n <= 1000

MATH RULES (MINIMAX & GAUSS SUMMATION):
If we are allowed 'x' drops, the first drop must be from floor 'x'.
If it breaks, we use our 1 remaining egg and 'x-1' remaining drops to linearly check floors 1 to x-1. (Total drops = 1 + x - 1 = x).
If it survives, we have 'x-1' drops left. To maintain the same worst-case scenario, our next jump can only be 'x-1' floors up.
This creates a decreasing arithmetic progression for the floor intervals: x, x-1, x-2, ..., 1.
The maximum number of floors we can cover with 'x' drops is the sum of this sequence: x*(x+1)/2.
We just need to find the smallest integer 'x' where x*(x+1)/2 >= n.

VISUALIZATION (n = 10):
Initial: drops = 0, floors_covered = 0

Iteration 1: drops = 1, floors_covered = 0 + 1 = 1
Iteration 2: drops = 2, floors_covered = 1 + 2 = 3
Iteration 3: drops = 3, floors_covered = 3 + 3 = 6
Iteration 4: drops = 4, floors_covered = 6 + 4 = 10

floors_covered (10) >= n (10). Loop ends.
Result: 4 drops ✓
"""

# STEP 1: Initialize counters for the number of drops allowed and the total floors those drops can cover.
# STEP 2: Use a while loop to increment the drops one by one until the floors covered meets or exceeds n.
# STEP 3: Add the current allowed drops to the floors covered, reflecting the decreasing arithmetic progression logic.
# STEP 4: Return the optimal number of drops.

class Solution:
    def twoEggDrop(self, n: int) -> int:
        
        drops = 0
        floors_covered = 0
        
        # Increase the drop budget until we can cover the entire building
        while floors_covered < n:
            drops += 1
            floors_covered += drops
            
        return drops

"""
WHY EACH PART:
- drops += 1: Simulates increasing our worst-case drop budget by 1.
- floors_covered += drops: Maps to the mathematical reality that a budget of 'd' drops allows the first egg to safely skip exactly 'd' floors higher than the last safe point.

HOW IT WORKS (Example: n = 6):

Initial: drops = 0, floors_covered = 0

Iteration 1:
├── drops = 0 + 1 = 1
└── floors_covered = 0 + 1 = 1 (Loop continues: 1 < 6)

Iteration 2:
├── drops = 1 + 1 = 2
└── floors_covered = 1 + 2 = 3 (Loop continues: 3 < 6)

Iteration 3:
├── drops = 2 + 1 = 3
└── floors_covered = 3 + 3 = 6 (Loop condition 6 < 6 becomes False)

Exit loop.

Return 3 ✓

KEY TECHNIQUE:
- Mathematical Reduction (Arithmetic Progression): Transforming a complex Dynamic Programming / Minimax problem into a simple summation sequence. 
- Iterative Root Finding: Instead of resolving the quadratic equation mathematically (which requires floating-point square root operations), calculating it iteratively in O(sqrt(N)) is extremely clean and safe.

EDGE CASES:
- n = 1: Loop runs exactly once. drops = 1, floors_covered = 1. Returns 1. Correct, we drop the egg from floor 1.

TIME COMPLEXITY: O(sqrt(N)) - The number of iterations is strictly the root 'x' of x*(x+1)/2 = N. For N = 1000, it runs maximum 45 times. Extremely fast.
SPACE COMPLEXITY: O(1) - Only two integer variables are allocated.

CONCEPTS USED:
- Dynamic Programming principles (Minimax)
- Gauss Summation / Arithmetic Series
- Math Modeling
"""
