# 892. Surface Area of 3D Shapes
# Difficulty: Easy
# https://leetcode.com/problems/surface-area-of-3d-shapes/

"""
PROBLEM:
You are given an n x n grid where you have placed some 1 x 1 x 1 cubes. Each value v = grid[i][j] represents a tower of v cubes placed on top of the cell (i, j).
After placing these cubes, you have decided to glue any directly adjacent cubes to each other, forming several irregular 3D shapes.
Return the total surface area of the resulting shapes.

EXAMPLES:
Input: grid = [[1,2],[3,4]]
Output: 34

Input: grid = [[1,1,1],[1,0,1],[1,1,1]]
Output: 32

Input: grid = [[2,2,2],[2,1,2],[2,2,2]]
Output: 46

CONSTRAINTS:
- n == grid.length == grid[i].length
- 1 <= n <= 50
- 0 <= grid[i][j] <= 50

SURFACE AREA RULES:
1 isolated cube = 6 faces
Tower of 'v' cubes = v * 4 + 2 faces (4 lateral per cube + 1 top + 1 bottom)
When two towers touch, they hide faces. The number of hidden faces between two adjacent towers is min(tower1, tower2) * 2.

Formula:
isolated_area = grid[i][j] * 4 + 2
hidden_area = min(current_tower, adjacent_tower) * 2
total_area = sum(isolated_area) - sum(hidden_area)

VISUALIZATION (grid = [[1,2],[3,4]]):

Grid cells:
(0,0)=1 cube   | (0,1)=2 cubes
(1,0)=3 cubes  | (1,1)=4 cubes

Process (0,0) -> 1 cube:  +6 faces  (Total: 6)
Process (0,1) -> 2 cubes: +10 faces (Total: 16)
  -> Check left (0,0): min(1, 2) * 2 = 2 hidden faces.  16 - 2 = 14
Process (1,0) -> 3 cubes: +14 faces (Total: 28)
  -> Check up (0,0): min(3, 1) * 2 = 2 hidden faces.    28 - 2 = 26
Process (1,1) -> 4 cubes: +18 faces (Total: 44)
  -> Check left (1,0): min(4, 3) * 2 = 6 hidden faces.  44 - 6 = 38
  -> Check up (0,1): min(4, 2) * 2 = 4 hidden faces.    38 - 4 = 34

Result: 34 ✓
"""

# STEP 1: Initialize total area counter
# STEP 2: Loop through every cell in the n x n grid
# STEP 3: If cell has cubes, add the isolated surface area of that tower
# STEP 4: Check the adjacent tower to the UP. Subtract hidden faces if it exists.
# STEP 5: Check the adjacent tower to the LEFT. Subtract hidden faces if it exists.

class Solution:
    def surfaceArea(self, grid: list[list[int]]) -> int:
        
        n = len(grid)                                                          # Get grid size (n x n)
        area = 0                                                               # Initialize total area counter
        
        for i in range(n):                                                     # Loop through rows
            for j in range(n):                                                 # Loop through columns
                
                if grid[i][j] > 0:                                             # If tower has at least 1 cube
                    
                    area += grid[i][j] * 4 + 2                                 # Add area as if it were completely isolated
                    
                    if i > 0:                                                  # If there is a row above
                        area -= min(grid[i][j], grid[i-1][j]) * 2              # Subtract overlapping faces with UP neighbor
                        
                    if j > 0:                                                  # If there is a column to the left
                        area -= min(grid[i][j], grid[i][j-1]) * 2              # Subtract overlapping faces with LEFT neighbor
                        
        return area                                                            # Return final calculated area

"""
WHY EACH PART:
- grid[i][j] * 4 + 2: Calculates the base area of a single vertical stack. 4 lateral sides per cube, plus 1 absolute top and 1 absolute bottom.
- if i > 0 / if j > 0: We only check UP and LEFT to avoid double counting the overlaps. Checking 2 directions out of 4 is mathematically sufficient for a full grid traversal.
- min(grid[i][j], grid[i-1][j]) * 2: The number of touching faces is determined by the shorter tower. We multiply by 2 because 1 face is lost from the current tower, and 1 from the neighbor.

HOW IT WORKS (Example: [[1,2],[3,4]]):

Initial: area = 0

Iteration 1 (i=0, j=0) -> grid[0][0] = 1:
├── area += 1 * 4 + 2 = 6
├── Left? No (j=0)
├── Up? No (i=0)
└── area = 6

Iteration 2 (i=0, j=1) -> grid[0][1] = 2:
├── area += 2 * 4 + 2 = 10 (area is now 16)
├── Left? Yes (j>0). Neighbor is grid[0][0]=1
├── Overlap: min(2, 1) * 2 = 2
├── area -= 2
└── area = 14

Iteration 3 (i=1, j=0) -> grid[1][0] = 3:
├── area += 3 * 4 + 2 = 14 (area is now 28)
├── Up? Yes (i>0). Neighbor is grid[0][0]=1
├── Overlap: min(3, 1) * 2 = 2
├── area -= 2
└── area = 26

Iteration 4 (i=1, j=1) -> grid[1][1] = 4:
├── area += 4 * 4 + 2 = 18 (area is now 44)
├── Up? Yes (i>0). Neighbor is grid[0][1]=2
├── Overlap: min(4, 2) * 2 = 4 (area is now 40)
├── Left? Yes (j>0). Neighbor is grid[1][0]=3
├── Overlap: min(4, 3) * 2 = 6 (area is now 34)
└── area = 34

Exit loops.
return 34 ✓

KEY TECHNIQUE:
- Inclusion-Exclusion Principle: Add all possible areas first, then subtract the overlaps.
- Forward Traversal Strategy: By checking only Up and Left as we iterate row by row, column by column, we capture all adjacent boundaries exactly once.

EDGE CASES:
- Grid with zeroes (e.g., [[1,0],[0,2]]): Returns 20 ✓ (The `if grid[i][j] > 0` condition prevents adding '2' for zero-height towers).
- 1x1 grid (e.g., [[2]]): Returns 10 ✓ (Never triggers the overlap subtractions).
- Uniform flat grid (e.g., [[1,1],[1,1]]): Handles multiple uniform overlaps cleanly.

TIME COMPLEXITY: O(n^2) - We visit each cell in the n x n grid exactly once.
SPACE COMPLEXITY: O(1) - We only use a single variable (area) to keep track of the result, no extra memory scaling with input size.

CONCEPTS USED:
- 2D Arrays / Matrix Traversal
- Inclusion-Exclusion Principle
- Basic Geometry / Spatial Math
"""
