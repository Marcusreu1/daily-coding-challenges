# 2280. Minimum Lines to Represent a Line Chart
# Difficulty: Medium
# https://leetcode.com/problems/minimum-lines-to-represent-a-line-chart/

"""
PROBLEM:
You are given a 2D integer array stockPrices where stockPrices[i] = [day_i, price_i] indicates the price of the stock on day_i is price_i. A line chart is created from the array by plotting the points on an XY plane with the X-axis representing the day and the Y-axis representing the price and connecting adjacent points. One continuous straight line can connect multiple adjacent points if they have the same slope.
Return the minimum number of lines needed to represent the line chart.

EXAMPLES:
Input: stockPrices = [[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]] → Output: 3
Explanation:
- The points (1,7), (2,6), (3,5), and (4,4) share the same negative slope. (1 line)
- The points (4,4) and (5,4) have a flat slope (0). (1 new line)
- The points (5,4), (6,3), (7,2), and (8,1) share a negative slope. (1 new line)
Total = 3 lines.

Input: stockPrices = [[3,4],[1,2],[7,8],[2,3]] → Output: 1
Explanation: After sorting by day: [1,2], [2,3], [3,4], [7,8]. All points fall on a single straight line with a slope of 1.

CONSTRAINTS:
- 1 <= stockPrices.length <= 10^5
- 1 <= day_i, price_i <= 10^9
- All day_i are distinct.

MATH RULES (CROSS-MULTIPLICATION & COLLINEARITY):
1. Ordering: The points are not guaranteed to be chronologically ordered. We must sort them by the X-axis (day) first.
2. The Floating-Point Trap: The slope 'm' between two points is (y2 - y1) / (x2 - x1). However, executing floating-point division causes precision loss for large numbers, causing the strict equality operator (==) to fail on collinear points.
3. Cross-Multiplication: To check if Slope A == Slope B mathematically without division:
   dy1 / dx1 == dy2 / dx2  =>  dy1 * dx2 == dy2 * dx1
   This uses pure integer multiplication, safely avoiding all floating-point inaccuracies and ensuring 100% mathematical precision.
"""

from typing import List

# STEP 1: Handle edge cases where the number of points cannot form multiple lines.
# STEP 2: Sort the array chronologically by 'day'.
# STEP 3: Initialize the line counter and calculate the delta vector (dx, dy) of the first line.
# STEP 4: Iterate from the 3rd point onwards, calculating the current delta vector.
# STEP 5: Use cross-multiplication to compare slopes. If they differ, increment the line count and update the reference vector.

class Solution:
    def minimumLines(self, stockPrices: List[List[int]]) -> int:
        
        n = len(stockPrices)
        
        # 0 points or 1 point require 0 lines to connect.
        if n <= 1:
            return 0
            
        # Sort chronologically by day
        stockPrices.sort()
        
        # We have at least 2 points, which guarantees at least 1 line
        lines = 1
        
        # Calculate the delta (dx, dy) for the first segment
        dx_prev = stockPrices[1][0] - stockPrices[0][0]
        dy_prev = stockPrices[1][1] - stockPrices[0][1]
        
        # Traverse the remaining points starting from the 3rd point (index 2)
        for i in range(2, n):
            
            dx_curr = stockPrices[i][0] - stockPrices[i - 1][0]
            dy_curr = stockPrices[i][1] - stockPrices[i - 1][1]
            
            # Cross-multiplication to check for collinearity without floating-point division
            if dy_prev * dx_curr != dy_curr * dx_prev:
                lines += 1
                # Update the reference slope to the new line's slope
                dx_prev = dx_curr
                dy_prev = dy_curr
                
        return lines

"""
WHY EACH PART:
- stockPrices.sort(): By default, Python sorts lists of lists by the first element of the sublists, which perfectly matches our need to sort by 'day'.
- dy_prev * dx_curr != dy_curr * dx_prev: The architectural core of the solution. It replaces `dy_prev / dx_prev != dy_curr / dx_curr`, granting immunity to precision loss while executing considerably faster at the ALU level.
- dx_prev = dx_curr: We only update our reference vector when the slope breaks, ensuring that we accurately track the trajectory of the current continuous line.

KEY TECHNIQUE:
- Computational Geometry: Eliminating division to maintain absolute integer precision in coordinate mathematics.

EDGE CASES:
- Only 1 point provided: Returns 0 seamlessly.
- Only 2 points provided: Sorts, bypasses the loop entirely, and returns 1 seamlessly.
- Colossal coordinates (10^9): Since Python handles arbitrarily large integers automatically, the multiplication (up to 10^18) will not overflow as it would in C++ or Java without using 64-bit `long long` types.

TIME COMPLEXITY: O(N log N) - Where N is the number of points. Sorting the array dictates the time complexity. The subsequent iteration takes strictly O(N) time.
SPACE COMPLEXITY: O(N) or O(1) - Depending on the language's sorting algorithm overhead. Python's Timsort takes O(N) auxiliary space in the worst case.
"""
