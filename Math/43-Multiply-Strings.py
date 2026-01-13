# 43. Multiply Strings
# Difficulty: Medium
# https://leetcode.com/problems/multiply-strings/

"""
PROBLEM:
Given two non-negative integers num1 and num2 represented as strings,
return the product of num1 and num2, also represented as a string.

RESTRICTIONS:
- Cannot use built-in BigInteger library
- Cannot convert inputs directly to integers

WHY THIS MATTERS:
Numbers can have up to 200 digits - way beyond int/long capacity.
Must simulate manual multiplication digit by digit.

EXAMPLES:
Input: num1 = "2", num2 = "3"       → Output: "6"
Input: num1 = "123", num2 = "456"   → Output: "56088"

CONSTRAINTS:
- 1 <= num1.length, num2.length <= 200
- num1 and num2 consist of digits only
- No leading zeros except "0" itself

KEY INSIGHT:
When multiplying digit at position i of num1 with digit at position j of num2:
- Result digit goes to position (i + j + 1)
- Carry goes to position (i + j)

MANUAL MULTIPLICATION ANALOGY:
        1 2 3
      ×   4 5
    ─────────
        6 1 5   ← 123 × 5
      4 9 2     ← 123 × 4 (shifted)
    ─────────
      5 5 3 5
"""

# STEP 1: Handle multiplication by zero
# STEP 2: Create result array of size (n + m)
# STEP 3: Multiply each digit pair from right to left
# STEP 4: Store digit at p2, propagate carry to p1
# STEP 5: Convert to string, remove leading zeros

class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        
        if num1 == "0" or num2 == "0":                                           # Multiplication by zero
            return "0"
        
        n, m = len(num1), len(num2)                                              # Get lengths
        resultado = [0] * (n + m)                                                # Max possible digits in result
        
        for i in range(n - 1, -1, -1):                                           # Right to left in num1
            for j in range(m - 1, -1, -1):                                       # Right to left in num2
                
                p1 = i + j                                                       # Position for carry (high digit)
                p2 = i + j + 1                                                   # Position for digit (low digit)
                
                producto = int(num1[i]) * int(num2[j])                           # Multiply single digits
                suma = producto + resultado[p2]                                  # Add to existing value
                
                resultado[p2] = suma % 10                                        # Store ones digit
                resultado[p1] += suma // 10                                      # Propagate carry
        
        resultado_str = ''.join(map(str, resultado))                             # Convert array to string
        return resultado_str.lstrip('0') or '0'                                  # Remove leading zeros

"""
WHY EACH PART:
- if num1 == "0" or num2 == "0": Quick return for zero multiplication
- resultado = [0] * (n + m): Product of n-digit × m-digit has at most n+m digits
- range(n-1, -1, -1): Iterate right to left (units first, like manual multiplication)
- p1 = i + j: Position where carry goes (one position left of p2)
- p2 = i + j + 1: Position where product digit goes
- int(num1[i]): Convert character '5' to integer 5
- suma = producto + resultado[p2]: Accumulate (multiple products contribute to same position)
- resultado[p2] = suma % 10: Keep only ones digit at this position
- resultado[p1] += suma // 10: Add carry to next position
- lstrip('0'): Remove leading zeros ("056088" → "56088")
- or '0': Handle edge case where result is all zeros

HOW IT WORKS (Example: "123" × "456"):

Position formula for result array [0,1,2,3,4,5]:

num1[i] × num2[j] → affects positions p1=i+j and p2=i+j+1

       j=0('4')  j=1('5')  j=2('6')
       ────────  ────────  ────────
i=0('1')  p2=1     p2=2     p2=3
i=1('2')  p2=2     p2=3     p2=4
i=2('3')  p2=3     p2=4     p2=5

Processing order (i=2,1,0 and j=2,1,0 for each i):
3×6=18 → pos 5 gets 8, carry 1 to pos 4
3×5=15+1=16 → pos 4 gets 6, carry 1 to pos 3
3×4=12+1=13 → pos 3 gets 3, carry 1 to pos 2
... and so on

Final: [0,5,6,0,8,8] → "56088" ✓

KEY TECHNIQUE:
- Digit-by-digit multiplication: Simulates manual process
- Position mapping: i+j and i+j+1 formula places results correctly
- Accumulation: Multiple products can contribute to same position
- Carry propagation: suma // 10 handles overflow to next position

EDGE CASES:
- Multiply by zero ("123" × "0"): Returns "0" ✓
- Single digits ("2" × "3"): Returns "6" ✓
- One digit × multiple ("9" × "99"): Returns "891" ✓
- Result with leading zeros: Handled by lstrip ✓
- Very large numbers (200 digits): Works without overflow ✓
- Same numbers ("111" × "111"): Returns "12321" ✓

TIME COMPLEXITY: O(n × m) - Nested loops over both string lengths
SPACE COMPLEXITY: O(n + m) - Result array size

CONCEPTS USED:
- String manipulation
- Array as digit storage
- Carry propagation
- Position mapping formula
- Manual multiplication simulation
- Leading zero removal
"""
