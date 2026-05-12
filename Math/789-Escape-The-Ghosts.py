# 789. Escape The Ghosts
# Difficulty: Medium
# https://leetcode.com/problems/escape-the-ghosts/

"""
PROBLEM:
You are playing a simplified Pac-Man game. You start at the origin (0, 0), and your destination is target = [target_x, target_y]. 
There are several ghosts on the map, the ith ghost starts at ghosts[i] = [x_i, y_i].
Each turn, you and all ghosts simultaneously *may* move one unit in any of the 4 cardinal directions. 
You escape if and only if you can reach the target before any ghost reaches you (or the target). 
If you reach any square (including the target) at the same time as a ghost, it catches you.
Return true if you can escape, false otherwise.

EXAMPLES:
Input: ghosts = [[1, 0], [0, 3]], target = [0, 1]   → Output: True
Explanation: 
- Your distance to target: |0-0| + |1-0| = 1
- Ghost 1 distance to target: |1-0| + |0-1| = 2
- Ghost 2 distance to target: |0-0| + |3-1| = 2
You are closer to the target than all ghosts. You can just walk to (0, 1) and win.

Input: ghosts = [[1, 0]], target = [2, 0]           → Output: False
Explanation: 
- Your distance to target: 2
- Ghost distance to target: 1
The ghost will reach the target before you and wait for you there.

CONSTRAINTS:
- 1 <= ghosts.length <= 100
- ghosts[i].length == 2
- -10^4 <= x_i, y_i <= 10^4
- target.length == 2
- -10^4 <= target_x, target_y <= 10^4

LOGIC RULES (MANHATTAN DISTANCE):
1. Because movement is strictly orthogonal (no diagonals), the shortest path between any two points is their Manhattan Distance.
2. A ghost does not need to intercept you mid-path. The most optimal strategy for a ghost is to simply walk to the target and wait.
3. Therefore, you can escape IF AND ONLY IF your Manhattan distance to the target is strictly LESS than the Manhattan distance 
   of EVERY ghost to the target.

VISUALIZATION (ghosts = [[2, 0]], target = [1, 0]):
My Position: (0, 0)
Target: (1, 0)
My Manhattan Distance: |1 - 0| + |0 - 0| = 1

Ghost Position: (2, 0)
Ghost Manhattan Distance to Target: |2 - 1| + |0 - 0| = 1

Condition: Is Ghost Dist (1) <= My Dist (1)? Yes.
Conclusion: The ghost reaches the target at the exact same time as me. I lose.
Result: False.
"""

# STEP 1: Calculate the player's Manhattan distance from (0,0) to the target
# STEP 2: Iterate through every ghost in the given list
# STEP 3: Calculate the ghost's Manhattan distance from its current position to the target
# STEP 4: If any ghost is closer to or at the same distance from the target as the player, return False
# STEP 5: If the loop finishes without returning False, the player is strictly closer than all ghosts. Return True.

class Solution:
    def escapeGhosts(self, ghosts: list[list[int]], target: list[int]) -> bool:
        
        # Calculate my distance from (0, 0) to target
        my_dist = abs(target[0]) + abs(target[1])
        
        # Check the distance for each ghost
        for ghost in ghosts:
            
            # Manhattan distance: |x1 - x2| + |y1 - y2|
            ghost_dist = abs(ghost[0] - target[0]) + abs(ghost[1] - target[1])
            
            # If a ghost can reach the target faster or at the same time, we can't escape
            if ghost_dist <= my_dist:
                return False
                
        # If no ghost can beat us to the target, we win!
        return True

"""
WHY EACH PART:
- abs(target[0]) + abs(target[1]): Since the player always starts at (0, 0), the calculation simplifies 
  from abs(target - 0) to just abs(target).
- abs(ghost[0] - target[0]) + abs(ghost[1] - target[1]): Standard Manhattan Distance formula.
- ghost_dist <= my_dist: The `<=` is crucial. If the distances are equal, you arrive at the target 
  simultaneously with the ghost, which means you get caught according to the rules.
- Returning False early inside the loop saves time if we find a winning ghost on the first check.

HOW IT WORKS (Example: ghosts = [[1, 2], [3, 3]], target = [2, 2]):

My Distance: |2 - 0| + |2 - 0| = 4

Iteration 1 (Ghost at [1, 2]):
├── Ghost Dist: |1 - 2| + |2 - 2| = 1 + 0 = 1
├── Is 1 <= 4? Yes!
└── Return False immediately. (The ghost is right next to the target!)

EDGE CASES:
- Target is negative coordinates: `abs()` handles negative coordinates effortlessly. ✓
- Ghosts start ON the target: Ghost distance will be 0. 0 <= my_dist will trigger True, returning False properly. ✓
- 100 ghosts far away: Loop processes very quickly, O(N) operations is tiny for N=100. ✓

TIME COMPLEXITY: O(N)
Where N is the number of ghosts. We iterate through the ghosts array exactly once. 
The math operations inside the loop are O(1) constant time.

SPACE COMPLEXITY: O(1)
We only store two integer variables (`my_dist` and `ghost_dist`). No additional data structures are created, 
so memory usage is perfectly flat and constant.
"""
