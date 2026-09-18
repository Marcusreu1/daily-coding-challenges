# 963. Minimum Area Rectangle II
# Difficulty: Medium
# https://leetcode.com/problems/minimum-area-rectangle-ii/

"""
PROBLEM:
You are given an array of points in the X-Y plane points where points[i] = [xi, yi].
Return the minimum area of any rectangle formed from these points, with sides not necessarily parallel to the X and Y axes. If there is not any such rectangle, return 0.
Answers within 10^-5 of the actual answer will be accepted.

EXAMPLES:
Input: points = [[1,2],[2,1],[1,0],[0,1]] → Output: 2.00000
Explanation: The minimum area rectangle occurs at [1,2],[2,1],[1,0],[0,1], with an area of 2.

Input: points = [[0,1],[2,1],[1,1],[1,0],[2,0]] → Output: 1.00000
Explanation: The minimum area rectangle occurs at [1,0],[1,1],[2,1],[2,0], with an area of 1.

CONSTRAINTS:
- 1 <= points.length <= 50
- points[i].length == 2
- 0 <= xi, yi <= 40000
- All the given points are unique.

MATH RULES (DIAGONAL PROPERTY OF RECTANGLES):
Checking 4 points for 90-degree angles takes O(N^4) and complex vector dot-products. 
Instead, we rely on a core geometric property: A quadrilateral is a rectangle if and only if its two diagonals bisect each other (share the same midpoint) and are equal in length.
We can iterate over all O(N^2) pairs of points, treating each pair as a diagonal.
We calculate its midpoint (cx, cy) and its squared length. We group all pairs sharing the same (cx, cy, length) in a Hash Map.
Any two pairs inside the same Hash Map bucket are mathematically guaranteed to form a rectangle.
The area of the rectangle formed by diagonals (p1, p2) and (p3, p4) is simply the product of adjacent sides: distance(p1, p3) * distance(p1, p4).

VISUALIZATION (points = [[1,2],[2,1],[1,0],[0,1]]):
Pair 1: [1,2] and [1,0]. 
  - Midpoint: ((1+1)/2, (2+0)/2) = (1.0, 1.0). 
  - Length Squared: (1-1)^2 + (2-0)^2 = 4.

Pair 2: [0,1] and [2,1].
  - Midpoint: ((0+2)/2, (1+1)/2) = (1.0, 1.0).
  - Length Squared: (0-2)^2 + (1-1)^2 = 4.

Match found! Both diagonals share Midpoint (1.0, 1.0) and Length Squared (4). They form a rectangle.
"""

import collections
import math
from typing import List

# STEP 1: Initialize a Hash Map (defaultdict) to group diagonals by their geometric signatures.
# STEP 2: Iterate over all unique pairs of points.
# STEP 3: For each pair, calculate the exact midpoint and squared length. Use them as the Hash Map key.
# STEP 4: Iterate through the grouped diagonals. If a bucket has > 1 diagonal, combinations of them form rectangles.
# STEP 5: Calculate the area for each valid combination using the distances of adjacent sides.
# STEP 6: Return the minimum area found, or 0.0 if no rectangles exist.

class Solution:
    def minAreaFreeRect(self, points: List[List[int]]) -> float:
        
        # Dictionary to store pairs of points. Key: (mid_x, mid_y, length_squared)
        diagonals = collections.defaultdict(list)
        n = len(points)
        
        # Group all possible diagonals
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = points[i]
                x2, y2 = points[j]
                
                # Using exact division. Half-coordinates end in .0 or .5, avoiding float precision drift.
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                
                # Squared distance avoids costly math.sqrt() and precision loss at the grouping stage
                l2 = (x1 - x2)**2 + (y1 - y2)**2
                
                diagonals[(cx, cy, l2)].append((points[i], points[j]))
                
        min_area = float('inf')
        
        # Evaluate grouped diagonals to calculate areas
        for pairs in diagonals.values():
            if len(pairs) > 1:
                m = len(pairs)
                
                # Check all combinations of rectangles within this specific signature bucket
                for i in range(m):
                    for j in range(i + 1, m):
                        p1, p2 = pairs[i]
                        p3, p4 = pairs[j]
                        
                        # Calculate the squared lengths of the two adjacent sides of the rectangle
                        # Point 1 connects to Point 3 and Point 4 to form the width and height
                        side1_sq = (p1[0] - p3[0])**2 + (p1[1] - p3[1])**2
                        side2_sq = (p1[0] - p4[0])**2 + (p1[1] - p4[1])**2
                        
                        # Area = width * height. 
                        # math.sqrt(a * b) is numerically safer and faster than math.sqrt(a) * math.sqrt(b)
                        area = math.sqrt(side1_sq * side2_sq)
                        
                        if area < min_area:
                            min_area = area
                            
        # Return 0.0 if the infinity placeholder was never updated
        return min_area if min_area != float('inf') else 0.0

"""
WHY EACH PART:
- cx = (x1 + x2) / 2: Floating point numbers ending in .0 or .5 are perfectly representable in binary IEEE 754, meaning these tuple keys are 100% immune to float-hash collision bugs.
- diagonals[(cx, cy, l2)]: This geometric "signature" acts as an absolute filter. Only diagonals that perfectly bisect each other and are equal in length share the same bucket.
- side1_sq * side2_sq: We multiply the squared sides first before taking the square root. This minimizes floating-point operations and guarantees maximum precision.

KEY TECHNIQUE:
- Geometric Hashing: Translating a visual 2D shape problem into a state-matching logic problem by isolating mathematical invariants (midpoints and lengths).
- Combinatorics Reduction: Reducing an O(N^4) brute force search into an O(N^2) pairing algorithm.

EDGE CASES:
- Less than 4 points provided: The inner combinations loop is never reached, gracefully returning 0.0.
- Collinear points mimicking diagonal lengths: Collinear points with the same midpoint and length are identical line segments (same exact points), which is impossible since all provided points are explicitly unique.

TIME COMPLEXITY: O(N^2) - Generating all pairs of points takes O(N^2). Evaluating them usually takes minimal time as buckets rarely exceed 2-3 collisions. Absolute worst-case (e.g., points forming a circle) scales gracefully due to the small N=50 constraint limit.
SPACE COMPLEXITY: O(N^2) - The dictionary will store exactly N(N-1)/2 pairs in the worst case.
"""
