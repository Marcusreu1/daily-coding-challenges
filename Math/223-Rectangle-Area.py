# 223. Rectangle Area
# Difficulty: Medium
# https://leetcode.com/problems/rectangle-area/

"""
PROBLEM:
Given the coordinates of two rectilinear rectangles in a 2D plane,
return the total area covered by the two rectangles.

The first rectangle is defined by (ax1, ay1) bottom-left and (ax2, ay2) top-right.
The second rectangle is defined by (bx1, by1) bottom-left and (bx2, by2) top-right.

EXAMPLES:
Input: ax1=-3, ay1=0, ax2=3, ay2=4, bx1=0, by1=-1, bx2=9, by2=2
Output: 45

Input: ax1=-2, ay1=-2, ax2=2, ay2=2, bx1=-2, by1=-2, bx2=2, by2=2
Output: 16 (identical rectangles)

CONSTRAINTS:
- -10^4 <= ax1 <= ax2 <= 10^4
- -10^4 <= ay1 <= ay2 <= 10^4
- -10^4 <= bx1 <= bx2 <= 10^4
- -10^4 <= by1 <= by2 <= 10^4

KEY INSIGHT:
Use the Inclusion-Exclusion Principle:
Total Area = Area1 + Area2 - Intersection Area

The intersection of two rectangles is also a rectangle (or empty).
Calculate overlap in X and Y axes separately.

CHALLENGES:
1. Rectangles might not overlap at all
2. One rectangle might be completely inside the other
3. Rectangles might just touch (no area overlap)

SOLUTION:
1. Calculate area of each rectangle
2. Find overlap width = max(0, min(right edges) - max(left edges))
3. Find overlap height = max(0, min(top edges) - max(bottom edges))
4. Total = Area1 + Area2 - (overlap_width × overlap_height)
"""

# STEP 1: Calculate area of rectangle 1
# STEP 2: Calculate area of rectangle 2
# STEP 3: Calculate overlap dimensions (0 if no overlap)
# STEP 4: Return total using inclusion-exclusion

class Solution:
    def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int,
                          bx1: int, by1: int, bx2: int, by2: int) -> int:
        
        # Area of rectangle 1
        area1 = (ax2 - ax1) * (ay2 - ay1)                                        # width × height
        
        # Area of rectangle 2
        area2 = (bx2 - bx1) * (by2 - by1)                                        # width × height
        
        # Calculate overlap dimensions
        overlap_width = max(0, min(ax2, bx2) - max(ax1, bx1))                    # X-axis overlap
        overlap_height = max(0, min(ay2, by2) - max(ay1, by1))                   # Y-axis overlap
        
        # Intersection area
        intersection = overlap_width * overlap_height
        
        # Inclusion-Exclusion: add both, subtract overlap (counted twice)
        return area1 + area2 - intersection


"""
WHY EACH PART:
- area1 = (ax2-ax1) × (ay2-ay1): Basic rectangle area formula
- area2 = (bx2-bx1) × (by2-by1): Same for second rectangle
- min(ax2, bx2): Rightmost left-edge of intersection
- max(ax1, bx1): Leftmost right-edge of intersection
- overlap_width: If negative, means no overlap → max(0, ...) makes it 0
- Same logic for overlap_height on Y-axis
- intersection: If either dimension is 0, intersection is 0
- area1 + area2 - intersection: Inclusion-exclusion principle

HOW IT WORKS (Example: ax1=-3, ay1=0, ax2=3, ay2=4, bx1=0, by1=-1, bx2=9, by2=2):

┌─ Calculate Individual Areas ──────────────────────────────┐
│                                                           │
│  area1 = (3 - (-3)) × (4 - 0)                             │
│        = 6 × 4 = 24                                       │
│                                                           │
│  area2 = (9 - 0) × (2 - (-1))                             │
│        = 9 × 3 = 27                                       │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Calculate Overlap Width ─────────────────────────────────┐
│                                                           │
│  Rect1 X-range: -3 ────────────── 3                       │
│  Rect2 X-range:      0 ────────────────── 9               │
│                                                           │
│  min(ax2, bx2) = min(3, 9) = 3   (left of right edges)    │
│  max(ax1, bx1) = max(-3, 0) = 0  (right of left edges)    │
│                                                           │
│  overlap_width = max(0, 3 - 0) = 3                        │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Calculate Overlap Height ────────────────────────────────┐
│                                                           │
│  Rect1 Y-range: 0 ───────────────── 4                     │
│  Rect2 Y-range:   -1 ─────── 2                            │
│                                                           │
│  min(ay2, by2) = min(4, 2) = 2   (lower of top edges)     │
│  max(ay1, by1) = max(0, -1) = 0  (higher of bottom edges) │
│                                                           │
│  overlap_height = max(0, 2 - 0) = 2                       │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Calculate Total Area ────────────────────────────────────┐
│                                                           │
│  intersection = 3 × 2 = 6                                 │
│                                                           │
│  total = area1 + area2 - intersection                     │
│        = 24 + 27 - 6                                      │
│        = 45 ✓                                             │
└───────────────────────────────────────────────────────────┘

WHY max(0, ...) FOR OVERLAP?
┌────────────────────────────────────────────────────────────┐
│  Case: No overlap in X                                     │
│                                                            │
│  Rect1: 0 ───── 2                                          │
│  Rect2:              5 ───── 8                             │
│                                                            │
│  min(ax2, bx2) - max(ax1, bx1) = min(2,8) - max(0,5)      │
│                                = 2 - 5 = -3 (negative!)    │
│                                                            │
│  max(0, -3) = 0  →  No overlap, intersection = 0           │
└────────────────────────────────────────────────────────────┘

VISUAL: Finding Intersection Rectangle
┌────────────────────────────────────────────────────────────┐
│                                                            │
│        ax1        ax2                                      │
│         ▼          ▼                                       │
│         ┌──────────┐                                       │
│         │          │                                       │
│         │    ┌─────┼─────┐ ◄─ bx2                         │
│         │    │█████│     │                                 │
│         │    │█████│     │                                 │
│         └────┼─────┘     │                                 │
│              │           │                                 │
│              └───────────┘                                 │
│              ▲                                             │
│             bx1                                            │
│                                                            │
│  Intersection left   = max(ax1, bx1)                       │
│  Intersection right  = min(ax2, bx2)                       │
│  Intersection bottom = max(ay1, by1)                       │
│  Intersection top    = min(ay2, by2)                       │
│                                                            │
│  Width  = right - left   (if positive)                     │
│  Height = top - bottom   (if positive)                     │
└────────────────────────────────────────────────────────────┘

INCLUSION-EXCLUSION PRINCIPLE:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   |A ∪ B| = |A| + |B| - |A ∩ B|                            │
│                                                            │
│   ┌─────────────────────┐                                  │
│   │         ┌───────────┼───────────┐                      │
│   │    A    │     A∩B   │     B     │                      │
│   │         │  (counted │           │                      │
│   │         │   twice!) │           │                      │
│   └─────────┼───────────┘           │                      │
│             └───────────────────────┘                      │
│                                                            │
│   If we just do A + B, the intersection is counted twice.  │
│   So we subtract it once to count it exactly once.         │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION (more verbose but clearer):

class Solution:
    def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int,
                          bx1: int, by1: int, bx2: int, by2: int) -> int:
        
        # Calculate individual areas
        area1 = (ax2 - ax1) * (ay2 - ay1)
        area2 = (bx2 - bx1) * (by2 - by1)
        
        # Check if rectangles overlap
        # No overlap if one is completely to the left/right/above/below
        if ax2 <= bx1 or bx2 <= ax1 or ay2 <= by1 or by2 <= ay1:
            return area1 + area2                                                 # No intersection
        
        # Calculate intersection
        left = max(ax1, bx1)
        right = min(ax2, bx2)
        bottom = max(ay1, by1)
        top = min(ay2, by2)
        
        intersection = (right - left) * (top - bottom)
        
        return area1 + area2 - intersection

EDGE CASES:
- No overlap: Returns area1 + area2 ✓
- Identical rectangles: Returns area (not 2×area) ✓
- One inside other: Returns larger area ✓
- Touch at edge: Returns area1 + area2 (no area overlap) ✓
- Touch at corner: Returns area1 + area2 ✓
- Negative coordinates: Handled correctly ✓

TEST CASES:
┌────────────────────────────────────────────────────────────┐
│  Case 1: Partial overlap (main example)                    │
│  ax1=-3, ay1=0, ax2=3, ay2=4                               │
│  bx1=0, by1=-1, bx2=9, by2=2                               │
│  Expected: 45 ✓                                            │
├────────────────────────────────────────────────────────────┤
│  Case 2: No overlap (separated)                            │
│  Rect1: (0,0) to (2,2)   Area = 4                          │
│  Rect2: (5,5) to (7,7)   Area = 4                          │
│  Expected: 8 ✓                                             │
├────────────────────────────────────────────────────────────┤
│  Case 3: One inside other                                  │
│  Rect1: (0,0) to (10,10)  Area = 100                       │
│  Rect2: (2,2) to (5,5)    Area = 9                         │
│  Intersection = 9                                          │
│  Expected: 100 + 9 - 9 = 100 ✓                             │
├────────────────────────────────────────────────────────────┤
│  Case 4: Same rectangle                                    │
│  Both: (-2,-2) to (2,2)  Area = 16 each                    │
│  Intersection = 16                                         │
│  Expected: 16 + 16 - 16 = 16 ✓                             │
└────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(1)
- Only arithmetic operations
- No loops or recursion
- Constant number of operations regardless of input

SPACE COMPLEXITY: O(1)
- Only storing a few integer variables
- No additional data structures

CONCEPTS USED:
- Coordinate geometry
- Inclusion-exclusion principle
- Rectangle intersection detection
- Min/Max for range overlap
- 2D geometric analysis
"""
