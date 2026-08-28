# 1812. Determine Color of a Chessboard Square
# Difficulty: Easy
# https://leetcode.com/problems/determine-color-of-a-chessboard-square/

"""
PROBLEM:
You are given coordinates, a string that represents the coordinates of a square of the chessboard.
Return true if the square is white, and false if the square is black.
The coordinate will always represent a valid chessboard square. The coordinate will always have the letter first, and the number second.

EXAMPLES:
Input: coordinates = "a1" → Output: false
Explanation: From the chessboard, the square with coordinates "a1" is black, so return false.

Input: coordinates = "h3" → Output: true
Explanation: From the chessboard, the square with coordinates "h3" is white, so return true.

Input: coordinates = "c7" → Output: false

CONSTRAINTS:
- coordinates.length == 2
- 'a' <= coordinates[0] <= 'h'
- '1' <= coordinates[1] <= '8'

MATH RULES (GRID PARITY):
If we map the chessboard columns to numbers ('a' = 1, 'b' = 2, ..., 'h' = 8) and keep the rows as numbers (1 to 8), we can observe a mathematical pattern:
- The square 'a1' is mapped to (1, 1). Sum = 1 + 1 = 2 (Even) -> Black
- The square 'b1' is mapped to (2, 1). Sum = 2 + 1 = 3 (Odd) -> White
- The square 'c2' is mapped to (3, 2). Sum = 3 + 2 = 5 (Odd) -> White
Rule: If the sum of the column's numerical value and the row's value is even, the square is black (False). If the sum is odd, the square is white (True).

VISUALIZATION (coordinates = "h3"):
Column character: 'h' -> ASCII value is 104. 104 - 96 = 8.
Row character: '3' -> integer 3.

Sum: 8 + 3 = 11.
Parity check: 11 % 2 != 0 (11 is an odd number).
Result: True (White) ✓
"""

# STEP 1: Extract the letter character and convert it to its numerical position (1-8) using ASCII values.
# STEP 2: Extract the number character and cast it to an integer.
# STEP 3: Sum the converted column value and the row value.
# STEP 4: Return True if the sum is odd (modulo 2 not equal to 0), otherwise False.

class Solution:
    def squareIsWhite(self, coordinates: str) -> bool:
        
        # Convert column letter to a 1-based index ('a' -> 1, 'b' -> 2, etc.)
        # ord('a') is 97, so we subtract 96.
        column_value = ord(coordinates[0]) - 96
        
        # Parse the row digit into an integer
        row_value = int(coordinates[1])
        
        # Determine color based on parity (Odd sum = White, Even sum = Black)
        return (column_value + row_value) % 2 != 0

"""
WHY EACH PART:
- ord(coordinates[0]) - 96: The 'ord()' function converts a character to its ASCII integer value. By subtracting 96, we map lowercase English letters to their alphabetical index.
- int(coordinates[1]): Casts the string representation of the row number into a calculable integer.
- % 2 != 0: A quick boolean check. It evaluates to True if the result is odd (remainder is 1) and False if it is even.

HOW IT WORKS (Example: coordinates = "c7"):

Initial: coordinates = "c7"

Execution:
├── coordinates[0] = 'c' -> ord('c') = 99
├── column_value = 99 - 96 = 3
├── coordinates[1] = '7' -> int('7') = 7
├── row_value = 7
├── sum = 3 + 7 = 10
└── check = 10 % 2 != 0 -> 0 != 0 -> False

Return False ✓

KEY TECHNIQUE:
- Grid Parity / ASCII Mapping: Translating a visual 2D grid logic into a purely mathematical O(1) evaluation using character byte values.

EDGE CASES:
- Edges of the board (e.g., 'h8'): (8, 8) -> 8 + 8 = 16 (Even). Returns False (Black). Perfectly handled by the logic.

TIME COMPLEXITY: O(1) - The solution relies on a direct mathematical calculation.
SPACE COMPLEXITY: O(1) - No extra data structures are initialized.

CONCEPTS USED:
- ASCII Values (ord)
- Modulo Arithmetic
- Coordinate Geometry Parity
"""
