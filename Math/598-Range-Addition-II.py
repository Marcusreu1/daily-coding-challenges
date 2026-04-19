"""
598. Range Addition II
Difficulty: Easy
https://leetcode.com/problems/range-addition-ii/

PROBLEM:
    Given an m x n matrix initialized to 0, and a list of operations ops
    where ops[i] = [ai, bi] means increment all cells in the rectangle
    from (0,0) to (ai-1, bi-1) by 1.
    Return the number of cells with the maximum value after all operations.

EXAMPLES:
    Input: m=3, n=3, ops=[[2,2],[3,3]]   → Output: 4
    Input: m=3, n=3, ops=[[2,2],[3,3],[3,3],[3,3],[2,2],[3,3],[3,3],[3,3],[2,2],[3,3],[3,3],[3,3]]
                                          → Output: 4
    Input: m=3, n=3, ops=[]               → Output: 9

CONSTRAINTS:
    1 <= m, n <= 4 × 10^4
    0 <= ops.length <= 10^4
    ops[i].length == 2
    1 <= ai <= m
    1 <= bi <= n

KEY INSIGHT:
    Every operation covers a rectangle starting from (0,0).
    The cells with maximum value are those covered by ALL operations.
    That's the INTERSECTION of all rectangles.

    Since all rectangles start at (0,0):
        intersection = min(ai) rows × min(bi) columns

    Result = min(ai) × min(bi)

CHALLENGES:
    Recognizing we don't need to build the matrix
    Handling empty ops array (result = m × n)
    Understanding why intersection = min × min

SOLUTION:
    Find min of all ai values and min of all bi values.
    Multiply them. That's the answer.
"""


# STEP 1: Initialize min dimensions to m and n
# STEP 2: For each operation, update minimums
# STEP 3: Return product of minimums


class Solution:
    def maxCount(self, m: int, n: int, ops: List[List[int]]) -> int:

        min_a = m                                                     # Start with full matrix height
        min_b = n                                                     # Start with full matrix width

        for a, b in ops:                                              # Check each operation
            min_a = min(min_a, a)                                     # Track smallest row count
            min_b = min(min_b, b)                                     # Track smallest column count

        return min_a * min_b                                          # Intersection area = answer


"""
WHY EACH PART:
    min_a = m, min_b = n:    If no operations, all m×n cells have max value (0)
    min(min_a, a):           Each operation shrinks the "guaranteed coverage" area
    min(min_b, b):           Same for columns
    min_a * min_b:           Area of intersection = count of max-value cells


HOW IT WORKS (Example: m=3, n=3, ops=[[2,2],[3,3]]):

    Init: min_a = 3, min_b = 3

    Operation [2,2]:
    ├── min_a = min(3, 2) = 2
    └── min_b = min(3, 2) = 2

    Operation [3,3]:
    ├── min_a = min(2, 3) = 2
    └── min_b = min(2, 3) = 2

    return 2 × 2 = 4 


HOW IT WORKS (Example: m=3, n=3, ops=[]):

    Init: min_a = 3, min_b = 3

    No operations → loop doesn't execute

    return 3 × 3 = 9 

    (All cells are 0, which is the maximum)


HOW IT WORKS (Example: m=4, n=5, ops=[[2,3],[3,2],[2,2]]):

    Init: min_a = 4, min_b = 5

    Operation [2,3]:
    ├── min_a = min(4, 2) = 2
    └── min_b = min(5, 3) = 3

    Operation [3,2]:
    ├── min_a = min(2, 3) = 2
    └── min_b = min(3, 2) = 2

    Operation [2,2]:
    ├── min_a = min(2, 2) = 2
    └── min_b = min(2, 2) = 2

    return 2 × 2 = 4 

    Visual verification:
    After all 3 operations:
        3 2 1 0 0      max = 3, appears at:
        2 2 1 0 0      (0,0) (0,1) (1,0) (1,1) → 4 cells ✓
        1 1 1 0 0
        0 0 0 0 0


WHY THE INTERSECTION IS min(ai) × min(bi):
    Each operation [a,b] covers rows 0..a-1 and cols 0..b-1.
    
    A cell (i,j) is covered by operation [a,b] iff:
        i < a  AND  j < b

    Cell (i,j) covered by ALL operations iff:
        i < a₁ AND i < a₂ AND ... AND i < aₖ
        j < b₁ AND j < b₂ AND ... AND j < bₖ
    
    Which simplifies to:
        i < min(a₁, a₂, ..., aₖ) = min_a
        j < min(b₁, b₂, ..., bₖ) = min_b

    Number of valid cells:
        min_a choices for i (0, 1, ..., min_a-1)
        × min_b choices for j (0, 1, ..., min_b-1)
        = min_a × min_b 


WHY INITIALIZE WITH m AND n:
    If ops is empty:
        All cells are 0 (the maximum)
        Answer should be m × n (all cells)

    Initializing min_a=m, min_b=n handles this naturally:
        No iterations → min_a stays m, min_b stays n
        return m × n 

    If ops is not empty:
        Since 1 <= ai <= m and 1 <= bi <= n (constraints),
        min(m, ai) = ai (ai is always ≤ m)
        So m doesn't affect the result — it's just a safe default.


WHY WE DON'T NEED THE ACTUAL MATRIX:
    ┌──────────────────────────────────────────┐
    │  Approach        │ Time      │ Space     │
    ├──────────────────┼───────────┼───────────┤
    │  Build matrix    │ O(k×m×n)  │ O(m×n)    │
    │  Just find min   │ O(k)      │ O(1)      │
    └──────────────────┴───────────┴───────────┘

    With m, n up to 40,000:
        Matrix approach: 40,000 × 40,000 = 1.6 billion cells 
        Min approach: just track 2 numbers 

    The key insight is that we only care about the COUNT of
    max-value cells, not the actual values.


THE VISUAL INTUITION:
    Think of each operation as a "spotlight" shining from (0,0):

    ops = [[2,2], [3,3], [2,3]]

    ┌─────────┐
    │■■│··│   │     ■ = lit by ALL spotlights (max value)
    │■■│··│   │     · = lit by SOME spotlights
    ├──┼──┤   │       = lit by fewer or none
    │··│··│   │
    │──┴──┘   │
    │         │
    └─────────┘

    The brightest area (■) = intersection of all spotlights
    = min(rows) × min(cols)


HANDLING SPECIAL CASES:
    Empty ops []:         All cells are 0 → return m × n ✓
    Single operation:     Return a × b directly ✓
    All ops are [m,n]:    Every cell incremented equally → return m × n ✓
    One op is [1,1]:      Only (0,0) has max → return 1 ✓
    All ops same:         min = that op → return a × b ✓


KEY TECHNIQUE:
    Intersection of rectangles:  min × min when anchored at origin
    Avoid simulation:            Don't build what you don't need
    Initialize with bounds:      m, n as safe defaults for empty ops
    Reduce to min:               Entire problem collapses to two min operations


EDGE CASES:
    ops = []:                m × n ✓
    ops = [[1,1]]:           1 ✓
    ops = [[m,n]]:           m × n ✓
    m=1, n=1, any ops:       1 ✓
    All ops identical:       ai × bi ✓
    m=40000, n=40000:        Handles without building matrix ✓
    Single row or column:    min handles correctly ✓


TIME COMPLEXITY: O(k)
    k = number of operations
    Single pass through ops to find minimums
    No matrix construction needed

SPACE COMPLEXITY: O(1)
    Only two integer variables (min_a, min_b)
    No matrix, no arrays


CONCEPTS USED:
    Rectangle intersection (anchored at origin)
    Running minimum
    Mathematical simplification (avoid simulation)
    Edge case handling (empty operations)
"""
