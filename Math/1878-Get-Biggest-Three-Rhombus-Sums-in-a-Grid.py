# 1878. Get Biggest Three Rhombus Sums in a Grid
# Difficulty: Medium
# https://leetcode.com/problems/get-biggest-three-rhombus-sums-in-a-grid/

"""
PROBLEM:
You are given an m x n integer matrix grid.
A rhombus sum is the sum of the elements that form the border of a regular rhombus shape in grid. The rhombus must have the shape of a square rotated 45 degrees with each of the vertices centered on a grid cell. The length of the side can be 0, which means the rhombus is just a single cell.
Return the biggest three distinct rhombus sums in the grid in descending order. If there are less than three distinct values, return all of them.

EXAMPLES:
Input: grid = [[3,4,5,1,3],[3,3,4,2,3],[20,30,200,40,10],[1,5,5,4,1],[4,3,2,2,5]]
Output: [228,216,211]
Explanation: The rhombus shapes for the three biggest distinct rhombus sums are highlighted in the prompt's image. 
- 228 is formed by vertices at (0,2), (1,3), (2,2), (1,1).
- 216 is formed by vertices at (1,2), (2,3), (3,2), (2,1).
- 211 is formed by a single cell at (2,2) with value 200, which is technically a rhombus of side length 0.

CONSTRAINTS:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- 1 <= grid[i][j] <= 10^5

MATH RULES (GEOMETRY TRAVERSAL & HASH SETS):
Because the grid dimensions are extremely small (at most 100x100), we can systematically verify every possible rhombus in the grid.
For any given cell (i, j) acting as the TOP vertex of the rhombus:
- A size L = 0 rhombus sum is just grid[i][j].
- A size L > 0 rhombus has 4 vertices:
  - Top: (i, j)
  - Right: (i + L, j + L)
  - Bottom: (i + 2*L, j)
  - Left: (i + L, j - L)
We dynamically increase L until any of the boundary conditions fail. For each valid L, we iterate along the 4 edges connecting the vertices and sum the cell values.
To maintain the uniqueness constraint ("distinct sums"), we store all calculated sums in a Hash Set. 

VISUALIZATION (L = 1 from Top (0, 1)):
L = 1 implies we move exactly 1 step diagonally in each direction.
Top (0,1) to Right (1,2) -> grid[0][1]
Right (1,2) to Bottom (2,1) -> grid[1][2]
Bottom (2,1) to Left (1,0) -> grid[2][1]
Left (1,0) to Top (0,1) -> grid[1][0]
Sum = grid[0][1] + grid[1][2] + grid[2][1] + grid[1][0]
"""

from typing import List

# STEP 1: Initialize a set to automatically filter duplicate sums.
# STEP 2: Iterate through every cell (i, j) in the matrix treating it as the top vertex of a rhombus.
# STEP 3: Add the side-length 0 rhombus (the cell itself) to the set.
# STEP 4: While the expanded rhombus fits within the grid bounds, iterate through its 4 edges to calculate the perimeter sum.
# STEP 5: Add the calculated sum to the set and increment the expansion length L.
# STEP 6: Sort the unique set elements in descending order and return up to the top 3.

class Solution:
    def getBiggestThree(self, grid: List[List[int]]) -> List[int]:
        
        m = len(grid)
        n = len(grid[0])
        distinct_sums = set()
        
        # Traverse every cell to act as the TOP vertex of the rhombus
        for i in range(m):
            for j in range(n):
                
                # Length 0 rhombus (just the single cell)
                distinct_sums.add(grid[i][j])
                
                # Expand the rhombus by length L
                L = 1
                
                # Check bounds: Bottom vertex, Left vertex, Right vertex
                while i + 2 * L < m and j - L >= 0 and j + L < n:
                    
                    current_sum = 0
                    
                    # Traverse Edge 1: Top to Right
                    for k in range(L):
                        current_sum += grid[i + k][j + k]
                        
                    # Traverse Edge 2: Right to Bottom
                    for k in range(L):
                        current_sum += grid[i + L + k][j + L - k]
                        
                    # Traverse Edge 3: Bottom to Left
                    for k in range(L):
                        current_sum += grid[i + 2 * L - k][j - k]
                        
                    # Traverse Edge 4: Left to Top
                    for k in range(L):
                        current_sum += grid[i + L - k][j - L + k]
                        
                    # Add the perimeter sum to the hash set
                    distinct_sums.add(current_sum)
                    
                    # Expand the rhombus further
                    L += 1
                    
        # Sort the distinct sums descending and return the top 3
        return sorted(list(distinct_sums), reverse=True)[:3]

"""
WHY EACH PART:
- distinct_sums = set(): A Hash Set provides O(1) average time complexity for insertions and inherently rejects duplicate values, which is a strict problem requirement.
- while i + 2 * L < m and j - L >= 0 and j + L < n: The boundary check perfectly encapsulates all vertices. Since the Top vertex is inherently within bounds due to the for-loop, we only check if the furthest points (Bottom, Left, Right) exceed the grid limits.
- sorted(..., reverse=True)[:3]: Converts the set to a list, sorts it in descending order, and gracefully slices the first 3 elements (if the list has less than 3, Python slicing safely returns whatever is available).

KEY TECHNIQUE:
- 2D Array Traversal: Systematically plotting diagonal movements using linear loop offsets (+k, -k).
- Uniqueness Caching: Offloading uniqueness checks to Hash Sets.

EDGE CASES:
- Grid size is 1x1: The while loop condition fails immediately. Returns the only cell value safely.
- Grid with entirely identical numbers (e.g., all 5s): The Set will naturally collapse the results into fewer than 3 elements and return exactly what is required.

TIME COMPLEXITY: O(M * N * min(M, N)) - The two outer loops run M * N times. The while loop expands at most min(M, N)/2 times. The inner edge traversals are proportional to L. Overall time is well within limits for 100x100 arrays.
SPACE COMPLEXITY: O(M * N * min(M, N)) - In the absolute worst-case where every rhombus has a unique sum, the hash set stores all generated sums.

CONCEPTS USED:
- Matrices / 2D Arrays
- Hash Sets
- Geometry and Coordinate Math
"""
