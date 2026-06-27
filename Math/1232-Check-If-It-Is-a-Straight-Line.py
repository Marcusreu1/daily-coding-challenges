# 1232. Check If It Is a Straight Line
# Difficulty: Easy
# https://leetcode.com/problems/check-if-it-is-a-straight-line/

"""
PROBLEM:
You are given an array `coordinates`, `coordinates[i] = [x, y]`, where `[x, y]` represents 
the coordinate of a point. Check if these points make a straight line in the XY plane.

EXAMPLES:
Input: coordinates = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]
Output: true

Input: coordinates = [[1,1],[2,2],[3,4],[4,5],[5,6],[7,7]]
Output: false

CONSTRAINTS:
- 2 <= coordinates.length <= 1000
- coordinates[i].length == 2
- -10^4 <= coordinates[i][0], coordinates[i][1] <= 10^4
- coordinates contains no duplicate point.

MATHEMATICAL INTUITION (THE "TRICK"):
To check if multiple points lie on the same straight line, the slope (gradient) between 
any two points must be identical.
The mathematical formula for the slope between two points (x0, y0) and (x1, y1) is:
Slope = (y1 - y0) / (x1 - x0)

The naive approach is to calculate the slope of the first two points, and then check if 
every other point has the same slope. 
HOWEVER, this introduces a fatal flaw: Division by Zero. 
If the straight line is perfectly vertical (e.g., [[0,0], [0,1], [0,2]]), then `x1 - x0` 
is 0, and the program will crash with a ZeroDivisionError.

To fix this elegantly without writing messy `if/else` edge cases, we use Cross-Multiplication.
Instead of comparing division:
(y_i - y0) / (x_i - x0) == (y1 - y0) / (x1 - x0)

We cross-multiply to compare products:
(y_i - y0) * (x1 - x0) == (x_i - x0) * (y1 - y0)

Multiplication never crashes, perfectly handling vertical lines natively!
"""

# STEP 1: Extract the coordinates of the first two points to establish the reference slope.
# STEP 2: Calculate the delta X (dx) and delta Y (dy) for the reference points.
# STEP 3: Iterate through the rest of the points starting from index 2.
# STEP 4: For each point, calculate its delta with respect to the first point.
# STEP 5: Use cross-multiplication to check if the slopes match.
# STEP 6: If any point fails the check, return False. Otherwise, return True.

from typing import List

class Solution:
    def checkStraightLine(self, coordinates: List[List[int]]) -> bool:
        
        # Step 1: Get the first two reference points
        x0, y0 = coordinates[0]
        x1, y1 = coordinates[1]
        
        # Step 2: Calculate the reference differences (dx, dy)
        dx = x1 - x0
        dy = y1 - y0
        
        # Step 3: Check all other points against the reference
        for i in range(2, len(coordinates)):
            x, y = coordinates[i]
            
            # Step 4 & 5: Cross-multiplication to avoid Division by Zero
            # Standard: (y - y0) / (x - x0) == dy / dx
            # Cross-multiplied: (y - y0) * dx == (x - x0) * dy
            if (y - y0) * dx != (x - x0) * dy:
                return False
                
        # Step 6: All points passed the test
        return True

"""
WHY EACH PART:
- x0, y0 = coordinates[0]: We lock the first point as our anchor. Every other point is compared against this anchor to ensure they all share the exact same trajectory.
- (y - y0) * dx != (x - x0) * dy: The absolute core of the solution. It transforms a fragile rational equation (division) into a robust linear equation (multiplication).

HOW IT WORKS (Example: [[1,1], [2,2], [3,4]]):
Initial Anchor Points:
P0 = (1, 1), P1 = (2, 2)
dx = 2 - 1 = 1
dy = 2 - 1 = 1

Iteration 1 (Checking point P2 = (3, 4)):
├── x = 3, y = 4
├── Left side: (y - y0) * dx = (4 - 1) * 1 = 3 * 1 = 3
├── Right side: (x - x0) * dy = (3 - 1) * 1 = 2 * 1 = 2
└── 3 != 2. The slopes do not match! 
Return False ✓ (Indeed, (3,4) breaks the straight diagonal line).

TIME COMPLEXITY: O(N) - We iterate through the array of coordinates exactly once.
SPACE COMPLEXITY: O(1) - We only store a few integer variables (x0, y0, dx, dy) regardless of the input size.

CONCEPTS USED:
- Cartesian Geometry
- Cross-Multiplication (Algebraic transformation)
- Edge-Case Prevention
"""
