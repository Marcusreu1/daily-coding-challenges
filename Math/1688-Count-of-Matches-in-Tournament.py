# 1688. Count of Matches in Tournament
# Difficulty: Easy
# https://leetcode.com/problems/count-of-matches-in-tournament/

"""
PROBLEM:
You are given an integer n, the number of teams in a tournament that has strange rules:
- If the current number of teams is even, each team gets paired with another team. A total of n / 2 matches are played, and n / 2 teams advance to the next round.
- If the current number of teams is odd, one team randomly advances in the tournament, and the rest get paired. A total of (n - 1) / 2 matches are played, and (n - 1) / 2 + 1 teams advance to the next round.
Return the number of matches played in the tournament until a winner is decided.

EXAMPLES:
Input: n = 7 → Output: 6
Explanation: Details of the tournament: 
- 1st Round: Teams = 7, Matches = 3, and 4 teams advance.
- 2nd Round: Teams = 4, Matches = 2, and 2 teams advance.
- 3rd Round: Teams = 2, Matches = 1, and 1 team advances.
Total matches = 3 + 2 + 1 = 6.

Input: n = 14 → Output: 13
Explanation: Details of the tournament:
- 1st Round: Teams = 14, Matches = 7, and 7 teams advance.
- 2nd Round: Teams = 7, Matches = 3, and 4 teams advance.
- 3rd Round: Teams = 4, Matches = 2, and 2 teams advance.
- 4th Round: Teams = 2, Matches = 1, and 1 team advances.
Total matches = 7 + 3 + 2 + 1 = 13.

CONSTRAINTS:
- 1 <= n <= 200

MATH RULES (ELIMINATION LOGIC):
Instead of simulating the tournament round by round, we can observe the fundamental property of a knockout tournament:
- Every match played eliminates exactly one team.
- To determine exactly 1 winner out of 'n' teams, we must eliminate exactly 'n - 1' teams.
- Therefore, exactly 'n - 1' matches MUST be played, regardless of how the byes (odd number rule) are distributed.

VISUALIZATION (n=7):
Start: 7 teams
Target: 1 winner
Teams to eliminate = 7 - 1 = 6
Since 1 match = 1 elimination, total matches = 6 ✓
"""

# STEP 1: Understand the mathematical property of knockout tournaments.
# STEP 2: Return n - 1 directly without any iteration or simulation.

class Solution:
    def numberOfMatches(self, n: int) -> int:
        
        # In a knockout tournament, to get 1 winner from n teams, n-1 teams must be eliminated.
        # Since each match eliminates exactly 1 team, n-1 matches are required.
        result = n - 1
        
        return result

"""
WHY EACH PART:
- n - 1: Represents the exact number of eliminations needed to crown a single champion. 

HOW IT WORKS (Example: n = 7):

Initial: n = 7
Execution:
├── result = 7 - 1
└── result = 6

Return 6 ✓

ALTERNATIVE SIMULATION APPROACH (For comparison):
If we were to simulate it step by step, the code would look like this:
    matches = 0
    while n > 1:
        if n % 2 == 0:
            matches += n // 2
            n = n // 2
        else:
            matches += (n - 1) // 2
            n = (n - 1) // 2 + 1
    return matches
Both approaches yield the exact same answer, but the mathematical approach is strictly O(1).

KEY TECHNIQUE:
- Lateral Thinking / Graph Theory logic: Translating a procedural simulation problem into a simple state-evaluation problem (Initial state vs Final state).

EDGE CASES:
- n = 1: The tournament starts with 1 team. 1 - 1 = 0 matches played. The team is already the winner. ✓

TIME COMPLEXITY: O(1) - Returns the result instantly in a single mathematical operation.
SPACE COMPLEXITY: O(1) - No extra variables or data structures are used.

CONCEPTS USED:
- Discrete Mathematics (Tournament/Tree reduction)
- Lateral Thinking optimizations
"""
