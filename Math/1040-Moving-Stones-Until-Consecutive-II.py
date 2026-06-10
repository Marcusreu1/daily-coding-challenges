# 1040. Moving Stones Until Consecutive II
# Difficulty: Medium
# https://leetcode.com/problems/moving-stones-until-consecutive-ii/

"""
PROBLEM:
There are some stones in different positions on the X-axis. You are given an integer array `stones`, the positions of the stones.
Call a stone an endpoint stone if it has the smallest or largest position. In one move, you pick up an endpoint stone and move it to an unoccupied position so that it is no longer an endpoint stone.
In particular, if the stones are at say, `stones = [1,2,5]`, you cannot move the endpoint stone at position 5, since moving it to any position (such as 0, or 3) will still keep that stone as an endpoint stone.
The game ends when you cannot make any more moves, i.e., the stones are in consecutive positions.
Return an integer array `answer` of length 2 where:
- answer[0] is the minimum number of moves you can play.
- answer[1] is the maximum number of moves you can play.

EXAMPLES:
Input: stones = [7,4,9]
Output: [1,2]
(Sort to [4,7,9]. Min: move 9 to 5 or 6 (1 move). Max: move 4 to 8, then 9 to 5 (2 moves)).

Input: stones = [6,5,4,3,10]
Output: [2,3]
(Min: Move 3 to 8, then 10 to 7. Max: Move 3 to 7, 4 to 8, 5 to 9 (3 moves)).

CONSTRAINTS:
- 3 <= stones.length <= 10^4
- 1 <= stones[i] <= 10^9
- All values of stones are unique.

MATHEMATICAL REDUCTION:
Step 1: Sort the array to process stones sequentially.

MAXIMUM MOVES:
When we make our first move, we must abandon all empty spaces between the moved endpoint and its nearest neighbor. We can either lose the spaces between `stones[0]` and `stones[1]`, or between `stones[n-2]` and `stones[n-1]`. To maximize moves, we discard the smaller gap and collect all remaining spaces.
Max moves = Total empty spaces - Min(left_gap, right_gap)

MINIMUM MOVES:
We use a Sliding Window of maximum length `n`. We want to find a window that already contains the most stones. The empty slots in this window equal the number of moves needed to bring the outside stones in.
Moves = n - stones_in_window
EDGE CASE: If we have exactly n-1 contiguous stones and 1 outlier (e.g., [1,2,3,4, 10]), the math says 1 move. However, moving the outlier directly to the edge of the block is illegal because it violates the "must land strictly between endpoints" rule. We are forced to make exactly 2 moves (leapfrog one contiguous stone out, then bring the outlier in).

VISUALIZATION (stones = [1, 2, 3, 4, 10]):
Sort: [1, 2, 3, 4, 10]
n = 5

Max Moves calculation:
Spaces if we drop left gap (1 to 2): (10 - 2 + 1) - 4 = 5 spaces.
Spaces if we drop right gap (4 to 10): (4 - 1 + 1) - 4 = 0 spaces.
Max moves = max(5, 0) = 5.

Min Moves calculation (Sliding Window):
Window covers [1, 2, 3, 4]. Size = 4, length = 4.
This triggers the edge case: n-1 stones are perfectly contiguous.
Moves = 2.

Result: [2, 5] ✓
"""

# STEP 1: Sort the array to ensure spatial order.
# STEP 2: Calculate max_moves by measuring total spaces and dropping the smallest extreme gap.
# STEP 3: Use a sliding window (pointers i and j) to find the densest window of size <= n.
# STEP 4: Calculate min_moves dynamically, catching the specific n-1 contiguous edge case.
# STEP 5: Return the array containing [min_moves, max_moves].

class Solution:
    def numMovesStonesII(self, stones: list[int]) -> list[int]:
        
        stones.sort()                                                          # Sort stones sequentially
        n = len(stones)
        
        # Calculate maximum moves
        # Total spaces from index 1 to n-1: stones[n-1] - stones[1] - (n - 2)
        # Total spaces from index 0 to n-2: stones[n-2] - stones[0] - (n - 2)
        right_gap_spaces = stones[n-1] - stones[1] - n + 2
        left_gap_spaces = stones[n-2] - stones[0] - n + 2
        max_moves = max(right_gap_spaces, left_gap_spaces)
        
        # Calculate minimum moves using sliding window
        min_moves = n                                                          # Worst-case scenario
        i = 0                                                                  # Left pointer of the window
        
        for j in range(n):                                                     # Right pointer expands the window
            
            # If the current window size physically exceeds 'n', shrink it from the left
            while stones[j] - stones[i] >= n:
                i += 1
                
            window_stone_count = j - i + 1                                     # How many stones are inside our window
            
            # Edge Case: We have n-1 stones packed together, and 1 stone far away
            if window_stone_count == n - 1 and stones[j] - stones[i] == n - 2:
                min_moves = min(min_moves, 2)                                  # Forced into a 2-step hop
            else:
                # Normal Case: Moves needed = empty slots in the window
                min_moves = min(min_moves, n - window_stone_count)
                
        return [min_moves, max_moves]                                          # Return answers

"""
WHY EACH PART:
- max_moves = max(...): By evaluating both scenarios (abandoning the left vs abandoning the right), we guarantee we are capturing the maximum amount of "1-step" moves possible in the middle of the array.
- while stones[j] - stones[i] >= n: The physical span of our target consecutive group is `n`. If the distance between the two ends of our window is `n` or greater, we can't fit all these stones into a consecutive block. We must advance `i` to shrink the window.
- if window_stone_count == n - 1 and stones[j] - stones[i] == n - 2: The condition `stones[j] - stones[i] == n - 2` means the distance between the first and last stone in the window is exactly the number of gaps for n-1 stones. This mathematically proves there are zero holes in this specific block.

HOW IT WORKS (Example: [7, 4, 9]):

Initial State:
├── Unsorted: [7, 4, 9]
├── Sorted: [4, 7, 9]
└── n = 3

Max Moves:
├── right_gap_spaces = 9 - 7 - 3 + 2 = 1
├── left_gap_spaces = 7 - 4 - 3 + 2 = 2
└── max_moves = max(1, 2) = 2

Min Moves (Sliding Window):
Iteration 1 (j=0, i=0): window=[4], count=1, min_moves=min(3, 3-1) = 2
Iteration 2 (j=1, i=0): window=[4,7], dist=3 (>=3), i moves to 1. window=[7], count=1, min_moves=2
Iteration 3 (j=2, i=1): window=[7,9], dist=2 (<3), count=2. 
├── Is edge case? 2 == 2 AND 9-7 == 1? No (2!=1).
├── min_moves = min(2, 3-2) = 1

Exit:
return [1, 2] ✓

KEY TECHNIQUE:
- Two Pointers / Sliding Window + Greedy Strategy. 
The problem uniquely marries two optimal strategies. Greedy determines the worst-case path (max moves) by dropping the minimal bottleneck, while the Sliding Window identifies the optimal center of mass to pull the array together with minimum effort.

EDGE CASES:
- Array already consecutive (e.g., [1,2,3,4]): Both gap equations yield 0. Max moves = 0. Window encompasses all elements. Count = n, moves = n-n = 0. Returns [0, 0]. ✓
- Trailing outlier (e.g., [1,2,3, 100]): Left gap spaces yields huge number. Max moves scales perfectly. Window catches [1,2,3] and hits the edge case constraint. Returns [2, 96]. ✓

TIME COMPLEXITY: O(N log N) - We must sort the array first. The sliding window passes over the array in exactly O(N) time because the `i` pointer only ever moves forward.
SPACE COMPLEXITY: O(1) or O(N) - Depends on the language's sorting algorithm (Timsort in Python uses up to O(N) auxiliary space). The logic itself only uses primitive integer variables.

CONCEPTS USED:
- Arrays
- Sorting
- Two Pointers / Sliding Window
- Greedy Algorithms
"""
