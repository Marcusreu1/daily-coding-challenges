# 89. Gray Code
# Difficulty: Medium
# https://leetcode.com/problems/gray-code/

"""
PROBLEM:
An n-bit Gray Code sequence is a sequence of 2^n integers where:
- Every integer is in the range [0, 2^n - 1]
- The first integer is 0
- Each integer appears exactly once
- The binary representation of every pair of adjacent integers differs by exactly one bit

Return ANY valid n-bit Gray Code sequence.

EXAMPLES:
Input: n = 2  → Output: [0,1,3,2]
Binary: 00 → 01 → 11 → 10 (each step: 1 bit changes)

Input: n = 1  → Output: [0,1]
Binary: 0 → 1

CONSTRAINTS:
- 1 <= n <= 16

WHAT IS GRAY CODE?
A sequence where consecutive numbers differ by exactly ONE bit.
Used in rotary encoders, error reduction, Karnaugh maps, etc.

BINARY vs GRAY CODE:
Binary: 0,1,2,3 = 00,01,10,11 (01→10 changes 2 bits!)
Gray:   0,1,3,2 = 00,01,11,10 (always 1 bit change ✓)

KEY INSIGHT:
There's a simple formula to convert any number to its Gray Code:

    Gray(i) = i XOR (i >> 1)

This works because:
- XOR with shifted version cancels most bits
- Only the "edge" where bits change remains different
- Guarantees single-bit difference between consecutive values
"""

# STEP 1: Generate numbers from 0 to 2^n - 1
# STEP 2: Convert each number to Gray Code using i XOR (i >> 1)
# STEP 3: Return the sequence

class Solution:
    def grayCode(self, n: int) -> List[int]:
        return [i ^ (i >> 1) for i in range(1 << n)]                             # Gray formula

"""
WHY EACH PART:
- range(1 << n): Generate 0 to 2^n - 1 (1 << n = 2^n)
- i >> 1: Right shift i by 1 (divide by 2, drop last bit)
- i ^ (i >> 1): XOR gives Gray Code
- List comprehension: Compact way to build result

HOW THE FORMULA WORKS:

For i = 5 (binary 101):
  i     = 101
  i >> 1 = 010  (shift right)
  XOR   = 111 = 7

For i = 6 (binary 110):
  i     = 110
  i >> 1 = 011
  XOR   = 101 = 5

Notice: Gray(5)=7=111, Gray(6)=5=101
These differ by 1 bit (bit 1) ✓

COMPLETE TABLE FOR n=3:
┌─────┬────────┬──────────┬──────────┬───────────┐
│  i  │ Binary │  i >> 1  │   XOR    │ Gray Code │
├─────┼────────┼──────────┼──────────┼───────────┤
│  0  │  000   │   000    │   000    │     0     │
│  1  │  001   │   000    │   001    │     1     │
│  2  │  010   │   001    │   011    │     3     │
│  3  │  011   │   001    │   010    │     2     │
│  4  │  100   │   010    │   110    │     6     │
│  5  │  101   │   010    │   111    │     7     │
│  6  │  110   │   011    │   101    │     5     │
│  7  │  111   │   011    │   100    │     4     │
└─────┴────────┴──────────┴──────────┴───────────┘

Result: [0, 1, 3, 2, 6, 7, 5, 4]

Verify transitions (1 bit difference):
000 → 001 ✓ (bit 0)
001 → 011 ✓ (bit 1)
011 → 010 ✓ (bit 0)
010 → 110 ✓ (bit 2)
110 → 111 ✓ (bit 0)
111 → 101 ✓ (bit 1)
101 → 100 ✓ (bit 0)

KEY TECHNIQUE:
- Bit manipulation: XOR and shift operations
- Mathematical formula: Direct conversion without recursion
- Gray Code property: i XOR (i >> 1) always produces valid Gray Code

EDGE CASES:
- n = 1: Returns [0, 1] ✓
- n = 2: Returns [0, 1, 3, 2] ✓
- n = 16: Returns 65536 numbers, all valid ✓

TIME COMPLEXITY: O(2^n) - Generate 2^n numbers
SPACE COMPLEXITY: O(1) extra - Only the required output (O(2^n) for result)

CONCEPTS USED:
- Bit manipulation (XOR, shift)
- Gray Code properties
- Mathematical formula derivation
- Mirror/reflection pattern
- Binary number system
"""
