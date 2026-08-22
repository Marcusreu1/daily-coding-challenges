# 1753. Maximum Score From Removing Stones
# Difficulty: Medium
# https://leetcode.com/problems/maximum-score-from-removing-stones/

"""
PROBLEM:
You are playing a solitaire game with three piles of stones of sizes a, b, and c respectively.
Each turn you choose two different non-empty piles, take one stone from each, and add 1 point to your score.
The game stops when there are fewer than two non-empty piles (meaning you cannot take two stones anymore).
Return the maximum score you can get.

EXAMPLES:
Input: a = 2, b = 4, c = 6 → Output: 6
Explanation: 
The starting state is (2, 4, 6). One optimal set of moves is:
- Take from 1st and 3rd piles, state is now (1, 4, 5)
- Take from 1st and 3rd piles, state is now (0, 4, 4)
- Take from 2nd and 3rd piles, state is now (0, 3, 3)
- Take from 2nd and 3rd piles, state is now (0, 2, 2)
- Take from 2nd and 3rd piles, state is now (0, 1, 1)
- Take from 2nd and 3rd piles, state is now (0, 0, 0)
There are 6 moves in total, so the score is 6.

Input: a = 4, b = 4, c = 6 → Output: 7
Explanation: 
One optimal strategy yields a score of 7, leaving exactly 0 stones in the end since the total sum is 14 (14 // 2 = 7).

CONSTRAINTS:
- 1 <= a, b, c <= 10^5

MATH RULES (DOMINANCE & EQUILIBRIUM):
If we sort the piles such that x <= y <= z:
1. Dominance Condition: If z >= x + y
   The largest pile is larger than or equal to the sum of the other two. We can simply pair every stone in x and y with a stone in z. The game will end when x and y are empty. 
   Max score = x + y.
   
2. Equilibrium Condition: If z < x + y
   No single pile dominates. We can strategically pair stones such that all piles deplete almost simultaneously. We will be able to pair almost all stones, leaving at most 1 stone if the total sum is odd.
   Max score = (x + y + z) // 2.

VISUALIZATION (a = 2, b = 4, c = 6):
Sorted: x = 2, y = 4, z = 6
Condition Check: z (6) >= x + y (2 + 4 = 6) -> True!
This is a dominance scenario. 
Max score = x + y = 2 + 4 = 6 ✓
"""

# STEP 1: Store the values in an array and sort them in ascending order.
# STEP 2: Extract the smallest, middle, and largest values.
# STEP 3: Apply the Dominance rule: if the largest is >= the sum of the other two, return the sum of the other two.
# STEP 4: Apply the Equilibrium rule: otherwise, return the floor division of the total sum by 2.

class Solution:
    def maximumScore(self, a: int, b: int, c: int) -> int:
        
        # Sort the piles to easily identify the largest one
        piles = [a, b, c]
        piles.sort()
        
        small = piles[0]
        mid = piles[1]
        large = piles[2]
        
        # Scenario 1: The largest pile dominates
        if large >= small + mid:
            return small + mid
            
        # Scenario 2: Perfect or near-perfect equilibrium
        else:
            return (small + mid + large) // 2

"""
WHY EACH PART:
- piles.sort(): Sorting a 3-element array takes negligible O(1) time but perfectly sets up our mathematical logic.
- large >= small + mid: The core condition to determine if the biggest pile acts as an inescapable bottleneck.
- (small + mid + large) // 2: When no bottleneck exists, we can extract pairs equal to exactly half of all available stones. We use floor division (//) to drop the remainder if the total sum is odd.

HOW IT WORKS (Example: a = 4, b = 4, c = 6):

Initial state: a = 4, b = 4, c = 6

Execution:
├── piles.sort() -> [4, 4, 6]
├── small = 4, mid = 4, large = 6
├── Check: large >= small + mid -> 6 >= 4 + 4 -> 6 >= 8 (False)
├── Enters 'else' block (Equilibrium)
├── return (4 + 4 + 6) // 2
└── return 14 // 2 = 7

Return 7 ✓

ALTERNATIVE HEAP APPROACH (For comparison):
If we didn't use math, we would use a Max-Heap to simulate the game:
import heapq
# ... push negatives of a, b, c to max_heap ...
score = 0
while len(max_heap) > 1:
    first = heapq.heappop(max_heap)
    second = heapq.heappop(max_heap)
    score += 1
    if first + 1 < 0: heapq.heappush(max_heap, first + 1)
    if second + 1 < 0: heapq.heappush(max_heap, second + 1)
return score
This simulation runs in O(N log 3) time. Our math approach is strictly O(1).

KEY TECHNIQUE:
- Game Theory Optimization: Replacing simulation steps with the mathematical end-state formulas of the game.
- Pigeonhole / Dominance logic: Recognizing that the limiting factor in pairing problems is often the single largest entity.

EDGE CASES:
- Smallest values: a = 1, b = 1, c = 1. Sorted: 1, 1, 1. Equilibrium -> 3 // 2 = 1. ✓
- One massive pile: a = 1, b = 1, c = 10. Sorted: 1, 1, 10. Dominance -> 1 + 1 = 2. ✓

TIME COMPLEXITY: O(1) - Sorting 3 elements and basic arithmetic take constant time.
SPACE COMPLEXITY: O(1) - The array 'piles' size is strictly bounded to 3 elements.

CONCEPTS USED:
- Discrete Mathematics
- Game Strategy Analysis
- Sorting
"""
