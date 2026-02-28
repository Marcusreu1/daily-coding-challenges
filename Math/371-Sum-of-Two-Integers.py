"""
371. Sum of Two Integers
Difficulty: Medium
https://leetcode.com/problems/sum-of-two-integers/

PROBLEM:
Given two integers a and b, return the sum of the two integers
without using the operators + and -.

EXAMPLES:
Input: a = 1, b = 2 → Output: 3
Input: a = 2, b = 3 → Output: 5
Input: a = -1, b = 1 → Output: 0

CONSTRAINTS:
• -1000 <= a, b <= 1000

KEY INSIGHT:
Binary addition can be decomposed into:
1. SUM without carry = XOR (a ^ b)
2. CARRY = AND shifted left ((a & b) << 1)

Repeat until carry becomes 0.

BINARY ADDITION TABLE:
    a | b | Sum | Carry
    0 | 0 |  0  |   0
    0 | 1 |  1  |   0
    1 | 0 |  1  |   0
    1 | 1 |  0  |   1   ← XOR gives sum, AND gives carry

ALGORITHM:
    while b != 0:
        sum_without_carry = a ^ b
        carry = (a & b) << 1
        a = sum_without_carry
        b = carry
    return a

PYTHON SPECIFICS:
Python integers have arbitrary precision (infinite bits).
For negative numbers, we need to simulate 32-bit integers
using a mask to prevent infinite loops.

MASK = 0xFFFFFFFF (32 bits of 1s)
MAX_INT = 0x7FFFFFFF (maximum positive 32-bit integer)
"""


# ============================================================================
# SOLUTION 1: BIT MANIPULATION (With 32-bit handling for Python)
# ============================================================================

class Solution:
    def getSum(self, a: int, b: int) -> int:
        
        MASK = 0xFFFFFFFF                                        # 32 bits of 1s
        MAX_INT = 0x7FFFFFFF                                     # Max positive 32-bit int
        
        # Work with 32-bit representations
        a = a & MASK
        b = b & MASK
        
        while b != 0:
            carry = ((a & b) << 1) & MASK                        # AND + shift, masked to 32 bits
            a = (a ^ b) & MASK                                   # XOR for sum without carry
            b = carry
        
        # If a > MAX_INT, it's negative in 32-bit two's complement
        if a > MAX_INT:
            a = ~(a ^ MASK)                                      # Convert to Python negative int
        
        return a


# ============================================================================
# SOLUTION 2: RECURSIVE VERSION
# ============================================================================

class Solution:
    def getSum(self, a: int, b: int) -> int:
        
        MASK = 0xFFFFFFFF
        MAX_INT = 0x7FFFFFFF
        
        def add(x: int, y: int) -> int:
            if y == 0:
                return x
            
            sum_no_carry = (x ^ y) & MASK
            carry = ((x & y) << 1) & MASK
            
            return add(sum_no_carry, carry)
        
        result = add(a & MASK, b & MASK)
        
        return result if result <= MAX_INT else ~(result ^ MASK)


# ============================================================================
# SOLUTION 3: USING SUBTRACTION PROPERTY 
# ============================================================================

class Solution:
    def getSum(self, a: int, b: int) -> int:
        # a + b = -(-a - b) = -((~a + 1) + (~b + 1) - 2)
        # Using bit manipulation to compute negation
        
        MASK = 0xFFFFFFFF
        MAX_INT = 0x7FFFFFFF
        
        a, b = a & MASK, b & MASK
        
        while b:
            carry = ((a & b) << 1) & MASK
            a = (a ^ b) & MASK
            b = carry
        
        return a if a <= MAX_INT else ~(a ^ MASK)


"""
HOW IT WORKS (Visual trace):

Example: 5 + 3 = 8

    a = 0101 (5)
    b = 0011 (3)

    ═══════════════════════════════════════════════════════════
    ITERATION 1:
    ═══════════════════════════════════════════════════════════
    
    XOR (sum without carry):
        0101
      ^ 0011
      ──────
        0110 (6)
    
    AND then shift (carry):
        0101
      & 0011
      ──────
        0001  → shift left → 0010 (2)
    
    New: a = 6, b = 2

    ═══════════════════════════════════════════════════════════
    ITERATION 2:
    ═══════════════════════════════════════════════════════════
    
    XOR:
        0110
      ^ 0010
      ──────
        0100 (4)
    
    AND + shift:
        0110
      & 0010
      ──────
        0010  → shift left → 0100 (4)
    
    New: a = 4, b = 4

    ═══════════════════════════════════════════════════════════
    ITERATION 3:
    ═══════════════════════════════════════════════════════════
    
    XOR:
        0100
      ^ 0100
      ──────
        0000 (0)
    
    AND + shift:
        0100
      & 0100
      ──────
        0100  → shift left → 1000 (8)
    
    New: a = 0, b = 8

    ═══════════════════════════════════════════════════════════
    ITERATION 4:
    ═══════════════════════════════════════════════════════════
    
    XOR:
        0000
      ^ 1000
      ──────
        1000 (8)
    
    AND + shift:
        0000
      & 1000
      ──────
        0000  → shift left → 0000 (0)
    
    New: a = 8, b = 0

    ═══════════════════════════════════════════════════════════
    b = 0, DONE! Result: a = 8 ✓
    ═══════════════════════════════════════════════════════════

WHY XOR GIVES SUM WITHOUT CARRY:
┌────────────────────────────────────────────────────────────────┐
│  XOR truth table:                                              │
│    0 XOR 0 = 0  (0 + 0 = 0, no carry needed)                  │
│    0 XOR 1 = 1  (0 + 1 = 1, no carry needed)                  │
│    1 XOR 0 = 1  (1 + 0 = 1, no carry needed)                  │
│    1 XOR 1 = 0  (1 + 1 = 10, but XOR ignores carry → 0)      │
│                                                                │
│  XOR = sum of each bit position, ignoring carry!              │
└────────────────────────────────────────────────────────────────┘

WHY AND GIVES CARRY:
┌────────────────────────────────────────────────────────────────┐
│  AND truth table:                                              │
│    0 AND 0 = 0  (no carry)                                    │
│    0 AND 1 = 0  (no carry)                                    │
│    1 AND 0 = 0  (no carry)                                    │
│    1 AND 1 = 1  (CARRY! 1+1=10, carry the 1)                 │
│                                                                │
│  AND detects where both bits are 1 → carry generated          │
│  << 1 shifts carry to next position (that's where it goes)   │
└────────────────────────────────────────────────────────────────┘

WHY THE LOOP TERMINATES:
┌────────────────────────────────────────────────────────────────┐
│  Each iteration, the carry gets shifted left.                  │
│  Eventually, carry "falls off" the left side (becomes 0).     │
│  OR all bits that could generate carry get resolved.          │
│                                                                │
│  Maximum iterations = number of bits (32 for 32-bit ints)     │
└────────────────────────────────────────────────────────────────┘

HANDLING NEGATIVE NUMBERS:
┌────────────────────────────────────────────────────────────────┐
│  32-BIT TWO'S COMPLEMENT:                                      │
│                                                                │
│  Positive numbers: 0x00000000 to 0x7FFFFFFF                   │
│  Negative numbers: 0x80000000 to 0xFFFFFFFF                   │
│                                                                │
│  -1 = 0xFFFFFFFF (all 1s)                                     │
│  -2 = 0xFFFFFFFE                                              │
│                                                                │
│  In Python, integers are arbitrary precision.                  │
│  We use MASK = 0xFFFFFFFF to simulate 32-bit overflow.        │
│                                                                │
│  If result > 0x7FFFFFFF (MAX_INT), it represents a negative   │
│  number in two's complement. We convert it back:              │
│      ~(result ^ MASK) gives the Python negative integer       │
└────────────────────────────────────────────────────────────────┘

CONVERSION EXAMPLE:
┌────────────────────────────────────────────────────────────────┐
│  Result = 0xFFFFFFFE (which is -2 in 32-bit)                  │
│                                                                │
│  result > MAX_INT (0x7FFFFFFF)? YES                           │
│                                                                │
│  result ^ MASK = 0xFFFFFFFE ^ 0xFFFFFFFF = 0x00000001         │
│  ~0x00000001 = -2 in Python ✓                                 │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  a = 0, b = 5  → 0 ^ 5 = 5, carry = 0 → Result: 5            │
│  a = -1, b = 1 → Eventually resolves to 0 ✓                   │
│  a = -1, b = -1 → Should give -2 ✓                            │
│  a = 1000, b = -1000 → Should give 0 ✓                        │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(1)
├── Maximum 32 iterations (number of bits)
└── Each iteration is O(1) bit operations

SPACE COMPLEXITY: O(1)
├── Only using a few variables
└── No extra data structures

CONCEPTS USED:
• Bit Manipulation (XOR, AND, shift)
• Two's Complement Representation
• Binary Addition
• Carry Propagation
"""
