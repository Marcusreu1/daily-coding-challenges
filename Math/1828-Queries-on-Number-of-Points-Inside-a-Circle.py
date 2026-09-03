# 1828. Queries on Number of Points Inside a Circle
# Difficulty: Medium
# https://leetcode.com/problems/queries-on-number-of-points-inside-a-circle/

"""
PROBLEM:
You are given an array points where points[i] = [xi, yi] is the coordinates of the ith point on a 2D plane. Multiple points can have the same coordinates.
You are also given an array queries where queries[j] = [xj, yj, rj] describes a circle centered at (xj, yj) with a radius of rj.
For each query queries[j], compute the number of points inside the jth circle. Points on the border of the circle are considered inside.
Return an array answer, where answer[j] is the answer to the jth query.

EXAMPLES:
Input: points = [[1,3],[3,3],[5,3],[2,2]], queries = [[2,3,1],[4,3,1],[1,1,2]]
Output: [3,2,2]
Explanation: 
- Circle 1: centered at (2,3) with radius 1. Points inside: [1,3], [3,3], [2,2]. (3 points)
- Circle 2: centered at (4,3) with radius 1. Points inside: [3,3], [5,3]. (2 points)
- Circle 3: centered at (1,1) with radius 2. Points inside: [1,3], [2,2]. (2 points)

CONSTRAINTS:
- 1 <= points.length <= 500
- 1 <= queries.length <= 500
- points[i].length == 2
- queries[j].length == 3
- 0 <= xi, yi, xj, yj, rj <= 500

MATH RULES (EUCLIDEAN DISTANCE OPTIMIZATION):
To check if a point (px, py) is inside a circle with center (cx, cy) and radius r, we use the distance formula:
Distance = sqrt((px - cx)^2 + (py - cy)^2)
The condition is: Distance <= r.

However, calculating square roots is computationally expensive and can introduce floating-point precision errors. 
By squaring both sides of the inequality, we can work purely with integers:
(px - cx)^2 + (py - cy)^2 <= r^2

VISUALIZATION (point = [1,3], query = [2,3,1]):
Point: px = 1, py = 3
Circle: cx = 2, cy = 3, r = 1

Calculate squared radius: 1^2 = 1
Calculate squared distance:
  dx = (1 - 2) = -1  -> (-1)^2 = 1
  dy = (3 - 3) = 0   -> (0)^2 = 0
  Squared distance = 1 + 0 = 1

Evaluate: 1 <= 1 -> True. The point is on the border, so it is inside! ✓
"""

from typing import List

# STEP 1: Initialize an empty list to store the answers for each query.
# STEP 2: Iterate through every circle in the queries array.
# STEP 3: Precalculate the squared radius of the current circle to avoid computing it inside the inner loop.
# STEP 4: Iterate through all points for the current circle.
# STEP 5: Apply the integer-only Euclidean distance formula to check if the point is inside.
# STEP 6: Count the valid points and append the count to the answers list.

class Solution:
    def countPoints(self, points: List[List[int]], queries: List[List[int]]) -> List[int]:
        
        answer = []
        
        for cx, cy, r in queries:
            
            points_inside = 0
            # Precalculate r squared to optimize inner loop comparisons
            r_squared = r * r
            
            for px, py in points:
                # Calculate squared distance using pure integers
                squared_distance = (px - cx) ** 2 + (py - cy) ** 2
                
                # If the squared distance is <= squared radius, the point is inside
                if squared_distance <= r_squared:
                    points_inside += 1
                    
            answer.append(points_inside)
            
        return answer

"""
WHY EACH PART:
- r_squared = r * r: Extracted outside the inner loop. Calculating this once per query instead of per point saves N multiplications per query.
- ** 2: Python's exponentiation operator is highly optimized for integer squares.
- No math.sqrt(): Completely avoids importing the math module, type-casting to floats, and potential IEEE 754 precision inaccuracies.

KEY TECHNIQUE:
- Algebraic Simplification: Squaring constraints to remain inside the Integer domain for faster and safer evaluation.
- Nested Iteration: O(P * Q) brute force is acceptable here due to the small upper bounds (500 * 500 = 250,000 operations).

EDGE CASES:
- Point exactly on the center (px == cx and py == cy): Distance is 0, correctly evaluates to 0 <= r^2.
- Point exactly on the edge: Handled correctly by the inclusive '<=' operator.

TIME COMPLEXITY: O(P * Q) - Where P is the number of points and Q is the number of queries. We check every point against every circle.
SPACE COMPLEXITY: O(Q) - We allocate an array of size Q to store the results. No other auxiliary space is used.

CONCEPTS USED:
- Coordinate Geometry
- Optimization techniques (Loop invariant code motion)
- Array traversal
"""
