# 836. Rectangle Overlap
# Difficulty: Easy
# https://leetcode.com/problems/rectangle-overlap/

"""
PROBLEM:
An axis-aligned rectangle is represented as a list [x1, y1, x2, y2], where (x1, y1) is the coordinate of its 
bottom-left corner, and (x2, y2) is the coordinate of its top-right corner.
Two rectangles overlap if the area of their intersection is positive. To be clear, two rectangles that only 
touch at the corner or edges do not overlap.
Given two axis-aligned rectangles rec1 and rec2, return true if they overlap, otherwise return false.

EXAMPLES:
Input: rec1 = [0,0,2,2], rec2 = [1,1,3,3]  → Output: True
Explanation: Both rectangles intersect in the area from (1,1) to (2,2).

Input: rec1 = [0,0,1,1], rec2 = [1,0,2,1]  → Output: False
Explanation: The rectangles touch at the edge x=1, but their intersection area is 0.

CONSTRAINTS:
- rec1.length == 4
- rec2.length == 4
- -10^9 <= rec1[i], rec2[i] <= 10^9
- rec1 and rec2 represent a valid rectangle with a non-zero area.

LOGIC RULES (1D PROJECTIONS / SHADOWS):
1. Detecting 2D collisions via corners fails in edge cases (like when one rectangle perfectly crosses 
   another to form a "plus" + sign).
2. Instead, we project the rectangles down to 1D lines. A rectangle is just an X-axis line segment 
   and a Y-axis line segment.
3. Two 2D rectangles overlap IF AND ONLY IF their 1D X-projections overlap AND their 1D Y-projections overlap.
4. Two 1D line segments A and B overlap if: (Start_A < End_B) AND (Start_B < End_A).

VISUALIZATION (X-axis projection check):
rec1 = [0, y1, 2, y2]  --> X-shadow goes from 0 to 2
rec2 = [1, y1, 3, y2]  --> X-shadow goes from 1 to 3

Checking 1D overlap:
- Does rec1 start before rec2 ends? (0 < 3) -> True
- Does rec2 start before rec1 ends? (1 < 2) -> True
Conclusion: Their X-shadows overlap! (Do the same for Y-shadows).
"""

# STEP 1: Extract coordinates for both rectangles mentally or directly via indices
# STEP 2: Evaluate the 1D overlap logic for the X-axis (Left < Right)
# STEP 3: Evaluate the 1D overlap logic for the Y-axis (Bottom < Top)
# STEP 4: Return True if BOTH axes overlap, otherwise False

class Solution:
    def isRectangleOverlap(self, rec1: list[int], rec2: list[int]) -> bool:
        
        # rec1 = [x1, y1, x2, y2] 
        # rec2 = [x1, y1, x2, y2]
        
        # Step 2: Check overlap on the X-axis (Shadow on the floor)
        # (rec1_left < rec2_right) AND (rec2_left < rec1_right)
        x_overlap = rec1[0] < rec2[2] and rec2[0] < rec1[2]
        
        # Step 3: Check overlap on the Y-axis (Shadow on the wall)
        # (rec1_bottom < rec2_top) AND (rec2_bottom < rec1_top)
        y_overlap = rec1[1] < rec2[3] and rec2[1] < rec1[3]
        
        # Step 4: Both projections must overlap for a 2D collision
        return x_overlap and y_overlap

"""
WHY EACH PART:
- rec1[0] < rec2[2]: Uses strict strictly less than (<) instead of (<=) because touching edges do not count 
  as overlapping. The area must be positive.
- and: Logical AND operator ensures both conditions of the 1D overlap must be true. If `rec1` starts after 
  `rec2` ends, it will cleanly evaluate to False and short-circuit.

HOW IT WORKS (Example dry run for rec1 = [0,0,1,1], rec2 = [1,0,2,1]):

Check X-axis:
├── rec1_left (0) < rec2_right (2) ? True
├── rec2_left (1) < rec1_right (1) ? False (1 is not strictly less than 1)
└── x_overlap = False

Since x_overlap is False, the rectangles are horizontally adjacent but do not intersect.
Returns False. ✓

EDGE CASES:
- Rectangles touching by a corner (e.g. [0,0,1,1] and [1,1,2,2]): x_overlap False (1 < 1 fails), y_overlap False. Returns False. ✓
- One rectangle completely inside the other: Both 1D projections will show overlapping start and end points. Returns True. ✓
- Lines acting as rectangles (Area = 0): Constraints guarantee valid rectangles with non-zero areas, but 
  even if they were lines, the `<` operator would safely return False. ✓

TIME COMPLEXITY: O(1)
We only perform 4 boolean comparison operations, regardless of the coordinate values. Constant time.

SPACE COMPLEXITY: O(1)
Only computing primitive boolean values. No extra arrays or data structures are required.
"""
