# 1033. Moving Stones Until Consecutive
# Difficulty: Medium
# https://leetcode.com/problems/moving-stones-until-consecutive/

"""
PROBLEM:
There are three stones in different positions on the X-axis. You are given three integers a, b, and c, the positions of the stones.
In one move, you pick up a stone at an endpoint (i.e., either the lowest or highest position stone), and move it to an unoccupied position between those endpoints.
The game ends when you cannot make any more moves (i.e., the stones are in three consecutive positions).
Return an integer array answer of length 2 where:
- answer[0] is the minimum number of moves you can play.
- answer[1] is the maximum number of moves you can play.

EXAMPLES:
Input: a = 1, b = 2, c = 5
Output: [1, 2] (Move 5 to 3 for min. Move 5 to 4, then to 3 for max).

Input: a = 4, b = 3, c = 2
Output: [0, 0] (Already consecutive).

Input: a = 3, b = 5, c = 1
Output: [1, 2] (Sort to 1, 3, 5. Move 1 to 4 to finish in 1 move).

CONSTRAINTS:
- 1 <= a, b, c <= 100
- a, b, and c have different values.

MATHEMATICAL REDUCTION:
First, we must sort the positions into x, y, and z where x < y < z.
MAXIMUM MOVES:
To maximize moves, we move an endpoint stone exactly 1 space at a time. The total number of unoccupied spaces between the smallest and largest stone is exactly (z - x) - 2. This is our maximum moves.

MINIMUM MOVES:
We can resolve any configuration in at most 2 moves.
- 0 moves: The stones are already consecutive.
- 1 move: Two stones are either adjacent or exactly 1 empty space apart. We just move the third stone next to them (or right into the middle gap).
- 2 moves: The stones are far apart. We move x next to y, then z next to y.

VISUALIZATION (a = 1, b = 10, c = 20):
Sort: x = 1, y = 10, z = 20

Max Moves:
(20 - 1) - 2 = 17 empty spaces. We can creep inwards 1 space at a time for 17 moves.

Min Moves:
Gap 1 (y - x): 10 - 1 = 9
Gap 2 (z - y): 20 - 10 = 10
Both gaps are > 2. So we need 2 moves.
Move 1: Put 20 at position 9. (Board is now 1, 9, 10).
Move 2: Put 1 at position 8. (Board is now 8, 9, 10).

Result: [2, 17] ✓
"""

# STEP 1: Sort the input coordinates so we have a clear left, middle, and right stone.
# STEP 2: Calculate the maximum moves by counting all empty spaces between the left and right stones.
# STEP 3: Check if the maximum moves is 0. If so, minimum moves is also 0.
# STEP 4: Check if any two stones are adjacent or have exactly 1 empty space between them. If so, minimum moves is 1.
# STEP 5: For all other scattered configurations, the minimum moves is exactly 2.

class Solution:
    def numMovesStones(self, a: int, b: int, c: int) -> list[int]:
        
        x, y, z = sorted([a, b, c])                                            # Sort stones to x < y < z
        
        max_moves = (z - x) - 2                                                # Total empty spaces between extremes
        
        if max_moves == 0:                                                     # Already consecutive
            min_moves = 0
            
        elif y - x <= 2 or z - y <= 2:                                         # Gap is small enough to close in 1 move
            min_moves = 1
            
        else:                                                                  # Large gaps require exactly 2 moves
            min_moves = 2
            
        return [min_moves, max_moves]                                          # Return formatted answer array

"""
WHY EACH PART:
- sorted([a, b, c]): The problem does not guarantee the inputs are in order. Sorting maps them nicely to x, y, z.
- (z - x) - 2: If x=1 and z=4, the distance is 3. The inner spaces are 2 and 3 (which is 2 spaces). The formula precisely counts available spots.
- y - x <= 2 or z - y <= 2: This condition brilliantly catches BOTH adjacent stones (distance 1) and stones with a single gap (distance 2). For instance, if x=2 and y=4, distance is 2 (gap is at 3). We can move z straight to 3, winning in 1 move.

HOW IT WORKS (Example: a = 3, b = 5, c = 1):

Initial State:
├── Unsorted: a = 3, b = 5, c = 1
└── Sorted: x = 1, y = 3, z = 5

Max Moves Logic:
├── max_moves = (5 - 1) - 2 = 4 - 2 = 2

Min Moves Logic:
├── max_moves == 0 ? False (2 != 0)
├── (3 - 1 <= 2) or (5 - 3 <= 2) ? 
├── (2 <= 2) or (2 <= 2) ? True
└── min_moves = 1

Exit:
return [1, 2] ✓

KEY TECHNIQUE:
- Math / Greedy Logic. Instead of simulating the game board state by state, we reduce the rules to distances and logical boundaries, giving us an O(1) mathematical solution.

EDGE CASES:
- Stones are extremely far apart (1, 50, 100): Handled mathematically. Max moves will be (100 - 1) - 2 = 97. Min moves will trigger the 'else' block and yield 2. ✓
- One gap is huge, one is adjacent (1, 2, 100): Min moves triggers the <= 2 check and yields 1. Max moves yields 97. ✓

TIME COMPLEXITY: O(1) - We only sort 3 integers and perform basic arithmetic. It runs in constant time regardless of how large the coordinates are.
SPACE COMPLEXITY: O(1) - We only store a few integer variables.

CONCEPTS USED:
- Math
- Brainteaser
- Sorting
"""
