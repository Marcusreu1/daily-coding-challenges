# 2125. Number of Laser Beams in a Bank
# Difficulty: Medium
# https://leetcode.com/problems/number-of-laser-beams-in-a-bank/

"""
PROBLEM:
Anti-theft security devices are activated inside a bank. You are given a 0-indexed 1D integer array `bank` representing the floor plan of the bank, which is an m x n 2D matrix. bank[i] represents the ith row, consisting of '0's and '1's. '0' means the cell is empty, while '1' means the cell has a security device.
There is one laser beam between any two security devices if both conditions are met:
- The two devices are located on two different rows: r1 and r2, where r1 < r2.
- For each row i where r1 < i < r2, there are no security devices in the ith row.
Laser beams are independent, i.e., one beam does not interfere nor join with another.
Return the total number of laser beams in the bank.

EXAMPLES:
Input: bank = ["011001","000000","010100","001000"] → Output: 8
Explanation: 
- Row 0 has 3 devices.
- Row 1 is empty (transparent).
- Row 2 has 2 devices. Beams between row 0 and row 2 = 3 * 2 = 6.
- Row 3 has 1 device. Beams between row 2 and row 3 = 2 * 1 = 2.
Total = 6 + 2 = 8.

Input: bank = ["000","111","000"] → Output: 0
Explanation: There is only one row with security devices. No beams are formed.

CONSTRAINTS:
- m == bank.length
- n == bank[i].length
- 1 <= m, n <= 500
- bank[i][j] is either '0' or '1'.

MATH RULES (COMBINATORIAL PRODUCT & STATE FILTERING):
The problem asks for lines connecting nodes in separate layers. 
By the rule of product in combinatorics, if layer A has X nodes and layer B has Y nodes, the total number of edges connecting them is X * Y.
Because empty rows do not block lasers, we logically filter them out. We only need to multiply the device count of the CURRENT non-empty row with the device count of the PREVIOUS non-empty row.
"""

from typing import List

# STEP 1: Initialize the total beam counter and a state variable to hold the previous non-empty row's device count.
# STEP 2: Iterate through each row in the bank.
# STEP 3: Count the number of '1's (devices) in the current row.
# STEP 4: If the current row has devices, calculate the new beams by multiplying its count with the previous row's count.
# STEP 5: Add to the total and update the previous row's count to the current one.

class Solution:
    def numberOfBeams(self, bank: List[str]) -> int:
        
        total_beams = 0
        prev_row_devices = 0
        
        # Traverse the grid row by row
        for row in bank:
            # Python's built-in .count() is implemented in C and highly optimized for string parsing
            current_devices = row.count('1')
            
            # If the row is not completely empty
            if current_devices > 0:
                # Add the combinatorial product of beams connecting the previous layer to the current layer
                total_beams += prev_row_devices * current_devices
                
                # Update the state: The current layer becomes the "previous" layer for the next iterations
                prev_row_devices = current_devices
                
        return total_beams

"""
WHY EACH PART:
- prev_row_devices = 0: Initializes smoothly. On the very first non-empty row found, `0 * current_devices` adds 0 beams (which is mathematically correct, as beams require two separate rows).
- row.count('1'): Prevents writing a nested `for char in row` loop. It acts as an O(N) operation heavily optimized at the C-level in Python.
- if current_devices > 0: The filtering mechanism. If a row is all '0's, this block is skipped, leaving `prev_row_devices` intact so the lasers can "pass through" to the next row.

KEY TECHNIQUE:
- Combinatorics: Replacing 2D coordinate generation and geometric intersection checks with simple scalar multiplication.
- State Tracking: Remembering only the exact amount of historical data needed (the last valid row), dropping space complexity to O(1).

EDGE CASES:
- Bank with only 1 row of devices (e.g., ["00", "11", "00"]): The `total_beams` will remain 0 because the product will only ever be `0 * 2`, returning 0 perfectly.
- Complete empty bank (e.g., ["00", "00"]): The `if` condition is never met, returning 0.

TIME COMPLEXITY: O(M * N) - Where M is the number of rows and N is the length of each string. We traverse every character in the matrix exactly once during the `.count()` operation. This is optimally fast.
SPACE COMPLEXITY: O(1) - We only allocate two scalar integer variables, avoiding the need to store a cleaned array of row counts.
"""
