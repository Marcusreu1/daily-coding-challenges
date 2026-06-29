# 1238. Circular Permutation in Binary Representation
# Difficulty: Medium
# https://leetcode.com/problems/circular-permutation-in-binary-representation/

"""
PROBLEM:
Given 2 integers `n` and `start`. Your task is return any permutation p of (0,1,2.....,2^n -1) such that:
- p[0] = start
- p[i] and p[i+1] differ by only one bit in their binary representation.
- p[0] and p[2^n -1] must also differ by only one bit in their binary representation.

EXAMPLES:
Input: n = 2, start = 3
Output: [3,2,0,1]
Explanation: The binary representation of the permutation is (11,10,00,01). 
All the adjacent elements differ by one bit. Another valid permutation is [3,1,0,2].

Input: n = 3, start = 2
Output: [2,6,7,5,4,0,1,3]

CONSTRAINTS:
- 1 <= n <= 16
- 0 <= start < 2^n

ALGORITHMIC INTUITION (THE "TRICK"):
This problem is a direct application of "Gray Code", a binary numeral system where two successive 
values differ in only one bit.
The standard formula to generate the i-th number in a Gray Code sequence is: `i ^ (i >> 1)`.
This naturally generates a valid circular sequence from 0 to 2^n - 1.

However, the problem requires the sequence to begin at `start`, not 0.
The naive approach is to generate the standard Gray Code array, find the index of `start`, 
and rotate the array. 

The GENIUS approach relies on the properties of the XOR operation:
1. XORing a constant to a set of unique numbers (0 to 2^n - 1) creates a perfect Bijection 
   (it shuffles the numbers but guarantees all numbers from 0 to 2^n - 1 are still present).
2. XORing a constant preserves the "Hamming Distance". If two numbers differ by 1 bit, 
   XORing both by the exact same constant means their results will STILL differ by exactly 1 bit!
3. If we evaluate the 0-th Gray Code element: `0 ^ (0 >> 1) = 0`. If we XOR this with `start`, 
   we get `0 ^ start = start`.

Therefore, we can mathematically generate the shifted sequence in place: `start ^ (i ^ (i >> 1))`.
"""

# STEP 1: Loop from 0 up to (2^n - 1). The bitwise left shift `1 << n` calculates 2^n.
# STEP 2: For each `i`, calculate the standard Gray Code: `i ^ (i >> 1)`.
# STEP 3: XOR the standard Gray Code with `start` to shift the starting point.
# STEP 4: Store in an array and return.

from typing import List

class Solution:
    def circularPermutation(self, n: int, start: int) -> List[int]:
        
        # 1 << n is mathematically equivalent to 2^n
        # The list comprehension generates the entire sequence in O(2^n) time
        return [start ^ (i ^ (i >> 1)) for i in range(1 << n)]

"""
WHY EACH PART:
- 1 << n: Bitwise shifting `1` to the left by `n` positions is the most efficient way to compute 2^n.
- i ^ (i >> 1): The definitive mathematical formula for Gray Code.
- start ^ (...): Transforms the Gray code universe so that the sequence natively begins at `start` while perfectly preserving the 1-bit difference rule.

HOW IT WORKS (Example: n = 2, start = 3):
2^n = 4. We loop i from 0 to 3.

i = 0:
├── Gray Code: 0 ^ (0 >> 1) = 0
└── Result: 3 ^ 0 = 3

i = 1:
├── Gray Code: 1 ^ (1 >> 1) = 1 ^ 0 = 1
└── Result: 3 ^ 1 = 2 (Binary 11 ^ 01 = 10)

i = 2:
├── Gray Code: 2 ^ (2 >> 1) = 2 ^ 1 = 3 (Binary 10 ^ 01 = 11)
└── Result: 3 ^ 3 = 0 (Binary 11 ^ 11 = 00)

i = 3:
├── Gray Code: 3 ^ (3 >> 1) = 3 ^ 1 = 2 (Binary 11 ^ 01 = 10)
└── Result: 3 ^ 2 = 1 (Binary 11 ^ 10 = 01)

Final Array: [3, 2, 0, 1]. ✓
Matches example perfectly!

TIME COMPLEXITY: O(2^n) - We must generate an array of 2^n elements. This is mathematically the fastest possible time.
SPACE COMPLEXITY: O(2^n) - The space required to store the resulting permutation array.

CONCEPTS USED:
- Bit Manipulation (XOR, Right Shift, Left Shift)
- Gray Code (Reflected Binary Code)
- Mathematical Bijection
"""
