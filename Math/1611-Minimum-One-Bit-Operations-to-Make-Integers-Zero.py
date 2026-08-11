# 1611. Minimum One Bit Operations to Make Integers Zero
# Difficulty: Hard
# https://leetcode.com/problems/minimum-one-bit-operations-to-make-integers-zero/

"""
PROBLEM:
Given an integer `n`, you must transform it into 0 using the following operations any number of times:
1. Change the rightmost (0th) bit in the binary representation of `n`.
2. Change the ith bit in the binary representation of `n` if the (i-1)th bit is set to 1 and the (i-2)th through 0th bits are set to 0.
Return the minimum number of operations to transform `n` into 0.

EXAMPLES:
Input: n = 3
Output: 2
(Explanation: The binary representation of 3 is "11".
"11" -> "01" with the 2nd operation since the 0th bit is 1.
"01" -> "00" with the 1st operation.)

Input: n = 6
Output: 4
(Explanation: The binary representation of 6 is "110".
"110" -> "010" with the 2nd operation since the 1st bit is 1 and 0th through 0th bits are 0.
"010" -> "011" with the 1st operation.
"011" -> "001" with the 2nd operation since the 0th bit is 1.
"001" -> "000" with the 1st operation.)

CONSTRAINTS:
- 0 <= n <= 10^9

ALGORITHM LOGIC (Gray Code Decoding & Bitwise Operations):
1. The rules provided by the problem are the exact mathematical definition for generating a Gray Code sequence (a binary numeral system where two successive values differ in only one bit).
2. Transforming the number `n` to `0` under these specific rules is algebraically equivalent to finding the positional index of `n` in the standard Gray Code sequence.
3. Therefore, the problem reduces to: "Decode the Gray Code `n` back into its original binary integer."
4. The algorithm to convert a Gray Code to a normal binary integer involves a cascading XOR operation.
5. We repeatedly XOR the number with a right-shifted version of itself until the number becomes 0.
6. The accumulated XOR result is the exact minimum number of operations required.

VISUALIZATION (n = 6 -> binary 110):
ans = 0

Iteration 1:
ans = 0 ^ 6 = 6  (binary 110)
n = 6 >> 1 = 3   (binary 011)

Iteration 2:
ans = 6 ^ 3 = 5  (binary 101)
n = 3 >> 1 = 1   (binary 001)

Iteration 3:
ans = 5 ^ 1 = 4  (binary 100)
n = 1 >> 1 = 0   (binary 000)

Loop ends (n is 0). Return ans (4). ✓
"""

# STEP 1: Initialize the accumulator that will store our decoded integer (minimum operations)
# STEP 2: Start a while loop that processes until the number is completely shifted to 0
# STEP 3: Apply the cascading XOR property to decode the Gray Code
# STEP 4: Shift `n` one bit to the right to process the next bit sequence
# STEP 5: Return the accumulated result

class Solution:
    def minimumOneBitOperations(self, n: int) -> int:
        
        ans = 0
        
        # Cascading XOR to decode the Gray Code positional index
        while n > 0:
            ans ^= n
            n >>= 1
            
        return ans

"""
WHY EACH PART:
- ans ^= n: The core of the Gray Code to Binary conversion algorithm. In hardware and math, the `i-th` bit of the original binary number is the XOR sum of all bits from the most significant bit down to `i` in the Gray Code. This accumulator flawlessly computes that.
- n >>= 1: The bitwise right shift operator mathematically divides the number by 2, dropping the rightmost bit. This allows us to progress the cascading XOR evaluation in O(1) time per bit.

HOW IT WORKS (Example: n = 3 -> binary 011):
ans = 0 ^ 3 = 3. n = 1.
ans = 3 ^ 1 = 2. n = 0.
Returns 2. ✓

KEY TECHNIQUE:
- Advanced Bit Manipulation
- Gray Code (Reflected Binary Code) Sequence Theory
- Cascading XOR 

EDGE CASES:
- n = 0: The `while` loop condition `0 > 0` immediately evaluates to False. The function returns `0`. This is perfectly correct, as 0 operations are needed to turn 0 into 0. ✓
- Large power of 2 (e.g., n = 2^30): Executes blazingly fast in exactly 30 loop iterations, unlike BFS simulation which would require over a billion iterations and massive memory. ✓

TIME COMPLEXITY: O(log N) - The number of loop iterations is exactly equal to the number of bits in `n`. Since the max constraint is 10^9 (which fits in roughly 30 bits), the loop runs at most 30 times, making it effectively O(1) near-constant time.
SPACE COMPLEXITY: O(1) - Zero memory structures are allocated. We only mutate two strictly typed integer variables.
"""
