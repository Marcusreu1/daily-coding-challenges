"""
587. Erect the Fence
Difficulty: Hard
https://leetcode.com/problems/erect-the-fence/

PROBLEM:
    Given a set of points representing trees on a 2D plane,
    return the points that lie on the fence (convex hull boundary),
    INCLUDING points that lie ON the edges of the hull (collinear points).

EXAMPLES:
    Input: trees = [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]
    Output: [[1,1],[2,0],[2,4],[3,3],[4,2]]  (all except interior points)

    Input: trees = [[1,2],[2,2],[4,2]]
    Output: [[1,2],[2,2],[4,2]]  (collinear, all on the fence)

CONSTRAINTS:
    1 <= trees.length <= 3000
    0 <= xi, yi <= 100
    All points are unique

KEY INSIGHT:
    This is a Convex Hull problem with a twist: we must include
    ALL points on the boundary, including collinear ones.

    We use Andrew's Monotone Chain algorithm.
    The key difference: use strict inequality (< 0) for removal,
    which KEEPS collinear points on the hull.

    Standard convex hull uses <= 0 (removes collinear).
    This problem uses < 0 (keeps collinear).

CHALLENGES:
    Including collinear points on the hull boundary
    Cross product computation and sign interpretation
    Correctly building lower and upper hulls
    Deduplicating points that appear in both hulls

CROSS PRODUCT REVIEW:
    cross(O, A, B) = (A.x-O.x)(B.y-O.y) - (A.y-O.y)(B.x-O.x)

    > 0: counterclockwise turn (left turn)    ↺
    < 0: clockwise turn (right turn)          ↻
    = 0: collinear (straight line)            ──

SOLUTION:
    Sort points by (x, y).
    Build lower hull (left → right): pop while cross < 0.
    Build upper hull (right → left): pop while cross < 0.
    Union both hulls and deduplicate.
"""


# STEP 1: Sort points by x-coordinate, then by y-coordinate
# STEP 2: Build lower hull (left to right)
# STEP 3: Build upper hull (right to left)
# STEP 4: Combine both hulls, remove duplicates
# STEP 5: Return all unique points on the fence


class Solution:
    def outerTrees(self, trees: List[List[int]]) -> List[List[int]]:

        def cross(O, A, B):                                          # Cross product of vectors OA and OB
            return (A[0] - O[0]) * (B[1] - O[1]) - \
                   (A[1] - O[1]) * (B[0] - O[0])

        n = len(trees)

        if n <= 3:                                                    # 3 or fewer points: all on the hull
            return trees

        trees.sort()                                                  # Sort by x, then y

        # --- Build lower hull (left → right) ---
        lower = []                                                    # Lower boundary of convex hull
        for p in trees:                                               # Process points left to right
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:  # Clockwise → remove
                lower.pop()                                           # Remove point causing clockwise turn
            lower.append(p)                                           # Add current point

        # --- Build upper hull (right → left) ---
        upper = []                                                    # Upper boundary of convex hull
        for p in reversed(trees):                                     # Process points right to left
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) < 0:  # Clockwise → remove
                upper.pop()                                           # Remove point causing clockwise turn
            upper.append(p)                                           # Add current point

        # --- Combine and deduplicate ---
        return [list(p) for p in set(map(tuple, lower + upper))]      # Union of both hulls, no duplicates


"""
WHY EACH PART:
    cross(O, A, B):      Determines turn direction: >0 left, <0 right, =0 straight
    n <= 3:              3 or fewer points always form the complete hull
    trees.sort():        Andrew's algorithm requires sorted input (by x, then y)
    cross(...) < 0:      STRICT inequality — keeps collinear points (cross=0 stays)
    lower hull:          Traces the bottom boundary left → right
    upper hull:          Traces the top boundary right → left
    set(map(tuple,...)):  Removes duplicates where lower and upper overlap
    list(p):             Convert tuples back to lists (problem expects lists)


WHY cross < 0 (STRICT) INSTEAD OF cross <= 0:
    Standard convex hull:
        cross <= 0 → removes collinear points
        Result: minimal set of vertices

    This problem:
        cross < 0 → KEEPS collinear points (cross=0 not removed)
        Result: ALL points on the boundary

    Example: points (0,0), (1,1), (2,2)
        cross((0,0),(1,1),(2,2)) = 0 (collinear)
        
        With <= 0: removes (1,1) → hull = [(0,0),(2,2)]
        With < 0:  keeps (1,1)   → hull = [(0,0),(1,1),(2,2)] 


HOW IT WORKS (Example: trees = [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]):

    Sorted: [(1,1),(2,0),(2,2),(2,4),(3,3),(4,2)]

    LOWER HULL (→):
    ├── (1,1): lower = [(1,1)]
    ├── (2,0): lower = [(1,1),(2,0)]
    ├── (2,2): cross((1,1),(2,0),(2,2)) = 2 → not < 0 → keep
    │          lower = [(1,1),(2,0),(2,2)]
    ├── (2,4): cross((2,0),(2,2),(2,4)) = 0 → not < 0 → keep
    │          lower = [(1,1),(2,0),(2,2),(2,4)]
    ├── (3,3): cross((2,2),(2,4),(3,3)) = -2 < 0 → POP (2,4)
    │          cross((2,0),(2,2),(3,3)) = -2 < 0 → POP (2,2)
    │          cross((1,1),(2,0),(3,3)) = 4 → not < 0 → keep
    │          lower = [(1,1),(2,0),(3,3)]
    └── (4,2): cross((2,0),(3,3),(4,2)) = -4 < 0 → POP (3,3)
               cross((1,1),(2,0),(4,2)) = 4 → not < 0 → keep
               lower = [(1,1),(2,0),(4,2)]

    UPPER HULL (←):
    ├── (4,2): upper = [(4,2)]
    ├── (3,3): upper = [(4,2),(3,3)]
    ├── (2,4): cross((4,2),(3,3),(2,4)) = 0 → not < 0 → keep
    │          upper = [(4,2),(3,3),(2,4)]
    ├── (2,2): cross((3,3),(2,4),(2,2)) = 2 → not < 0 → keep
    │          upper = [(4,2),(3,3),(2,4),(2,2)]
    ├── (2,0): cross((2,4),(2,2),(2,0)) = 0 → not < 0 → keep
    │          upper = [(4,2),(3,3),(2,4),(2,2),(2,0)]
    └── (1,1): cross((2,2),(2,0),(1,1)) = -2 < 0 → POP (2,0)
               cross((2,4),(2,2),(1,1)) = -2 < 0 → POP (2,2)
               cross((3,3),(2,4),(1,1)) = 4 → not < 0 → keep
               upper = [(4,2),(3,3),(2,4),(1,1)]

    COMBINE:
    lower + upper = [(1,1),(2,0),(4,2),(4,2),(3,3),(2,4),(1,1)]
    
    Deduplicated set: {(1,1),(2,0),(4,2),(3,3),(2,4)}
    
    Result: [[1,1],[2,0],[2,4],[3,3],[4,2]] 


HOW IT WORKS (Collinear example: trees = [[1,2],[2,2],[4,2]]):

    Sorted: [(1,2),(2,2),(4,2)]
    
    n = 3 → return trees directly = [[1,2],[2,2],[4,2]] 
    
    All three points are on the fence (they're collinear).


WHY TWO SEPARATE HULLS (LOWER + UPPER):
    Think of the convex hull as two "chains":

                    * ─── * ─── *        ← upper hull
                   /               \
    leftmost *                       * rightmost
                   \               /
                    * ─── * ─── *        ← lower hull

    Lower hull: connects leftmost to rightmost along the BOTTOM
    Upper hull: connects rightmost to leftmost along the TOP

    Together they form the complete boundary.

    By processing sorted points left→right (lower) and
    right→left (upper), we trace both chains.


WHY SORTING BY (X, Y) IS IMPORTANT:
    Sorting ensures:
    1. We process points in a consistent left-to-right order
    2. Ties in x are broken by y (prevents ambiguity)
    3. The first and last sorted points are guaranteed on the hull

    Without sorting, the monotone chain algorithm wouldn't work
    because it depends on the x-monotone property.


WHAT THE CROSS PRODUCT TELLS US GEOMETRICALLY:
    For three consecutive points on the hull: O → A → B

    cross > 0 (left turn):
        B is to the LEFT of line O→A
        This is what we WANT for the upper hull

    cross < 0 (right turn):
        B is to the RIGHT of line O→A
        This point "dents inward" → remove it

    cross = 0 (straight):
        B is exactly ON line O→A
        KEEP it (problem says include boundary points)


HANDLING SPECIAL CASES:
    n = 1:               Single point is the hull ✓
    n = 2:               Two points form a line segment ✓
    n = 3:               Triangle (all on hull) ✓
    All collinear:       All points returned ✓
    All same point:      Returns that point ✓
    Square shape:        Returns 4 corners ✓
    Points on edges:     Kept by strict inequality ✓


KEY TECHNIQUE:
    Andrew's Monotone Chain:  Two-pass hull construction
    Cross product:            Determines turn direction
    Strict inequality (< 0):  Includes collinear boundary points
    Sort + two passes:        Splits hull into lower and upper chains
    Set deduplication:        Handles overlap between chains


EDGE CASES:
    Single point [[0,0]]:             Returns [[0,0]] ✓
    Two points [[0,0],[1,1]]:         Returns both ✓
    Three collinear [[0,0],[1,1],[2,2]]: Returns all three ✓
    All points same [[1,1],[1,1]]:    Returns [[1,1]] ✓
    Square [[0,0],[0,1],[1,0],[1,1]]: Returns all four ✓
    Complex polygon with interior:    Excludes interior points ✓


TIME COMPLEXITY: O(n log n)
    Sorting: O(n log n) ← dominates
    Lower hull construction: O(n) amortized (each point added/removed once)
    Upper hull construction: O(n) amortized
    Set deduplication: O(n)
    Overall: O(n log n)

SPACE COMPLEXITY: O(n)
    Lower hull: at most n points
    Upper hull: at most n points
    Set for deduplication: at most n points


CONCEPTS USED:
    Computational geometry (convex hull)
    Andrew's Monotone Chain algorithm
    Cross product (turn direction)
    Monotone stack pattern
    Collinear point handling
    Set deduplication
"""
