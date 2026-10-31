# 2338. Count the Number of Ideal Arrays
# Difficulty: Hard
# https://leetcode.com/problems/count-the-number-of-ideal-arrays/

"""
PROBLEM:
You are given two integers n and maxValue, which are used to describe an ideal array.
A 1-indexed integer array arr of length n is considered ideal if:
- 1 <= arr[i] <= maxValue, for all 1 <= i <= n.
- arr[i] divides arr[i+1], for all 1 <= i < n.
Return the number of distinct ideal arrays of length n. Since the answer may be very large, return it modulo 10^9 + 7.

CONSTRAINTS:
- 1 <= n, maxValue <= 10^4

MATH RULES (HARMONIC SERIES & COMBINATORICS DP):
1. State Compression: Any strictly increasing ideal sequence doubles its value at minimum. Thus, the absolute maximum length of a strictly increasing chain ending in 10^4 is 14 (since 2^13 = 8192). We can completely collapse the N-length DP down to just 14 levels.
2. Expansions via Combinations: If we find a strictly increasing sequence of length 'k', we can expand it to length 'n' by repeating elements. This mathematically maps to choosing (k - 1) transition jumps across (n - 1) available slots, calculated instantaneously via Binomial Coefficients (n - 1 choose k - 1).
3. Harmonic Sieve: To find multiples for the DP transitions, we iterate in steps of 'x' instead of checking all numbers. This reduces transition times to the Harmonic series sum O(M log M).
"""

import math

# STEP 1: Initialize the DP array to track strictly increasing chains ending at each value.
# STEP 2: Use a while loop constrained by the physical limit of multiples (approx 14 steps).
# STEP 3: Multiply the total valid chains of current length 'k' by the combinatorics distribution formula.
# STEP 4: Build the next DP state using a Harmonic jump traversal (x * 2, x * 3...).
# STEP 5: Add up the total modulo 10^9 + 7 and return.

class Solution:
    def idealArrays(self, n: int, maxValue: int) -> int:
        
        MOD = 10**9 + 7
        
        # dp[x] represents the number of strictly increasing sequences ending at x
        dp = [1] * (maxValue + 1)
        dp[0] = 0 # 1-indexed, ignore 0
        
        total_ideal_arrays = 0
        k = 1
        
        # k bounded safely by min(n, 14) organically because dp exhausts to 0 after ~14 iterations
        while k <= n:
            
            # S_k is the total number of purely strictly increasing sequences of length k
            S_k = sum(dp) % MOD
            
            # Short-circuit if no more strictly increasing chains are mathematically possible
            if S_k == 0:
                break
                
            # Expand the strictly increasing chain to size N using native C-optimized combinations
            combinations = math.comb(n - 1, k - 1) % MOD
            
            # Add to the global total
            total_ideal_arrays = (total_ideal_arrays + S_k * combinations) % MOD
            
            # Compute the strictly increasing chains of length k + 1
            next_dp = [0] * (maxValue + 1)
            
            for x in range(1, maxValue + 1):
                if dp[x] > 0:
                    # Harmonic jump loop: step by 'x' to visit only direct multiples natively
                    for y in range(x * 2, maxValue + 1, x):
                        next_dp[y] = (next_dp[y] + dp[x]) % MOD
                        
            dp = next_dp
            k += 1
            
        return total_ideal_arrays

"""
WHY EACH PART:
- math.comb(n - 1, k - 1): Bypasses the need to precompute modular inverse factorials. Python's native BigInt handling calculates this purely in C memory practically instantly, even for 10000 C 14.
- range(x * 2, maxValue + 1, x): The Harmonic sieve trick. Instead of division testing N elements, it literally steps through memory exclusively landing on perfect multiples.
- if S_k == 0: break: Protects the algorithm from running N times (10,000). It acts as an organic halt that guarantees execution in exactly 14 steps regardless of how large N is.

KEY TECHNIQUE:
- Combinatorial State Explosion: Compressing redundant data structures (repeated integers) into mathematical formulas (nCr) to drop O(N*M) bounds into O(M log M).

EDGE CASES:
- n = 1: Loop runs once. math.comb(0, 0) == 1. Returns exactly `maxValue`.
- Small maxValue (e.g., 2): The multiples exhaust extremely fast (only 1 -> 2). Breaks optimally at k = 3.

TIME COMPLEXITY: O(maxValue * log(maxValue) * log_2(maxValue)) - Generating the next states uses the Harmonic sum bounded to M log M. It executes at most 14 times (log2(M)). Total operations ~ 1.2 million. Exceedingly fast for a Hard problem.
SPACE COMPLEXITY: O(maxValue) - We strictly allocate 1D arrays of size 10000, achieving O(M) and completely bypassing the O(N * M) 2D matrix explosion.
"""
