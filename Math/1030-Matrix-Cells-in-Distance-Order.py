# 1030. Matrix Cells in Distance Order
# Difficulty: Easy
# https://leetcode.com/problems/matrix-cells-in-distance-order/

"""
PROBLEM:
You are given four integers `rows`, `cols`, `rCenter`, and `cCenter`. There is a `rows x cols` matrix and you are on the cell with the coordinates `(rCenter, cCenter)`.
Return the coordinates of all cells in the matrix, sorted by their distance from `(rCenter, cCenter)` from the smallest distance to the largest distance.
You may return the answer in any order that satisfies this condition.

The distance between two cells `(r1, c1)` and `(r2, c2)` is the Manhattan distance: `|r1 - r2| + |c1 - c2|`.

EXAMPLES:
Input: rows = 1, cols = 2, rCenter = 0, cCenter = 0
Output: [[0,0],[0,1]] 
(Distance from (0,0) to (0,0) is 0. Distance from (0,0) to (0,1) is 1).

Input: rows = 2, cols = 2, rCenter = 0, cCenter = 1
Output: [[0,1],[0,0],[1,1],[1,0]]
(Distances are 0, 1, 1, and 2 respectively).

CONSTRAINTS:
- 1 <= rows, cols <= 100
- 0 <= rCenter < rows
- 0 <= cCenter < cols

MATHEMATICAL REDUCTION:
Instead of simulating a Breadth-First Search (BFS) to radiate outwards from the center cell, we can leverage the fact that the maximum matrix size is 100x100 (10,000 cells). 
Sorting 10,000 items is highly efficient.
We can simply generate every valid `[r, c]` coordinate pair in the matrix.
Then, we sort this list using a custom key: the Manhattan Distance formula.
Manhattan Distance = abs(r - rCenter) + abs(c - cCenter).
Python's built-in Timsort is highly optimized and will handle this sorting operation gracefully.

VISUALIZATION (rows = 2, cols = 2, rCenter = 0, cCenter = 1):
Generate all cells:
[0, 0], [0, 1], [1, 0], [1, 1]

Calculate Manhattan Distances to (0, 1):
[0, 0] -> |0-0| + |0-1| = 1
[0, 1] -> |0-0| + |1-1| = 0 (Center)
[1, 0] -> |1-0| + |0-1| = 2
[1, 1] -> |1-0| + |1-1| = 1

Sort based on computed distances:
Distance 0: [0, 1]
Distance 1: [0, 0], [1, 1]
Distance 2: [1, 0]

Result: [[0, 1], [0, 0], [1, 1], [1, 0]] ✓
"""

# STEP 1: Generate a list of all coordinates [r, c] in the matrix using list comprehension.
# STEP 2: Sort the generated list in-place using the `sort()` method.
# STEP 3: Provide a lambda function as the sorting `key` to evaluate the Manhattan distance.
# STEP 4: Return the sorted list.

class Solution:
    def allCellsDistOrder(self, rows: int, cols: int, rCenter: int, cCenter: int) -> list[list[int]]:
        
        # Generate all possible cell coordinates in the matrix
        cells = [[r, c] for r in range(rows) for c in range(cols)]
        
        # Sort the cells based on their Manhattan distance to the center
        cells.sort(key=lambda cell: abs(cell[0] - rCenter) + abs(cell[1] - cCenter))
        
        return cells                                                           # Return the sorted grid

"""
WHY EACH PART:
- [[r, c] for r in range(rows) for c in range(cols)]: List comprehension is the most Pythonic and fastest way to generate Cartesian products (all combinations of rows and cols) without writing verbose nested for-loops.
- cells.sort(): Modifies the list in-place, which is slightly more memory-efficient than using `sorted()`.
- key=lambda cell: The sorting engine will pass each `[r, c]` pair into this anonymous function. The returned integer (the distance) dictates the element's sorted position.
- abs(): The built-in absolute value function correctly handles coordinates that fall mathematically "behind" the center (preventing negative distances).

HOW IT WORKS (Example: rows = 1, cols = 2, rCenter = 0, cCenter = 0):

Initial State:
├── cells = [[0, 0], [0, 1]]

Lambda Evaluation during Sort:
├── cell [0, 0] -> abs(0 - 0) + abs(0 - 0) = 0
├── cell [0, 1] -> abs(0 - 0) + abs(1 - 0) = 1

Sorting:
├── 0 < 1, so [0, 0] remains before [0, 1]

Exit:
return [[0, 0], [0, 1]] ✓

KEY TECHNIQUE:
- Cartesian Product + Custom Sort Key. By offloading the traversal logic to the language's highly optimized sorting algorithm, we avoid the heavy boilerplate code of queue-based BFS traversal.

EDGE CASES:
- 1x1 Matrix: Generates a single element, lambda evaluates to 0, sorting does nothing. Returns correctly. ✓
- Center is on a corner/edge: The absolute value completely ignores the directionality, computing distances safely without out-of-bounds errors. ✓

TIME COMPLEXITY: O(R * C * log(R * C)) - Generating the list takes O(R * C) where R is rows and C is cols. Sorting the list takes O(N log N) where N is the total number of cells (R * C).
SPACE COMPLEXITY: O(R * C) - We must store all generated coordinates in memory to return them.

CONCEPTS USED:
- Arrays / Matrix
- Sorting
- Manhattan Distance / Geometry
"""
