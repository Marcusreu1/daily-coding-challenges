"""
668. Kth Smallest Number in Multiplication Table
Difficulty: Hard
https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

Given three integers m, n, and k, consider the multiplication table
of size m × n where table[i][j] = i * j (1-indexed).

Return the kth smallest number in the multiplication table.

EXAMPLES:

    Input: m=3, n=3, k=5  → Output: 3
        Table:  1  2  3
                2  4  6
                3  6  9
        Sorted: [1, 2, 2, 3, 3, 4, 6, 6, 9] → 5th = 3

    Input: m=2, n=3, k=6  → Output: 6
        Table:  1  2  3
                2  4  6
        Sorted: [1, 2, 2, 3, 4, 6] → 6th = 6

CONSTRAINTS:

    1 <= m, n <= 3 * 10^4
    1 <= k <= m * n

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

We CANNOT generate and sort the full table (up to 9×10^8 elements).
Instead, we BINARY SEARCH on the answer value X and ask:

    "How many values in the table are ≤ X?"

For row i: values are i, 2i, 3i, ..., ni
    Count of values ≤ X in row i = min(X // i, n)

Total count = Σ min(X // i, n) for i = 1 to m → O(m) time

Binary search finds the smallest X where count(X) ≥ k.

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. BRUTE FORCE IS IMPOSSIBLE: Table can have 900 million entries
2. COUNTING EFFICIENTLY: Need O(m) counting, not O(m×n)
3. BINARY SEARCH ON VALUE: Searching the answer space, not indices
4. EXISTENCE GUARANTEE: Ensuring result is actually in the table

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Set binary search range [1, m * n]
STEP 2: For each mid, count how many table values are ≤ mid
STEP 3: If count ≥ k → search lower (mid might be answer)
STEP 4: If count < k → search higher (mid too small)
STEP 5: When lo == hi, that's our answer

COUNTING FORMULA:
    For a given value X:
    Row i contains: i, 2i, 3i, ..., ni
    Values ≤ X: i*j ≤ X → j ≤ X/i → count = min(X // i, n)
    Total = sum over all rows
"""


class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:

        def count_leq(x: int) -> int:
            """
            Counts how many values in the m×n multiplication table are ≤ x.
            For row i: values are i, 2i, ..., ni → count ≤ x is min(x // i, n)
            """
            total = 0                                                             # Accumulate count across all rows
            for i in range(1, m + 1):                                             # Iterate through each row
                total += min(x // i, n)                                           # Count values ≤ x in row i
            return total

        # ── Binary search on the answer value ──
        lo, hi = 1, m * n                                                         # Answer is between 1 and m*n

        while lo < hi:                                                            # Standard binary search
            mid = (lo + hi) // 2                                                  # Candidate answer
            if count_leq(mid) >= k:                                               # At least k values ≤ mid
                hi = mid                                                          # mid could be answer, search lower
            else:                                                                 # Fewer than k values ≤ mid
                lo = mid + 1                                                      # mid too small, search higher

        return lo                                                                 # lo == hi → found the answer


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

count_leq(x):
    The core helper function. For a candidate value x, it counts
    how many entries in the entire multiplication table are ≤ x.
    This lets us determine if x is "big enough" to be the kth value.

for i in range(1, m + 1):
    Row i of the table contains: i×1, i×2, i×3, ..., i×n.
    We process each row independently in O(1).

min(x // i, n):
    x // i gives how many multiples of i are ≤ x.
    But row i only has n columns, so we cap at n.
    Example: x=10, i=2, n=3 → 10//2=5, but only 3 columns → min(5,3)=3

lo, hi = 1, m * n:
    The smallest possible value in the table is 1 (at position 1,1).
    The largest possible value is m×n (at position m,n).
    Our answer must be somewhere in this range.

count_leq(mid) >= k → hi = mid:
    If there are at least k values ≤ mid, then mid might be our answer
    (or something smaller). We keep mid in the search range.

else → lo = mid + 1:
    If fewer than k values are ≤ mid, then mid is definitely too small.
    The kth value must be strictly greater than mid.

return lo:
    When lo == hi, the search converges to the exact answer.
    This value is guaranteed to exist in the table.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: m=3, n=3, k=5):
════════════════════════════════════════════════════════════════

    Table:  1  2  3
            2  4  6
            3  6  9
    Sorted: [1, 2, 2, 3, 3, 4, 6, 6, 9]

    Binary search: lo=1, hi=9

    Iteration 1: mid = 5
    ├── Row 1: min(5//1, 3) = 3
    ├── Row 2: min(5//2, 3) = 2
    ├── Row 3: min(5//3, 3) = 1
    ├── count = 6 ≥ 5 → hi = 5
    └── Search range: [1, 5]

    Iteration 2: mid = 3
    ├── Row 1: min(3//1, 3) = 3
    ├── Row 2: min(3//2, 3) = 1
    ├── Row 3: min(3//3, 3) = 1
    ├── count = 5 ≥ 5 → hi = 3
    └── Search range: [1, 3]

    Iteration 3: mid = 2
    ├── Row 1: min(2//1, 3) = 2
    ├── Row 2: min(2//2, 3) = 1
    ├── Row 3: min(2//3, 3) = 0
    ├── count = 3 < 5 → lo = 3
    └── Search range: [3, 3]

    lo == hi == 3 → Return 3 ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: m=2, n=3, k=6):
════════════════════════════════════════════════════════════════

    Table:  1  2  3
            2  4  6
    Sorted: [1, 2, 2, 3, 4, 6]

    Binary search: lo=1, hi=6

    Iteration 1: mid = 3
    ├── Row 1: min(3//1, 3) = 3
    ├── Row 2: min(3//2, 3) = 1
    ├── count = 4 < 6 → lo = 4
    └── Search range: [4, 6]

    Iteration 2: mid = 5
    ├── Row 1: min(5//1, 3) = 3
    ├── Row 2: min(5//2, 3) = 2
    ├── count = 5 < 6 → lo = 6
    └── Search range: [6, 6]

    lo == hi == 6 → Return 6 ✓

════════════════════════════════════════════════════════════════
WHY THE ANSWER IS GUARANTEED TO BE IN THE TABLE:
════════════════════════════════════════════════════════════════

    The count function is a "staircase" — it only increases at
    values that EXIST in the table:

    Value:  1  2  3  4  5  6  7  8  9
    Count:  1  3  5  6  6  8  8  8  9
                   ↑        ↑
                jumps    no change (5 not in table)

    count(2) = 3 < 5
    count(3) = 5 ≥ 5  ← first time count reaches 5

    Binary search finds this exact "jump point" where count
    first reaches k. This always corresponds to a table value.

    Mathematical proof:
    If X is NOT in the table, then count(X) == count(X-1).
    So binary search would never settle on X — it would keep
    moving left to find a smaller value with the same count.

════════════════════════════════════════════════════════════════
WHY BINARY SEARCH ON VALUE (NOT INDEX):
════════════════════════════════════════════════════════════════

    Approach 1 — Generate and sort:
    ├── Space: O(m × n) → up to 9 × 10^8 → IMPOSSIBLE
    ├── Time: O(m × n × log(m × n)) → WAY too slow
    └── ✗ Memory limit exceeded

    Approach 2 — Min-heap (pop k times):
    ├── Start with first row, pop smallest, push next from same row
    ├── Time: O(k × log(m)) → k can be up to 9 × 10^8
    └── ✗ Time limit exceeded for large k

    Approach 3 — Binary search on value:
    ├── Search range: log(m × n) iterations
    ├── Each count: O(m)
    ├── Total: O(m × log(m × n))
    └── ✓ Fast enough!

════════════════════════════════════════════════════════════════
COUNTING VISUALIZATION:
════════════════════════════════════════════════════════════════

    For m=4, n=5, counting values ≤ 7:

    Row 1: 1  2  3  4  5     → min(7//1, 5) = 5 (all ≤ 7)
    Row 2: 2  4  6  [8  10]  → min(7//2, 5) = 3 (2,4,6 ≤ 7)
    Row 3: 3  6  [9  12  15] → min(7//3, 5) = 2 (3,6 ≤ 7)
    Row 4: 4  [8  12  16 20] → min(7//4, 5) = 1 (4 ≤ 7)
                                              ───
                                    Total = 11 values ≤ 7

    [brackets] = values > 7 (not counted)

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    k = 1                    → smallest value is always 1 ✓
    k = m * n                → largest value is always m * n ✓
    m = 1 (single row)       → answer is k ✓
    n = 1 (single column)    → answer is k ✓
    m = 1, n = 1, k = 1     → answer is 1 ✓
    Large m, n (30000×30000) → binary search handles it ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(m × log(m × n))
════════════════════════════════════════════════════════════════

    Binary search range: [1, m × n]
    → log(m × n) iterations

    Each iteration: count_leq runs in O(m)
    → m operations per iteration

    Total: O(m × log(m × n))

    For m = n = 30000:
    → 30000 × log(900000000) ≈ 30000 × 30 ≈ 900,000 operations
    → Very fast! ✓

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(1)
════════════════════════════════════════════════════════════════

    Only a few integer variables (lo, hi, mid, total, i).
    No arrays, no heaps, no additional data structures.

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Binary search on answer (searching value space, not indices)
    Counting function (how many values ≤ X in structured data)
    Multiplication table properties (row i has multiples of i)
    Monotonic function (count_leq is non-decreasing → binary search works)
    Mathematical optimization (O(m) counting per row instead of O(m×n))
"""
