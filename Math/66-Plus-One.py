# 66. Plus One
# Difficulty: Easy
# https://leetcode.com/problems/plus-one/

"""
PROBLEM:
Given a large integer represented as an array of digits (most significant first),
increment the integer by one and return the resulting array of digits.

EXAMPLES:
Input: digits = [1,2,3]   → Output: [1,2,4]   (123 + 1 = 124)
Input: digits = [4,3,2,1] → Output: [4,3,2,2] (4321 + 1 = 4322)
Input: digits = [9]       → Output: [1,0]     (9 + 1 = 10)
Input: digits = [9,9,9]   → Output: [1,0,0,0] (999 + 1 = 1000)

CONSTRAINTS:
- 1 <= digits.length <= 100
- 0 <= digits[i] <= 9
- No leading zeros (except for "0" itself)

KEY INSIGHT:
When adding 1, only two things can happen to each digit:
1. Digit < 9: Add 1 and we're done (no carry)
2. Digit = 9: Becomes 0, carry 1 to next position

Special case: All 9s → Need to prepend 1 to array

VISUALIZATION:
[1,2,9] + 1:
     9 + 1 = 10 → write 0, carry 1
     2 + 1 = 3  → write 3, done
Result: [1,3,0]

[9,9,9] + 1:
     9 + 1 = 10 → write 0, carry
     9 + 1 = 10 → write 0, carry
     9 + 1 = 10 → write 0, carry
     Still have carry! → prepend 1
Result: [1,0,0,0]
"""

# STEP 1: Traverse array from right to left (least significant digit first)
# STEP 2: If digit < 9, add 1 and return (no carry needed)
# STEP 3: If digit = 9, set to 0 and continue (implicit carry)
# STEP 4: If loop completes, all digits were 9, prepend 1

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        
        for i in range(len(digits) - 1, -1, -1):                                 # Right to left
            
            if digits[i] < 9:                                                    # No carry needed
                digits[i] += 1                                                   # Add 1
                return digits                                                    # Done!
            
            digits[i] = 0                                                        # 9 becomes 0 (carry)
        
        return [1] + digits                                                      # All 9s: prepend 1

"""
WHY EACH PART:
- range(len(digits)-1, -1, -1): Iterate from last index to 0 (right to left)
- if digits[i] < 9: If digit is 0-8, adding 1 won't cause carry
- digits[i] += 1: Simply increment and we're done
- return digits: Early exit - no need to check other digits
- digits[i] = 0: Digit was 9, becomes 0, carry is implicit (continue loop)
- return [1] + digits: Loop completed means all were 9s, now all are 0s, prepend 1

HOW IT WORKS (Example: [1,2,9]):
i=2: digits[2]=9, not < 9, so digits[2]=0 → [1,2,0]
i=1: digits[1]=2, 2 < 9, so digits[1]=3 → [1,3,0], return

HOW IT WORKS (Example: [9,9,9]):
i=2: digits[2]=9, not < 9, so digits[2]=0 → [9,9,0]
i=1: digits[1]=9, not < 9, so digits[1]=0 → [9,0,0]
i=0: digits[0]=9, not < 9, so digits[0]=0 → [0,0,0]
Loop ends → return [1] + [0,0,0] = [1,0,0,0]

KEY TECHNIQUE:
- Implicit carry: Don't need a carry variable
- Early termination: Return as soon as no carry
- Simple logic: Only check if digit is 9 or not

ALTERNATIVE APPROACH (Explicit carry):
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry = 1
        
        for i in range(len(digits) - 1, -1, -1):
            total = digits[i] + carry
            digits[i] = total % 10
            carry = total // 10
            
            if carry == 0:
                break
        
        if carry:
            digits.insert(0, 1)
        
        return digits

# More traditional

EDGE CASES:
- Single digit not 9 [5]: Returns [6] ✓
- Single digit 9 [9]: Returns [1,0] ✓
- All 9s [9,9,9]: Returns [1,0,0,0] ✓
- Ends in 9 [1,9]: Returns [2,0] ✓
- Multiple 9s at end [1,9,9]: Returns [2,0,0] ✓
- No 9s [1,2,3]: Returns [1,2,4] ✓
- Large array (100 digits): Works correctly ✓

TIME COMPLEXITY: O(n) worst case, O(1) best case
- Best: Last digit not 9 → single operation
- Worst: All digits are 9 → traverse entire array + create new array

SPACE COMPLEXITY: O(n) worst case, O(1) best case
- Best: Modify in-place, return same array
- Worst: All 9s → create new array [1] + digits

CONCEPTS USED:
- Array traversal (right to left)
- Carry propagation
- Early termination
- In-place modification
- Edge case handling (all 9s)
"""
