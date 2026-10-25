# 2249. Count Lattice Points Inside a Circle
# Difficulty: Medium
# https://leetcode.com/problems/count-lattice-points-inside-a-circle/

"""
PROBLEM:
Given a 2D integer array circles where circles[i] = [xi, yi, ri] represents the center (xi, yi) and radius ri of the ith circle drawn on a grid, return the number of lattice points that are present inside at least one circle.
A lattice point is a point with integer coordinates.
A point lies inside a circle if its distance to the circle's center is less than or equal to its radius.

EXAMPLES:
Input: circles = [[2,2,1]] → Output: 5
Explanation:
The circle is centered at (2,2) with radius 1.
The valid lattice points are (1,2), (2,1), (2,2), (2,3), and (3,2).

Input: circles = [[2,2,2],[3,4,1]] → Output: 16
Explanation:
The circles heavily overlap. Points like (2,3) and (3,3) reside in both circles, but are only counted exactly once.

CONSTRAINTS:
- 1 <= circles.length <= 200
- 1 <= xi, yi <= 100
- 1 <= ri <= min(xi, yi)

MATH RULES (SEARCH SPACE INVERSION & EUCLIDEAN GEOMETRY):
Instead of calculating all points per circle and storing them in a hash set (which performs redundant iterations on highly overlapped areas), we invert the logic.
1. Global Bounding Box: We determine the absolute minimum and maximum X and Y boundaries encompassing all circles.
2. Euclidean Distance: A point (X, Y) is inside circle (x, y, r) if (X - x)^2 + (Y - y)^2 <= r^2. We use squared distances to avoid floating-point square roots.
3. Greedy Early Pruning: By sorting the circles by radius in descending order, the largest circles are evaluated first. If a point falls inside a massive circle, we count it and instantly `break`, bypassing the need to check the remaining smaller circles.
"""

from typing import List

# STEP 1: Calculate the absolute physical boundaries of all combined circles (Global Bounding Box).
# STEP 2: Sort circles by descending radius and pre-calculate r^2 to optimize ALU cycles.
# STEP 3: Sweep every lattice point in the global box.
# STEP 4: Check against circles. Break instantly upon finding a match (Early Pruning).

class Solution:
    def countLatticePoints(self, circles: List[List[int]]) -> int:
        
        # Step 1: Find the global bounding box for the entire system of circles
        min_x = min(x - r for x, y, r in circles)
        max_x = max(x + r for x, y, r in circles)
        min_y = min(y - r for x, y, r in circles)
        max_y = max(y + r for x, y, r in circles)
        
        # Step 2: Sort descending by radius for optimized Early Pruning
        circles.sort(key=lambda c: c[2], reverse=True)
        
        # Precompute squared radii so it's strictly calculated once per circle, not per point
        processed_circles = [(x, y, r * r) for x, y, r in circles]
        
        valid_points = 0
        
        # Step 3: Iterate through every unique coordinate in the global bounding canvas
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                
                # Step 4: Check if the point exists in any circle
                for x, y, r2 in processed_circles:
                    
                    # Integer squared Euclidean distance check
                    if (i - x) ** 2 + (j - y) ** 2 <= r2:
                        valid_points += 1
                        # Crucial optimization: If it's inside one circle, no need to check others
                        break 
                        
        return valid_points

"""
WHY EACH PART:
- circles.sort(key=lambda c: c[2], reverse=True): Puts the circles with the largest surface area at the front. The mathematical probability of a point falling into a large circle is exponentially higher, allowing the inner loop to short-circuit almost instantly.
- r * r precomputation: Prevents executing the exponentiation operation X*Y times inside the deepest loop.
- break: Ensures we never double-count overlapping areas and saves millions of redundant checks.

KEY TECHNIQUE:
- Search Pruning: Intelligently sorting constraints so that success conditions trigger as early as possible.
- Inversion of Control: Looping over the fixed canvas instead of the variable floating objects.

EDGE CASES:
- Fully contained circles (e.g., a circle of radius 1 exactly inside a circle of radius 5): The large circle triggers the `break` first. The small circle is flawlessly ignored, saving computation.
- Singular dot circles: Handled naturally by the <= r2 boundary logic.

TIME COMPLEXITY: O(W * H * C) - Where W and H are the width and height of the global bounding box, and C is the number of circles. In the absolute worst theoretical case, it's roughly 200 * 200 * 200 = 8,000,000 operations. However, due to Early Pruning, it runs drastically closer to O(W * H), finishing in milliseconds.
SPACE COMPLEXITY: O(C) - Creating the processed_circles array requires space strictly proportional to the number of circles, which is minimal.
"""
