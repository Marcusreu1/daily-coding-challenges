# 149. Max Points on a Line
# Difficulty: Hard
# https://leetcode.com/problems/max-points-on-a-line/

"""
PROBLEM:
Given an array of points where points[i] = [xi, yi] represents a point
on the X-Y plane, return the maximum number of points that lie on the
same straight line.

EXAMPLES:
Input: points = [[1,1],[2,2],[3,3]]  → Output: 3 (all on y = x)
Input: points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]] → Output: 4

CONSTRAINTS:
- 1 <= points.length <= 300
- -10^4 <= xi, yi <= 10^4
- All points are unique

KEY INSIGHT:
For each point P, count how many other points share the same SLOPE from P.
Points with the same slope from P are collinear (on the same line through P).

CHALLENGES:
1. Division by zero (vertical lines)
2. Floating point precision (1/3 vs 2/6)

SOLUTION:
- Use FRACTIONS instead of decimals
- Store slope as (dy, dx) after reducing by GCD
- Normalize sign so same slopes have same representation

SLOPE REPRESENTATION:
Instead of: slope = dy / dx = 0.666...
We store:   (dy, dx) = (2, 3) after GCD reduction

This avoids floating point errors!
"""

# STEP 1: Handle base cases (n <= 2)
# STEP 2: For each point as "anchor", count slopes to all other points
# STEP 3: Points with same slope are collinear with anchor
# STEP 4: Track maximum (count + 1 for anchor point)

from collections import defaultdict
from math import gcd

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        
        n = len(points)
        
        if n <= 2:                                                               # 1-2 points always collinear
            return n
        
        max_puntos = 0
        
        for i in range(n):                                                       # Each point as anchor
            pendientes = defaultdict(int)                                        # slope → count
            
            for j in range(n):                                                   # Compare with all others
                if i == j:
                    continue
                
                dx = points[j][0] - points[i][0]                                 # Δx
                dy = points[j][1] - points[i][1]                                 # Δy
                
                g = gcd(abs(dx), abs(dy))                                        # Reduce fraction
                dx //= g
                dy //= g
                
                if dx < 0 or (dx == 0 and dy < 0):                               # Normalize sign
                    dx = -dx
                    dy = -dy
                
                pendientes[(dy, dx)] += 1                                        # Count this slope
            
            if pendientes:
                max_local = max(pendientes.values()) + 1                         # +1 for anchor
                max_puntos = max(max_puntos, max_local)
        
        return max_puntos

"""
WHY EACH PART:
- n <= 2: Base case - any 1-2 points are always on a line
- for i in range(n): Try each point as the "anchor" of potential lines
- defaultdict(int): Auto-initialize missing keys to 0
- dx, dy: Vector from anchor to current point
- gcd: Reduce fraction to canonical form (4/6 → 2/3)
- Normalize sign: Ensure (-2,-3) and (2,3) are same slope
- pendientes[(dy,dx)] += 1: Count points with this slope from anchor
- max(values) + 1: Most common slope count + anchor itself

HOW IT WORKS (Example: [[1,1],[2,2],[3,3]]):

Anchor = (1,1):
├── To (2,2): dx=1, dy=1, gcd=1 → slope (1,1)
├── To (3,3): dx=2, dy=2, gcd=2 → slope (1,1)
└── pendientes = {(1,1): 2}
    max_local = 2 + 1 = 3

Anchor = (2,2):
├── To (1,1): dx=-1, dy=-1 → normalize → (1,1)
├── To (3,3): dx=1, dy=1 → (1,1)
└── pendientes = {(1,1): 2}
    max_local = 3

Result: 3 ✓

WHY USE FRACTIONS:
Decimal: 1/3 = 0.33333... and 2/6 = 0.33333...
         But computers might store them slightly differently!

Fraction: (1,3) and (2,6) → both reduce to (1,3)
         Exact match guaranteed ✓

WHY NORMALIZE SIGN:
Without: slope from A→B = (2,3), slope from B→A = (-2,-3)
         These are SAME line but DIFFERENT keys!

With normalization: both become (2,3) ✓

HANDLING SPECIAL CASES:
- Vertical line (dx=0): Store as (1,0) or just (dy,0) with dy>0
- Horizontal line (dy=0): Store as (0,1) or just (0,dx) with dx>0
- The GCD and sign normalization handle both naturally

KEY TECHNIQUE:
- Slope as fraction: Avoid floating point errors
- GCD reduction: Canonical form for same slopes
- Sign normalization: Same line, same key
- Anchor point pattern: Count from one fixed point

EDGE CASES:
- Single point: Returns 1 ✓
- Two points: Returns 2 ✓
- All points collinear: Returns n ✓
- No 3 points collinear: Returns 2 ✓
- Vertical line (same x): Handled by (dy, 0) ✓
- Horizontal line (same y): Handled by (0, dx) ✓
- Negative coordinates: Handled by sign normalization ✓

TIME COMPLEXITY: O(n² × log(max_coordinate))
- O(n²) point pairs
- O(log(max)) for GCD calculation

SPACE COMPLEXITY: O(n) - Dictionary for slopes

CONCEPTS USED:
- Analytical geometry (slopes, collinearity)
- GCD for fraction reduction
- Hash map for counting
- Sign normalization
- Avoiding floating point errors
"""
