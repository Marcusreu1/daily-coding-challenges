# 48. Rotate Image
# Difficulty: Medium
# https://leetcode.com/problems/rotate-image/

"""
PROBLEM:
Given an n x n 2D matrix representing an image, rotate it 90 degrees clockwise.
You must rotate the image IN-PLACE (modify input matrix directly).

EXAMPLES:
Input:              Output:
[[1,2,3],           [[7,4,1],
 [4,5,6],     →      [8,5,2],
 [7,8,9]]            [9,6,3]]

Input:                      Output:
[[5,1,9,11],                [[15,13,2,5],
 [2,4,8,10],        →        [14,3,4,1],
 [13,3,6,7],                 [12,6,8,9],
 [15,14,12,16]]              [16,7,10,11]]

CONSTRAINTS:
- n == matrix.length == matrix[i].length
- 1 <= n <= 20
- -1000 <= matrix[i][j] <= 1000

KEY INSIGHT:
90° clockwise rotation = Transpose + Reverse each row

TRANSPOSE: Flip over diagonal (swap rows and columns)
┌───┬───┬───┐      ┌───┬───┬───┐
│ 1 │ 2 │ 3 │      │ 1 │ 4 │ 7 │
│ 4 │ 5 │ 6 │  →   │ 2 │ 5 │ 8 │
│ 7 │ 8 │ 9 │      │ 3 │ 6 │ 9 │
└───┴───┴───┘      └───┴───┴───┘

REVERSE ROWS: Flip each row horizontally
┌───┬───┬───┐      ┌───┬───┬───┐
│ 1 │ 4 │ 7 │      │ 7 │ 4 │ 1 │
│ 2 │ 5 │ 8 │  →   │ 8 │ 5 │ 2 │
│ 3 │ 6 │ 9 │      │ 9 │ 6 │ 3 │
└───┴───┴───┘      └───┴───┴───┘

RESULT: 90° clockwise rotation ✓
"""

# STEP 1: Transpose the matrix (swap matrix[i][j] with matrix[j][i])
# STEP 2: Reverse each row

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)                                                          # Matrix size (n x n)
        
        # Transpose: swap elements across diagonal
        for i in range(n):                                                       # Each row
            for j in range(i + 1, n):                                            # Only above diagonal (j > i)
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]          # Swap symmetric elements
        
        # Reverse each row
        for row in matrix:                                                       # Each row
            row.reverse()                                                        # Reverse in-place

"""
WHY EACH PART:
- n = len(matrix): Get matrix dimension (n x n square matrix)
- for j in range(i + 1, n): Only process above diagonal to avoid double-swapping
- matrix[i][j], matrix[j][i] = ...: Python tuple swap (no temp variable needed)
- row.reverse(): In-place reversal, O(n/2) swaps per row

WHY j STARTS AT i + 1:
- Diagonal elements (i == j) don't need swapping (they stay in place)
- If we process j < i, we'd swap the same pair twice (reverting the change)
- Only process each pair once: (0,1), (0,2), (1,2), etc.

HOW IT WORKS (Example: 3x3 matrix):

Original:           After Transpose:     After Reverse Rows:
┌───┬───┬───┐      ┌───┬───┬───┐       ┌───┬───┬───┐
│ 1 │ 2 │ 3 │      │ 1 │ 4 │ 7 │       │ 7 │ 4 │ 1 │
├───┼───┼───┤  →   ├───┼───┼───┤   →   ├───┼───┼───┤
│ 4 │ 5 │ 6 │      │ 2 │ 5 │ 8 │       │ 8 │ 5 │ 2 │
├───┼───┼───┤      ├───┼───┼───┤       ├───┼───┼───┤
│ 7 │ 8 │ 9 │      │ 3 │ 6 │ 9 │       │ 9 │ 6 │ 3 │
└───┴───┴───┘      └───┴───┴───┘       └───┴───┴───┘

Transpose swaps:
(0,1)↔(1,0): 2↔4
(0,2)↔(2,0): 3↔7
(1,2)↔(2,1): 6↔8

Reverse rows:
[1,4,7] → [7,4,1]
[2,5,8] → [8,5,2]
[3,6,9] → [9,6,3]

KEY TECHNIQUE:
- Decomposition: Complex rotation = two simple operations
- In-place swapping: No extra matrix needed
- Diagonal property: Transpose only needs half the swaps

ROTATION FORMULAS FOR REFERENCE:
┌───────────────────────┬─────────────────────────────────────┐
│ Rotation              │ Operations                          │
├───────────────────────┼─────────────────────────────────────┤
│ 90° clockwise         │ Transpose → Reverse rows            │
│ 90° counter-clockwise │ Reverse rows → Transpose            │
│                       │ OR: Transpose → Reverse columns     │
│ 180°                  │ Reverse rows → Reverse each row     │
│                       │ OR: Rotate 90° twice                │
│ 270° (= -90°)         │ Same as 90° counter-clockwise       │
└───────────────────────┴─────────────────────────────────────┘

EDGE CASES:
- 1x1 matrix: No change needed (single element) ✓
- 2x2 matrix: Works correctly ✓
- Even dimension (4x4): Works correctly ✓
- Odd dimension (3x3): Works correctly (center stays) ✓
- All same values: Works (no visible change) ✓
- Negative numbers: Works correctly ✓

TIME COMPLEXITY: O(n²) - Visit each element once
                 Transpose: n(n-1)/2 swaps
                 Reverse: n rows × n/2 swaps
                 Total: O(n²)

SPACE COMPLEXITY: O(1) - All operations in-place, only use temp variables

CONCEPTS USED:
- Matrix transpose (swap across diagonal)
- In-place array reversal
- Decomposition of complex operation into simple steps
- 2D array manipulation
- Python tuple swapping
"""
