# 1252. Cells with Odd Values in a Matrix
# Difficulty: Easy
# https://leetcode.com/problems/cells-with-odd-values-in-a-matrix/

"""
PROBLEM:
There is an m x n matrix that is initialized to all 0's. There is also a 2D array indices 
where each indices[i] = [ri, ci] represents a 0-indexed location to perform some mutation on the matrix.
For each location indices[i], do both of the following:
1. Increment all the cells on row ri.
2. Increment all the cells on column ci.
Given m, n, and indices, return the number of cells with odd values in the matrix after applying the mutation.

EXAMPLES:
Input: m = 2, n = 3, indices = [[0,1],[1,1]]
Output: 6
(Explanation: 
Initial matrix = [[0,0,0],[0,0,0]].
After applying [0,1]: row 0 gets +1, col 1 gets +1 -> matrix = [[1,2,1],[0,1,0]].
After applying [1,1]: row 1 gets +1, col 1 gets +1 -> matrix = [[1,3,1],[1,2,1]].
Cells with odd values are [0,0], [0,1], [0,2], [1,0], [1,1], [1,2] = all 6 cells.)

Input: m = 2, n = 2, indices = [[1,1],[0,0]]
Output: 0
(Explanation: Final matrix is [[2,2],[2,2]]. No odd values.)

CONSTRAINTS:
- 1 <= m, n <= 50
- 1 <= indices.length <= 100
- 0 <= ri < m
- 0 <= ci < n

ALGORITHM LOGIC (Parity & Combinatorics):
1. A cell (r, c) becomes odd ONLY if (row 'r' is incremented an odd number of times AND col 'c' an even number of times) 
   OR (row 'r' is even AND col 'c' is odd). Odd + Even = Odd.
2. Instead of building the entire matrix O(m * n), we can just track the parity (odd/even state) of each row and column independently using booleans.
3. We toggle (flip) the boolean state for the respective row and column for each index given.
4. Count how many rows ended up odd (odd_rows) and how many columns ended up odd (odd_cols).
5. The number of even rows is (m - odd_rows) and even cols is (n - odd_cols).
6. Total odd cells = (odd_rows * even_cols) + (even_rows * odd_cols).

VISUALIZATION (m = 2, n = 3, indices = [[0,1],[1,1]]):
Initial State:
Rows (size 2): [False, False]
Cols (size 3): [False, False, False]

Apply [0,1] -> Flip Row 0, Flip Col 1:
Rows: [True, False]
Cols: [False, True, False]

Apply [1,1] -> Flip Row 1, Flip Col 1:
Rows: [True, True]
Cols: [False, False, False] (Col 1 flips back to False!)

Calculation:
odd_rows = 2 (Rows 0 and 1)
odd_cols = 0 
Total odd cells = (2 * (3 - 0)) + (0 * (2 - 2)) 
                = (2 * 3) + 0 
                = 6 ✓
"""

# STEP 1: Initialize boolean arrays for rows and columns to track parity
# STEP 2: Iterate through indices and toggle the parity of the targeted row and column
# STEP 3: Count the total number of True (odd) rows and True (odd) columns
# STEP 4: Calculate odd cells crossing odd rows with even columns
# STEP 5: Calculate odd cells crossing even rows with odd columns
# STEP 6: Return the sum of both calculations

class Solution:
    def oddCells(self, m: int, n: int, indices: list[list[int]]) -> int:
        
        row_parity = [False] * m                                     # Tracks if a row has been affected an odd number of times
        col_parity = [False] * n                                     # Tracks if a col has been affected an odd number of times
        
        for r, c in indices:                                         # Loop through the operations
            row_parity[r] ^= True                                    # Toggle parity for row 'r' (XOR with True)
            col_parity[c] ^= True                                    # Toggle parity for col 'c' (XOR with True)
            
        odd_rows = sum(row_parity)                                   # Count how many rows are odd (True acts as 1 in Python)
        odd_cols = sum(col_parity)                                   # Count how many columns are odd
        
        even_rows = m - odd_rows                                     # Calculate remaining even rows
        even_cols = n - odd_cols                                     # Calculate remaining even columns
        
        total_odd_cells = (odd_rows * even_cols) + (even_rows * odd_cols)  # Combinatorial calculation
        
        return total_odd_cells

"""
WHY EACH PART:
- [False] * m: Using booleans instead of integers saves space and perfectly models the binary nature of parity (Odd/Even).
- ^= True: The XOR assignment operator (`^=`) acts as a switch. False ^ True = True. True ^ True = False. It flips the state effortlessly.
- sum(row_parity): In Python, True is evaluated as 1 and False as 0 in arithmetic operations, making counting extremely clean.
- (odd_rows * even_cols): This represents the intersections where the row contributes an odd number and the column contributes an even number. Mathematically, Odd + Even = Odd.

HOW IT WORKS (Example: m = 2, n = 2, indices = [[1,1],[0,0]]):
Index [1,1]: row_parity = [False, True], col_parity = [False, True]
Index [0,0]: row_parity = [True, True], col_parity = [True, True]
Counting: odd_rows = 2, odd_cols = 2
even_rows = 2 - 2 = 0, even_cols = 2 - 2 = 0
Formula: (2 * 0) + (0 * 2) = 0 + 0 = 0 odd cells. ✓

KEY TECHNIQUE:
- Combinatorics and Geometry simplification: Turning a 2D matrix simulation problem into two independent 1D array problems. 
- Boolean XOR Toggling: A highly efficient way to track odd/even states without risking integer overflow or doing unnecessary modulo operations.

EDGE CASES:
- Overlapping same index multiple times ([[0,0], [0,0]]): Parity toggles back to False (Even), accurately reflecting that +2 doesn't change the odd/even state. ✓
- Large m and n, no indices: Evaluates to (0 * n) + (m * 0) = 0. ✓
- Matrix size 1x1: Handles perfectly without index out of bounds. ✓

TIME COMPLEXITY: O(L + m + n) - Where L is the length of `indices`. We iterate through the indices array once, and then we sum up the rows and columns arrays. This is drastically faster than the O(L * (m + n) + m * n) brute force simulation.
SPACE COMPLEXITY: O(m + n) - We only allocate two 1D arrays instead of an m x n 2D matrix. Highly optimal.

CONCEPTS USED:
- Math / Combinatorics
- Boolean Logic (XOR)
- Parity property of integers
- Array manipulation
"""
