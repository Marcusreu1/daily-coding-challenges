# 1453. Maximum Number of Darts Inside of a Circular Dartboard
# Difficulty: Hard
# https://leetcode.com/problems/maximum-number-of-darts-inside-of-a-circular-dartboard/

"""
PROBLEM:
Alice is throwing `n` darts on a very large wall. You are given an array `darts` where darts[i] = [xi, yi] is the position of the ith dart.
You have a circular dartboard of radius `r`.
Return the maximum number of darts that can fall inside or on the border of the dartboard.

EXAMPLES:
Input: darts = [[-2,0],[2,0],[0,2],[0,-2]], r = 2
Output: 4
(Explanation: Circle dartboard with center in (0,0) and radius = 2 contain all points.)

Input: darts = [[-3,0],[3,0],[2,6],[5,4],[0,9],[7,8]], r = 5
Output: 5
(Explanation: Circle dartboard with center in (0,4) and radius = 5 contain all points except the point (7,8).)

CONSTRAINTS:
- 1 <= darts.length <= 100
- darts[i].length == 2
- -10^4 <= darts[i][0], darts[i][1] <= 10^4
- 1 <= r <= 5000

ALGORITHM LOGIC (Rigid Boundary Principle & Center Projection):
1. Any optimal circle that covers the maximum number of points can be shifted so that at least two points lie exactly on its circumference.
2. We can iterate over all pairs of points (A, B).
3. For each pair, if the distance between them is <= 2r, there are exactly two circles of radius `r` that pass through both points.
4. We mathematically find the centers of these two circles using the midpoint of AB and Pythagorean height projection.
5. Once a candidate center is found, we iterate through all `n` darts to count how many fall within `r` distance of this center.
6. We keep track of the global maximum count.
7. Due to floating-point imprecision when using `math.sqrt`, we add an epsilon (1e-5) when checking if a point lies inside the circle.

VISUALIZATION:
Given A(x1, y1) and B(x2, y2).
Midpoint M = ((x1+x2)/2, (y1+y2)/2).
Distance AB = d.
Vector AB = (x2-x1, y2-y1).
Orthogonal (perpendicular) vector = (y1-y2, x2-x1).
Distance from M to Circle Center C is h = sqrt(r^2 - (d/2)^2).
Centers C1/C2 = M +/- (Orthogonal Vector normalized by d) * h.
"""

import math

# STEP 1: Handle trivial cases and prepare squared radius for optimization
# STEP 2: Dual loop to form every possible pair of darts
# STEP 3: Validate if a circle can physically bridge the two darts
# STEP 4: Mathematically project the two candidate circle centers
# STEP 5: Count total enclosed darts for both centers and update global maximum

class Solution:
    def numPoints(self, darts: list[list[int]], r: int) -> int:
        
        n = len(darts)
        if n <= 1:
            return n
            
        ans = 1
        r_sq = r ** 2
        
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = darts[i]
                x2, y2 = darts[j]
                
                # Distance squared between dart A and dart B
                d_sq = (x2 - x1)**2 + (y2 - y1)**2
                
                # If they are further apart than the diameter, no circle can enclose both
                if d_sq > 4 * r_sq:
                    continue
                    
                # Calculate Midpoint
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                
                d = math.sqrt(d_sq)
                # Height from midpoint to the true center of the circle (Pythagorean)
                # max(0, ...) acts as a safeguard against floating point negative zero
                h = math.sqrt(max(0, r_sq - (d / 2)**2))
                
                # Project the two possible circle centers using orthogonal vectors
                c1x = mx + h * (y1 - y2) / d
                c1y = my + h * (x2 - x1) / d
                
                c2x = mx - h * (y1 - y2) / d
                c2y = my - h * (x2 - x1) / d
                
                # Evaluate Candidate Center 1
                count1 = 0
                for px, py in darts:
                    # Using squared distances for the check, adding epsilon for float safety
                    if (px - c1x)**2 + (py - c1y)**2 <= r_sq + 1e-5:
                        count1 += 1
                        
                # Evaluate Candidate Center 2
                count2 = 0
                for px, py in darts:
                    if (px - c2x)**2 + (py - c2y)**2 <= r_sq + 1e-5:
                        count2 += 1
                        
                # Update global max
                ans = max(ans, count1, count2)
                
        return ans

"""
WHY EACH PART:
- d_sq > 4 * r_sq: (2r)^2 = 4r^2. If the distance between two points is greater than the diameter, it is geometrically impossible for a single circle to touch both. Skipping this saves massive CPU cycles.
- max(0, r_sq - (d / 2)**2): Sometimes float precision makes `r_sq` barely smaller than `(d/2)^2` (like by -0.00000001) which crashes `math.sqrt`. `max(0)` sanitizes this.
- <= r_sq + 1e-5: The Epsilon shield. Because our centers `c1x/c1y` are derived from square roots, they are slightly imprecise. Without `1e-5`, a dart perfectly on the boundary might be evaluated as 0.00001 outside the circle and rejected incorrectly.

HOW IT WORKS (Geometric logic):
By checking every pair of points, we systematically "pin" the theoretical circle against every combination of bounds. One of those pairs is guaranteed to be the defining rigid boundary of the most optimal placement. 

KEY TECHNIQUE:
- Computational Geometry (Rigid Boundary)
- Trigonometric Vector Projection
- Floating-Point Epsilon Tolerances

EDGE CASES:
- All darts in the exact same coordinate: Handled flawlessly. Midpoint calculation succeeds, distance is 0, vector logic collapses to the exact point safely via limits/skips. 
- Dispersed darts: If no two darts can share a circle, `d_sq > 4 * r_sq` triggers constantly, and `ans` remains 1. ✓

TIME COMPLEXITY: O(N^3) - There are roughly N^2 / 2 pairs of points. For each pair, we loop through N points to count the enclosures. With N = 100, N^3 is 1,000,000 operations, which runs in less than 0.1 seconds in Python.
SPACE COMPLEXITY: O(1) - We strictly allocate a few float variables to track coordinates and counts. No geometric matrices or objects are constructed in memory.
"""
