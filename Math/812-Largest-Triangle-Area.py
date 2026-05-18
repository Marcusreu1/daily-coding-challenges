# 812. Largest Triangle Area
# Difficulty: Easy
# https://leetcode.com/problems/largest-triangle-area/

"""
PROBLEM:
Given an array of points on the X-Y plane points where points[i] = [xi, yi], 
return the area of the largest triangle that can be formed by any three different points. 
Answers within 10^-5 of the actual answer will be accepted.

EXAMPLES:
Input: points = [[0,0],[0,1],[1,0],[0,2],[2,0]]   → Output: 2.00000
Explanation: 
The five points are plotted on a 2D plane.
The maximum area is formed by the points [0,0], [0,2], and [2,0].
Base = 2, Height = 2. Area = (2 * 2) / 2 = 2.0.

Input: points = [[1,0],[0,0],[0,1]]              → Output: 0.50000

CONSTRAINTS:
- 3 <= points.length <= 50
- -50 <= points[i][0], points[i][1] <= 50
- All the given points are unique.

LOGIC RULES (BRUTE FORCE & SHOELACE FORMULA):
1. The maximum number of points is 50. The number of combinations of 3 points out of 50 is 
   (50 * 49 * 48) / 6 = 19,600. This is an extremely small number for modern processors.
2. We can safely use Brute Force to iterate through every unique triplet of points.
3. To calculate the area of a triangle purely from its 3 vertex coordinates A(x1, y1), B(x2, y2), C(x3, y3),
   we use the coordinate geometry formula:
   Area = 0.5 * |x1(y2 - y3) + x2(y3 - y1) + x3(y1 - y2)|
4. We track the maximum area found and return it.

VISUALIZATION (points = [[0,0], [0,2], [2,0]]):
Let A = [0,0], B = [0,2], C = [2,0]

Apply formula:
Area = 0.5 * |0(2 - 0) + 0(0 - 0) + 2(0 - 2)|
Area = 0.5 * |0 + 0 + 2(-2)|
Area = 0.5 * |-4|
Area = 0.5 * 4
Area = 2.0 ✓
"""

# STEP 1: Import itertools to easily generate unique combinations
# STEP 2: Initialize max_area variable to 0
# STEP 3: Iterate through every unique triplet of points
# STEP 4: Unpack coordinates for readability
# STEP 5: Apply the coordinate geometry area formula and update max_area

import itertools

class Solution:
    def largestTriangleArea(self, points: list[list[int]]) -> float:
        
        max_area = 0.0
        
        # Step 3: Get all unique triplets of points
        for p1, p2, p3 in itertools.combinations(points, 3):
            
            # Step 4: Unpack coordinates (x1, y1), (x2, y2), (x3, y3)
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            
            # Step 5: Calculate the area using the determinant formula
            current_area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            
            # Update max_area if the new area is larger
            if current_area > max_area:
                max_area = current_area
                
        return max_area

"""
WHY EACH PART:
- itertools.combinations(points, 3): This is the Pythonic way to replace 3 nested for-loops. 
  It guarantees that we pick exactly 3 items and that order doesn't matter (so we don't calculate the same triangle twice).
- abs(...): The order of points might result in a negative area mathematically. Distance and area must always 
  be positive, so the absolute value rectifies this.
- 0.5 *: Matches the (base * height) / 2 logic inherent in the determinant formula for a triangle.

HOW IT WORKS (Example dry run for 4 points):
points = A, B, C, D

itertools.combinations generates:
1. (A, B, C) -> Area calculated
2. (A, B, D) -> Area calculated, max_area updated if larger
3. (A, C, D) -> Area calculated, max_area updated if larger
4. (B, C, D) -> Area calculated, max_area updated if larger

Total loops = 4. Extremely clean and fast.

EDGE CASES:
- Collinear points (points forming a straight line): The formula will naturally calculate their area as 0.0. 
  Since max_area starts at 0.0, it simply ignores them. ✓
- Minimum constraints (exactly 3 points): The loop runs exactly once, calculates the area, and returns it. ✓
- Negative coordinates: Handled perfectly by the mathematical formula without needing any offset adjustments. ✓

TIME COMPLEXITY: O(N^3)
Where N is the number of points. We evaluate every possible combination of 3 points. 
Since N <= 50, N^3 is roughly 125,000 maximum iterations. This executes in less than 50 milliseconds.

SPACE COMPLEXITY: O(1)
The itertools.combinations function returns an iterator (it doesn't store all combinations in memory at once). 
We only store a few float variables, making memory overhead strictly constant.
"""
