# 2038. Remove Colored Pieces if Both Neighbors are the Same Color
# Difficulty: Medium
# https://leetcode.com/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/

"""
PROBLEM:
There are n pieces arranged in a line, and each piece is colored either by 'A' or by 'B'. You are given a string colors of length n where colors[i] is the color of the ith piece.
Alice and Bob are playing a game where they take alternating turns removing pieces from the line. In this game, Alice moves first.
- Alice is only allowed to remove a piece colored 'A' if both its neighbors are also colored 'A'. She is not allowed to remove pieces from the edges.
- Bob is only allowed to remove a piece colored 'B' if both its neighbors are also colored 'B'. He is not allowed to remove pieces from the edges.
- Alice and Bob cannot choose pieces from each other's color.
- If a player cannot make a move on their turn, that player loses and the other player wins.
Assuming Alice and Bob play optimally, return true if Alice wins, or return false if Bob wins.

EXAMPLES:
Input: colors = "AAABABB" → Output: true
Explanation:
- Alice's turn: "AAABABB" -> "AABABB".
- Bob's turn: Bob cannot make a move on his turn because there are no 'B's whose neighbors are both 'B'.
Alice wins, so return true.

Input: colors = "AA" → Output: false
Explanation: Alice has no valid moves. Bob wins, return false.

Input: colors = "ABBBBBBBAAA" → Output: false
Explanation:
- Alice has 1 valid move (the 'A' in the middle of the three 'A's).
- Bob has 5 valid moves.
Because Bob has vastly more moves, Alice will run out of moves first. Return false.

CONSTRAINTS:
- 1 <= colors.length <= 10^5
- colors only consists of the letters 'A' and 'B'.

MATH RULES (NON-INTERACTING GAME THEORY):
In many games, removing a piece alters the state of the board in a way that affects the opponent. 
However, since a piece can ONLY be removed if it is strictly surrounded by pieces of the SAME color, removing a piece will NEVER accidentally bring opposite colors together.
For instance, Alice removing an 'A' will just shorten an 'A' block. It will never merge two 'B' blocks.
Therefore, Alice's moves and Bob's moves are 100% mutually exclusive and independent. 
The game is completely deterministic from the start: it is simply a race of who has more valid moves available.
Since Alice goes first, she must have STRICTLY MORE moves than Bob to win. If they have the same number of moves, Alice will exhaust hers first and lose.

VISUALIZATION (colors = "AAABBB"):
Index 1: 'A' surrounded by 'A's -> Alice + 1
Index 2: 'A' not surrounded by 'A's.
Index 3: 'B' not surrounded by 'B's.
Index 4: 'B' surrounded by 'B's -> Bob + 1

Total: Alice = 1, Bob = 1.
Alice > Bob -> 1 > 1 is False.
Bob wins! ✓
"""

# STEP 1: Initialize counters for the total independent moves available to Alice and Bob.
# STEP 2: Iterate through the string starting from the second character and ending at the second-to-last character.
# STEP 3: Check triplets. If three consecutive characters are identical, increment the respective player's counter.
# STEP 4: Return True if Alice has strictly more moves than Bob.

class Solution:
    def winnerOfGame(self, colors: str) -> bool:
        
        alice_moves = 0
        bob_moves = 0
        
        # We start at index 1 and stop before the last index to safely check i-1 and i+1
        for i in range(1, len(colors) - 1):
            
            # Check if the current piece is identical to both its left and right neighbors
            if colors[i - 1] == colors[i] == colors[i + 1]:
                
                # Assign the valid move to the corresponding player
                if colors[i] == 'A':
                    alice_moves += 1
                else:
                    bob_moves += 1
                    
        # Alice plays first, so she needs strictly greater moves to win
        return alice_moves > bob_moves

"""
WHY EACH PART:
- range(1, len(colors) - 1): Eliminates the need for boundary checks (like `if i > 0 and i < n-1`) inside the loop, making the iteration exceptionally clean and fast.
- colors[i - 1] == colors[i] == colors[i + 1]: Python elegantly supports chained comparisons, resolving the triplet check in a highly readable format.
- alice_moves > bob_moves: If alice_moves == bob_moves, Bob wins because Alice is forced to make the first move and will run out of moves exactly one turn before Bob does.

KEY TECHNIQUE:
- Game Theory Invariants: Recognizing that operations are non-destructive to the opponent's state, converting a simulation problem into a simple linear counting problem.

EDGE CASES:
- String length is 1 or 2 (e.g., "A", "AB"): The loop range is empty. Both counts remain 0. `0 > 0` returns False (Bob wins). Correct, as Alice has no initial moves.
- String with alternating characters (e.g., "ABABAB"): No triplets exist. Returns False. Handled flawlessly.

TIME COMPLEXITY: O(N) - We iterate through the string of length N exactly once.
SPACE COMPLEXITY: O(1) - Only two integer counters are allocated in memory.

CONCEPTS USED:
- Independent Game Theory
- Array/String sliding window (size 3)
- Counting & Invariants
"""
