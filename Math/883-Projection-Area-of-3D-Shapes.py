# 883. Projection Area of 3D Shapes
# Difficulty: Easy
# https://leetcode.com/problems/projection-area-of-3d-shapes/

"""
PROBLEM:
You are given an n x n grid where we place some 1 x 1 x 1 cubes that are axis-aligned 
with the x, y, and z axes.
Each value v = grid[i][j] represents a tower of v cubes placed on top of the cell (i, j).
We view the projection of these cubes onto the xy, yz, and zx planes.
A projection is like a shadow, that maps our 3-dimensional figure to a 2-dimensional plane.
Return the total area of all three projections.

EXAMPLES:
Input: grid = [[1,2],[3,4]]
Output: 17
Explanation: 
Here are the three projections:
1. Top (xy-plane): 4 blocks have a height > 0. Area = 4.
2. Front (zx-plane): Max of col 0 is 3, max of col 1 is 4. Area = 3 + 4 = 7.
3. Side (yz-plane): Max of row 0 is 2, max of row 1 is 4. Area = 2 + 4 = 6.
Total = 4 + 7 + 6 = 17.

CONSTRAINTS:
- n == grid.length == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] <= 50

GEOMETRIC DECONSTRUCTION:
Instead of treating this as a complex 3D problem, we decouple the axes:
1. Top Projection (xy-plane): The shadow looking straight down. Height doesn't matter. 
   If a cell has at least 1 block, it casts a shadow of area 1.
   Formula: sum(1 for v in grid if v > 0)
2. Side Projection (yz-plane): The shadow looking from the side. We only see the tallest 
   building in each row. Smaller buildings are hidden behind it.
   Formula: sum(max(row) for row in grid)
3. Front Projection (zx-plane): The shadow looking from the front. We only see the tallest 
   building in each column.
   Formula: sum(max(col) for col in columns)
"""

# STEP 1: Get the dimension `n` of the square grid.
# STEP 2: Initialize total area accumulator.
# STEP 3: Iterate through indices `i` to represent the current row and column simultaneously.
# STEP 4: Track the maximum height for the i-th row and the i-th column.
# STEP 5: Add 1 to the area if the current cell grid[i][j] > 0 (Top projection).
# STEP 6: Add the max row and max column values to the total area (Side and Front projections).

from typing import List

class Solution:
    def projectionArea(self, grid: List[List[int]]) -> int:
        n = len(grid)
        total_area = 0
        
        for i in range(n):
            max_row = 0
            max_col = 0
            
            for j in range(n):
                # 1. Top Projection: Check if there is a block standing here
                if grid[i][j] > 0:
                    total_area += 1
                
                # 2. Side Projection: Find the tallest block in the current row 'i'
                if grid[i][j] > max_row:
                    max_row = grid[i][j]
                
                # 3. Front Projection: Find the tallest block in the current column 'i'
                # Note the swapped indices [j][i] to traverse vertically
                if grid[j][i] > max_col:
                    max_col = grid[j][i]
            
            # Add the highest shadows of the current row and column to the total
            total_area += max_row + max_col
            
        return total_area

"""
WHY EACH PART:
- if grid[i][j] > 0: Maps the 3D space to a 2D floor footprint. A tower of height 5 casts the same top shadow as a tower of height 1.
- grid[j][i] for max_col: This is a brilliant optimization. Because the grid is always an N x N square, we can traverse the columns in the exact same nested loop we use for rows just by swapping the coordinates. 
- total_area += max_row + max_col: We add the dimensional maximums per plane at the end of every `i` loop once that row/col has been fully evaluated.

HOW IT WORKS (Example: grid = [[1,2], [3,4]]):

Outer Loop i = 0 (Evaluating Row 0 and Col 0):
├── j = 0: grid[0][0] is 1. Top area +1. max_row updates to 1. grid[0][0] is 1. max_col updates to 1.
├── j = 1: grid[0][1] is 2. Top area +1. max_row updates to 2. grid[1][0] is 3. max_col updates to 3.
└── End of i=0: Add max_row(2) + max_col(3) to area. Total area so far: 2 (Top) + 5 (Shadows) = 7.

Outer Loop i = 1 (Evaluating Row 1 and Col 1):
├── j = 0: grid[1][0] is 3. Top area +1. max_row updates to 3. grid[0][1] is 2. max_col updates to 2.
├── j = 1: grid[1][1] is 4. Top area +1. max_row updates to 4. grid[1][1] is 4. max_col updates to 4.
└── End of i=1: Add max_row(4) + max_col(4) to area. Total area: 7 + 2 (Top) + 8 (Shadows) = 17.

Returns 17. ✓

KEY TECHNIQUE:
- Dimensional Decoupling: Treating a 3D intersection problem as three isolated 2D maximization problems.
- Transposed Matrix Traversal: Using `grid[j][i]` to read columns inside a row-major loop, avoiding the need for multiple independent loops or zip() manipulations.

TIME COMPLEXITY: O(N^2) where N is the length of the grid. We visit every cell exactly twice (once as grid[i][j] and once as grid[j][i]). Extremely efficient.
SPACE COMPLEXITY: O(1) auxiliary space. We only store simple integer trackers (max_row, max_col, total_area).

CONCEPTS USED:
- 3D Geometry / Orthographic Projection
- Matrix Traversal
- In-place tracking
"""
