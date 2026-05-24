# 858. Mirror Reflection
# Difficulty: Medium
# https://leetcode.com/problems/mirror-reflection/

"""
PROBLEM:
There is a special square room with mirrors on each of the 4 walls. Except for the southwest corner, 
there are receptors on each of the remaining corners, numbered 0, 1, and 2.
The square room has walls of length `p`, and a laser ray from the southwest corner 
first meets the east wall at a distance `q` from the 0th receptor.
Given the two integers `p` and `q`, return the number of the receptor that the ray meets first.
The test cases are guaranteed so that the ray will meet a receptor eventually.

CORNERS:
- Southwest (SW): Origin (Laser starting point)
- Southeast (SE): Receptor 0
- Northeast (NE): Receptor 1
- Northwest (NW): Receptor 2

EXAMPLES:
Input: p = 2, q = 1
Output: 2
Explanation: The ray meets receptor 2 the first time it gets reflected back to the left wall.

CONSTRAINTS:
- 1 <= q <= p <= 1000

MATHEMATICAL REFLECTION (UNFOLDING) RULES:
Instead of simulating reflections, imagine expanding the room into a grid of identical rooms. 
The laser simply travels in a continuous straight line. 
It hits a receptor when it reaches a coordinate (x, y) where both x and y are multiples of p.
- x = m * p (m is the number of room widths crossed)
- y = n * p (n is the number of room heights crossed)

By simplifying the ratio of p and q by dividing out their greatest common divisor (GCD), 
we determine the parity (even/odd) of the room coordinates:
- If p is EVEN and q is ODD: Lands on Top-Left (Receptor 2)
- If p is ODD and q is ODD: Lands on Top-Right (Receptor 1)
- If p is ODD and q is EVEN: Lands on Bottom-Right (Receptor 0)
- (p EVEN and q EVEN is impossible after reducing the fraction)

VISUALIZATION (Parity Grid):
    (Even p)     (Odd p)
      Left        Right
    ┌──────────┬──────────┐
    │ Rec 2    │ Rec 1    │ Top (Odd q)
    ├──────────┼──────────┤
    │ Origin   │ Rec 0    │ Bottom (Even q)
    └──────────┴──────────┘
"""

# STEP 1: Simplify the ratio of p and q by dividing by 2 as long as both are even
# STEP 2: This is equivalent to dividing by their greatest common divisor until one is odd
# STEP 3: Check the parity of the simplified p and q
# STEP 4: If p is even, it hit the left wall (Receptor 2)
# STEP 5: If q is even, it hit the bottom wall (Receptor 0)
# STEP 6: If both are odd, it hit the top right corner (Receptor 1)

class Solution:
    def mirrorReflection(self, p: int, q: int) -> int:
        
        # Reduce p and q to their simplest parity form by removing common factors of 2
        while p % 2 == 0 and q % 2 == 0:
            p //= 2
            q //= 2
            
        # Evaluate parity to determine the destination corner
        if p % 2 == 0:
            return 2       # Even horizontal (Left), Odd vertical (Top)
        elif q % 2 == 0:
            return 0       # Odd horizontal (Right), Even vertical (Bottom)
        else:
            return 1       # Odd horizontal (Right), Odd vertical (Top)

"""
WHY EACH PART:
- while p % 2 == 0 and q % 2 == 0: We only care about the parity (odd/even nature) of the grid coordinates where the laser lands. Dividing both by 2 is functionally simplifying the fraction p/q until we hit our first odd number.
- p % 2 == 0: If the simplified p is even, it means the laser traveled an even number of rooms horizontally, bringing it back to the left side of the grid.
- q % 2 == 0: If the simplified q is even, it means the laser traveled an even number of rooms vertically, bringing it back to the bottom of the grid.

HOW IT WORKS (Example: p=2, q=1):
Initial: p=2, q=1
├── Loop: q is odd (1 % 2 != 0), so the while loop is skipped.
├── Parity check: p is even (2 % 2 == 0).
└── Returns 2. 
Conceptually: The laser travels 2 units horizontally (1 room width) and 1 unit vertically (half a room height). To hit a corner, it must travel 2 full room widths (x=4) to achieve 1 full room height (y=2). Thus, it crosses an EVEN number of horizontal rooms and an ODD number of vertical rooms, landing at the top-left (Receptor 2).

KEY TECHNIQUE:
- "Unfolding" or "Mirror Expansion": A classic competitive programming geometry trick. Converting a reflection problem inside a bounded box into a linear trajectory problem on an infinite grid.
- Fraction simplification / Parity matching: Reducing the geometrical problem to a simple odd/even state machine.

EDGE CASES:
- Laser hitting exactly in one reflection: Handled perfectly without needing to track bounces.
- Large constraints: Since p, q <= 1000, the bitwise-equivalent shifts (division by 2) run in near-instantaneous time.

TIME COMPLEXITY: O(log(max(p, q))) - In the worst case, we are dividing by 2 repeatedly, which is logarithmic time. Exceptionally fast.
SPACE COMPLEXITY: O(1) - Only modifying the given integer variables, no extra memory used.

CONCEPTS USED:
- Analytical Geometry
- Number Theory (Parity and GCD)
- Simulation via Unfolding
"""
