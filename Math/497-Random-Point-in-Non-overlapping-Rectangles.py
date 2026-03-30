"""
497. Random Point in Non-overlapping Rectangles
Difficulty: Medium
https://leetcode.com/problems/random-point-in-non-overlapping-rectangles/

PROBLEM:
    Given a list of non-overlapping axis-aligned rectangles rects where
    rects[i] = [ai, bi, xi, yi] represents (bottom-left, top-right),
    implement pick() that returns a random integer point [x, y] inside
    one of the rectangles. Each integer point MUST have EQUAL probability.

EXAMPLES:
    Input: rects = [[-2,-2,1,1],[2,2,4,6]]
    pick() → could return [1,-2], [2,4], [-1,0], etc.
    Each of the 20 + 15 = 35 integer points has probability 1/35.

CONSTRAINTS:
    1 <= rects.length <= 100
    -10^9 <= ai < xi <= 10^9
    -10^9 <= bi < yi <= 10^9
    xi - ai <= 2000
    yi - bi <= 2000
    All rectangles do NOT overlap
    At most 10^4 calls to pick

KEY INSIGHT:
    We need WEIGHTED random selection: rectangles with more integer
    points should be picked more often. Use PREFIX SUM of point counts
    + BINARY SEARCH to select rectangle, then map to a coordinate.

    Points in rect [a,b,x,y] = (x - a + 1) * (y - b + 1)

CHALLENGES:
    Uniform probability across ALL points (not per rectangle)
    Efficiently selecting the right rectangle (binary search)
    Mapping a single number to a 2D coordinate inside a rectangle

SOLUTION:
    __init__: Count points per rectangle, build prefix sum
    pick:     Random number → binary search for rectangle → map to (x, y)
"""


# STEP 1: Count integer points in each rectangle
# STEP 2: Build prefix sum array for weighted selection
# STEP 3: pick() generates random number in [1, total]
# STEP 4: Binary search to find which rectangle owns that number
# STEP 5: Map the number to an (x, y) coordinate inside the rectangle


import random
from bisect import bisect_left

class Solution:

    def __init__(self, rects: List[List[int]]):

        self.rects = rects                                            # Store rectangles for pick()
        self.prefix = []                                              # Prefix sum of point counts
        total = 0                                                     # Running total of points

        for a, b, x, y in rects:                                     # For each rectangle
            points = (x - a + 1) * (y - b + 1)                       # Count integer points inside
            total += points                                           # Add to running total
            self.prefix.append(total)                                 # Store cumulative count

        self.total = total                                            # Total points across all rectangles

    def pick(self) -> List[int]:

        r = random.randint(1, self.total)                             # Random point number (1-indexed)

        idx = bisect_left(self.prefix, r)                             # Binary search: which rectangle?

        a, b, x, y = self.rects[idx]                                 # Get that rectangle's coordinates

        prev = self.prefix[idx - 1] if idx > 0 else 0                # Points BEFORE this rectangle
        offset = r - prev - 1                                        # 0-indexed position within rectangle

        width = x - a + 1                                             # Rectangle width (columns)

        col = offset % width                                          # Column within rectangle
        row = offset // width                                         # Row within rectangle

        return [a + col, b + row]                                     # Map to actual (x, y) coordinate


"""
WHY EACH PART:
    self.rects:         Need original coordinates in pick() to map back to (x, y)
    prefix sum:         Allows weighted selection — more points = bigger range = higher chance
    self.total:         Upper bound for random number generation
    randint(1, total):  Each number represents one unique integer point
    bisect_left:        O(log n) search for which rectangle "owns" this number
    prev:               How many points belong to previous rectangles
    offset:             Which specific point WITHIN this rectangle (0-indexed)
    col = offset % w:   Column position (wraps around at rectangle width)
    row = offset // w:  Row position (increments after each full row)
    a + col, b + row:   Translate local (col, row) to global (x, y) coordinates


HOW IT WORKS (Example: rects = [[1,1,2,2], [3,3,5,5]]):

    __init__:
    ├── Rect 0 [1,1,2,2]: (2-1+1)×(2-1+1) = 4 points
    ├── Rect 1 [3,3,5,5]: (5-3+1)×(5-3+1) = 9 points
    ├── prefix = [4, 13]
    └── total = 13

    pick() → r = 3:
    ├── bisect_left([4, 13], 3) → idx = 0 → Rect 0
    ├── prev = 0 (first rectangle)
    ├── offset = 3 - 0 - 1 = 2
    ├── width = 2 - 1 + 1 = 2
    ├── col = 2 % 2 = 0, row = 2 // 2 = 1
    └── return [1 + 0, 1 + 1] = [1, 2] 

    pick() → r = 10:
    ├── bisect_left([4, 13], 10) → idx = 1 → Rect 1
    ├── prev = prefix[0] = 4
    ├── offset = 10 - 4 - 1 = 5
    ├── width = 5 - 3 + 1 = 3
    ├── col = 5 % 3 = 2, row = 5 // 3 = 1
    └── return [3 + 2, 3 + 1] = [5, 4] 

    Verification for Rect 1 [3,3,5,5] offset mapping:
    offset: 0→(3,3) 1→(4,3) 2→(5,3)
            3→(3,4) 4→(4,4) 5→(5,4)  ← offset 5 = [5,4] ✓
            6→(3,5) 7→(4,5) 8→(5,5)


WHY PREFIX SUM + BINARY SEARCH:
    Without prefix sum:
        For each pick(), iterate all rectangles → O(n) per call

    With prefix sum + binary search:
        Build prefix once O(n), then each pick() is O(log n)
        
    With 10^4 calls and 100 rectangles:
        Without: 10^4 × 100 = 10^6 operations
        With:    10^4 × log(100) ≈ 10^4 × 7 = 7×10^4 operations 


WHY randint(1, total) AND NOT randint(0, total-1):
    Using 1-indexed makes bisect_left work naturally:

    prefix = [4, 13]
    r = 4  → bisect_left finds idx 0 (last point of rect 0)
    r = 5  → bisect_left finds idx 1 (first point of rect 1)
    r = 13 → bisect_left finds idx 1 (last point of rect 1)

    Clean boundary handling without off-by-one errors!


WHY offset % width AND offset // width:
    Think of the rectangle as a 1D array wrapped into 2D:

    Rectangle [1,1,3,2] → width=3, height=2, 6 points:
    
    offset: 0  1  2  3  4  5
    grid:   (1,1)(2,1)(3,1)(1,2)(2,2)(3,2)
    
    offset 4:
    ├── col = 4 % 3 = 1 → x = 1 + 1 = 2
    ├── row = 4 // 3 = 1 → y = 1 + 1 = 2
    └── point = (2, 2) 

    It's like converting a 1D index to 2D coordinates!


HANDLING SPECIAL CASES:
    Single rectangle:     prefix has one entry, bisect always returns 0 ✓
    1×1 rectangle [a,b,a,b]: 1 point, always returns [a, b] ✓
    Large coordinates:    Only affects mapping, not algorithm logic ✓
    Many pick() calls:    Each is O(log n), independent of previous calls ✓


KEY TECHNIQUE:
    Weighted random selection:   Prefix sum encodes probability weights
    Binary search (bisect_left): Efficiently finds which "bucket" a number falls in
    1D → 2D mapping:             offset → (row, col) using division and modulo
    Prefix sum pattern:          Common for range-based probability problems


EDGE CASES:
    Single rectangle:              Always picks within it ✓
    Single point rectangle [a,b,a,b]: Always returns [a,b] ✓
    Very large rectangles:         2000×2000 = 4×10^6 points max ✓
    Negative coordinates:          Math works the same with negatives ✓
    Many rectangles (100):         Binary search handles efficiently ✓


TIME COMPLEXITY:
    __init__: O(n) — iterate all rectangles to build prefix sum
    pick():   O(log n) — binary search over prefix array

SPACE COMPLEXITY: O(n)
    Prefix sum array with n entries
    Store reference to rects array


CONCEPTS USED:
    Weighted random sampling
    Prefix sum (cumulative distribution)
    Binary search (bisect_left)
    1D to 2D index mapping (modulo + division)
    Probability and uniform distribution
"""
