# 1266. Minimum Time Visiting All Points
# Difficulty: Easy
# https://leetcode.com/problems/minimum-time-visiting-all-points/

"""
PROBLEM:
On a 2D plane, there are n points with integer coordinates points[i] = [xi, yi]. 
Return the minimum time in seconds to visit all the points in the order given by points.
You can move according to these rules:
- In 1 second, you can either:
  - move vertically by one unit,
  - move horizontally by one unit, or
  - move diagonally sqrt(2) units (in other words, move one unit vertically then 
    one unit horizontally in 1 second).
- You have to visit the points in the same order as they appear in the array.
- You are allowed to pass through points that appear later in the order, but these 
  do not count as visits.

EXAMPLES:
Input: points = [[1,1],[3,4],[-1,0]]
Output: 7
(Explanation: 
From [1,1] to [3,4]: 
- Move diagonally 2 steps to [3,3] (takes 2 seconds)
- Move vertically 1 step to [3,4] (takes 1 second)
Total time = 3 seconds.
From [3,4] to [-1,0]: 
- Move diagonally 4 steps to [-1,0] (takes 4 seconds)
Total time = 4 seconds.
Overall time = 3 + 4 = 7 seconds.)

Input: points = [[3,2],[-2,2]]
Output: 5

CONSTRAINTS:
- points.length == n
- 1 <= n <= 100
- points[i].length == 2
- -1000 <= points[i][0], points[i][1] <= 1000

ALGORITHM LOGIC (Chebyshev Distance):
1. Because diagonal movement allows us to traverse 1 unit in X and 1 unit in Y simultaneously 
   for the cost of 1 second, it is always optimal to move diagonally as much as possible.
2. The number of diagonal moves we can make is bounded by the smaller coordinate difference. 
   Once we align on one axis, we finish the journey moving in a straight line on the other axis.
3. Therefore, the minimum time to travel between two points A(x1, y1) and B(x2, y2) is exactly:
   max(|x1 - x2|, |y1 - y2|)
4. This metric is known mathematically as the Chebyshev distance. We just sum this distance 
   for all consecutive pairs of points.

VISUALIZATION (points = [[1,1], [3,4], [-1,0]]):
Pair 1: [1,1] to [3,4]
dx = |3 - 1| = 2
dy = |4 - 1| = 3
Time = max(2, 3) = 3 seconds.

Pair 2: [3,4] to [-1,0]
dx = |-1 - 3| = 4
dy = |0 - 4| = 4
Time = max(4, 4) = 4 seconds.

Total time = 3 + 4 = 7 seconds. ✓
"""

# STEP 1: Initialize total_time counter to 0
# STEP 2: Iterate through the points array starting from the second point (index 1)
# STEP 3: Extract the current point and the previous point
# STEP 4: Calculate the absolute difference in X (dx) and Y (dy)
# STEP 5: Add the maximum of dx and dy (Chebyshev distance) to the total time
# STEP 6: Return the accumulated total time

class Solution:
    def minTimeToVisitAllPoints(self, points: list[list[int]]) -> int:
        
        total_time = 0                                               # Accumulator for total seconds
        
        for i in range(1, len(points)):                              # Start from index 1 to compare with i-1
            
            x1, y1 = points[i - 1]                                   # Previous point coordinates
            x2, y2 = points[i]                                       # Current point coordinates
            
            dx = abs(x2 - x1)                                        # Absolute distance on X-axis
            dy = abs(y2 - y1)                                        # Absolute distance on Y-axis
            
            total_time += max(dx, dy)                                # Chebyshev distance rule
            
        return total_time

"""
WHY EACH PART:
- range(1, len(points)): We need to look at pairs of points. Starting at index 1 allows us to safely reference `i - 1` without going out of bounds.
- x1, y1 = points[i - 1]: Python unpacking makes the code highly readable. Instead of writing points[i-1][0], we extract both coordinates immediately.
- abs(x2 - x1): We use absolute value because moving backwards (e.g., from x=3 to x=-1) is a distance of 4, not -4. Time cannot be negative.
- max(dx, dy): The core mathematical shortcut of the problem. It replaces the need for a while loop simulating diagonal and straight steps.

HOW IT WORKS (Example: points = [[3,2], [-2,2]]):
Iteration 1 (i = 1):
Previous point (x1, y1) = [3, 2]
Current point (x2, y2) = [-2, 2]
dx = |-2 - 3| = |-5| = 5
dy = |2 - 2| = 0
Time added = max(5, 0) = 5
Loop ends.
Returns 5. ✓

KEY TECHNIQUE:
- Geometric simplification (Chebyshev Distance).
- Array pairwise iteration.

EDGE CASES:
- Only two points provided: Loop runs exactly once, calculates distance properly. ✓
- Consecutive points are exactly the same (e.g., [[1,1], [1,1]]): dx=0, dy=0, max=0. Correctly adds 0 time. ✓
- Going backwards into negative coordinates: The `abs()` function handles negative spaces flawlessly. ✓

TIME COMPLEXITY: O(N) - Where N is the number of points in the array. We iterate through the array exactly once.
SPACE COMPLEXITY: O(1) - We only store a few integer variables (`total_time`, `dx`, `dy`) regardless of how many points exist in the input.

CONCEPTS USED:
- Geometry (Chebyshev distance)
- Array Iteration
- Absolute values & Max functions
"""
