# 1103. Distribute Candies to People
# Difficulty: Easy
# https://leetcode.com/problems/distribute-candies-to-people/

"""
PROBLEM:
We distribute some number of `candies`, to a row of `n = num_people` people in the following way:
We give 1 candy to the first person, 2 candies to the second person, and so on until we give 
`n` candies to the last person. Then, we go back to the start of the row, giving `n + 1` candies 
to the first person, `n + 2` to the second person, and so on.
This process repeats until we run out of candies. The last person will receive all of our 
remaining candies. Return an array representing the final distribution of candies.

EXAMPLES:
Input: candies = 7, num_people = 4
Output: [1, 2, 3, 1]
Explanation:
- Turn 1: Give 1 candy to person 0. (candies = 6)
- Turn 2: Give 2 candies to person 1. (candies = 4)
- Turn 3: Give 3 candies to person 2. (candies = 1)
- Turn 4: Try to give 4 to person 3, but only 1 is left. Give 1. (candies = 0)

CONSTRAINTS:
- 1 <= candies <= 10^9
- 1 <= num_people <= 1000

ALGORITHMIC INTUITION:
Instead of finding a complex mathematical formula (which exists but is prone to edge-case errors), 
we can simply simulate the process. The constraints allow simulation because the number of candies 
given increases incrementally (1, 2, 3, 4...). 
The sum of an arithmetic progression grows quadratically (n * (n + 1) / 2). Because of this, 
even for 10^9 candies, the while loop will only run approximately sqrt(2 * 10^9) ≈ 44,721 times, 
which executes in milliseconds.

We need to manage three states:
1. Wrap-around indexing: Using modulo `%` to make the linear array behave like a circle.
2. The "Reality Check": We want to give `x` candies, but we only give `min(x, remaining_candies)`.
3. State updating: Decrement candies and increment the target give amount.
"""

# STEP 1: Initialize an array of size `num_people` with 0s.
# STEP 2: Track the current amount to `give` (starting at 1).
# STEP 3: Loop while we still have candies.
# STEP 4: Calculate actual candies to give using min().
# STEP 5: Find the correct person using modulo arithmetic.
# STEP 6: Update the person's count, subtract from total candies, and increment `give`.

from typing import List

class Solution:
    def distributeCandies(self, candies: int, num_people: int) -> List[int]:
        
        result = [0] * num_people                                # Array to store results
        give = 1                                                 # Start giving 1 candy
        
        while candies > 0:                                       # While supplies last
            
            actual_give = min(give, candies)                     # We give what we want OR what we have
            
            index = (give - 1) % num_people                      # Wrap-around logic
            
            result[index] += actual_give                         # Add candies to the person
            candies -= actual_give                               # Deduct from total stock
            give += 1                                            # Next turn gives 1 more
            
        return result

"""
WHY EACH PART:
- [0] * num_people: Pre-allocating the array size is O(N) and prevents dynamic resizing overhead.
- min(give, candies): This cleanly handles the edge case of the final turn without needing an if/else block.
- (give - 1) % num_people: 
  If give=1, people=4 -> (1-1)%4 = 0 (Person 1)
  If give=4, people=4 -> (4-1)%4 = 3 (Person 4)
  If give=5, people=4 -> (5-1)%4 = 0 (Back to Person 1!)

HOW IT WORKS (Example: candies = 10, num_people = 3):
Initial: candies = 10, give = 1, result = [0, 0, 0]

Iteration 1 (give = 1):
├── actual_give = min(1, 10) = 1
├── index = (1 - 1) % 3 = 0
├── result = [1, 0, 0]
└── candies = 9, give = 2

Iteration 2 (give = 2):
├── actual_give = min(2, 9) = 2
├── index = (2 - 1) % 3 = 1
├── result = [1, 2, 0]
└── candies = 7, give = 3

Iteration 3 (give = 3):
├── actual_give = min(3, 7) = 3
├── index = (3 - 1) % 3 = 2
├── result = [1, 2, 3]
└── candies = 4, give = 4

Iteration 4 (give = 4):
├── actual_give = min(4, 4) = 4
├── index = (4 - 1) % 3 = 0  <-- Wrapped around!
├── result = [5, 2, 3]
└── candies = 0, give = 5

Exit Loop. Return [5, 2, 3] ✓

TIME COMPLEXITY: O(sqrt(C)) - Where C is the total number of candies. The amount given out grows linearly, meaning the total sum grows quadratically. Thus, the loop runs roughly sqrt(C) times.
SPACE COMPLEXITY: O(N) - Where N is the number of people, to store the result array.
"""
