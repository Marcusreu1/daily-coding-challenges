# 1237. Find Positive Integer Solution for a Given Equation
# Difficulty: Medium
# https://leetcode.com/problems/find-positive-integer-solution-for-a-given-equation/

"""
PROBLEM:
Given a callable function `f(x, y)` with a hidden formula and a value `z`, reverse engineer 
the formula and return all positive integer pairs `x` and `y` where `f(x,y) == z`. 

The API `CustomFunction` is provided, which has a single method `f(x, y)`.
You are guaranteed that the function is STRICTLY INCREASING.
- f(x, y) < f(x + 1, y)
- f(x, y) < f(x, y + 1)

EXAMPLES:
Input: function_id = 1, z = 5 (where f(x, y) = x + y)
Output: [[1,4],[2,3],[3,2],[4,1]]

Input: function_id = 2, z = 5 (where f(x, y) = x * y)
Output: [[1,5],[5,1]]

CONSTRAINTS:
- 1 <= function_id <= 9
- 1 <= z <= 100
- It's guaranteed that the solutions of f(x, y) == z will be in the range 1 <= x, y <= 1000.

ALGORITHMIC INTUITION (THE "TRICK"):
Since we don't know the formula, we can only observe its behavior. 
The naive approach is O(N^2): Test all combinations from x=1 to 1000 and y=1 to 1000.
We can optimize this to O(N log N) using Binary Search: For every x, binary search the y.

But the most elegant solution is O(N) using the Two-Pointer technique.
Because the function is strictly increasing, we can treat the (x, y) coordinate plane 
like a sorted 2D Matrix. 
If we start at the extremes: `x = 1` (the smallest possible x) and `y = 1000` (the largest possible y).
- If f(x, y) > z: The result is too big. Since x is already at its minimum, the ONLY way to make the result smaller is to decrease y.
- If f(x, y) < z: The result is too small. We must increase x.
- If f(x, y) == z: We found a valid pair! We save it, and to find new pairs, we must BOTH increase x and decrease y.
"""

# STEP 1: Initialize the starting boundaries (x = 1, y = 1000).
# STEP 2: Create a results array to store valid pairs.
# STEP 3: Loop while x and y remain within the valid domain [1, 1000].
# STEP 4: Call the black-box function `customfunction.f(x, y)`.
# STEP 5: If the result matches `z`, save the pair and shift both pointers.
# STEP 6: If the result is too large, decrease `y`.
# STEP 7: If the result is too small, increase `x`.

from typing import List

# """
# This is the custom function interface.
# You should not implement it, or speculate about its implementation
# """
# class CustomFunction:
#     def f(self, x: int, y: int) -> int:
#         pass

class Solution:
    def findSolution(self, customfunction: 'CustomFunction', z: int) -> List[List[int]]:
        
        result = []
        
        # Step 1: Start at the top-left of our conceptual grid
        x = 1
        y = 1000
        
        # Step 3: Traverse the domain
        while x <= 1000 and y >= 1:
            
            # Step 4: Evaluate the hidden function
            current_val = customfunction.f(x, y)
            
            if current_val == z:
                # Step 5: Found a match
                result.append([x, y])
                x += 1
                y -= 1
                
            elif current_val > z:
                # Step 6: Too big, reduce the upper bound
                y -= 1
                
            else:
                # Step 7: Too small, increase the lower bound
                x += 1
                
        return result

"""
WHY EACH PART:
- x = 1, y = 1000: This asymmetrical start (min X, max Y) is the secret to moving efficiently. If we started at (1,1), and the result was too small, we wouldn't know whether to increase X or increase Y.
- x += 1 AND y -= 1 on match: If we found the target, increasing only X would mathematically guarantee a result > z. Decreasing only Y would guarantee a result < z. We must do both to find the next possible balance.

HOW IT WORKS (Conceptual Example: z = 10):
Assume the hidden function is f(x, y) = x + y

Initial: x = 1, y = 1000
├── f(1, 1000) = 1001. 
├── 1001 > 10. Decrease y.
└── y becomes 999.

... Fast forward ...

State: x = 1, y = 9
├── f(1, 9) = 10. Match!
├── result.append([1, 9])
└── x = 2, y = 8.

State: x = 2, y = 8
├── f(2, 8) = 10. Match!
└── result.append([2, 8]) ... and so on.

TIME COMPLEXITY: O(X + Y) -> O(1000 + 1000) -> O(N). In the worst case, we increment x 1000 times and decrement y 1000 times. We do at most 2000 evaluations.
SPACE COMPLEXITY: O(1) - Disregarding the output array, we only use two pointers.

CONCEPTS USED:
- Black Box Testing / API interaction
- Two-Pointer Technique
- Matrix Search / Monotonicity
"""
