# 2139. Minimum Moves to Reach Target Score
# Difficulty: Medium
# https://leetcode.com/problems/minimum-moves-to-reach-target-score/

"""
PROBLEM:
You are playing a game with integers. You start at the integer 1 and you want to reach the integer target.
In one move, you can:
- Increment the current integer by 1 (curr = curr + 1).
- Double the current integer (curr = 2 * curr). You can use this operation at most maxDoubles times.
Given the two integers target and maxDoubles, return the minimum number of moves needed to reach target.

EXAMPLES:
Input: target = 5, maxDoubles = 0 → Output: 4
Explanation: Keep incrementing by 1: 1 -> 2 -> 3 -> 4 -> 5 (4 moves).

Input: target = 19, maxDoubles = 2 → Output: 7
Explanation: 
Reverse sequence: 19 -> 18 -> 9 -> 8 -> 4 -> 2 -> 1.
Total = 7 moves.

Input: target = 10, maxDoubles = 4 → Output: 4
Explanation:
Reverse sequence: 10 -> 5 -> 4 -> 2 -> 1.
Total = 4 moves.

CONSTRAINTS:
- 1 <= target <= 10^9
- 0 <= maxDoubles <= 100

MATH RULES (REVERSE GREEDY & O(1) SHORT-CIRCUITING):
Forward search (1 -> target) has branching factor ambiguity: when to double vs increment.
Working backwards (target -> 1) is completely deterministic:
1. If the current number is odd, it CANNOT be produced by doubling. The previous move MUST have been an increment.
   Therefore, we must decrement: target -= 1. (1 move).
2. If the current number is even and we have doubles available, halving it (target //= 2) cuts the search space by 50% in a single operation.
   Greedily, this always beats decrementing by 1.
3. Once maxDoubles == 0, no more divisions are possible. To reach 1 from the current target strictly using decrements,
   it takes exactly (target - 1) moves. We can add this directly in O(1) and break out.
"""

# STEP 1: Initialize a counter for total moves made.
# STEP 2: Loop while target is strictly greater than 1.
# STEP 3: If maxDoubles is 0, add (target - 1) directly to moves and break.
# STEP 4: If target is odd, decrement by 1 and increment moves.
# STEP 5: If target is even and maxDoubles > 0, divide target by 2, decrement maxDoubles, and increment moves.
# STEP 6: Return the accumulated moves.

class Solution:
    def minMoves(self, target: int, maxDoubles: int) -> int:
        
        moves = 0
        
        while target > 1:
            # If no doubles are left, we must decrement 1 step at a time to reach 1
            if maxDoubles == 0:
                moves += target - 1
                break
                
            # If target is odd, we must have arrived here via addition (+1)
            if target % 2 != 0:
                target -= 1
                moves += 1
            else:
                # If target is even, greedily divide by 2
                target //= 2
                maxDoubles -= 1
                moves += 1
                
        return moves

"""
WHY EACH PART:
- target > 1: The terminal target is 1. When target reaches 1, zero additional moves are needed.
- if maxDoubles == 0: moves += target - 1: Bypasses potentially up to 10^9 loop iterations when out of doubles. Reduces worst-case time to O(1) from that point forward.
- target //= 2: Uses integer floor division to keep values strictly as standard integers, avoiding floating-point precision overhead.

KEY TECHNIQUE:
- Working Backwards: Removing combinatorial branching by reversing the timeline.
- Greedy Choice Property: Halving an even number always saves at least as many or more moves than decrementing.

EDGE CASES:
- target = 1: The loop condition `target > 1` is immediately False. Returns 0 moves. Correct.
- maxDoubles = 0 initially: The first check triggers immediately: `moves += target - 1`, break. Runs in O(1) time.

TIME COMPLEXITY: O(min(log(target), maxDoubles)) - Halving reduces target exponentially. In the worst case, halving takes at most ~30 steps (since 2^30 > 10^9). Once doubles run out, the remaining distance is computed in O(1).
SPACE COMPLEXITY: O(1) - Only scalar integer variables are allocated.

CONCEPTS USED:
- Greedy Algorithms
- Invariant & Backward Analysis
- Arithmetic Optimization
"""
