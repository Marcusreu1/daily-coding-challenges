# 1217. Minimum Cost to Move Chips to The Same Position
# Difficulty: Easy
# https://leetcode.com/problems/minimum-cost-to-move-chips-to-the-same-position/

"""
PROBLEM:
We have `n` chips, where the position of the `i-th` chip is `position[i]`.
We can perform the following types of moves any number of times (possibly zero) on any chip:
- Move the `i-th` chip by 2 units to the left or to the right with a cost of 0.
- Move the `i-th` chip by 1 unit to the left or to the right with a cost of 1.

Return the minimum cost needed to move all the chips to the same position.

EXAMPLES:
Input: position = [1,2,3]
Output: 1
Explanation: First step: Move the chip at position 3 to position 1 with cost = 0.
Second step: Move the chip at position 2 to position 1 with cost = 1.
Total cost is 1.

Input: position = [2,2,2,3,3]
Output: 2
Explanation: We can move the two chips at position 3 to position 2. Each move costs 1. Total cost = 2.

CONSTRAINTS:
- 1 <= position.length <= 100
- 1 <= position[i] <= 10^9

ALGORITHMIC INTUITION (THE "TRICK"):
The problem seems to ask for an optimal target position, but the movement rules hide a massive shortcut:
Moving by 2 costs absolutely NOTHING. 
This means a chip at position 2 can move to 4, 6, 8, 10... or 0 for free. 
A chip at position 1 can move to 3, 5, 7, 9... or 1 for free.

Notice the pattern? 
- ALL chips at EVEN positions can be moved to the exact same even position (e.g., position 0) for a cost of 0.
- ALL chips at ODD positions can be moved to the exact same odd position (e.g., position 1) for a cost of 0.

So, virtually, we don't have chips scattered across 10^9 positions. We only ever have two piles of chips:
1. The "Even" pile
2. The "Odd" pile
These two piles are exactly 1 unit apart. To merge them, we must pay 1 coin per chip. 
To minimize the cost, we simply move the smaller pile into the larger pile.
The answer is just `min(even_count, odd_count)`.
"""

# STEP 1: Initialize counters for chips at even and odd positions.
# STEP 2: Iterate through the given positions.
# STEP 3: If the position is even, increment the even counter.
# STEP 4: If the position is odd, increment the odd counter.
# STEP 5: Return the minimum of the two counters.

from typing import List

class Solution:
    def minCostToMoveChips(self, position: List[int]) -> int:
        
        even_count = 0
        odd_count = 0
        
        # Step 2-4: Count the parity of the positions
        for p in position:
            if p % 2 == 0:
                even_count += 1
            else:
                odd_count += 1
                
        # Step 5: The cost is moving the smaller pile to the larger one
        return min(even_count, odd_count)

"""
WHY EACH PART:
- p % 2 == 0: The standard mathematical check for parity (even numbers).
- min(even_count, odd_count): Since the two piles are 1 unit apart, every chip in the pile we decide to move will cost exactly 1. Minimizing the cost means moving the pile with fewer chips.

HOW IT WORKS (Example: position = [2,2,2,3,3]):
Initial: even_count = 0, odd_count = 0

Counting Loop:
├── Chip 1 at pos 2 -> Even (even_count = 1)
├── Chip 2 at pos 2 -> Even (even_count = 2)
├── Chip 3 at pos 2 -> Even (even_count = 3)
├── Chip 4 at pos 3 -> Odd  (odd_count = 1)
└── Chip 5 at pos 3 -> Odd  (odd_count = 2)

Totals:
├── Evens = 3 chips
└── Odds = 2 chips

Merge Calculation:
├── Move Evens to Odds? Cost = 3 * 1 = 3
├── Move Odds to Evens? Cost = 2 * 1 = 2
└── min(3, 2) = 2.

Return 2. ✓

TIME COMPLEXITY: O(N) - We iterate through the list of chips exactly once.
SPACE COMPLEXITY: O(1) - We only store two integer counters, regardless of the number of chips.

CONCEPTS USED:
- Math (Parity)
- Greedy Algorithm
- Abstraction / Reduction
"""
