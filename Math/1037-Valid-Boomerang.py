# 1037. Valid Boomerang
# Difficulty: Easy
# https://leetcode.com/problems/valid-boomerang/

"""
PROBLEM:
Given an array `points` where points[i] = [xi, yi] represents a point on the X-Y plane, return true if these points are a boomerang.
A boomerang is a set of three points that are all distinct and not in a straight line.

EXAMPLES:
Input: points = [[1,1],[2,3],[3,2]]
Output: true (Forms a triangle).

Input: points = [[1,1],[2,2],[3,3]]
Output: false (Forms a straight line).

CONSTRAINTS:
- points.length == 3
- points[i].length == 2
- 0 <= xi, yi <= 100

MATHEMATICAL REDUCTION:
To check if three points A(x1, y1), B(x2, y2), and C(x3, y3) form a boomerang, they must not be collinear.
Normally, we check collinearity by comparing the slopes of segment AB and segment AC:
(y2 - y1) / (x2 - x1) == (y3 - y1) / (x3 - x1)

However, calculating slopes using division is dangerous in programming due to the risk of Division by Zero (which occurs with vertical lines where x1 == x2).
To avoid division entirely, we use cross-multiplication:
(y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)

If the cross products are equal, the points are in a straight line (or some points are identical). 
To be a valid boomerang, the cross products MUST NOT be equal.

VISUALIZATION (points = [[1,1], [2,3], [3,2]]):
A = (1, 1)
B = (2, 3)
C = (3, 2)

Left side (Slope AB's Y difference * Slope AC's X difference):
(y2 - y1) * (x3 - x1) = (3 - 1) * (3 - 1) = 2 * 2 = 4

Right side (Slope AC's Y difference * Slope AB's X difference):
(y3 - y1) * (x2 - x1) = (2 - 1) * (2 - 1) = 1 * 1 = 1

Compare:
4 != 1  -> True (They are not collinear).

Result: True ✓
"""

# STEP 1: Unpack the three coordinates into easily readable variables (x1, y1, etc.)
# STEP 2: Calculate the left side of the cross-multiplication formula.
# STEP 3: Calculate the right side of the cross-multiplication formula.
# STEP 4: Return True if they are not equal, meaning the points form a valid triangle.

class Solution:
    def isBoomerang(self, points: list[list[int]]) -> bool:
        
        x1, y1 = points[0]                                                     # Point A
        x2, y2 = points[1]                                                     # Point B
        x3, y3 = points[2]                                                     # Point C
        
        left_side = (y2 - y1) * (x3 - x1)                                      # Cross multiplication Part 1
        right_side = (y3 - y1) * (x2 - x1)                                     # Cross multiplication Part 2
        
        return left_side != right_side                                         # True if not collinear

"""
WHY EACH PART:
- Unpacking (x1, y1 = points[0]): This makes the mathematical formula explicitly clear and prevents index-clutter like points[0][0], which is prone to typos.
- left_side != right_side: We want to return True ONLY when the points are NOT collinear. If they are equal, it forms a straight line or the points overlap.

HOW IT WORKS (Example: [[1,1], [2,2], [3,3]]):

Initial State:
├── x1=1, y1=1
├── x2=2, y2=2
├── x3=3, y3=3

Math Evaluation:
├── left_side = (2 - 1) * (3 - 1) = 1 * 2 = 2
├── right_side = (3 - 1) * (2 - 1) = 2 * 1 = 2
└── 2 != 2 -> False

Exit:
return False ✓

KEY TECHNIQUE:
- Geometry / Cross Multiplication. Transforming division into multiplication completely neutralizes the ZeroDivisionError edge case, providing a robust, purely arithmetic O(1) solution.

EDGE CASES:
- Identical points (e.g., [1,1], [1,1], [2,2]): Differences become 0. The equation becomes 0 != 0 (False), correctly identifying it is not a boomerang. ✓
- Vertical lines (e.g., [1,1], [1,2], [1,3]): X differences are 0. Cross multiplication yields 0 != 0 (False), successfully avoiding division by zero crashes. ✓
- Horizontal lines (e.g., [1,1], [2,1], [3,1]): Y differences are 0. Yields 0 != 0 (False). ✓

TIME COMPLEXITY: O(1) - The algorithm performs a fixed number of basic arithmetic operations regardless of input.
SPACE COMPLEXITY: O(1) - Memory allocation is limited to a few integer variables.

CONCEPTS USED:
- Math
- Geometry (Collinearity)
"""
