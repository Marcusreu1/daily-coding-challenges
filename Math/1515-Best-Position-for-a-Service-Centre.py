# 1515. Best Position for a Service Centre
# Difficulty: Hard
# https://leetcode.com/problems/best-position-for-a-service-centre/

"""
PROBLEM:
A delivery company wants to build a new service center in a new city. The company knows the 
positions of all the customers in this city on a 2D-Map and wants to build the new center in a 
position such that the sum of the euclidean distances to all customers is minimum.
Given an array `positions` where positions[i] = [xi, yi], return the minimum sum of distances.
Answers within 10^-5 of the actual value will be accepted.

EXAMPLES:
Input: positions = [[0,1],[1,0],[1,2],[2,1]]
Output: 4.00000
(Explanation: As shown in the visualization, you can see that choosing [x_center, y_center] = [1, 1] 
will make the distance to each customer = 1, to all customers = 4, which is the minimum possible.)

Input: positions = [[1,1],[3,3]]
Output: 2.82843
(Explanation: The minimum distance sum is along the straight line between the two points.)

CONSTRAINTS:
- 1 <= positions.length <= 50
- 0 <= positions[i][0], positions[i][1] <= 100

ALGORITHM LOGIC (Weiszfeld's Algorithm / Geometric Median):
1. The mathematical point that minimizes the sum of absolute Euclidean distances to a set of points is called the Geometric Median.
2. Unlike the Centroid (which minimizes squared distances), the Geometric Median has no direct closed-form formula.
3. We solve it using Weiszfeld's algorithm, an Iteratively Reweighted Least Squares (IRLS) technique.
4. We start with a reasonable guess: the mathematical Centroid (average of coords).
5. Iteratively, we calculate a new center by treating the inverse of the distance (1 / d) as a "gravitational weight" for each point.
6. The formula updates the center dynamically. If a calculated distance drops to exactly 0, we clamp it to a microscopic epsilon (1e-10) to prevent ZeroDivisionError.
7. We halt the iterative process when the shift in the center's position is strictly less than a strict tolerance (1e-7), guaranteeing we have settled at the optimal global minimum.

VISUALIZATION:
Initial Guess (Centroid) -> Iteration 1 -> Iteration 2 -> ... -> Convergence.
Since the function for Euclidean distance is strictly convex, it acts like a smooth bowl. The iterative steps mathematically "slide" down the walls of the bowl until they settle permanently at the absolute lowest point at the bottom.
"""

import math

# STEP 1: Handle base cases and establish the initial Centroid guess
# STEP 2: Initialize the iterative Weiszfeld engine
# STEP 3: Iterate through all points, applying the inverse-distance weights
# STEP 4: Protect the mathematics with an epsilon limit against division-by-zero
# STEP 5: Re-calculate the center and check for infinitesimal drift (convergence)
# STEP 6: Return the final optimized distance sum

class Solution:
    def getMinDistSum(self, positions: list[list[int]]) -> float:
        
        n = len(positions)
        if n == 1:
            return 0.0
            
        # Phase 1: Initial guess using standard average (Centroid)
        cx = sum(p[0] for p in positions) / n
        cy = sum(p[1] for p in positions) / n
        
        # Phase 2: Weiszfeld Iterative Optimization
        while True:
            num_x = 0.0
            num_y = 0.0
            den = 0.0
            
            for px, py in positions:
                # Euclidean distance from current center to the point
                d = math.sqrt((cx - px)**2 + (cy - py)**2)
                
                # Zero-Division Epsilon Shield
                if d < 1e-10:
                    d = 1e-10
                
                # Inverse distance acts as the normalizing weight
                weight = 1.0 / d
                num_x += px * weight
                num_y += py * weight
                den += weight
                
            # Compute the derived coordinates for the next iteration
            nx = num_x / den
            ny = num_y / den
            
            # Phase 3: Convergence evaluation (Has the center stopped moving?)
            drift = math.sqrt((cx - nx)**2 + (cy - ny)**2)
            if drift < 1e-7:
                cx, cy = nx, ny
                break
                
            # Update center for the next cycle
            cx, cy = nx, ny
            
        # Final Phase: Calculate the sum of distances from the optimal Geometric Median
        return sum(math.sqrt((cx - px)**2 + (cy - py)**2) for px, py in positions)

"""
WHY EACH PART:
- 1e-10: An infinitesimally small value. In the rare event the center locks exactly onto a customer's coordinate, `d` becomes 0. Dividing by 0 crashes the engine. This epsilon keeps the math valid without skewing the coordinates.
- drift < 1e-7: The LeetCode requirement is 10^-5 precision. Checking for a center displacement of less than 10^-7 guarantees that our final distance calculation is comfortably beyond the precision threshold requested by the judge.
- math.sqrt(): Essential because we are explicitly calculating the L2 norm (Euclidean linear distance), not Manhattan distance or squared Euclidean.

HOW IT WORKS (Mathematical properties):
Because the Euclidean distance sum is a convex function, it contains no "local minima" traps. The Weiszfeld algorithm is mathematically guaranteed to monotonically converge to the one true global minimum. It acts as a deterministic funnel.

KEY TECHNIQUE:
- Calculus / Numerical Analysis (Iteratively Reweighted Least Squares)
- Geometric Median / Fermat-Weber point resolution
- Mathematical optimization under precision constraints

EDGE CASES:
- Only one point provided: Handled optimally at the beginning `if n == 1`. Returns 0.0 distance natively without engaging the math engine. ✓
- All points form a straight line: The convex geometry holds, and the point settles flawlessly in the mathematical center. ✓

TIME COMPLEXITY: O(N * I) - Where N is the number of points in `positions` (max 50) and I is the number of iterations required for the drift to drop below 1e-7. For this constraint size, `I` is generally less than 100. The execution is virtually instantaneous (O(1) relative processing time).
SPACE COMPLEXITY: O(1) - The algorithm strictly utilizes a set of dynamic tracking variables (`num_x`, `den`, `drift`), allocating absolutely zero scaling memory resources.
"""
