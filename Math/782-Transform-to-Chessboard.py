# 782. Transform to Chessboard
# Difficulty: Hard
# https://leetcode.com/problems/transform-to-chessboard/

"""
PROBLEM:
You are given an n x n binary grid board. In each move, you can swap any two rows with each other, 
or any two columns with each other.
Return the minimum number of moves to transform the board into a chessboard board. 
If the task is impossible, return -1.
A chessboard board is a board where no 0's and no 1's are 4-directionally adjacent.

EXAMPLES:
Input: board = [[0,1,1,0],[0,1,1,0],[1,0,0,1],[1,0,0,1]]  → Output: 2
Explanation: One possible sequence of moves is:
- Swap row 0 with row 2 -> [[1,0,0,1],[0,1,1,0],[0,1,1,0],[1,0,0,1]]
- Swap col 1 with col 2 -> [[1,0,1,0],[0,1,0,1],[0,1,0,1],[1,0,1,0]] (Valid chessboard)

Input: board = [[0, 1], [1, 0]]  → Output: 0
Explanation: Already a chessboard.

CONSTRAINTS:
- n == board.length == board[i].length
- 2 <= n <= 30
- board[i][j] is either 0 or 1.

LOGIC RULES (XOR & DIMENSIONAL INDEPENDENCE):
1. A valid transformable board can only have 2 unique types of rows, and they must be bitwise inversions 
   of each other. The same goes for columns. 
   This is mathematically verified if for any 4 corners of a subgrid: `board[0][0] ^ board[i][0] ^ board[0][j] ^ board[i][j] == 0`.
2. Row swaps and column swaps are completely independent. We can solve them as two 1D array problems.
3. The count of 1s and 0s in any valid row/col must be exactly n/2 (if n is even) or differ by exactly 1 (if n is odd).
4. One swap fixes exactly 2 misplaced elements. 

VISUALIZATION (Counting Swaps):
Suppose 1D array: [1, 1, 0, 0] (n = 4, even)
Ideal pattern 1:  [0, 1, 0, 1] -> Mismatches: idx 0, idx 3 -> Total 2 mismatches. (2 / 2 = 1 swap)
Ideal pattern 2:  [1, 0, 1, 0] -> Mismatches: idx 1, idx 2 -> Total 2 mismatches. (2 / 2 = 1 swap)
We take the minimum: 1 swap.

Suppose 1D array: [0, 1, 1] (n = 3, odd)
Ideal pattern 1:  [0, 1, 0] -> Mismatches: idx 2 -> Total 1 mismatch. (Impossible to swap just 1 item!)
Ideal pattern 2:  [1, 0, 1] -> Mismatches: idx 0, idx 1 -> Total 2 mismatches. (2 / 2 = 1 swap)
For odd 'n', we MUST pick the pattern that yields an EVEN number of mismatches.
"""

# STEP 1: Verify the fundamental property of the board using the XOR rule
# STEP 2: Count the 1s in the first row and column to ensure valid proportions
# STEP 3: Count how many elements are misplaced assuming a base pattern of 0, 1, 0, 1...
# STEP 4: Calculate the minimum row and column swaps depending on whether 'n' is even or odd

class Solution:
    def movesToChessboard(self, board: list[list[int]]) -> int:
        n = len(board)
        
        # Step 1: Validate XOR property for all rectangles starting from (0,0)
        for i in range(n):
            for j in range(n):
                if board[0][0] ^ board[i][0] ^ board[0][j] ^ board[i][j] != 0:
                    return -1
                    
        # Step 2: Validate the counts of 1s in the first row and first column
        row_sum = sum(board[0])
        col_sum = sum(board[i][0] for i in range(n))
        
        # In a valid board, sum of 1s must be n//2 or (n+1)//2
        if row_sum < n // 2 or row_sum > (n + 1) // 2: return -1
        if col_sum < n // 2 or col_sum > (n + 1) // 2: return -1
        
        # Step 3: Count misplaced elements assuming the ideal sequence is 0, 1, 0, 1...
        # We only need to check the first column (for row swaps) and first row (for col swaps)
        row_miss = sum(board[i][0] != i % 2 for i in range(n))
        col_miss = sum(board[0][j] != j % 2 for j in range(n))
        
        # Step 4: Calculate actual swaps needed
        if n % 2 == 0:
            # If even, we can choose either pattern (0101... or 1010...). We take the minimum.
            row_swaps = min(row_miss, n - row_miss) // 2
            col_swaps = min(col_miss, n - col_miss) // 2
        else:
            # If odd, the number of misplaced elements MUST be even to be swappable.
            if row_miss % 2 != 0: row_miss = n - row_miss
            if col_miss % 2 != 0: col_miss = n - col_miss
            
            row_swaps = row_miss // 2
            col_swaps = col_miss // 2
            
        return row_swaps + col_swaps

"""
WHY EACH PART:
- board[0][0] ^ board[i][0] ^ board[0][j] ^ board[i][j] != 0: If this XOR is 1, it means the rows 
  are not exact clones or exact inversions. A chessboard mathematically requires exactly 2 inverse row types.
- row_sum < n // 2 or row_sum > (n + 1) // 2: A chessboard of size 5 must have either three 1s and two 0s, 
  or two 1s and three 0s. Anything else is impossible to balance.
- board[i][0] != i % 2: We compare the current layout with an alternating sequence starting with 0. 
- n - row_miss: If `row_miss` is the mismatches for pattern starting with 0, then `n - row_miss` represents 
  the mismatches for the pattern starting with 1.
- // 2: Because one swap operation moves two elements into their correct places simultaneously.

HOW IT WORKS (Example: n = 4, valid board):

1. XOR validation passes.
2. row_sum and col_sum check passes (e.g., exactly two 1s and two 0s).
3. We check the first column to calculate row_miss. Let's say first col is [0, 0, 1, 1].
   ├── i=0: 0 != 0%2 (0 != 0) -> False (0 miss)
   ├── i=1: 0 != 1%2 (0 != 1) -> True  (1 miss)
   ├── i=2: 1 != 2%2 (1 != 0) -> True  (2 miss)
   ├── i=3: 1 != 3%2 (1 != 1) -> False (2 miss)
   └── row_miss = 2.
4. n is 4 (even). min(2, 4-2) // 2 = 2 // 2 = 1 row swap needed.
5. Same is done for columns. Total is returned. ✓

EDGE CASES:
- Impossible patterns: XOR check catches randomly scattered 1s and 0s instantly and returns -1. ✓
- Unbalanced 1s and 0s: (e.g., all 1s). The row_sum check catches it and returns -1. ✓
- Odd dimension constraints: The odd logic seamlessly forces the use of the only valid pattern by picking the even mismatch count. ✓

TIME COMPLEXITY: O(N^2)
We iterate over the n x n grid once to validate the XOR property. The row/col counting takes O(N). 
Overall time is strictly bounded by the grid traversal: O(N^2).

SPACE COMPLEXITY: O(1)
We only store a few integer variables (row_sum, col_sum, row_miss, col_miss). No extra data structures are built.
"""
