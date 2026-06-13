# 1073. Adding Two Negabinary Numbers
# Difficulty: Medium
# https://leetcode.com/problems/adding-two-negabinary-numbers/

"""
PROBLEM:
Given two numbers arr1 and arr2 in base -2, return the result of adding them together.
Each number is given in array format, as a sequence of 0s and 1s, from most significant 
bit to least significant bit. The returned array must also be in base -2, with no leading zeros.

EXAMPLES:
Input: arr1 = [1,1,1,1,1], arr2 = [1,0,1]
Output: [1,0,0,0,0]
Explanation: 
arr1 represents 11111 in base -2 = 16 - 8 + 4 - 2 + 1 = 11
arr2 represents 101 in base -2 = 4 - 0 + 1 = 5
11 + 5 = 16. 16 in base -2 is 10000.

CONSTRAINTS:
- 1 <= arr1.length, arr2.length <= 1000
- arr1[i] and arr2[i] are 0 or 1
- arr1 and arr2 have no leading zeros

MATHEMATICAL INTUITION (THE "TRICK"):
In standard binary (base 2), when total = 2 at position 'i', it means 2 * 2^i.
We carry over 1 to position 'i+1' because: 2 * 2^i = 1 * 2^(i+1).

In negabinary (base -2), when total = 2 at position 'i', it means 2 * (-2)^i.
To express this in terms of the next position 'i+1', we do the math:
2 * (-2)^i = -1 * (-2)^(i+1)
Therefore, a sum of 2 generates a carry of -1, NOT +1.

But what if total = -1? (This happens if carry is -1 and both current bits are 0).
-1 at position 'i' means: -1 * (-2)^i
We can rewrite this as: 1 * (-2)^i + 1 * (-2)^(i+1)
So, if total = -1, we write down 1 for the current bit, and carry over +1.

Thanks to Python's floor division handling of negative numbers:
bit = total % 2
carry = -(total // 2)
This handles ALL cases perfectly (0, 1, 2, 3, and -1)!
"""

# STEP 1: Initialize pointers at the end of both arrays.
# STEP 2: Loop while there are digits to process or a carry exists.
# STEP 3: Sum the current bits plus the carry.
# STEP 4: Use the negabinary math formulas to find the bit and the new carry.
# STEP 5: Append the bit to the result.
# STEP 6: Remove any trailing zeros (which become leading zeros after reversal).
# STEP 7: Reverse the result array and return.

from typing import List

class Solution:
    def addNegabinary(self, arr1: List[int], arr2: List[int]) -> List[int]:
        
        res = []
        carry = 0
        i = len(arr1) - 1
        j = len(arr2) - 1
        
        while i >= 0 or j >= 0 or carry:
            
            # Get values or 0 if array is exhausted
            val1 = arr1[i] if i >= 0 else 0
            val2 = arr2[j] if j >= 0 else 0
            
            # Sum current position
            total = val1 + val2 + carry
            
            # Negabinary magic formulas
            res.append(total % 2)       # The bit to write (always 0 or 1)
            carry = -(total // 2)       # The carry for the next position
            
            i -= 1
            j -= 1
            
        # Remove trailing zeros (these would be leading zeros when reversed)
        # We keep at least one digit if the answer is literally 0
        while len(res) > 1 and res[-1] == 0:
            res.pop()
            
        # Reverse because we built from least significant to most significant
        return res[::-1]

"""
WHY EACH PART:
- carry = -(total // 2): This translates the mathematical reality of base -2. 
  In Python, -1 // 2 is -1. So -(-1) = 1. This correctly handles the total = -1 case!
- total % 2: In Python, -1 % 2 is 1. This correctly extracts the positive bit we need.
- while len(res) > 1 and res[-1] == 0: Processing carries can sometimes leave excess 0s 
  at the highest powers. We must trim them before reversing.

HOW IT WORKS (Example: [1] + [1] -> 1 + 1 = 2):
Initial: i=0, j=0, carry=0, res=[]

Iteration 1 (i=0, j=0):
├── total = 1 + 1 + 0 = 2
├── res.append(2 % 2) -> res = [0]
└── carry = -(2 // 2) = -1

Iteration 2 (i=-1, j=-1, carry=-1):
├── total = 0 + 0 + (-1) = -1
├── res.append(-1 % 2) -> res = [0, 1]
└── carry = -(-1 // 2) = -(-1) = 1

Iteration 3 (i=-1, j=-1, carry=1):
├── total = 0 + 0 + 1 = 1
├── res.append(1 % 2) -> res = [0, 1, 1]
└── carry = -(1 // 2) = 0

Exit Loop.
Trim Zeros: Not needed, last element is 1.
Reverse: res[::-1] = [1, 1, 0] (Which is exactly 2 in base -2). ✓

KEY TECHNIQUE:
- Floor Division Math: Leveraging how a specific programming language handles negative modulo and division to simplify complex logic.
- Two-Pointer Addition: The standard architecture for adding numbers represented as arrays.

TIME COMPLEXITY: O(max(N, M)) - Where N and M are the lengths of arr1 and arr2.
SPACE COMPLEXITY: O(max(N, M)) - The result array will be at most max(N, M) + 2 elements long.
"""
