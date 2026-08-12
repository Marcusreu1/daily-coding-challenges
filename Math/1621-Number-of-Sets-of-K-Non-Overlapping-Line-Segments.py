# 1621. Number of Sets of K Non-Overlapping Line Segments
# Difficulty: Medium
# https://leetcode.com/problems/number-of-sets-of-k-non-overlapping-line-segments/

"""
PROBLEM:
Given `n` points on a 1-D plane, where the points are numbered from 0 to n-1. 
You are given an integer `k`. Find the number of ways to draw exactly `k` non-overlapping line segments.
Two segments are allowed to share a single endpoint (touching is permitted).
Return the answer modulo 10^9 + 7.

EXAMPLES:
Input: n = 4, k = 2
Output: 5
(Explanation: The 5 valid sets of 2 segments are:
1. [0,1] and [1,2]
2. [0,1] and [1,3]
3. [0,1] and [2,3]
4. [0,2] and [2,3]
5. [1,2] and [2,3])

Input: n = 3, k = 1
Output: 3
(Explanation: The 3 valid segments are [0,1], [1,2], and [0,2].)

Input: n = 30, k = 7
Output: 796297179

CONSTRAINTS:
- 2 <= n <= 1000
- 1 <= k <= n-1

ALGORITHM LOGIC (Combinatorial Bijection):
1. A standard Dynamic Programming approach leads to O(N^2) or O(N*K) time complexity, which is overly complex.
2. We can solve this with pure combinatorics by eliminating the "endpoints can touch" exception.
3. To strictly enforce separation so we can use standard combinations, we inject virtual "buffer" points between the segments.
4. If we have `k` segments, there are `k - 1` gaps between them. We add `k - 1` extra points to our total `n` points.
5. Our new expanded domain has `n + k - 1` points.
6. In this expanded domain, touching is mathematically impossible. Thus, choosing any `2k` points natively perfectly forms `k` separated segments.
7. The absolute mathematical answer is simply the Binomial Coefficient: (n + k - 1) Choose (2k).

VISUALIZATION (n = 4, k = 2):
Original points = 4.
Segments to pick = 2 (requires 4 points total).
Gaps to inject = 1.
Expanded domain = 4 + 1 = 5 points.

Formula: 5 Choose 4 = 5.
Result is 5. (Matches the manual counting exactly!). ✓
"""

import math

# STEP 1: Define the target modulo to prevent integer overflow bounds
# STEP 2: Compute the expanded spatial domain `N` (n + k - 1)
# STEP 3: Compute the required discrete points `K` (2 * k)
# STEP 4: Calculate the combinatorial mathematically and apply the modulo

class Solution:
    def numberOfSets(self, n: int, k: int) -> int:
        
        MOD = 10**9 + 7
        
        # Combinatorial Bijection Mapping
        expanded_points = n + k - 1
        points_to_choose = 2 * k
        
        # Calculate (expanded_points Choose points_to_choose)
        total_ways = math.comb(expanded_points, points_to_choose)
        
        return total_ways % MOD

"""
WHY EACH PART:
- n + k - 1: Translates the flexible "touching allowed" geometry into strict "touching forbidden" geometry.
- 2 * k: Because 1 segment strictly requires exactly 2 endpoints.
- math.comb(): Python's built-in combinatorics engine (written in highly optimized C). It inherently handles the heavy factorial math `N! / (K! * (N-K)!)` infinitely faster than a manual loop.
- % MOD: Strictly required by the problem to maintain standard 32/64-bit integer limits for competitive programming output.

HOW IT WORKS (Example: n = 3, k = 1):
expanded_points = 3 + 1 - 1 = 3
points_to_choose = 2 * 1 = 2
math.comb(3, 2) = 3.
Returns 3. ✓

KEY TECHNIQUE:
- Combinatorics (Binomial Coefficients)
- Bijective Mapping (Space Transformation)
- O(1) Mathematical Abstraction over DP

EDGE CASES:
- k is maximum possible (k = n - 1): Expanded points = `n + n - 2`. Points to choose = `2n - 2`. `math.comb(2n-2, 2n-2)` evaluates safely to 1. ✓
- Massive inputs (n = 1000): Python's `math.comb` processes 2000! instantaneously, no memory exhaustion or deep recursion crashes like DP. ✓

TIME COMPLEXITY: O(K) - The combinatorial function technically executes in O(min(K, N-K)) time to compute the factorial products, which practically takes less than a millisecond given the maximum bound of N=1000. Effectively O(1) in the context of competitive programming runtime limits.
SPACE COMPLEXITY: O(1) - Zero multidimensional DP arrays are built. Complete mathematical evaluation using minimal constant memory.
"""
