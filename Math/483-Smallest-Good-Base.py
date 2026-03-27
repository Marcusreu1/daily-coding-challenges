"""
483. Smallest Good Base
Difficulty: Hard
https://leetcode.com/problems/smallest-good-base/

PROBLEM:
Given an integer n represented as a string, return the smallest "good base"
of n. A good base k (k ≥ 2) is a base where n has a representation of
ALL ONES: 111...1 in base k.

EXAMPLES:
Input: n = "13"            → Output: "3"
    13 = 111 in base 3 (1 + 3 + 9 = 13)

Input: n = "4681"          → Output: "8"
    4681 = 11111 in base 8 (1 + 8 + 64 + 512 + 4096 = 4681)

Input: n = "1000000000000000000" → Output: "999999999999999999"
    10^18 = 11 in base (10^18 - 1)

CONSTRAINTS:
    n is an integer in range [3, 10^18]
    n is given as a string

KEY INSIGHT:
111...1 (m ones) in base k = 1 + k + k² + ... + k^(m-1) = (k^m - 1)/(k - 1)

Smaller k → larger m (more ones). So iterate m from LARGEST to SMALLEST.
For each m, compute k ≈ n^(1/(m-1)) and verify the geometric sum.
First valid k found is the smallest.

CHALLENGES:
    n can be up to 10^18 — very large
    Floating point precision for computing roots
    Understanding the inverse relationship between k and m
    Proving that iterating m downward gives smallest k first

MATHEMATICAL FOUNDATION:
    n = 1 + k + k² + ... + k^(m-1) = (k^m - 1) / (k - 1)
    
    For fixed n: larger m → smaller k (inverse relationship)
    Max m: when k=2 → m ≤ log₂(n+1) ≈ 60
    Min m: m=2 → k = n-1 (always works, but largest k)

SOLUTION:
    1. Try m from largest (log₂n) down to 3
    2. For each m, compute k = floor(n^(1/(m-1)))
    3. Verify geometric sum = n (check k and k+1 for float safety)
    4. First valid k is the answer (smallest possible)
    5. Fallback: k = n-1 (m=2 always works)
"""

# STEP 1: Convert string to integer
# STEP 2: Try m from largest to smallest
# STEP 3: For each m, compute and verify k
# STEP 4: Fallback to k = n-1 if no better base found

class Solution:
    def smallestGoodBase(self, n: str) -> str:

        num = int(n)                                                     # Convert string to integer

        max_m = num.bit_length()                                         # Max possible m (when k=2)

        for m in range(max_m, 2, -1):                                    # Try m from largest to 3
            k = int(num ** (1.0 / (m - 1)))                              # Approximate k = n^(1/(m-1))

            if k < 2:                                                    # Base must be ≥ 2
                continue

            if (k ** m - 1) // (k - 1) == num:                           # Verify: geometric sum = n?
                return str(k)

            k += 1                                                       # Try k+1 (float precision safety)
            if (k ** m - 1) // (k - 1) == num:                           # Verify with k+1
                return str(k)

        return str(num - 1)                                              # Fallback: m=2, k=n-1 always works

"""
WHY EACH PART:

    num = int(n): Problem gives n as string, need integer for math
    max_m = num.bit_length(): log₂(n)+1, maximum ones when k=2
    range(max_m, 2, -1): Try m from largest to 3 (m=2 is fallback)
    int(num ** (1.0/(m-1))): Approximate k via (m-1)-th root of n
    if k < 2: continue: Base must be at least 2
    (k**m - 1) // (k-1): Geometric sum formula: 1+k+k²+...+k^(m-1)
    == num: Does this base/length combination exactly produce n?
    k += 1: Float rounding might give k-1 instead of k, check both
    return str(num-1): m=2 means n = 1+k → k=n-1 (always valid)

HOW IT WORKS (Example: n = "13"):

    num = 13, max_m = 4 (bit_length of 13 = 1101)

    m=4: k = ⌊13^(1/3)⌋ = ⌊2.35⌋ = 2
    ├── (2⁴-1)/(2-1) = 15/1 = 15 ≠ 13 → SKIP
    ├── k+1=3: (3⁴-1)/(3-1) = 80/2 = 40 ≠ 13 → SKIP
    └── Continue

    m=3: k = ⌊13^(1/2)⌋ = ⌊3.60⌋ = 3
    ├── (3³-1)/(3-1) = 26/2 = 13 = num ✓
    └── return "3"

    Result: "3" (13 = 111 in base 3) ✓

HOW IT WORKS (Example: n = "4681"):

    num = 4681, max_m = 13

    m=13: k = ⌊4681^(1/12)⌋ = 2
    ├── (2¹³-1)/1 = 8191 ≠ 4681 → SKIP
    └── Continue

    m=12 to m=6: various k values, none match → SKIP

    m=5: k = ⌊4681^(1/4)⌋ = ⌊8.27⌋ = 8
    ├── (8⁵-1)/(8-1) = 32767/7 = 4681 = num ✓
    └── return "8"

    Result: "8" (4681 = 11111 in base 8)
    Verification: 1 + 8 + 64 + 512 + 4096 = 4681 ✓

WHY ITERATE m DOWNWARD (LARGEST FIRST):

    For fixed n, larger m means smaller k:
    ├── n = 13, m=3: k=3    (111 in base 3)
    ├── n = 13, m=2: k=12   (11 in base 12)
    └── Smaller k comes from larger m!

    By trying m from max to min:
    ├── m=max: find smallest possible k
    ├── m=max-1: next smallest k
    ├── ...
    └── First k found IS the answer (smallest base)

    This is because n^(1/(m-1)) is DECREASING as m increases:
    ├── m=60: n^(1/59) ≈ small k
    ├── m=3:  n^(1/2) = √n ≈ large k  
    └── m=2:  k = n-1 ≈ huge k

WHY THE GEOMETRIC SUM FORMULA:

    1 + k + k² + ... + k^(m-1)
    
    This is a geometric series with ratio k:
    Sum = (k^m - 1) / (k - 1)
    
    Example: 1 + 3 + 9 = (27-1)/(3-1) = 26/2 = 13 ✓

    We use this to verify: does this (k, m) pair produce exactly n?

WHY k+1 CHECK (FLOATING POINT SAFETY):

    n^(1/(m-1)) might be slightly imprecise:
    
    True value: k = 8.0000000000
    Float might give: 7.9999999998 → int() = 7 (WRONG!)
    
    By also checking k+1 = 8, we catch this case.
    
    Example: n = 4681, m = 5
    ├── 4681^(1/4) might give 8.27... or 7.99...
    ├── int() gives 8 or 7
    ├── If 7: check 7 (fail), check 8 (success!) ✓
    └── Either way, we find k=8

WHY m=2 ALWAYS WORKS (FALLBACK):

    For m=2: n = 1 + k → k = n - 1
    
    13 = 1 + 12 → "11" in base 12 ✓
    4681 = 1 + 4680 → "11" in base 4680 ✓
    
    This ALWAYS produces a valid "good base",
    just not necessarily the smallest one.
    
    If no m ≥ 3 works, we return n-1 as the answer.

WHY bit_length() FOR max_m:

    Smallest possible base is k=2.
    With k=2: n = 2^m - 1 → m = log₂(n+1)
    
    Python's bit_length() ≈ ⌊log₂(n)⌋ + 1
    
    Example: 13.bit_length() = 4 (1101 in binary)
    Max m with k=2: 2⁴-1 = 15 ≥ 13, so m=4 is possible range
    
    For n = 10^18: bit_length ≈ 60
    So we check at most ~58 values of m → very fast!

TOTAL ITERATIONS ANALYSIS:

    Outer loop: ~60 iterations (m from 60 to 3)
    Each iteration: 
    ├── One exponentiation: O(1)
    ├── One power: O(m × log(k)) → fast with Python big ints
    └── One division + comparison: O(1)
    
    Total: ~60 iterations with simple math → essentially O(1)!

GEOMETRIC SUM INTUITION:

    Base 10:  111 = 1 + 10 + 100 = 111
    Base 3:   111 = 1 + 3 + 9 = 13
    Base 8:   11111 = 1 + 8 + 64 + 512 + 4096 = 4681
    Base k:   111...1 (m digits) = (k^m - 1) / (k - 1)

    "All ones" means each digit contributes exactly one power of k.
    Like "111" in decimal = one hundred + one ten + one unit.

EDGE CASES:

    n = "3": 3 = 11 in base 2 → return "2" ✓
    n = "7": 7 = 111 in base 2 → return "2" ✓
    n = "4": 4 = 11 in base 3 → return "3" ✓
    Large n (10^18): At most ~60 iterations → fast ✓
    n where only m=2 works: returns n-1 ✓
    Perfect geometric sum: Exact match found ✓
    Float precision edge: k+1 check catches it ✓

TIME COMPLEXITY: O(log²(n))
    Outer loop: O(log n) iterations (bit_length)
    Each iteration: O(log n) for exponentiation
    Total: O(log²(n)), effectively constant for n ≤ 10^18

SPACE COMPLEXITY: O(1)
    Only a few integer variables
    No data structures needed

CONCEPTS USED:
    Geometric series (1 + k + k² + ... + k^(m-1))
    Inverse relationship between base and digit count
    Root computation for candidate base
    Floating point safety (check k and k+1)
    Bit manipulation (bit_length for log₂)
    Mathematical proof of optimality (largest m → smallest k)
    Fallback guarantee (m=2 always works)
"""
