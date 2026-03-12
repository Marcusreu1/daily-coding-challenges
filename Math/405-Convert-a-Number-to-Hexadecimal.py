"""
405. Convert a Number to Hexadecimal
Difficulty: Easy
https://leetcode.com/problems/convert-a-number-to-hexadecimal/

PROBLEM:
Given a 32-bit integer num, return its hexadecimal representation
as a string. For negative numbers, use two's complement method.

    - All letters in the answer must be lowercase
    - No leading zeros (except "0" itself)
    - Do NOT use built-in hex() function

EXAMPLES:
Input: num = 26  → Output: "1a"
    26 = 1×16 + 10 → '1' + 'a' = "1a"

Input: num = -1  → Output: "ffffffff"
    -1 in 32-bit two's complement = 0xFFFFFFFF

CONSTRAINTS:
    -2^31 <= num <= 2^31 - 1

KEY INSIGHT:
Each hex digit = 4 bits. Extract last 4 bits with & 0xF,
shift right by 4, repeat. For negatives, add 2^32 to get
the two's complement unsigned representation first.

CHALLENGES:
    Negative numbers need two's complement conversion
    Python integers have arbitrary precision (not fixed 32 bits)
    No leading zeros allowed
    Can't use built-in hex()

SOLUTION:
    1. Handle zero edge case
    2. Convert negative to 32-bit unsigned (num + 2^32)
    3. Extract hex digits with bit masking (& 0xF) and shifting (>> 4)
    4. Build result string from right to left
"""

# STEP 1: Handle zero edge case
# STEP 2: Convert negative to 32-bit two's complement
# STEP 3: Extract hex digits via bit manipulation
# STEP 4: Build and return result string

class Solution:
    def toHex(self, num: int) -> str:

        if num == 0:                                                     # Zero is special: just "0"
            return "0"

        if num < 0:                                                      # Negative → two's complement
            num += 2 ** 32                                               # Convert to unsigned 32-bit

        hex_chars = "0123456789abcdef"                                   # Lookup table: index → hex char
        result = ""                                                      # Build string right to left

        while num > 0:                                                   # Extract digits until nothing left
            result = hex_chars[num & 0xF] + result                       # Last 4 bits → hex char, prepend
            num >>= 4                                                    # Shift right 4 bits (÷16)

        return result                                                    # Final hex string

"""
WHY EACH PART:

    if num == 0: return "0": Loop won't execute for 0, handle separately
    num += 2**32: Python ints are arbitrary size, this gives 32-bit two's complement
    hex_chars = "0123456789abcdef": Map 0-15 to hex characters via indexing
    result = "": We prepend each digit (building right to left)
    num & 0xF: Bit mask extracts last 4 bits (0-15) = one hex digit
    hex_chars[num & 0xF]: Convert 0-15 to '0'-'f'
    + result: Prepend because we extract least significant digit first
    num >>= 4: Remove last 4 bits, equivalent to num //= 16

HOW IT WORKS (Example: num = 26):

    hex_chars = "0123456789abcdef"
    26 in binary: 00011010

    Iteration 1:
    ├── num = 26 (binary: 00011010)
    ├── 26 & 0xF = 10 (binary: 1010) → hex_chars[10] = 'a'
    ├── result = "a"
    └── num = 26 >> 4 = 1 (binary: 0001)

    Iteration 2:
    ├── num = 1 (binary: 0001)
    ├── 1 & 0xF = 1 → hex_chars[1] = '1'
    ├── result = "1" + "a" = "1a"
    └── num = 1 >> 4 = 0

    num = 0 → STOP
    Result: "1a" ✓

HOW IT WORKS (Example: num = -1):

    Step 0: num = -1 + 2^32 = 4294967295
    Binary: 11111111 11111111 11111111 11111111

    Iteration 1: 4294967295 & 0xF = 15 → 'f', >> 4 = 268435455
    Iteration 2: 268435455  & 0xF = 15 → 'f', >> 4 = 16777215
    Iteration 3: 16777215   & 0xF = 15 → 'f', >> 4 = 1048575
    Iteration 4: 1048575    & 0xF = 15 → 'f', >> 4 = 65535
    Iteration 5: 65535      & 0xF = 15 → 'f', >> 4 = 4095
    Iteration 6: 4095       & 0xF = 15 → 'f', >> 4 = 255
    Iteration 7: 255        & 0xF = 15 → 'f', >> 4 = 15
    Iteration 8: 15         & 0xF = 15 → 'f', >> 4 = 0

    Result: "ffffffff" ✓

WHY num & 0xF WORKS:

    0xF in binary = 1111 (four 1-bits)
    AND with any number keeps only the last 4 bits:

    26 = 0001 1010
    0F = 0000 1111
    &  = 0000 1010 = 10 = 'a' ✓

    This is equivalent to num % 16 but faster (bitwise operation)

WHY num += 2^32 FOR NEGATIVES:

    Python: -1 is just -1 (arbitrary precision, no fixed bits)
    C/Java: -1 is 0xFFFFFFFF (32 fixed bits, two's complement)

    Adding 2^32 simulates the two's complement wrap-around:
    ├── -1 + 4294967296 = 4294967295 = 0xFFFFFFFF ✓
    ├── -2 + 4294967296 = 4294967294 = 0xFFFFFFFE ✓
    └── -2147483648 + 4294967296 = 2147483648 = 0x80000000 ✓

    General: for any negative num in [-2^31, -1]:
    num + 2^32 gives the correct unsigned 32-bit representation

BIT MANIPULATION vs DIVISION:

    Bit manipulation:              Division:
    digit = num & 0xF              digit = num % 16
    num >>= 4                      num //= 16

    Both produce identical results because 16 = 2^4
    Bit manipulation is more "computer science-y" and slightly faster

EDGE CASES:

    num = 0: Returns "0" (special case) ✓
    num = 1: Returns "1" ✓
    num = 15: Returns "f" ✓
    num = 16: Returns "10" ✓
    num = -1: Returns "ffffffff" (all bits set) ✓
    num = -2^31: Returns "80000000" (minimum 32-bit) ✓
    num = 2^31-1: Returns "7fffffff" (maximum 32-bit) ✓

TIME COMPLEXITY: O(1)
    At most 8 iterations (32 bits ÷ 4 bits per hex digit = 8 digits max)
    Constant regardless of input value

SPACE COMPLEXITY: O(1)
    Result string is at most 8 characters
    Only a few variables used

CONCEPTS USED:
    Hexadecimal number system (base 16)
    Two's complement for negative numbers
    Bit masking (& 0xF to extract 4 bits)
    Bit shifting (>> 4 to divide by 16)
    String building (prepend for right-to-left extraction)
    Lookup table (string indexing for char mapping)
"""
