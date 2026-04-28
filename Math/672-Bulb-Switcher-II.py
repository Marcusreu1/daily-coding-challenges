# 672. Bulb Switcher II
# Difficulty: Medium
# https://leetcode.com/problems/bulb-switcher-ii/

"""
PROBLEM:
There is a room with n bulbs labeled from 1 to n that all are turned on initially, and 4 buttons on the wall. 
Each of the 4 buttons has a different functionality:
1. Flips the status of all the bulbs.
2. Flips the status of all the bulbs with even labels (i.e., 2, 4, 6, ...).
3. Flips the status of all the bulbs with odd labels (i.e., 1, 3, 5, ...).
4. Flips the status of all the bulbs with a label j = 3k + 1 where k = 0, 1, 2, ... (i.e., 1, 4, 7, 10, ...).

Given two integers n and presses, return the number of different possible statuses after performing all button presses.

EXAMPLES:
Input: n = 1, presses = 1   → Output: 2 (Status can be: [off] or [on])
Input: n = 2, presses = 1   → Output: 3 (Status can be: [off, off], [on, off], [off, on])
Input: n = 3, presses = 1   → Output: 4 (Status can be: [off, off, off], [off, on, off], [on, off, on], [off, off, on])

CONSTRAINTS:
- 1 <= n <= 1000
- 0 <= presses <= 1000

LOGIC RULES (STATE REDUCTION):
1. Pressing a button twice is equivalent to not pressing it at all.
2. Pressing Button 1 is equivalent to pressing Button 2 and Button 3 together.
3. The state of the bulbs repeats every 6 bulbs. Thus, observing the first 3 bulbs is enough to distinguish all unique states.
4. Maximum possible unique states for ANY number of bulbs and presses is exactly 8.

VISUALIZATION (Max States logic):
Button combinations yield at most 8 states.
If n >= 3:
- presses = 0: 1 state (All ON)
- presses = 1: 4 states (Press B1, B2, B3, or B4)
- presses = 2: 7 states (Combinations of 2 buttons. Cannot reach the 8th state which requires 3 independent button presses)
- presses >= 3: 8 states (All possible mathematical states unlocked)
"""

# STEP 1: Handle the zero presses edge case immediately
# STEP 2: Handle the case where we only have 1 bulb
# STEP 3: Handle the case where we have exactly 2 bulbs depending on the presses
# STEP 4: Handle the case for 3 or more bulbs (the maximum threshold)

class Solution:
    def flipLights(self, n: int, presses: int) -> int:
        
        if presses == 0:                                             # No buttons pressed
            return 1                                                 # Only 1 state (All On)
            
        if n == 1:                                                   # Only 1 bulb exists
            return 2                                                 # Can only be On or Off
            
        if n == 2:                                                   # Exactly 2 bulbs exist
            if presses == 1:
                return 3                                             # 1 press yields 3 distinct states
            else:
                return 4                                             # 2 or more presses hit the max of 4 states
                
        # If n >= 3 (3 or more bulbs)
        if presses == 1:
            return 4                                                 # 1 press = 4 distinct buttons = 4 states
        elif presses == 2:
            return 7                                                 # 2 presses unlock 7 distinct combinations
        else:
            return 8                                                 # 3+ presses unlock the absolute max of 8 states

"""
WHY EACH PART:
- if presses == 0: Base condition. Without interaction, the system remains in its initial state.
- if n == 1: B1, B3, and B4 all flip Bulb 1. B2 does nothing. The bulb flips or it doesn't -> 2 states.
- if n == 2: B4 acts the same as B3 for the first two bulbs. B1 flips both. B2 flips bulb 2. B3 flips bulb 1.
  This creates 4 maximum mathematical states. A single press can only reach 3 of them.
- return 8: Because B1 = B2 + B3, the buttons are linearly dependent. We effectively have 3 independent variables,
  so 2^3 = 8 maximum states, regardless of how large 'n' is.

HOW IT WORKS (Example: n = 3, presses = 1):

Initial state: [ON, ON, ON]
Since presses = 1, we must press exactly one button:
├── Press B1 (All): [OFF, OFF, OFF]
├── Press B2 (Even): [ON, OFF, ON]
├── Press B3 (Odd): [OFF, ON, OFF]
└── Press B4 (3k+1): [OFF, ON, ON]

Result: We generated exactly 4 distinct states. Returns 4. ✓

EDGE CASES:
- n = 1000, presses = 1000: Bypasses heavy simulation, falls into `n >= 3` and `presses >= 3`, returns 8 instantly. ✓
- presses = 0: Returns 1 (initial state). ✓

TIME COMPLEXITY: O(1) 
This is a pure math/logic deduction. We are just evaluating constant conditions. 
There are no loops or recursions.

SPACE COMPLEXITY: O(1) 
No auxiliary data structures (like arrays, lists, or hash maps) are created. 
Memory footprint is constant.
"""
