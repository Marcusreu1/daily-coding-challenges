# 679. 24 Game
# Difficulty: Hard
# https://leetcode.com/problems/24-game/

"""
PROBLEM:
You are given an integer array cards of length 4. You have four cards, each containing a number in the range [1, 9].
You must arrange the numbers on these cards in a mathematical expression using the operators ['+', '-', '*', '/'] 
and the parentheses '(' and ')' to get the value 24.
Return true if you can get such expression and false otherwise.

EXAMPLES:
Input: cards = [4, 1, 8, 7]   → Output: True (Explanation: (8 - 1 / 4) * 7 = 24)
Input: cards = [1, 2, 1, 2]   → Output: False (Explanation: Cannot reach 24)

CONSTRAINTS:
- cards.length == 4
- 1 <= cards[i] <= 9
- Division is real division, not integer division.

LOGIC RULES (BACKTRACKING):
1. We start with 4 numbers. 
2. We pick any 2 numbers, apply an operator (+, -, *, /), and replace them with the result. Now we have 3 numbers.
3. Repeat the process to get 2 numbers, and finally 1 number.
4. If the final number is 24, we return True.
5. Because division can produce floating-point inaccuracies (e.g., 23.999999999), we use a small epsilon (1e-6) for comparison.
6. Order matters for subtraction and division (A - B != B - A).

VISUALIZATION (cards = [4, 1, 8, 7]):
State 1: [4, 1, 8, 7]
├── Pick 1 and 4, apply division (1/4) -> 0.25
State 2: [8, 7, 0.25]
├── Pick 8 and 0.25, apply subtraction (8 - 0.25) -> 7.75
State 3: [7, 7.75]
├── Pick 7 and 7.75, apply multiplication (7 * 7.75) -> 54.25 (Wait, (31/4)*7 is 217/4 = 54.25. Let's find the real 24!)
Backtrack!

Wait, correct math for [4,1,8,7]: 
(8 - 1) = 7 -> [4, 7, 7]. Not 24.
Actually, (8 - 1) = 7 -> 7 * 4 = 28 -> 28 - 7 = 21. No.
Wait, the actual solution for 8,4,7,1 is 8 / (1 - (3/8)) for [8,3,8,1]. 
For [4,1,8,7]: (8 - 1/4) * 7 = (31/4) * 7. Still not 24.
Correct one: (8 - 1/4) doesn't work. Wait! 
(8 - 4) = 4 -> 4 * 7 = 28 -> 28 - 1 = 27. No.
(4 - 1) = 3 -> 8 / (7 / 3) = 24/7. No.
(8 * 4) = 32 -> 32 - 7 = 25 -> 25 - 1 = 24!
Ah! (8 * 4) - 7 - 1 = 24.
Result: True ✓
"""

# STEP 1: Define a recursive helper function to handle lists of varying lengths
# STEP 2: Base case: if length is 1, check if the value is extremely close to 24
# STEP 3: Iterate through all possible pairs of numbers in the list
# STEP 4: Create a new list with the remaining unpicked numbers
# STEP 5: Calculate all 6 possible outcomes of combining the 2 picked numbers
# STEP 6: Append each outcome to the new list, recurse, and backtrack

import math

class Solution:
    def judgePoint24(self, cards: list[int]) -> bool:
        
        def backtrack(nums: list[float]) -> bool:
            
            if len(nums) == 1:                                               # Base Case: 1 number left
                return math.isclose(nums[0], 24.0, abs_tol=1e-6)             # Compare with 24 using a tiny tolerance
            
            for i in range(len(nums)):                                       # First pointer for pair
                for j in range(len(nums)):                                   # Second pointer for pair
                    if i != j:                                               # Can't pick the same card twice
                        
                        next_nums = []                                       # Array for the next recursive step
                        for k in range(len(nums)):                           # Add all OTHER numbers to next_nums
                            if k != i and k != j:
                                next_nums.append(nums[k])
                                
                        a, b = nums[i], nums[j]
                        
                        # Generate all possible results from a and b
                        results = [a + b, a - b, b - a, a * b]
                        if b != 0: results.append(a / b)                     # Avoid division by zero
                        if a != 0: results.append(b / a)                     # Order matters for division
                        
                        for res in results:                                  # Try every valid result
                            next_nums.append(res)                            # Add the result to our next state
                            
                            if backtrack(next_nums):                         # Recurse deeper! If we hit 24, return True
                                return True
                                
                            next_nums.pop()                                  # Backtrack: remove the result to try the next one
                            
            return False                                                     # If no combinations work, return False
            
        return backtrack([float(x) for x in cards])                          # Initial call, convert ints to floats

"""
WHY EACH PART:
- math.isclose(..., abs_tol=1e-6): Float arithmetic is imprecise (e.g., 8 / (3 - 8/3) = 23.999999). 
  We need a tolerance to correctly identify 24.
- i != j: We need exactly two distinct numbers to perform an operation.
- next_nums: We build a fresh list containing the unused numbers so we don't mutate the current state mid-loop.
- next_nums.pop(): This is the core of "Backtracking". After trying a path, we undo our choice (remove 'res') 
  so the next iteration starts with a clean slate.
- [float(x) for x in cards]: We convert the initial integer cards to floats to ensure all divisions are real divisions.

HOW IT WORKS (Simplified recursion depth trace):

Initial call: [4.0, 1.0, 8.0, 7.0]
├── Pick 8.0 and 4.0. Operation: MULTIPLY. Result = 32.0.
├── Recurse with [1.0, 7.0, 32.0]
    ├── Pick 32.0 and 7.0. Operation: SUBTRACT. Result = 25.0.
    ├── Recurse with [1.0, 25.0]
        ├── Pick 25.0 and 1.0. Operation: SUBTRACT. Result = 24.0.
        ├── Recurse with [24.0]
            ├── Length is 1. Is 24.0 == 24.0? YES. Return True.
        ├── Propagates True all the way up! ✓

EDGE CASES:
- [1, 1, 1, 1]: Explores all paths, max sum is 4. Returns False. ✓
- Tricky float cases like [8, 4, 7, 1]: Explores path 8 / (1 - (4/7)) ... wait, the real classic is 8/(3-8/3). 
  Our code handles these fractions flawlessly because of float conversion and math.isclose. ✓
- Division by zero: Guarded by `if b != 0` and `if a != 0`. Prevents ZeroDivisionError. ✓

TIME COMPLEXITY: O(1) 
This looks like an O(N!) algorithm, but since N is ALWAYS exactly 4, the number of operations is strictly bounded.
Combinations to pick 2 from 4 = 6. Operations = 6. 
Next step: pick 2 from 3 = 3. Operations = 6.
Next step: pick 2 from 2 = 1. Operations = 6.
Roughly 6 * 6 * 3 * 6 * 1 * 6 = ~3,888 constant operations max. Therefore, Time Complexity is O(1).

SPACE COMPLEXITY: O(1) 
The recursion tree depth is at most 3. The `next_nums` arrays store at most 4, 3, 2, and 1 elements.
Memory footprint is strictly bounded and constant. Space Complexity is O(1).
"""
