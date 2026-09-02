# 1823. Find the Winner of the Circular Game
# Difficulty: Medium
# https://leetcode.com/problems/find-the-winner-of-the-circular-game/

"""
PROBLEM:
There are n friends that are playing a game. The friends are sitting in a circle and are numbered from 1 to n in clockwise order.
Rules of the game:
1. Start at the 1st friend.
2. Count the next k friends in the clockwise direction including the friend you started at. 
3. The last friend you counted leaves the circle and loses the game.
4. If there is still more than one friend in the circle, go back to step 2 starting from the friend immediately clockwise of the friend who just lost and repeat.
5. Else, the last friend in the circle wins the game.
Given the number of friends, n, and an integer k, return the winner of the game.

EXAMPLES:
Input: n = 5, k = 2 → Output: 3
Explanation: Here are the steps of the game:
1) Start at friend 1.
2) Count 2 friends clockwise, which are friends 1 and 2.
3) Friend 2 leaves the circle. Next start is friend 3.
4) Count 2 friends clockwise, which are friends 3 and 4.
5) Friend 4 leaves the circle. Next start is friend 5.
6) Count 2 friends clockwise, which are friends 5 and 1.
7) Friend 1 leaves the circle. Next start is friend 3.
8) Count 2 friends clockwise, which are friends 3 and 5.
9) Friend 5 leaves the circle. Only friend 3 is left, so they are the winner.

CONSTRAINTS:
- 1 <= k <= n <= 500

MATH RULES (THE JOSEPHUS PROBLEM):
Simulating the array deletions takes O(N^2) time due to shifting elements. 
Instead, we can use dynamic programming (bottom-up mathematics) to track the winner's index.
Using 0-based indexing:
- When there is 1 person, the winner is at index 0.
- When there are 'i' people, the winner's position shifts by 'k'. 
- The formula to find the previous position is: winner_index = (winner_index + k) % i
We can iterate from a circle of size 2 up to n, applying this formula. 
Finally, we add 1 to the result to convert it back to 1-based indexing as requested by the problem.

VISUALIZATION (n = 5, k = 2):
Initial: winner_index = 0 (Base case for 1 person left)

Circle size = 2: winner_index = (0 + 2) % 2 = 0
Circle size = 3: winner_index = (0 + 2) % 3 = 2
Circle size = 4: winner_index = (2 + 2) % 4 = 0
Circle size = 5: winner_index = (0 + 2) % 5 = 2

Final winner_index (0-based) = 2. 
Convert to 1-based: 2 + 1 = 3. 
Result: 3 ✓
"""

# STEP 1: Initialize the winner's index at 0, representing the base case (1 person left, 0-indexed).
# STEP 2: Iterate through circle sizes starting from 2 up to n.
# STEP 3: Dynamically calculate the winner's shifted position using the Josephus formula.
# STEP 4: Return the final index + 1 to account for the 1-based numbering in the problem description.

class Solution:
    def findTheWinner(self, n: int, k: int) -> int:
        
        # Track the index of the winner using 0-based indexing
        winner_index = 0
        
        # Simulate the circle growing from size 2 up to n
        for circle_size in range(2, n + 1):
            
            # Mathematical shift to find where the winner was before the elimination
            winner_index = (winner_index + k) % circle_size
            
        # Convert 0-based index to 1-based friend number
        return winner_index + 1

"""
WHY EACH PART:
- winner_index = 0: Essential starting point. We mathematically solve this bottom-up. If only 1 person exists, they are at index 0.
- range(2, n + 1): We are iterating over the 'sizes' of the circle, ending exactly when the circle has 'n' people.
- (winner_index + k) % circle_size: The modulo operation perfectly wraps the index around the circular boundary without out-of-bounds errors.
- winner_index + 1: A simple offset calculation to match the output requirements of the problem.

KEY TECHNIQUE:
- Dynamic Programming / Josephus Recurrence: Eliminating the need to simulate data structure mutations by mathematically predicting the final state.
- Time & Space Optimization: Avoiding Lists or Queues drops the space complexity to O(1) and time complexity to O(N).

EDGE CASES:
- k = 1: The modulo logic naturally increments the index by 1 each time. For n=5, winner will be (0+1)%2=1 -> (1+1)%3=2 -> (2+1)%4=3 -> (3+1)%5=4. +1 = 5. Works flawlessly.

TIME COMPLEXITY: O(N) - The loop runs exactly N - 1 times, performing constant-time mathematical operations.
SPACE COMPLEXITY: O(1) - Only a single integer variable is updated in-place.

CONCEPTS USED:
- Discrete Mathematics (The Josephus Problem)
- Modulo Arithmetic
- Bottom-Up Dynamic Programming
"""
