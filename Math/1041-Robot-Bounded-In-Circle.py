# 1041. Robot Bounded In Circle
# Difficulty: Medium
# https://leetcode.com/problems/robot-bounded-in-circle/

"""
PROBLEM:
On an infinite plane, a robot initially stands at (0, 0) and faces north.
The robot can receive a sequence of instructions: 'G' (go straight), 'L' (turn left 90 degrees), 
and 'R' (turn right 90 degrees). The robot repeats these instructions forever.
Return true if and only if there exists a circle in the plane such that the robot never leaves the circle.

EXAMPLES:
Input: instructions = "GGLLGG"   → Output: true (Returns to origin after 1 cycle)
Input: instructions = "GG"       → Output: false (Goes infinitely North)
Input: instructions = "GL"       → Output: true (Forms a square, returns to origin after 4 cycles)

CONSTRAINTS:
- 1 <= instructions.length <= 100
- instructions[i] is 'G', 'L' or, 'R'.

MATHEMATICAL INTUITION (THE "TRICK"):
A robot will remain bounded in a circle if, after executing exactly ONE sequence of instructions, either:
1. It returns to the starting origin (x = 0, y = 0).
2. It changes its facing direction (it is NO LONGER facing North).
   - Why? Because if it faces South, the second cycle will cancel out the displacement of the first, bringing it back to (0,0).
   - If it faces East or West, it will trace a square over 4 cycles and return to (0,0).
If it ends up in a different position BUT still faces North, it will continue drifting infinitely.

VISUALIZATION (instructions="GL"):
Start: (0,0) facing North ↑
'G': Moves to (0,1) facing North ↑
'L': Stays at (0,1) facing West ←
End of Cycle 1: (0,1) facing West. 
Since direction changed, it WILL loop!
Cycle 2 ("GL"): Move West to (-1,1), face South ↓
Cycle 3 ("GL"): Move South to (-1,0), face East →
Cycle 4 ("GL"): Move East to (0,0), face North ↑ (Back to start!)
"""

# STEP 1: Define directional vectors (North, East, South, West) in clockwise order.
# STEP 2: Initialize the starting position (x=0, y=0) and direction index (0 = North).
# STEP 3: Iterate through each instruction.
# STEP 4: If 'L' or 'R', update direction using modulo arithmetic.
# STEP 5: If 'G', update x and y coordinates using the current direction vector.
# STEP 6: After the loop, check the bounded conditions (at origin OR not facing North).

class Solution:
    def isRobotBounded(self, instructions: str) -> bool:
        
        # Directions: North, East, South, West (Clockwise)
        # (dx, dy) changes for Cartesian plane
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        x = 0                                            # Current X coordinate
        y = 0                                            # Current Y coordinate
        idx = 0                                          # Current direction (0 = North)
        
        for instruction in instructions:                 # Process sequence once
            
            if instruction == 'G':                       # Move forward
                x += directions[idx][0]                  # Add dx
                y += directions[idx][1]                  # Add dy
                
            elif instruction == 'L':                     # Turn Left (Counter-clockwise)
                idx = (idx + 3) % 4                      # +3 is same as -1 in modulo 4
                
            elif instruction == 'R':                     # Turn Right (Clockwise)
                idx = (idx + 1) % 4                      # Move to next direction
                
        # Return True if at origin OR direction changed (not North)
        return (x == 0 and y == 0) or idx != 0

"""
WHY EACH PART:
- directions array: Maps the direction index to coordinate changes. Ordered clockwise to make turning math easy.
- idx = (idx + 3) % 4: Turning left means moving backwards in our array. To avoid negative numbers, adding 3 in mod 4 is mathematically equivalent to subtracting 1.
- idx = (idx + 1) % 4: Turning right means moving forward one index.
- (x == 0 and y == 0) or idx != 0: The core mathematical proof. It saves us from simulating multiple loops.

HOW IT WORKS (Example: "GL"):

Initial: x=0, y=0, idx=0 (North)

Iteration 1 (instruction='G'):
├── directions[0] = (0, 1)
├── x = 0 + 0 = 0
└── y = 0 + 1 = 1

Iteration 2 (instruction='L'):
├── idx = (0 + 3) % 4 = 3 (Now facing West)

Exit Loop: x=0, y=1, idx=3

Condition Check:
├── (x == 0 and y == 0) -> False (0 == 0 and 1 == 0 is False)
├── idx != 0 -> True (3 != 0 is True)
└── False or True -> True
return True ✓

KEY TECHNIQUE:
- Vector Mapping: Representing spatial directions as coordinate pairs in an array.
- Cycle Detection via State Check: Deductive reasoning to predict infinite loops based on a single cycle's end state (Position + Direction).
- Circular Array / Modulo Arithmetic: Elegant handling of compass directions without writing messy nested if/else statements.

EDGE CASES:
- Only turns ("LLLL"): Returns True (Stays at origin, cycles naturally) ✓
- Returns to start facing North ("GGLLGG"): Returns True (First condition met) ✓
- Goes straight infinitely ("G"): Returns False (Moves away, still faces North) ✓
- Loops after multiple cycles ("GL"): Returns True (Second condition met) ✓

TIME COMPLEXITY: O(N) - Where N is the length of the string. We iterate through the instructions exactly once.
SPACE COMPLEXITY: O(1) - We only store a fixed array of 4 directions and three integer variables (x, y, idx).

CONCEPTS USED:
- Simulation
- Cartesian Geometry (Vector displacement)
- Modulo Arithmetic
- State Machine
"""
