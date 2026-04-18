"""
593. Valid Square
Difficulty: Medium
https://leetcode.com/problems/valid-square/

PROBLEM:
    Given the coordinates of four points in 2D space, return whether
    the four points can construct a valid square.
    Points are given in ANY order.

EXAMPLES:
    Input: p1=[0,0], p2=[1,1], p3=[1,0], p4=[0,1] → Output: true
    Input: p1=[0,0], p2=[0,0], p3=[0,0], p4=[0,0] → Output: false
    Input: p1=[1,0], p2=[-1,0], p3=[0,1], p4=[0,-1] → Output: true

CONSTRAINTS:
    p1.length == p2.length == p3.length == p4.length == 2
    -10^4 <= xi, yi <= 10^4

KEY INSIGHT:
    Among 4 points there are exactly 6 pairwise distances.
    A valid square has:
        - 4 equal distances (sides)
        - 2 equal distances (diagonals, longer than sides)
        - All sides > 0

    Sort the 6 squared distances and verify these 3 conditions.

    Using distance² avoids floating point issues.

CHALLENGES:
    Points can come in any order (not necessarily in sequence)
    Must handle degenerate cases (all same point, collinear)
    Floating point avoidance (use squared distances)

SOLUTION:
    Compute all 6 pairwise squared distances.
    Sort them.
    Check: first 4 equal, last 2 equal, first > 0.
"""


# STEP 1: Define helper to compute squared distance
# STEP 2: Compute all 6 pairwise distances
# STEP 3: Sort the distances
# STEP 4: Check the 3 conditions for a valid square


class Solution:
    def validSquare(self, p1, p2, p3, p4) -> bool:

        def dist_sq(a, b):                                            # Squared distance (avoids sqrt)
            return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

        points = [p1, p2, p3, p4]                                    # Group all 4 points

        dists = []                                                    # Store all 6 pairwise distances²
        for i in range(4):                                            # For each pair of points
            for j in range(i + 1, 4):                                 # Avoid duplicate pairs
                dists.append(dist_sq(points[i], points[j]))

        dists.sort()                                                  # Sort: [s, s, s, s, d, d]

        return (dists[0] > 0 and                                      # Sides are non-zero
                dists[0] == dists[1] == dists[2] == dists[3] and      # 4 equal sides
                dists[4] == dists[5])                                  # 2 equal diagonals


"""
WHY EACH PART:
    dist_sq(a, b):           Squared distance avoids floating point errors
    points = [p1..p4]:       Easier to iterate with indices
    range(i+1, 4):           Generates all unique pairs: (0,1)(0,2)(0,3)(1,2)(1,3)(2,3) = 6 pairs
    dists.sort():            After sorting: [side, side, side, side, diag, diag]
    dists[0] > 0:            Ensures not all points are the same (degenerate case)
    dists[0]==...==dists[3]:  All 4 sides must be equal
    dists[4] == dists[5]:    Both diagonals must be equal


HOW IT WORKS (Example: [0,0],[1,1],[1,0],[0,1]):

    Compute 6 distances²:
    ├── (0,0)↔(1,1) = 1+1 = 2
    ├── (0,0)↔(1,0) = 1+0 = 1
    ├── (0,0)↔(0,1) = 0+1 = 1
    ├── (1,1)↔(1,0) = 0+1 = 1
    ├── (1,1)↔(0,1) = 1+0 = 1
    └── (1,0)↔(0,1) = 1+1 = 2

    dists = [2, 1, 1, 1, 1, 2]
    sorted = [1, 1, 1, 1, 2, 2]

    dists[0] = 1 > 0
    1 == 1 == 1 == 1
    2 == 2

    return True 


HOW IT WORKS (Example: rotated square [0,0],[1,2],[3,1],[2,-1]):

    Compute 6 distances²:
    ├── (0,0)↔(1,2)  = 1+4  = 5
    ├── (0,0)↔(3,1)  = 9+1  = 10
    ├── (0,0)↔(2,-1) = 4+1  = 5
    ├── (1,2)↔(3,1)  = 4+1  = 5
    ├── (1,2)↔(2,-1) = 1+9  = 10
    └── (3,1)↔(2,-1) = 1+4  = 5

    sorted = [5, 5, 5, 5, 10, 10]

    5 > 0
    5 == 5 == 5 == 5
    10 == 10

    return True 


HOW IT WORKS (Example: all same points [0,0],[0,0],[0,0],[0,0]):

    All distances² = 0
    sorted = [0, 0, 0, 0, 0, 0]

    dists[0] = 0, NOT > 0

    return False 


HOW IT WORKS (Rhombus that's NOT a square):

    points: [0,0],[1,2],[2,0],[1,-2]

    sorted distances² = [4, 5, 5, 5, 5, 16]

    dists[0]=4 ≠ dists[1]=5 (first four not equal)

    return False (rhombus, not square)


HOW IT WORKS (Rectangle that's NOT a square):

    points: [0,0],[2,0],[2,1],[0,1]

    Distances²:
    ├── (0,0)↔(2,0) = 4
    ├── (0,0)↔(2,1) = 5
    ├── (0,0)↔(0,1) = 1
    ├── (2,0)↔(2,1) = 1
    ├── (2,0)↔(0,1) = 5
    └── (2,1)↔(0,1) = 4

    sorted = [1, 1, 4, 4, 5, 5]

    dists[0]=1 ≠ dists[2]=4 (first four not equal)

    return False  (rectangle, not square)


WHY SQUARED DISTANCE INSTEAD OF REAL DISTANCE:
    Real distance: sqrt((x₂-x₁)² + (y₂-y₁)²)
    
    Problem with sqrt:
        sqrt(2) = 1.41421356237...
        sqrt(8) = 2.82842712474...
        
        sqrt(2) * 2 == sqrt(8)?
        2.82842712474... == 2.82842712474...
        MAYBE — floating point might differ by tiny amount!
    
    With squared distances:
        2 * 2 == 8?  →  4 == 8?  NO (clearly different)
        
    Wait, that's a different check. The point is:
        dist_sq(A,B) == dist_sq(C,D) → EXACT integer comparison 
        dist(A,B) == dist(C,D)       → APPROXIMATE float comparison 


WHY 6 DISTANCES CAPTURE ALL INFORMATION:
    4 points = C(4,2) = 6 unique pairs
    These 6 distances FULLY characterize the shape.

    ┌───────────────────────────────┐
    │  Pair    │  In a square       │
    ├──────────┼────────────────────┤
    │  AB      │  side or diagonal  │
    │  AC      │  side or diagonal  │
    │  AD      │  side or diagonal  │
    │  BC      │  side or diagonal  │
    │  BD      │  side or diagonal  │
    │  CD      │  side or diagonal  │
    └──────────┴────────────────────┘

    We don't need to know WHICH are sides vs diagonals.
    After sorting, the pattern [s,s,s,s,d,d] emerges.


WHY THE 3 CONDITIONS ARE SUFFICIENT:
    Condition 1 (sides > 0):     Not a degenerate point
    Condition 2 (4 equal):       All sides equal → RHOMBUS
    Condition 3 (2 equal):       Both diagonals equal → RECTANGLE

    Rhombus ∩ Rectangle = SQUARE 

    No other quadrilateral has exactly 4 equal shorter
    distances and 2 equal longer distances.


HANDLING SPECIAL CASES:
    All same point:         dists[0]=0 → false ✓
    3 same, 1 different:    Not all 4 sides equal → false ✓
    Rectangle (not square): Sides not all equal → false ✓
    Rhombus (not square):   Diagonals not equal → false ✓
    Collinear points:       Pattern won't be [s,s,s,s,d,d] → false ✓
    Rotated square:         Works perfectly (rotation doesn't change distances) ✓
    Negative coordinates:   Squared differences handle negatives ✓


KEY TECHNIQUE:
    Distance² comparison:    Avoids floating point errors
    Sort-based validation:   Pattern matching on sorted distances
    Combinatorial pairs:     C(4,2) = 6 covers all relationships
    Geometric reasoning:     Rhombus + Rectangle = Square


EDGE CASES:
    All same point [0,0]×4:             false ✓
    Valid axis-aligned square:           true ✓
    Valid rotated square:                true ✓
    Rectangle (not square):             false ✓
    Rhombus (not square):               false ✓
    Three collinear + one off:          false ✓
    All collinear:                      false ✓
    Negative coordinates:               true/false correctly ✓
    Large coordinates (±10^4):          No overflow (max dist² ≈ 8×10^8) ✓


TIME COMPLEXITY: O(1)
    6 distance calculations: O(1)
    Sorting 6 elements: O(1)
    3 comparisons: O(1)
    Everything is constant — exactly 4 points always

SPACE COMPLEXITY: O(1)
    Array of exactly 6 distances
    No scaling with input


CONCEPTS USED:
    Computational geometry (distance formula)
    Squared distance trick (avoid floating point)
    Combinatorial enumeration (all pairs)
    Sort-based pattern matching
    Geometric properties (rhombus + rectangle = square)
"""
