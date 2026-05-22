# 840. Magic Squares In Grid
# Difficulty: Medium
# https://leetcode.com/problems/magic-squares-in-grid/

"""
PROBLEM:
A 3 x 3 magic square is a 3 x 3 grid filled with distinct numbers from 1 to 9 such that each row, 
column, and both diagonals all have the same sum.
Given a row x col grid of integers, how many 3 x 3 "magic square" subgrids are there? 
Every magic square subgrid may share numbers or cells.

EXAMPLES:
Input: grid = [[4,3,8,4],
               [9,5,1,9],
               [2,7,6,2]]
Output: 1
Explanation: 
The following subgrid is a 3 x 3 magic square:
4 3 8
9 5 1
2 7 6
Sum of rows = 15. Sum of cols = 15. Sum of diags = 15. 
The right-shifted subgrid (starting at col 1) has 4,9,2 in its right col, which doesn't sum to 15.

CONSTRAINTS:
- 1 <= row, col <= 10
- 0 <= grid[i][j] <= 15

LOGIC RULES (MATHEMATICAL PRUNING):
1. A 3x3 magic square with distinct numbers from 1 to 9 has a total sum of 45. 
   Thus, every single row, column, and diagonal MUST sum to exactly 15.
2. By solving the system of equations for the intersecting lines at the center, 
   the center cell of a 3x3 magic square of 1-9 MUST be exactly 5.
3. Therefore, instead of validating every possible 3x3 grid, we only validate grids 
   where the center cell is 5, saving a massive amount of computation.

VISUALIZATION (Scanning the grid):
Grid: 
[4, 3, 8, 4]
[9, 5, 1, 9]
[2, 7, 6, 2]

Possible centers (can't be on the absolute edge):
- Center at (r=1, c=1): Value is 5. Matches! -> Validate the 3x3 around it -> Valid! (count = 1)
- Center at (r=1, c=2): Value is 1. Not 5. Skipped instantly.
"""

# STEP 1: Guard clause to return 0 if the grid is too small to form a 3x3 square
# STEP 2: Create a helper function to validate the uniqueness and bounds of the 1-9 digits
# STEP 3: In the helper, validate that diagonals, rows, and columns sum to 15
# STEP 4: Iterate through all valid center points of the grid (excluding outer borders)
# STEP 5: Prune searches by checking if the center is exactly 5 before calling the helper

class Solution:
    def numMagicSquaresInside(self, grid: list[list[int]]) -> int:
        
        rows, cols = len(grid), len(grid[0])
        if rows < 3 or cols < 3:                                         # Step 1
            return 0
            
        def is_magic(r: int, c: int) -> bool:                            # Step 2
            
            # Ensure numbers are exactly from 1 to 9 and all distinct
            seen = set()
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    val = grid[i][j]
                    if val < 1 or val > 9 or val in seen:
                        return False
                    seen.add(val)
                    
            # Step 3: Check Diagonals, Rows, and Columns sum to 15
            # Center is guaranteed 5 and distinct 1-9, so checking is straightforward
            if grid[r-1][c-1] + grid[r][c] + grid[r+1][c+1] != 15: return False # Main Diag
            if grid[r-1][c+1] + grid[r][c] + grid[r+1][c-1] != 15: return False # Anti Diag
            
            if grid[r-1][c-1] + grid[r-1][c] + grid[r-1][c+1] != 15: return False # Top Row
            if grid[r+1][c-1] + grid[r+1][c] + grid[r+1][c+1] != 15: return False # Bottom Row
            if grid[r-1][c-1] + grid[r][c-1] + grid[r+1][c-1] != 15: return False # Left Col
            if grid[r-1][c+1] + grid[r][c+1] + grid[r+1][c+1] != 15: return False # Right Col
            
            # Middle row/col inherently sum to 15 if the others do due to the math properties, 
            # but they can be explicitly checked if desired.
            
            return True

        magic_count = 0
        
        # Step 4: Iterate through the grid, skipping the outer edges
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                
                # Step 5: Huge mathematical optimization (Pruning)
                if grid[r][c] == 5:
                    if is_magic(r, c):
                        magic_count += 1
                        
        return magic_count

"""
WHY EACH PART:
- range(1, rows - 1): We cannot center a 3x3 square on the top row (r=0) because it would go out of bounds. 
  Starting at 1 and ending before `rows-1` keeps our 3x3 frame safely inside the grid.
- if val < 1 or val > 9 or val in seen: A magic square strictly requires digits 1-9. Constraints say numbers 
  can be up to 15, so we must filter out 10-15 and 0. `seen` prevents duplicate numbers (e.g., all 5s).
- grid[r][c] == 5: Serves as a primary index filter. We bypass 90% of the grid without doing a single loop or sum.

HOW IT WORKS (Example dry run for Center r=1, c=1 containing '5'):

Initial checks: grid is large enough. Loop hits (1,1). Value is 5.
Calls `is_magic(1, 1)`:
├── Loop 3x3 area: collects {4,3,8,9,5,1,2,7,6}. 
├── Are all between 1-9? Yes. Are there 9 distinct numbers? Yes.
├── Main Diag: 4 + 5 + 6 = 15. Valid.
├── Anti Diag: 8 + 5 + 2 = 15. Valid.
├── Top Row:   4 + 3 + 8 = 15. Valid.
├── Bottom Row:2 + 7 + 6 = 15. Valid.
├── Left Col:  4 + 9 + 2 = 15. Valid.
└── Right Col: 8 + 1 + 6 = 15. Valid.

Returns True. magic_count becomes 1. ✓

EDGE CASES:
- Grid smaller than 3x3: Handled by Step 1. Returns 0 instantly. ✓
- Numbers > 9 or < 1: Handled by the `set` building loop safely. Returns False. ✓
- Multiple overlapping magic squares: The nested loops will check every single valid center independently. ✓

TIME COMPLEXITY: O(R * C)
Where R is rows and C is cols. We iterate through the matrix once. The inner `is_magic` function checks exactly 
9 cells and does a few O(1) additions. Since max grid size is 10x10, this completes in sub-milliseconds.

SPACE COMPLEXITY: O(1)
The `seen` set stores at most 9 integers. The memory footprint is strictly constant.
"""
