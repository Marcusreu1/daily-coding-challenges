# 69. Sqrt(x)
# Difficulty: Easy
# https://leetcode.com/problems/sqrtx/

"""
PROBLEM:
Given a non-negative integer x, return the square root of x rounded down
to the nearest integer. The returned integer should be non-negative.

You must NOT use any built-in exponent function or operator (**, pow()).

EXAMPLES:
Input: x = 4  → Output: 2 (√4 = 2.0)
Input: x = 8  → Output: 2 (√8 = 2.828..., truncated to 2)

CONSTRAINTS:
- 0 <= x <= 2^31 - 1

KEY INSIGHT:
We're looking for the largest integer r such that r² ≤ x.
Since squares are ordered (1, 4, 9, 16, 25, ...), we can use BINARY SEARCH.

VISUALIZATION:
For x = 8, find r where r² ≤ 8 < (r+1)²

r:  1   2   3   4   5   ...
r²: 1   4   9  16  25  ...
         ↑
         2² = 4 ≤ 8 ✓
             3² = 9 > 8 ✗
             
Answer: 2
"""

# STEP 1: Handle special cases (x < 2)
# STEP 2: Set binary search range [1, x//2]
# STEP 3: Binary search for largest r where r² ≤ x
# STEP 4: Return the result

class Solution:
    def mySqrt(self, x: int) -> int:
        
        if x < 2:                                                                # √0 = 0, √1 = 1
            return x
        
        izq = 1                                                                  # Minimum possible sqrt
        der = x // 2                                                             # Maximum possible sqrt (for x >= 2)
        resultado = 0                                                            # Store best answer found
        
        while izq <= der:                                                        # Binary search
            medio = (izq + der) // 2                                             # Middle point
            cuadrado = medio * medio                                             # Calculate square
            
            if cuadrado == x:                                                    # Perfect square found
                return medio
            elif cuadrado < x:                                                   # medio might be answer
                resultado = medio                                                # Save as candidate
                izq = medio + 1                                                  # Search for larger
            else:                                                                # cuadrado > x
                der = medio - 1                                                  # Search for smaller
        
        return resultado                                                         # Return best candidate

"""
WHY EACH PART:
- x < 2: Handle edge cases (0 and 1)
- der = x // 2: For x >= 2, √x ≤ x/2 (reduces search space)
- resultado = medio: When medio² < x, medio is a valid answer (but maybe not the best)
- izq = medio + 1: If medio² < x, try to find something bigger
- der = medio - 1: If medio² > x, must find something smaller
- return resultado: After loop, resultado holds the largest r where r² ≤ x

HOW IT WORKS (Example: x = 8):

Initial: izq=1, der=4, resultado=0

Iteration 1:
├── medio = (1+4)//2 = 2
├── cuadrado = 4
├── 4 < 8 → resultado=2, izq=3
└── State: izq=3, der=4, resultado=2

Iteration 2:
├── medio = (3+4)//2 = 3
├── cuadrado = 9
├── 9 > 8 → der=2
└── State: izq=3, der=2, resultado=2

Exit: izq > der (3 > 2)
Return: 2 ✓

Verification: 2² = 4 ≤ 8 ✓, 3² = 9 > 8 ✓

KEY TECHNIQUE:
- Binary search: O(log n) instead of O(√n)
- Search for condition: Find largest r where r² ≤ x
- Save candidate: Keep track of valid answers while searching

EDGE CASES:
- x = 0: Returns 0 ✓
- x = 1: Returns 1 ✓
- Perfect square (x = 16): Returns 4 ✓
- Not perfect square (x = 8): Returns 2 (floor) ✓
- Large number (x = 2147483647): Returns 46340 ✓
- x = 2: Returns 1 ✓

TIME COMPLEXITY: O(log x) - Binary search halves range each iteration
SPACE COMPLEXITY: O(1) - Only use fixed number of variables

CONCEPTS USED:
- Binary search
- Search for condition (largest r where r² ≤ x)
- Integer arithmetic (avoid floating point)
- Newton-Raphson method (alternative)
- Candidate tracking in binary search
"""
