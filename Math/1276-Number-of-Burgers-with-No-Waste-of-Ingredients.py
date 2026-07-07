# 1276. Number of Burgers with No Waste of Ingredients
# Difficulty: Medium
# https://leetcode.com/problems/number-of-burgers-with-no-waste-of-ingredients/

"""
PROBLEM:
Given two integers tomatoSlices and cheeseSlices. The ingredients of different burgers are as follows:
- Jumbo Burger: 4 tomato slices and 1 cheese slice.
- Small Burger: 2 tomato slices and 1 cheese slice.
Return [total_jumbo, total_small] so that the number of remaining tomatoSlices equal to 0 
and the number of remaining cheeseSlices equal to 0. If it is not possible to make the remaining 
ingredients equal to 0, return [].

EXAMPLES:
Input: tomatoSlices = 16, cheeseSlices = 7
Output: [1, 6]
(Explanation: 1 Jumbo Burger requires 4 tomatoes and 1 cheese. 
6 Small Burgers require 12 tomatoes and 6 cheeses. 
Total tomatoes: 4 + 12 = 16. Total cheese: 1 + 6 = 7. Matches perfectly.)

Input: tomatoSlices = 17, cheeseSlices = 4
Output: []
(Explanation: There will be no way to use all ingredients perfectly because 17 is odd, 
and all burgers use an even amount of tomatoes.)

Input: tomatoSlices = 4, cheeseSlices = 17
Output: []
(Explanation: Making 1 Jumbo Burger leaves 0 tomatoes and 16 cheese. We can't make anymore burgers. Impossible.)

CONSTRAINTS:
- 0 <= tomatoSlices, cheeseSlices <= 10^7

ALGORITHM LOGIC (Linear Equations System):
1. Let J be the number of Jumbo Burgers and S be the number of Small Burgers.
2. We can build a system of two equations based on the ingredients:
   - Equation 1 (Tomatoes): 4*J + 2*S = tomatoSlices
   - Equation 2 (Cheese):   J + S = cheeseSlices
3. From Equation 2, we know that S = cheeseSlices - J.
4. Substitute S into Equation 1:
   4*J + 2*(cheeseSlices - J) = tomatoSlices
   4*J + 2*cheeseSlices - 2*J = tomatoSlices
   2*J = tomatoSlices - 2*cheeseSlices
   J = (tomatoSlices - 2*cheeseSlices) / 2
5. For the solution to be physically possible (no negative or fractional burgers):
   - tomatoSlices must be EVEN (modulo 2 == 0).
   - tomatoSlices must be >= 2 * cheeseSlices (scenario where all burgers are Small).
   - tomatoSlices must be <= 4 * cheeseSlices (scenario where all burgers are Jumbo).

VISUALIZATION:
tomatoSlices = 16, cheeseSlices = 7
1. Validation: 
   - Is 16 even? Yes.
   - Is 16 >= 14? Yes.
   - Is 16 <= 28? Yes.
2. Calculate Jumbo:
   J = (16 - 2 * 7) / 2 
   J = (16 - 14) / 2
   J = 2 / 2 = 1
3. Calculate Small:
   S = cheeseSlices - J
   S = 7 - 1 = 6
Result: [1, 6] ✓
"""

# STEP 1: Validate if it's mathematically possible to use all ingredients without fractions or negative numbers
# STEP 2: If validation fails, return an empty array []
# STEP 3: If valid, apply the algebraic formula to find the exact number of Jumbo burgers
# STEP 4: Calculate the Small burgers by subtracting Jumbo burgers from the total cheese slices
# STEP 5: Return the result array [jumbo, small]

class Solution:
    def numOfBurgers(self, tomatoSlices: int, cheeseSlices: int) -> list[int]:
        
        if (tomatoSlices % 2 == 0) and (2 * cheeseSlices <= tomatoSlices <= 4 * cheeseSlices):  # Validation checks
            
            jumbo = (tomatoSlices - 2 * cheeseSlices) // 2           # Formula derived from isolating J
            small = cheeseSlices - jumbo                             # Total burgers (cheese) minus Jumbo
            
            return [jumbo, small]                                    # Return successful distribution
            
        return []                                                    # Impossible to distribute evenly

"""
WHY EACH PART:
- tomatoSlices % 2 == 0: Since both burgers require an even number of tomatoes (4 and 2), an odd number of total tomatoes guarantees waste.
- 2 * cheeseSlices <= tomatoSlices: The absolute minimum number of tomatoes needed for 'c' burgers is 2*c (all small). If we have fewer tomatoes than this, we will have leftover cheese.
- tomatoSlices <= 4 * cheeseSlices: The absolute maximum number of tomatoes we can use for 'c' burgers is 4*c (all jumbo). If we have more tomatoes than this, we will have leftover tomatoes.
- // 2: Using integer division ensures our result is an integer type, though we already mathematically proved the division will be clean by checking parity.

HOW IT WORKS (Example: tomatoSlices = 0, cheeseSlices = 0):
Validation:
- Is 0 even? Yes.
- Is 0 >= 0? Yes.
- Is 0 <= 0? Yes.
Calculation:
jumbo = (0 - 0) // 2 = 0
small = 0 - 0 = 0
Returns [0, 0] ✓

KEY TECHNIQUE:
- Pure Mathematics (Algebra): Translating a word problem into a system of linear equations avoids the need for loops, recursion, or complex data structures.

EDGE CASES:
- 0 tomatoes and 0 cheeses: Handles gracefully and returns [0, 0]. ✓
- 0 tomatoes but >0 cheeses: Fails the 2*c constraint, returns []. ✓
- Odd number of tomatoes: Fails parity check, returns []. ✓

TIME COMPLEXITY: O(1) - The code executes a constant number of basic mathematical operations regardless of the size of the input.
SPACE COMPLEXITY: O(1) - We allocate no extra memory other than the return array and a couple of integer variables. Highly optimal.

CONCEPTS USED:
- Math / Algebra
- Systems of Linear Equations
- Boundary Checking
"""
