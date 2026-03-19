"""
447. Number of Boomerangs
Difficulty: Medium
https://leetcode.com/problems/number-of-boomerangs/

PROBLEM:
You are given n points in the plane. Return the number of boomerangs.
A boomerang is a tuple (i, j, k) such that the distance between i and j
equals the distance between i and k.

ORDER MATTERS: (i, j, k) ≠ (i, k, j) — both count as separate boomerangs.

EXAMPLES:
Input: points = [[0,0],[1,0],[2,0]]     → Output: 2
    Center (1,0): dist to (0,0) = dist to (2,0) = 1
    Boomerangs: ((1,0),(0,0),(2,0)) and ((1,0),(2,0),(0,0))

Input: points = [[1,1],[2,2],[3,3]]     → Output: 2
Input: points = [[1,1]]                 → Output: 0

CONSTRAINTS:
    n == points.length
    1 <= n <= 500
    -10^4 <= points[i][0], points[i][1] <= 10^4
    All points are unique

KEY INSIGHT:
For each point as "center", count how many other points are at each
distance. If c points share the same distance from center, they form
c × (c-1) boomerangs (ordered permutations of 2 from c).

Use SQUARED distance to avoid floating point errors and sqrt overhead.

CHALLENGES:
    Floating point precision if using actual distance
    Understanding why c × (c-1) and not c × (c-1) / 2
    Efficiently grouping points by distance

SOLUTION:
    1. For each point as center, compute dist² to all others
    2. Group counts by distance using HashMap
    3. For each group of size c, add c × (c-1) boomerangs
    4. Sum across all centers
"""

# STEP 1: For each point as center
# STEP 2: Compute squared distances to all other points
# STEP 3: Count groups by distance, apply permutation formula
# STEP 4: Accumulate total boomerangs

from collections import defaultdict

class Solution:
    def numberOfBoomerangs(self, points: List[List[int]]) -> int:

        total = 0                                                        # Total boomerang count

        for i in range(len(points)):                                     # Each point as center
            dist_count = defaultdict(int)                                # dist² → count of points

            for j in range(len(points)):                                 # Compare with all others
                if i == j:                                               # Skip self
                    continue

                dx = points[i][0] - points[j][0]                        # Δx
                dy = points[i][1] - points[j][1]                        # Δy
                dist_sq = dx * dx + dy * dy                              # Distance squared (no sqrt!)

                dist_count[dist_sq] += 1                                 # Count this distance

            for count in dist_count.values():                            # For each distance group
                total += count * (count - 1)                             # Permutations P(c, 2)

        return total

"""
WHY EACH PART:

    total = 0: Accumulates boomerangs across ALL centers
    for i (center): Every point gets a turn as the boomerang vertex
    dist_count = defaultdict(int): Fresh map for each center
    if i == j: continue: A point can't be in a boomerang with itself
    dx, dy: Vector from center to other point
    dx*dx + dy*dy: Squared distance — avoids sqrt and float errors
    dist_count[dist_sq] += 1: Group points by their distance to center
    count * (count - 1): Ordered permutations of 2 from count points

HOW IT WORKS (Example: [[0,0],[1,0],[2,0]]):

    CENTER = points[0] = (0,0):
    ├── to (1,0): dx=1, dy=0, dist²=1 → dist_count = {1: 1}
    ├── to (2,0): dx=2, dy=0, dist²=4 → dist_count = {1: 1, 4: 1}
    ├── Group 1: count=1 → 1×0 = 0
    ├── Group 4: count=1 → 1×0 = 0
    └── total = 0

    CENTER = points[1] = (1,0):
    ├── to (0,0): dx=-1, dy=0, dist²=1 → dist_count = {1: 1}
    ├── to (2,0): dx=1, dy=0, dist²=1  → dist_count = {1: 2}
    ├── Group 1: count=2 → 2×1 = 2
    └── total = 0 + 2 = 2

    CENTER = points[2] = (2,0):
    ├── to (0,0): dx=-2, dy=0, dist²=4 → dist_count = {4: 1}
    ├── to (1,0): dx=-1, dy=0, dist²=1 → dist_count = {4: 1, 1: 1}
    ├── Group 4: count=1 → 1×0 = 0
    ├── Group 1: count=1 → 1×0 = 0
    └── total = 2 + 0 = 2

    Result: 2 ✓

WHY SQUARED DISTANCE INSTEAD OF ACTUAL DISTANCE:

    Actual distance: √((dx)² + (dy)²)
    ├── Involves sqrt → slow
    ├── Returns float → precision errors
    └── √2 might not equal √2 in floating point!

    Squared distance: (dx)² + (dy)²
    ├── No sqrt → fast
    ├── Always integer → exact comparison
    └── If dist_A = dist_B, then dist²_A = dist²_B ✓

WHY c × (c-1) AND NOT c × (c-1) / 2:

    c × (c-1) / 2 = COMBINATIONS (unordered pairs)
    c × (c-1)     = PERMUTATIONS (ordered pairs)

    The problem says ORDER MATTERS:
    (center, A, B) ≠ (center, B, A) → both count!

    Example: 3 points at same distance [A, B, C]:
    ├── Combinations: {A,B}, {A,C}, {B,C} → 3 pairs
    ├── Permutations: (A,B), (B,A), (A,C), (C,A), (B,C), (C,B) → 6
    └── 3 × 2 = 6 ✓

WHY FRESH HASHMAP PER CENTER:

    Each center has its OWN set of distances.
    Distances from (0,0) have nothing to do with distances from (1,0).

    dist_count = defaultdict(int)  ← reset for each new center

    If we reused the same map, we'd mix distances from different
    centers → wrong count!

WHY WE DON'T NEED TO STORE THE ACTUAL POINTS:

    We only need the COUNT of points at each distance.
    We don't care WHICH points they are, just HOW MANY.

    dist_count = {1: 3, 4: 2}  ← "3 points at dist²=1, 2 at dist²=4"
    That's all we need for the permutation formula.

EDGE CASES:

    Single point [[1,1]]: No pairs possible → 0 ✓
    Two points: Only 1 at each distance → 1×0 = 0 per center → 0 ✓
    Three equidistant: Each center has 2 at same dist → 2 boomerangs each ✓
    All points same distance from one center: c×(c-1) ✓
    Negative coordinates: Squaring makes them positive ✓
    Maximum n=500: 500² = 250,000 iterations → fast enough ✓

TIME COMPLEXITY: O(n²)
    For each of n points, compute distance to n-1 others
    HashMap operations are O(1) average
    Total: O(n²)

SPACE COMPLEXITY: O(n)
    HashMap stores at most n-1 distance entries per center
    Recreated for each center, so O(n) at any time

CONCEPTS USED:
    Squared distance (avoids float/sqrt)
    HashMap for grouping by distance
    Permutations P(c,2) = c × (c-1)
    Anchor point pattern (each point as center)
    Geometry: equidistant points from a center
"""
