# 939. Minimum Area Rectangle
# Difficulty: Medium
# https://leetcode.com/problems/minimum-area-rectangle/

"""
PROBLEM:
You are given an array of points in the X-Y plane `points` where points[i] = [xi, yi].
Return the minimum area of a rectangle formed from these points, with sides parallel 
to the X and Y axes. If there is not any such rectangle, return 0.

EXAMPLES:
Input: points = [[1,1],[1,3],[3,1],[3,3],[2,2]]
Output: 4
Explanation: The points (1,1), (1,3), (3,1), and (3,3) form a rectangle of area 2 * 2 = 4.

Input: points = [[1,1],[1,3],[3,1],[3,3],[4,1],[4,3]]
Output: 2
Explanation: The points (3,1), (3,3), (4,1), and (4,3) form a rectangle of area 1 * 2 = 2.

CONSTRAINTS:
- 1 <= points.length <= 500
- points[i].length == 2
- 0 <= xi, yi <= 40000
- All the given points are unique.

GEOMETRIC INTUITION (THE "TRICK"):
The brute force approach is to pick 4 points and check if they form a rectangle. 
Checking 4 points combinations is O(N^4), which will cause a Time Limit Exceeded error.

Instead of looking for 4 points, look for a DIAGONAL (2 points).
If we pick any two points (x1, y1) and (x2, y2), they can form the diagonal of a rectangle 
parallel to the axes IF AND ONLY IF they are not on the same horizontal or vertical line 
(meaning x1 != x2 AND y1 != y2).

If they form a valid diagonal, the geometry forces the other two corners to be at 
exact coordinates: (x1, y2) and (x2, y1).
We just need to check if these two forced corners exist in our list of points. 
To do this instantly in O(1) time, we store all points in a Hash Set.
"""

# STEP 1: Convert the list of point arrays into a Hash Set of tuples for O(1) lookups.
# STEP 2: Initialize `min_area` to infinity.
# STEP 3: Iterate through all possible pairs of points (acting as potential diagonals).
# STEP 4: Ensure the pair forms a valid diagonal (not sharing an x or y coordinate).
# STEP 5: Check if the Hash Set contains the two implied opposite corners.
# STEP 6: If they exist, calculate the area and update `min_area`.
# STEP 7: Return `min_area`, or 0 if no rectangle was ever found.

from typing import List

class Solution:
    def minAreaRect(self, points: List[List[int]]) -> int:
        
        # Step 1: Create a hash set of coordinates (tuples are hashable in Python)
        point_set = set((x, y) for x, y in points)
        
        min_area = float('inf')
        n = len(points)
        
        # Step 3: Check every pair of points
        for i in range(n):
            x1, y1 = points[i]
            
            for j in range(i + 1, n):
                x2, y2 = points[j]
                
                # Step 4: Check if they form a valid diagonal
                if x1 != x2 and y1 != y2:
                    
                    # Step 5: Check for the opposite corners in O(1) time
                    if (x1, y2) in point_set and (x2, y1) in point_set:
                        
                        # Step 6: Calculate Area = base * height
                        area = abs(x1 - x2) * abs(y1 - y2)
                        
                        if area < min_area:
                            min_area = area
                            
        # Step 7: Return result or 0 if infinity
        return min_area if min_area != float('inf') else 0

"""
WHY EACH PART:
- set((x,y) ...): Arrays/Lists cannot be hashed in Python. We must convert [x, y] to (x, y) tuples to use a Set.
- if x1 != x2 and y1 != y2: Points on the same axis line have zero area and cannot be diagonals of our target rectangles.
- in point_set: The reason we built the set. Without it, searching the array for the corners would take O(N), making the total algorithm O(N^3).

HOW IT WORKS (Example: Diagonal (1,1) and (3,3)):
Iteration picks: p1 = (1,1), p2 = (3,3)

Valid diagonal check:
├── 1 != 3 (True)
└── 1 != 3 (True)

Corner lookup:
├── We need corner A: (x1, y2) -> (1, 3)
├── We need corner B: (x2, y1) -> (3, 1)
└── Are (1,3) and (3,1) in point_set? Yes!

Area calculation:
├── base = abs(1 - 3) = 2
├── height = abs(1 - 3) = 2
└── area = 2 * 2 = 4

Update min_area = 4 ✓

TIME COMPLEXITY: O(N^2) - Where N is the number of points. We check every pair of points exactly once using a nested loop. The set lookup is O(1).
SPACE COMPLEXITY: O(N) - We store all N points in a Hash Set.

CONCEPTS USED:
- Cartesian Geometry
- Hash Set / Hashing
- Combinatorics (Pair generation)
"""
