# 67. Add Binary
# Difficulty: Easy
# https://leetcode.com/problems/add-binary/

"""
PROBLEM:
Given two binary strings a and b, return their sum as a binary string.

EXAMPLES:
Input: a = "11", b = "1"      → Output: "100"   (3 + 1 = 4)
Input: a = "1010", b = "1011" → Output: "10101" (10 + 11 = 21)

CONSTRAINTS:
- 1 <= a.length, b.length <= 10^4
- a and b consist only of '0' or '1'
- No leading zeros except for "0" itself

BINARY ADDITION RULES:
0 + 0 = 0
0 + 1 = 1
1 + 0 = 1
1 + 1 = 10 (write 0, carry 1)
1 + 1 + 1 = 11 (write 1, carry 1)

Formula:
total = digit_a + digit_b + carry
result_digit = total % 2
new_carry = total // 2

VISUALIZATION (a="1010", b="1011"):
      1 0 1 0
    + 1 0 1 1
    ─────────
    1 0 1 0 1

Position 0: 0+1+0=1 → write 1, carry 0
Position 1: 1+1+0=2 → write 0, carry 1
Position 2: 0+0+1=1 → write 1, carry 0
Position 3: 1+1+0=2 → write 0, carry 1
Position 4: 0+0+1=1 → write 1, carry 0

Result: "10101" ✓
"""

# STEP 1: Initialize pointers at end of both strings
# STEP 2: Process digits from right to left
# STEP 3: Handle different lengths (use 0 for missing digits)
# STEP 4: Continue while there are digits or carry
# STEP 5: Reverse result (built right to left)

class Solution:
    def addBinary(self, a: str, b: str) -> str:
        
        resultado = []                                                           # Build result here
        carry = 0                                                                # Carry bit
        
        i = len(a) - 1                                                           # Pointer to end of a
        j = len(b) - 1                                                           # Pointer to end of b
        
        while i >= 0 or j >= 0 or carry:                                         # While work remains
            
            digito_a = int(a[i]) if i >= 0 else 0                                # Get digit or 0
            digito_b = int(b[j]) if j >= 0 else 0                                # Get digit or 0
            
            total = digito_a + digito_b + carry                                  # Sum digits and carry
            
            resultado.append(str(total % 2))                                     # Append result bit
            carry = total // 2                                                   # Calculate new carry
            
            i -= 1                                                               # Move pointer left
            j -= 1                                                               # Move pointer left
        
        return ''.join(resultado[::-1])                                          # Reverse and join

"""
WHY EACH PART:
- i, j at end: Start from least significant bit (rightmost)
- while i >= 0 or j >= 0 or carry: Continue until all digits and carry processed
- int(a[i]) if i >= 0 else 0: Get digit or 0 if string exhausted
- total % 2: Get the bit to write (0 or 1)
- total // 2: Get the carry (0 or 1)
- resultado[::-1]: We built right-to-left, need to reverse

HOW IT WORKS (Example: "11" + "1"):

Initial: i=1, j=0, carry=0, resultado=[]

Iteration 1 (i=1, j=0):
├── digito_a = int('1') = 1
├── digito_b = int('1') = 1
├── total = 1 + 1 + 0 = 2
├── resultado.append('0')  [2 % 2 = 0]
├── carry = 1              [2 // 2 = 1]
└── resultado = ['0']

Iteration 2 (i=0, j=-1):
├── digito_a = int('1') = 1
├── digito_b = 0 (j < 0)
├── total = 1 + 0 + 1 = 2
├── resultado.append('0')
├── carry = 1
└── resultado = ['0', '0']

Iteration 3 (i=-1, j=-2, carry=1):
├── digito_a = 0 (i < 0)
├── digito_b = 0 (j < 0)
├── total = 0 + 0 + 1 = 1
├── resultado.append('1')
├── carry = 0
└── resultado = ['0', '0', '1']

Exit: i<0, j<0, carry=0

resultado[::-1] = ['1', '0', '0']
return "100" ✓

KEY TECHNIQUE:
- Two-pointer from end: Process least significant bits first
- Implicit padding: Use 0 for missing digits
- Universal carry handling: Same formula for all cases
- Build and reverse: Common pattern for building strings right-to-left

EDGE CASES:
- Same length ("11" + "11"): Returns "110" ✓
- Different length ("1" + "111"): Returns "1000" ✓
- Single digits ("1" + "1"): Returns "10" ✓
- No carry needed ("10" + "01"): Returns "11" ✓
- All ones ("111" + "111"): Returns "1110" ✓
- One is "0" ("0" + "1"): Returns "1" ✓
- Both "0" ("0" + "0"): Returns "0" ✓
- Very long strings (10^4 digits): Works correctly ✓

TIME COMPLEXITY: O(max(n, m)) - Process each digit once
SPACE COMPLEXITY: O(max(n, m)) - Result string length

CONCEPTS USED:
- Binary number system
- Carry propagation
- Two-pointer technique (from end)
- String building and reversal
- Handling different-length inputs
- Modulo and integer division for digit extraction
"""
