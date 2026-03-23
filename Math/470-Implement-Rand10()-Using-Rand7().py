"""
470. Implement Rand10() Using Rand7()
Difficulty: Medium
https://leetcode.com/problems/implement-rand10-using-rand7/

PROBLEM:
Given the API rand7() which generates a uniform random integer in
the range [1, 7], write a function rand10() which generates a
uniform random integer in the range [1, 10].

You can only call the API rand7(), no other random functions.

EXAMPLES:
Input: n = 1  → Output: [2]     (one call, random 1-10)
Input: n = 3  → Output: [3,8,1] (three calls, each random 1-10)

CONSTRAINTS:
    1 <= n <= 10^5
    rand7() is predefined
    Each value [1,10] must have equal probability

KEY INSIGHT:
Use two rand7() calls to generate a uniform number in [1, 49].
    idx = (rand7()-1) × 7 + rand7()

Accept values [1, 40] → map to [1, 10] via modulo.
Reject values [41, 49] → try again (rejection sampling).

40 is the largest multiple of 10 that fits in [1, 49],
giving each output exactly 4/40 = 1/10 probability.

CHALLENGES:
    Can't just sum or mod rand7() (non-uniform distribution)
    Need EXACTLY uniform probability for each output
    Must handle the 9 "wasted" values (41-49) correctly
    Understanding why rejection sampling preserves uniformity

TECHNIQUE: REJECTION SAMPLING
    1. Generate uniform number in a LARGER range
    2. Accept if it maps cleanly to target range
    3. Reject and retry otherwise
    Conditional on acceptance, distribution is perfectly uniform.

SOLUTION:
    1. Generate idx in [1, 49] using two rand7() calls
    2. If idx ≤ 40: return (idx-1) % 10 + 1
    3. If idx > 40: repeat from step 1
"""

# STEP 1: Generate uniform number in [1, 49]
# STEP 2: Accept if ≤ 40, reject and retry otherwise
# STEP 3: Map accepted value to [1, 10]

class Solution:
    def rand10(self) -> int:

        while True:                                                      # Retry until we get a valid value
            row = rand7() - 1                                            # Row: 0 to 6
            col = rand7()                                                # Col: 1 to 7
            idx = row * 7 + col                                          # Uniform in [1, 49]

            if idx <= 40:                                                # Accept: maps cleanly to [1, 10]
                return (idx - 1) % 10 + 1                                # Map to [1, 10]

"""
WHY EACH PART:

    while True: Rejection sampling may need multiple attempts
    row = rand7() - 1: Shift to 0-6 for row calculation
    col = rand7(): Column stays 1-7
    idx = row * 7 + col: 2D coordinates → 1D index, range [1, 49]
    if idx <= 40: Only accept values that map evenly to 10 outcomes
    (idx-1) % 10 + 1: Map [1,40] → [1,10] with 4 values per output
    No else/break needed: while True + return handles the loop

HOW IT WORKS (Example: generating rand10()):

    Attempt 1:
    ├── rand7() = 4 → row = 3
    ├── rand7() = 2 → col = 2
    ├── idx = 3×7 + 2 = 23
    ├── 23 ≤ 40 → ACCEPT
    ├── (23-1) % 10 + 1 = 22%10 + 1 = 2+1 = 3
    └── return 3 ✓

    Attempt with rejection:
    ├── rand7() = 7 → row = 6
    ├── rand7() = 7 → col = 7
    ├── idx = 6×7 + 7 = 49
    ├── 49 > 40 → REJECT, try again
    │
    ├── rand7() = 2 → row = 1
    ├── rand7() = 5 → col = 5
    ├── idx = 1×7 + 5 = 12
    ├── 12 ≤ 40 → ACCEPT
    ├── (12-1) % 10 + 1 = 11%10 + 1 = 1+1 = 2
    └── return 2 ✓

WHY (rand7()-1) × 7 + rand7() IS UNIFORM:

    Row = rand7()-1: {0,1,2,3,4,5,6} each with P = 1/7
    Col = rand7():   {1,2,3,4,5,6,7} each with P = 1/7

    Since row and col are INDEPENDENT:
    P(row=r, col=c) = 1/7 × 1/7 = 1/49

    idx = r×7 + c produces each value in [1,49] exactly once:
    ├── r=0: idx = 1,2,3,4,5,6,7
    ├── r=1: idx = 8,9,10,11,12,13,14
    ├── ...
    └── r=6: idx = 43,44,45,46,47,48,49

    Each of 49 values has probability 1/49 ✓

THE MAPPING TABLE (idx → output):

    idx:  1  2  3  4  5  6  7  8  9  10  → output: 1  2  3  4  5  6  7  8  9  10
    idx: 11 12 13 14 15 16 17 18 19  20  → output: 1  2  3  4  5  6  7  8  9  10
    idx: 21 22 23 24 25 26 27 28 29  30  → output: 1  2  3  4  5  6  7  8  9  10
    idx: 31 32 33 34 35 36 37 38 39  40  → output: 1  2  3  4  5  6  7  8  9  10
    idx: 41 42 43 44 45 46 47 48 49      → REJECTED

    Each output (1-10) has exactly 4 accepted values → P = 4/49 each
    Conditional on acceptance: P = (4/49) / (40/49) = 4/40 = 1/10 ✓

WHY REJECT 41-49 (NOT KEEP THEM):

    If we mapped 41-49 to 1-9:
    ├── Output 1: values {1,11,21,31,41} → 5 values
    ├── Output 10: values {10,20,30,40}  → 4 values
    ├── P(1) = 5/49 ≠ P(10) = 4/49
    └── NOT uniform! ✗

    By rejecting 41-49, we guarantee each output has
    EXACTLY 4 generating values → perfectly uniform ✓

WHY 40 AND NOT ANOTHER NUMBER:

    40 = largest multiple of 10 that is ≤ 49
    
    Could we use 30? → accept [1,30], reject [31,49]
    ├── Works! But rejects 19 values instead of 9
    ├── P(accept) = 30/49 ≈ 61.2% (worse)
    └── More wasted rand7() calls

    40 maximizes acceptance rate:
    ├── P(accept) = 40/49 ≈ 81.6%
    └── Minimum expected calls to rand7()

PROBABILITY ANALYSIS:

    P(accept on one try) = 40/49 ≈ 0.816
    P(reject on one try) = 9/49  ≈ 0.184

    Expected attempts = 1 / (40/49) = 49/40 = 1.225
    Expected rand7() calls = 2 × 1.225 ≈ 2.45

    P(need 1 attempt) = 40/49         ≈ 81.6%
    P(need 2 attempts) = 9/49 × 40/49 ≈ 15.0%
    P(need 3 attempts) = (9/49)² × 40/49 ≈ 2.8%
    P(need 4+ attempts) ≈ 0.6%

    Geometric distribution: very fast in practice ✓

WHY NOT JUST USE rand7() + rand7() % 10:

    rand7() + rand7() ranges from 2 to 14
    ├── P(2) = 1/49 (only 1+1)
    ├── P(7) = 6/49 (many combinations)
    ├── P(8) = 7/49 (most combinations)
    └── NOT uniform → violates the requirement ✗

    Sum of random variables creates a TRIANGULAR distribution,
    not a uniform one. Only multiplication-based indexing works.

GENERAL TECHNIQUE (randN from randM):

    To generate randN() from randM():
    1. Find k such that M^k ≥ N (use k calls to randM)
    2. Generate uniform [1, M^k]
    3. Accept if ≤ largest multiple of N that fits
    4. Map to [1, N] via modulo

    rand10 from rand7: k=2, 7²=49, accept ≤ 40
    rand7 from rand2:  k=3, 2³=8,  accept ≤ 7

EDGE CASES:

    All 10 outputs possible: Each has P = 1/10 ✓
    Multiple calls: Each independent ✓
    Worst case: Many rejections (unlikely but possible) ✓
    Loop terminates: P(infinite loop) = lim (9/49)^n = 0 ✓
    Large n (10^5 calls): ~2.45 rand7() calls each → ~245K total ✓

TIME COMPLEXITY: O(1) expected
    Expected 1.225 iterations per call
    Each iteration: O(1) (two rand7() calls + arithmetic)
    Geometric distribution → expected constant time

SPACE COMPLEXITY: O(1)
    Only a few variables: row, col, idx

CONCEPTS USED:
    Rejection sampling
    Uniform distribution generation
    2D to 1D coordinate mapping
    Probability theory (geometric distribution)
    Modular arithmetic for range mapping
    Independence of random variables
"""
