# 1401. Circle and Rectangle Overlapping
# Difficulty: Medium
# https://leetcode.com/problems/circle-and-rectangle-overlapping/

"""
PROBLEM:
You are given a circle represented as (radius, xCenter, yCenter) and an axis-aligned 
rectangle represented as (x1, y1, x2, y2), where (x1, y1) are the coordinates of the 
bottom-left corner, and (x2, y2) are the coordinates of the top-right corner of the rectangle.
Return true if the circle and rectangle are overlapped otherwise return false. 
In other words, check if there is any point (xi, yi) that belongs to the circle and the 
rectangle at the same time.

EXAMPLES:
Input: radius = 1, xCenter = 0, yCenter = 0, x1 = 1, y1 = -1, x2 = 3, y2 = 1
Output: True
(Explanation: The circle and rectangle share the exact point (1,0).)

Input: radius = 1, xCenter = 1, yCenter = 1, x1 = 1, y1 = -3, x2 = 2, y2 = -1
Output: False
(Explanation: The circle is strictly above the rectangle and they do not share any points.)

Input: radius = 1, xCenter = 0, yCenter = 0, x1 = -1, y1 = 0, x2 = 0, y2 = 1
Output: True

CONSTRAINTS:
- 1 <= radius <= 2000
- -10^4 <= xCenter, yCenter <= 10^4
- -10^4 <= x1 < x2 <= 10^4
- -10^4 <= y1 < y2 <= 10^4

ALGORITHM LOGIC (Geometry & Clamping):
1. Instead of checking complex intersection boundaries, we just need to find the single 
   point on the rectangle that is algebraically CLOSEST to the circle's center.
2. We find this point using a technique called "Clamping". We constrain the circle's 
   x-coordinate to fall within the boundaries of [x1, x2]. 
   Formula: closest_x = max(x1, min(xCenter, x2))
3. We do the exact same clamping for the y-coordinate using [y1, y2].
4. Now we possess (closest_x, closest_y), which is the absolute closest point on (or inside) 
   the rectangle to our circle's center.
5. We calculate the Pythagorean distance between the circle's center and this closest point.
6. If this distance is less than or equal to the circle's radius, they overlap.
7. Optimization: Instead of using square roots (which introduce floating-point inaccuracies), 
   we compare squared distance against squared radius (d^2 <= r^2).

VISUALIZATION (radius=1, xCenter=0, yCenter=0 | Rect: x1=1, y1=-1, x2=3, y2=1):
Center of circle is at (0, 0).
Clamp X: min(0, 3) = 0. max(1, 0) = 1. -> closest_x = 1
Clamp Y: min(0, 1) = 0. max(-1, 0) = 0. -> closest_y = 0
Closest point on rect to the circle is (1, 0).

Distance X: 0 - 1 = -1
Distance Y: 0 - 0 = 0
Squared distance = (-1)^2 + (0)^2 = 1 + 0 = 1
Radius squared = 1^2 = 1
1 <= 1 ? True! They overlap on the edge. ✓
"""

# STEP 1: Find the closest X point on the rectangle to the circle's center using clamping
# STEP 2: Find the closest Y point on the rectangle to the circle's center using clamping
# STEP 3: Calculate the delta differences in X and Y
# STEP 4: Compare the sum of squared distances to the squared radius. Return the boolean.

class Solution:
    def checkOverlap(self, radius: int, xCenter: int, yCenter: int, x1: int, y1: int, x2: int, y2: int) -> bool:
        
        # Clamp the circle's center coordinates to the rectangle's boundaries
        closest_x = max(x1, min(xCenter, x2))
        closest_y = max(y1, min(yCenter, y2))
        
        # Calculate horizontal and vertical distances from the center to the closest point
        distance_x = xCenter - closest_x
        distance_y = yCenter - closest_y
        
        # Pythagorean theorem avoiding math.sqrt() to maintain strict integer precision
        return (distance_x ** 2) + (distance_y ** 2) <= radius ** 2

"""
WHY EACH PART:
- max(x1, min(...)): This effectively restricts a value. If `xCenter` is greater than `x2`, `min()` forces it to `x2`. If it's smaller than `x1`, `max()` forces it up to `x1`. If it's in between, both allow it to pass through unharmed.
- (distance_x ** 2): Calculating the squares keeps the data type as purely integers. This completely circumvents floating-point truncation issues that plague geometry algorithms in computational environments.
- <= radius ** 2: The `<=` is crucial because if the distance perfectly matches the radius, the circle and rectangle are touching exactly on the boundary, which counts as an overlap according to the problem.

HOW IT WORKS (Example: Circle strictly inside the rectangle):
xCenter=5, yCenter=5, radius=2
Rect: x1=0, y1=0, x2=10, y2=10

closest_x = max(0, min(5, 10)) -> 5
closest_y = max(0, min(5, 10)) -> 5
distance_x = 5 - 5 = 0
distance_y = 5 - 5 = 0
Squared dist = 0. 0 <= 4 ? True. Overlaps! ✓

KEY TECHNIQUE:
- Computational Geometry (Clamping)
- Math (Pythagorean theorem with squared values)

EDGE CASES:
- Tangent edge touch: Handled correctly via `<=`. ✓
- Circle completely swallows the rectangle: The clamped point will just be a corner of the rectangle, and the distance will still be evaluated correctly as less than the radius. ✓
- Negative coordinates: The `min/max` logic behaves identically and perfectly on the negative axis. ✓

TIME COMPLEXITY: O(1) - The algorithm purely resolves 5 basic arithmetic expressions. It executes in strictly constant time.
SPACE COMPLEXITY: O(1) - Only minimal tracking variables (`closest_x`, `closest_y`, `distance_x`, `distance_y`) are allocated.
"""
