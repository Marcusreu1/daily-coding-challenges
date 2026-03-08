"""
391. Perfect Rectangle
Difficulty: Hard
https://leetcode.com/problems/perfect-rectangle/

PROBLEM:
Given an array of rectangles where rectangles[i] = [xi, yi, ai, bi] represents
an axis-aligned rectangle with bottom-left point (xi, yi) and top-right (ai, bi).

Return true if all rectangles together form an exact cover of a rectangular region.

An exact cover means:
- No gaps
- No overlaps

EXAMPLES:
Input: rectangles = [[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]]
Output: true
    All 5 rectangles form a perfect 3x3 square.

Input: rectangles = [[1,1,2,3],[1,3,2,4],[3,1,4,2],[3,2,4,4]]
Output: false
    There's a gap between the rectangles.

Input: rectangles = [[1,1,3,3],[3,1,4,2],[1,3,2,4],[2,2,4,4]]
Output: false
    There's an overlap between rectangles.

CONSTRAINTS:
• 1 <= rectangles.length <= 2 * 10⁴
• rectangles[i].length == 4
• -10⁵ <= xi, yi, ai, bi <= 10⁵

KEY INSIGHT:
Two conditions must be satisfied:

1. AREA CONDITION:
   Sum of all rectangle areas = area of bounding box

2. CORNER CONDITION:
   Every corner should appear an EVEN number of times,
   EXCEPT for the 4 corners of the bounding box (appear exactly ONCE).

   Using XOR logic with a set: add if not present, remove if present.
   Final set should contain exactly the 4 bounding box corners.

WHY CORNER COUNTING WORKS:
- Internal corners are shared by 2 or 4 rectangles → even count → cancel out
- Edge corners (not main 4) are shared by 2 rectangles → even count → cancel out
- The 4 main corners appear exactly once → odd count → remain in set
"""

from typing import List


# ============================================================================
# SOLUTION 1: SET FOR CORNERS (Recommended)
# ============================================================================

class Solution:
    def isRectangleCover(self, rectangles: List[List[int]]) -> bool:
        
        # Track corners using set (add if absent, remove if present)
        corners = set()
        area = 0
        
        # Track bounding box
        x_min = y_min = float('inf')
        x_max = y_max = float('-inf')
        
        for x1, y1, x2, y2 in rectangles:
            # Update bounding box
            x_min = min(x_min, x1)
            y_min = min(y_min, y1)
            x_max = max(x_max, x2)
            y_max = max(y_max, y2)
            
            # Add area
            area += (x2 - x1) * (y2 - y1)
            
            # Toggle corners (XOR logic using symmetric difference)
            for corner in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]:
                if corner in corners:
                    corners.remove(corner)
                else:
                    corners.add(corner)
        
        # Check 1: Area must match
        expected_area = (x_max - x_min) * (y_max - y_min)
        if area != expected_area:
            return False
        
        # Check 2: Only 4 corners of bounding box should remain
        expected_corners = {(x_min, y_min), (x_min, y_max), 
                          (x_max, y_min), (x_max, y_max)}
        
        return corners == expected_corners


# ============================================================================
# SOLUTION 2: USING SYMMETRIC DIFFERENCE OPERATOR
# ============================================================================

class Solution:
    def isRectangleCover(self, rectangles: List[List[int]]) -> bool:
        
        corners = set()
        area = 0
        
        x_min = y_min = float('inf')
        x_max = y_max = float('-inf')
        
        for x1, y1, x2, y2 in rectangles:
            # Update bounding box
            x_min, y_min = min(x_min, x1), min(y_min, y1)
            x_max, y_max = max(x_max, x2), max(y_max, y2)
            
            # Add area
            area += (x2 - x1) * (y2 - y1)
            
            # Symmetric difference (XOR) with rectangle corners
            rect_corners = {(x1, y1), (x1, y2), (x2, y1), (x2, y2)}
            corners ^= rect_corners                              # XOR operation on sets
        
        # Verify conditions
        expected_area = (x_max - x_min) * (y_max - y_min)
        expected_corners = {(x_min, y_min), (x_min, y_max), 
                          (x_max, y_min), (x_max, y_max)}
        
        return area == expected_area and corners == expected_corners


# ============================================================================
# SOLUTION 3: DICTIONARY COUNTING (More explicit)
# ============================================================================

from collections import defaultdict


class Solution:
    def isRectangleCover(self, rectangles: List[List[int]]) -> bool:
        
        corner_count = defaultdict(int)
        area = 0
        
        x_min = y_min = float('inf')
        x_max = y_max = float('-inf')
        
        for x1, y1, x2, y2 in rectangles:
            # Update bounding box
            x_min, y_min = min(x_min, x1), min(y_min, y1)
            x_max, y_max = max(x_max, x2), max(y_max, y2)
            
            # Add area
            area += (x2 - x1) * (y2 - y1)
            
            # Count corners
            for corner in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]:
                corner_count[corner] += 1
        
        # Check area
        expected_area = (x_max - x_min) * (y_max - y_min)
        if area != expected_area:
            return False
        
        # Check corners: only 4 main corners should have odd count
        main_corners = {(x_min, y_min), (x_min, y_max), 
                       (x_max, y_min), (x_max, y_max)}
        
        for corner, count in corner_count.items():
            if corner in main_corners:
                if count % 2 != 1:                               # Must be odd (1, 3, ...)
                    return False
            else:
                if count % 2 != 0:                               # Must be even (2, 4, ...)
                    return False
        
        return True


"""
HOW IT WORKS (Detailed Trace):

Example: rectangles = [[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]]

═══════════════════════════════════════════════════════════════════
STEP 1: Process each rectangle
═══════════════════════════════════════════════════════════════════

corners = {} (empty set)
area = 0
Bounding: x_min=∞, y_min=∞, x_max=-∞, y_max=-∞

R1 = [1,1,3,3]:
    Bounding: x_min=1, y_min=1, x_max=3, y_max=3
    area = 0 + (3-1)*(3-1) = 4
    corners: add (1,1), (1,3), (3,1), (3,3)
    corners = {(1,1), (1,3), (3,1), (3,3)}

R2 = [3,1,4,2]:
    Bounding: x_min=1, y_min=1, x_max=4, y_max=3
    area = 4 + (4-3)*(2-1) = 5
    Toggle: (3,1)→remove, (3,2)→add, (4,1)→add, (4,2)→add
    corners = {(1,1), (1,3), (3,3), (3,2), (4,1), (4,2)}

R3 = [3,2,4,4]:
    Bounding: x_min=1, y_min=1, x_max=4, y_max=4
    area = 5 + (4-3)*(4-2) = 7
    Toggle: (3,2)→remove, (3,4)→add, (4,2)→remove, (4,4)→add
    corners = {(1,1), (1,3), (3,3), (4,1), (3,4), (4,4)}

R4 = [1,3,2,4]:
    area = 7 + (2-1)*(4-3) = 8
    Toggle: (1,3)→remove, (1,4)→add, (2,3)→add, (2,4)→add
    corners = {(1,1), (3,3), (4,1), (3,4), (4,4), (1,4), (2,3), (2,4)}

R5 = [2,3,3,4]:
    area = 8 + (3-2)*(4-3) = 9
    Toggle: (2,3)→remove, (2,4)→remove, (3,3)→remove, (3,4)→remove
    corners = {(1,1), (4,1), (4,4), (1,4)}

═══════════════════════════════════════════════════════════════════
STEP 2: Verify conditions
═══════════════════════════════════════════════════════════════════

Bounding box: (1,1) to (4,4)
Expected area = (4-1) * (4-1) = 9
Actual area = 9 ✓

Expected corners = {(1,1), (1,4), (4,1), (4,4)}
Actual corners = {(1,1), (4,1), (4,4), (1,4)} ✓

RETURN: True ✓

═══════════════════════════════════════════════════════════════════

WHY CORNER XOR WORKS:
┌────────────────────────────────────────────────────────────────┐
│  Perfect cover properties:                                     │
│                                                                │
│  INTERNAL CORNER (shared by 4 rectangles):                    │
│      ┌──┬──┐                                                  │
│      │  │  │  Corner appears 4 times                          │
│      ├──┼──┤  4 = even → XOR cancels out                      │
│      │  │  │                                                  │
│      └──┴──┘                                                  │
│                                                                │
│  EDGE CORNER (shared by 2 rectangles):                        │
│      ┌──┬──┐                                                  │
│      │  │  │  Corner appears 2 times                          │
│      └──┴──┘  2 = even → XOR cancels out                      │
│                                                                │
│  MAIN CORNER (only 1 rectangle touches it):                   │
│      ●──────                                                  │
│      │      Corner appears 1 time                              │
│      │      1 = odd → stays in set                            │
│                                                                │
│  Final set should have EXACTLY the 4 main corners!           │
└────────────────────────────────────────────────────────────────┘

VISUALIZING THE EXAMPLE:
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  (1,4)●────────●(2,4)────●(3,4)────●(4,4)                     │
│       │   R4   │   R5    │   R3    │                          │
│  (1,3)●────────●(2,3)────●(3,3)────●                          │
│       │                  │         │                          │
│       │       R1         │         │                          │
│       │                  │   R2    │                          │
│  (1,1)●──────────────────●(3,1)────●(4,1)                     │
│                                                                │
│  Main corners: (1,1), (1,4), (4,1), (4,4) - appear once       │
│  All others appear 2 or 4 times                               │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  Single rectangle     → Trivially valid                       │
│  Two identical rects  → Area doubles → False                  │
│  Gap in middle        → Area mismatch or corner mismatch      │
│  Partial overlap      → Corner count will be wrong            │
└────────────────────────────────────────────────────────────────┘

WHY BOTH CHECKS ARE NEEDED:
┌────────────────────────────────────────────────────────────────┐
│  Area alone is NOT sufficient:                                 │
│      Two same-area arrangements might have different shapes    │
│                                                                │
│  Corners alone is NOT sufficient:                              │
│      Need area to catch overlaps where corners still work     │
│                                                                │
│  Together they are NECESSARY AND SUFFICIENT                   │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(n)
├── Process each rectangle once: O(n)
├── Each rectangle has 4 corners: O(1) per rectangle
├── Set operations: O(1) average
└── Total: O(n)

SPACE COMPLEXITY: O(n)
├── Set can have at most 4n corners (but typically much less)
├── After XOR, most cancel out
└── Worst case: O(n)

CONCEPTS USED:
• Geometric reasoning
• XOR/symmetric difference for parity checking
• Set operations
• Bounding box calculation
"""
