# 780. Reaching Points
# Difficulty: Hard
# https://leetcode.com/problems/reaching-points/

"""
PROBLEM:
Given four integers sx, sy, tx, and ty, return true if it is possible to convert the point (sx, sy) 
to the point (tx, ty) through some operations, or false otherwise.
The allowed operation on some point (x, y) is to convert it to either (x, x + y) or (x + y, y).

EXAMPLES:
Input: sx = 1, sy = 1, tx = 3, ty = 5   → Output: True
Explanation: (1, 1) -> (1, 2) -> (3, 2) -> (3, 5)

Input: sx = 1, sy = 1, tx = 2, ty = 2   → Output: False
Explanation: (1,1) -> (1,2) or (2,1). Neither can reach (2,2).

CONSTRAINTS:
- 1 <= sx, sy, tx, ty <= 10^9

LOGIC RULES (WORKING BACKWARDS & MODULO):
1. Working forwards creates a binary tree of paths (O(2^N)), which leads to Time Limit Exceeded.
2. Working backwards from (tx, ty) is deterministic. If tx > ty, the previous state MUST have been (tx - ty, ty).
3. Repeated subtractions (tx - ty - ty - ty...) can be heavily optimized using the Modulo operator (tx % ty).
4. Once one of the target coordinates matches the start coordinate, we just verify if the remaining gap 
   can be bridged by repeatedly adding the other coordinate.

VISUALIZATION (sx=1, sy=1, tx=3, ty=5):
Start backwards from Target (3, 5):
- Since 5 > 3: The previous move MUST have been changing Y. 
  Instead of doing 5 - 3 = 2, we use modulo: 5 % 3 = 2.
  New Target = (3, 2)

- Since 3 > 2: The previous move MUST have been changing X.
  Modulo: 3 % 2 = 1.
  New Target = (1, 2)

Now tx (1) matches sx (1). The loop stops.
- Check Y: Can we reach ty=2 from sy=1 by adding sx=1?
  (2 - 1) % 1 == 0 -> 1 % 1 == 0 -> True.
Result: True ✓
"""

# STEP 1: Loop while target coordinates are strictly greater than start coordinates
# STEP 2: Use modulo to simulate multiple reverse operations in O(1) time
# STEP 3: Handle the breakout condition if tx reaches sx
# STEP 4: Handle the breakout condition if ty reaches sy

class Solution:
    def reachingPoints(self, sx: int, sy: int, tx: int, ty: int) -> bool:
        
        # Work backwards from the target until we hit or pass the start boundaries
        while tx > sx and ty > sy:
            if tx > ty:
                tx %= ty                                     # Simulate repeated subtractions of ty from tx
            else:
                ty %= tx                                     # Simulate repeated subtractions of tx from ty
                
        # If we successfully aligned the X coordinate
        if tx == sx and ty >= sy:
            return (ty - sy) % sx == 0                       # Check if the remaining Y gap is a multiple of X
            
        # If we successfully aligned the Y coordinate
        if ty == sy and tx >= sx:
            return (tx - sx) % sy == 0                       # Check if the remaining X gap is a multiple of Y
            
        return False                                         # If neither aligned properly, it's unreachable

"""
WHY EACH PART:
- while tx > sx and ty > sy: We strictly use > instead of >= to prevent the modulo operation 
  from reducing a coordinate to 0 or below the starting point prematurely.
- tx %= ty: This is the magic shortcut. Instead of `tx -= ty` running potentially millions of times 
  (e.g., target 1,000,000,000 and 1), modulo jumps directly to the remainder.
- (ty - sy) % sx == 0: Once X matches, the only allowed operation left is adding X to Y. 
  Therefore, the distance between current Y and target Y must be perfectly divisible by X.

HOW IT WORKS (Example: sx=1, sy=1, tx=1000000000, ty=1):

Initial check: tx (1,000,000,000) > sx (1). But ty (1) is NOT > sy (1). 
The while loop is skipped entirely!

Checks below the loop:
├── tx == sx (1000000000 == 1)? False.
├── ty == sy (1 == 1) AND tx >= sx (1000000000 >= 1)? TRUE!
    ├── Return (1000000000 - 1) % 1 == 0
    ├── 999999999 % 1 == 0 -> True.

Returns True in O(1) time instead of 1 billion loops! ✓

EDGE CASES:
- Target is exactly the start (sx=tx, sy=ty): Bypasses the loop, passes the alignment check -> returns True. ✓
- Unreachable path (tx=2, ty=2 from sx=1, sy=1): Loop skipped. tx != sx and ty != sy -> returns False. ✓
- Same X and Y initially (e.g., tx=5, ty=5): Modulo results in 0, breaks loop, returns False properly. ✓

TIME COMPLEXITY: O(log(max(tx, ty)))
The modulo operation acts similarly to the Euclidean algorithm for finding the Greatest Common Divisor (GCD). 
In the worst case (Fibonacci sequence numbers), it takes logarithmic time.

SPACE COMPLEXITY: O(1)
We are only modifying the input variables directly. No extra memory is allocated.
"""
