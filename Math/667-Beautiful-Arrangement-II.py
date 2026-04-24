"""
667. Beautiful Arrangement II
Difficulty: Medium
https://leetcode.com/problems/beautiful-arrangement-ii/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

Given two integers n and k, construct a list containing n different
positive integers ranging from 1 to n such that the absolute differences
between consecutive elements produce exactly k distinct values.

Return any valid list.

EXAMPLES:

    Input: n=3, k=1  → Output: [1,2,3]
        Differences: |1-2|=1, |2-3|=1 → {1} → 1 distinct ✓

    Input: n=3, k=2  → Output: [1,3,2]
        Differences: |1-3|=2, |3-2|=1 → {1,2} → 2 distinct ✓

CONSTRAINTS:

    1 <= k < n <= 10^4

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

Alternating between the smallest and largest unused values creates
DECREASING differences: k, k-1, k-2, ..., 1

    [1, k+1, 2, k, 3, k-1, ...]  → differences: k, k-1, k-2, ...

This gives us exactly k distinct differences using k+1 elements.
Then we fill the remaining positions (k+2 to n) in ascending order,
which only adds differences of 1 (already counted).

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. Understanding HOW to control the number of distinct differences
2. Realizing that zigzag pattern creates decreasing differences
3. Knowing when to stop zigzagging and start filling in order
4. Ensuring the fill portion doesn't introduce NEW differences

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Use first k+1 elements in zigzag pattern (low-high alternating)
STEP 2: Fill remaining positions k+2 to n in ascending order
STEP 3: Return the constructed array

ZIGZAG MECHANISM:
    With values [1, 2, ..., k+1]:
    Take low, high, low, high, ...
    → Produces differences: k, k-1, k-2, ..., 1
    → Exactly k distinct differences
"""


class Solution:
    def constructArray(self, n: int, k: int) -> list:

        result = []                                                               # Array to build
        low, high = 1, k + 1                                                      # Pointers for zigzag range [1, k+1]

        # ── STEP 1: Zigzag the first k+1 elements ──
        for i in range(k + 1):                                                    # k+1 elements → k differences
            if i % 2 == 0:                                                        # Even index → take from low end
                result.append(low)
                low += 1
            else:                                                                 # Odd index → take from high end
                result.append(high)
                high -= 1

        # ── STEP 2: Fill the rest in ascending order ──
        for val in range(k + 2, n + 1):                                           # Remaining values: k+2, k+3, ..., n
            result.append(val)                                                    # Append in order (difference = 1)

        return result


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

low, high = 1, k + 1:
    We only need values 1 through k+1 for the zigzag portion.
    low starts at the smallest (1), high at the largest (k+1).
    These two pointers move toward each other as we alternate.

for i in range(k + 1):
    We place k+1 elements in zigzag order. Between k+1 elements
    there are k consecutive differences — exactly what we need.

i % 2 == 0 → take low / else → take high:
    Even positions get the next smallest value (ascending).
    Odd positions get the next largest value (descending).
    This creates the alternating low-high pattern.

    Visually: low, HIGH, low, HIGH, low...
              1,   k+1,  2,   k,   3...

for val in range(k + 2, n + 1):
    After the zigzag, values k+2 through n haven't been used.
    We append them in ascending order. Each consecutive pair
    differs by 1, which is already in our set of differences.

Why ascending order is safe:
    The last zigzag element connects to k+2 with a small difference
    (either 1 or 2, both already present). From there, every
    difference is exactly 1 — no new distinct values introduced.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n=7, k=3):
════════════════════════════════════════════════════════════════

STEP 1 - Zigzag with values [1..4], low=1, high=4:
    ├── i=0 (even):  append low=1,  low→2    result=[1]
    ├── i=1 (odd):   append high=4, high→3   result=[1,4]
    ├── i=2 (even):  append low=2,  low→3    result=[1,4,2]
    └── i=3 (odd):   append high=3, high→2   result=[1,4,2,3]

    Differences so far: |1-4|=3, |4-2|=2, |2-3|=1
    Distinct: {3, 2, 1} → k=3 ✓

STEP 2 - Fill remaining [5, 6, 7]:
    result = [1, 4, 2, 3, 5, 6, 7]

    New differences: |3-5|=2, |5-6|=1, |6-7|=1
    All already in {1, 2, 3} → still k=3 ✓

    Final: [1, 4, 2, 3, 5, 6, 7] ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n=3, k=1):
════════════════════════════════════════════════════════════════

STEP 1 - Zigzag with values [1..2], low=1, high=2:
    ├── i=0 (even): append 1    result=[1]
    └── i=1 (odd):  append 2    result=[1,2]

    Differences: |1-2|=1 → {1} → k=1 ✓

STEP 2 - Fill remaining [3]:
    result = [1, 2, 3]

    New difference: |2-3|=1 → already in {1} ✓

    Final: [1, 2, 3] ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n=5, k=4, maximum k):
════════════════════════════════════════════════════════════════

STEP 1 - Zigzag with values [1..5], low=1, high=5:
    ├── i=0: append 1    → [1]
    ├── i=1: append 5    → [1,5]
    ├── i=2: append 2    → [1,5,2]
    ├── i=3: append 4    → [1,5,2,4]
    └── i=4: append 3    → [1,5,2,4,3]

    Differences: 4, 3, 2, 1 → {1,2,3,4} → k=4 ✓

STEP 2 - No remaining values (k+1 = n)

    Final: [1, 5, 2, 4, 3] ✓

════════════════════════════════════════════════════════════════
WHY THE ZIGZAG CREATES k DISTINCT DIFFERENCES:
════════════════════════════════════════════════════════════════

    Using values [1, 2, ..., k+1] in zigzag:

    Position:  1    k+1    2     k    3    k-1  ...
    Diff:        k    k-1   k-2   k-3  k-4  ...

    The differences are EXACTLY k, k-1, k-2, ..., 1
    That's k distinct values!

    Why? Each zigzag step "shrinks" the gap by 1:
    ├── 1 to k+1:  gap = k
    ├── k+1 to 2:  gap = k-1
    ├── 2 to k:    gap = k-2
    └── ... and so on, decreasing by 1 each time

════════════════════════════════════════════════════════════════
WHY THE FILL DOESN'T ADD NEW DIFFERENCES:
════════════════════════════════════════════════════════════════

    After zigzag, we append k+2, k+3, k+4, ..., n
    
    All consecutive → all differences = 1
    Difference of 1 is ALWAYS already in our set
    (since the last zigzag step produces difference = 1)

    Connection point (last zigzag to k+2):
    ├── If k is odd:  last element = (k+3)/2, next = k+2
    │   Difference ≥ 1 (already counted)
    └── If k is even: last element = (k+2)/2, next = k+2
        Difference ≥ 1 (already counted)

════════════════════════════════════════════════════════════════
VISUAL PATTERN:
════════════════════════════════════════════════════════════════

    n=8, k=4:
    
    Zigzag portion [1..5]:    Fill portion [6..8]:
    
    5 ·       · ·                              
    4 · · · · · ·                              
    3 · · · · · · ·                            
    2 · · · · · · · · 8                        
    1 · · · · · · · · · ·                      
      1 5 2 4 3 | 6 7 8
      \_zigzag_/ \_fill_/
    
    Diffs: 4,3,2,1,3,1,1 → {1,2,3,4} → k=4 ✓

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    n=1, k=0 (trivial)      → [1] ✓ (no differences needed)
    n=2, k=1                 → [1,2] ✓
    k=1 (minimum)            → [1,2,3,...,n] all diffs=1 ✓
    k=n-1 (maximum)          → Full zigzag, no fill portion ✓
    Large n, small k         → Short zigzag + long ordered tail ✓
    Large n, large k (n-1)   → Full zigzag over all n values ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(n)
════════════════════════════════════════════════════════════════

    Zigzag loop: O(k+1)
    Fill loop: O(n - k - 1)
    Total: O(k + 1 + n - k - 1) = O(n)
    Single pass to build the array.

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(n)
════════════════════════════════════════════════════════════════

    Output array of size n (required by the problem).
    No additional data structures beyond a few variables.

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Constructive algorithm (building a valid answer directly)
    Two-pointer technique (low/high converging)
    Zigzag pattern (alternating extremes for controlled differences)
    Greedy filling (sequential values for neutral differences)
    Mathematical observation (zigzag → decreasing differences)
"""
