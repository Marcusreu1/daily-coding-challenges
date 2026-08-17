# 1686. Stone Game VI
# Difficulty: Medium
# https://leetcode.com/problems/stone-game-vi/

"""
PROBLEM:
Alice and Bob take turns playing a game, with Alice starting first.
There are n stones. On each player's turn, they can remove a stone from the pile.
Alice and Bob value the stones differently. 
- aliceValues[i] is the value of the i-th stone for Alice.
- bobValues[i] is the value of the i-th stone for Bob.
Both players play optimally to maximize their score.
Return 1 if Alice wins, -1 if Bob wins, or 0 if it's a draw.

EXAMPLES:
Input: aliceValues = [1,3], bobValues = [2,1] → Output: 1
Explanation:
If Alice takes stone 1 (value 3), Bob takes stone 0 (value 2).
Alice's score = 3, Bob's score = 2. Alice wins (1).

Input: aliceValues = [1,2], bobValues = [3,1] → Output: 0
Explanation:
If Alice takes stone 0, she gets 1. Bob takes stone 1, getting 1.
Score: Alice = 1, Bob = 1. Draw (0).

CONSTRAINTS:
- n == aliceValues.length == bobValues.length
- 1 <= n <= 10^5
- 1 <= aliceValues[i], bobValues[i] <= 100

MATH RULES (GREEDY STRATEGY & OPPORTUNITY COST):
When a player picks stone 'i', they not only gain their value but also prevent the opponent from getting their value.
Net impact of stone 'i' on the score difference = aliceValues[i] + bobValues[i].
Thus, the strictly optimal strategy for BOTH players is to always pick the available stone with the highest sum of (aliceValues[i] + bobValues[i]).

VISUALIZATION (alice = [2,4,3], bob = [1,6,7]):
1. Calculate Sums:
   Stone 0: 2 + 1 = 3
   Stone 1: 4 + 6 = 10
   Stone 2: 3 + 7 = 10

2. Combine and Sort by sum descending:
   [ (10, 4, 6), (10, 3, 7), (3, 2, 1) ]
      sum a  b    sum a  b    sum a  b

3. Simulate Turns:
   Turn 1 (Alice - index 0): Picks (10, 4, 6). Alice gets 4.
   Turn 2 (Bob - index 1): Picks (10, 3, 7). Bob gets 7.
   Turn 3 (Alice - index 2): Picks (3, 2, 1). Alice gets 2.

4. Calculate Final Score:
   Alice = 4 + 2 = 6
   Bob = 7
   Alice (6) < Bob (7). Bob wins. Return -1 ✓
"""

from typing import List

# STEP 1: Create a list of tuples containing (sum_value, alice_value, bob_value) for each stone.
# STEP 2: Sort the list in descending order based on the sum_value.
# STEP 3: Iterate through the sorted list, distributing stones based on turn index (even for Alice, odd for Bob).
# STEP 4: Compare total scores and return the expected integer (1, -1, or 0).

class Solution:
    def stoneGameVI(self, aliceValues: List[int], bobValues: List[int]) -> int:
        
        n = len(aliceValues)
        stones = []                                                          # Array to hold combined stone data
        
        # Build the list of stones with their combined opportunity cost
        for i in range(n):
            combined_sum = aliceValues[i] + bobValues[i]
            stones.append((combined_sum, aliceValues[i], bobValues[i]))
            
        # Sort stones descending primarily by the combined sum
        stones.sort(key=lambda x: x[0], reverse=True)
        
        alice_score = 0
        bob_score = 0
        
        # Simulate the optimal game
        for i in range(n):
            if i % 2 == 0:                                                   # Alice's turn (Even indices: 0, 2, 4...)
                alice_score += stones[i][1]
            else:                                                            # Bob's turn (Odd indices: 1, 3, 5...)
                bob_score += stones[i][2]
                
        # Determine the winner
        if alice_score > bob_score:
            return 1
        elif bob_score > alice_score:
            return -1
        else:
            return 0

"""
WHY EACH PART:
- stones.append((...)): We group the data into tuples so that when we sort by the sum, we don't lose the original individual values for Alice and Bob.
- sort(key=lambda x: x[0], reverse=True): Sorts the list from highest sum to lowest sum. The lambda function explicitly tells Python to sort using the first element of the tuple (the sum).
- i % 2 == 0: Since Alice always goes first, she will always pick on indices 0, 2, 4, etc. Bob picks on the remaining odd indices.

KEY TECHNIQUE:
- Greedy Algorithm: Making the locally optimal choice at each stage (picking the highest sum) leads to the globally optimal solution.
- Zipping/Tuple Grouping: Keeping related data properties together during a sort operation.

EDGE CASES:
- Stones with identical sums: The order doesn't mathematically matter for the final outcome because the net score swing remains identical. Python's stable sort handles it gracefully.
- n = 1: Alice automatically takes the only stone and wins (unless her value is 0 and Bob's is 0, which violates constraints).

TIME COMPLEXITY: O(n log n) - The dominant operation is sorting the 'stones' array. Iterating takes O(n).
SPACE COMPLEXITY: O(n) - We allocate a new array 'stones' of size n to store the combined tuples.

CONCEPTS USED:
- Greedy Algorithms
- Game Theory (Zero-sum game evaluation)
- Sorting with custom keys
- Modulo operator for alternating turns
"""
