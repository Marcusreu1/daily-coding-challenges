# 1492. The kth Factor of n
# Difficulty: Medium (Follow-up optimized)
# https://leetcode.com/problems/the-kth-factor-of-n/

"""
PROBLEM:
You are given two positive integers `n` and `k`. A factor of an integer `n` is defined as an integer `i` where `n % i == 0`.
Consider a list of all factors of `n` sorted in ascending order, return the kth factor in this list or return -1 if `n` has less than `k` factors.

EXAMPLES:
Input: n = 12, k = 3
Output: 3
(Explanation: Factors list is [1, 2, 3, 4, 6, 12], the 3rd factor is 3.)

Input: n = 7, k = 2
Output: 7
(Explanation: Factors list is [1, 7], the 2nd factor is 7.)

Input: n = 4, k = 4
Output: -1
(Explanation: Factors list is [1, 2, 4], there is no 4th factor.)

CONSTRAINTS:
- 1 <= k <= n <= 1000
- Follow up: Could you solve this problem in less than O(n) complexity?

ALGORITHM LOGIC (O(sqrt(N)) Two-Pass Mirror Search):
1. Divisors of a number are symmetrically paired around its square root.
2. Phase 1 (Left side of the mirror): We iterate `i` from 1 up to floor(sqrt(n)). 
   If `i` is a factor, we decrement `k`. If `k` reaches 0, we return `i` immediately.
3. Phase 2 (Right side of the mirror): If we haven't found the kth factor, it lies in the upper half of the divisors.
   We iterate `i` backwards from floor(sqrt(n)) down to 1.
4. By calculating `n // i` during a backward iteration of the lower half, we mathematically generate the upper half factors in strict ascending order.
5. If `n` is a perfect square, the square root divisor acts as a central pivot. We must use `i * i == n` to `continue` and avoid counting the square root twice during Phase 2.
6. If both loops finish and `k > 0`, the number has fewer than `k` factors, so we return -1.

VISUALIZATION (n = 16, k = 4):
limit = isqrt(16) = 4.

Phase 1 (Ascending 1 to 4):
i=1: valid! k=3
i=2: valid! k=2
i=3: invalid
i=4: valid! k=1

Phase 2 (Descending 4 to 1):
i=4: i*i == 16. PERFECT SQUARE. Skip to avoid double counting!
i=3: invalid
i=2: valid! k=0. -> We hit k=0! Return `16 // 2` -> 8. ✓

The 4th factor of 16 is indeed 8 (Factors: 1, 2, 4, 8, 16).
"""

import math

# STEP 1: Calculate the mathematical square root boundary
# STEP 2: Iterate ascendingly for the lower-bound divisors
# STEP 3: Iterate descendingly for the upper-bound divisors, skipping perfect square collision
# STEP 4: Mathematically derive the upper bounds using integer division (n // i)
# STEP 5: Return -1 if all factors are exhausted without fulfilling `k`

class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        
        limit = math.isqrt(n)
        
        # Phase 1: Scan factors up to the square root
        for i in range(1, limit + 1):
            if n % i == 0:
                k -= 1
                if k == 0:
                    return i
                    
        # Phase 2: Scan the mirrored factors above the square root
        for i in range(limit, 0, -1):
            
            # Prevent double-counting the pivot of a perfect square
            if i * i == n:
                continue
                
            if n % i == 0:
                k -= 1
                if k == 0:
                    # Generate the ascending upper factors by dividing downwards
                    return n // i
                    
        # If both loops conclude, n doesn't have k factors
        return -1

"""
WHY EACH PART:
- limit = math.isqrt(n): Constrains our physical loop to O(sqrt(n)). For N=1000, we only do a maximum of 31 loops per phase instead of 1000 loops.
- range(limit, 0, -1): Reversing the loop allows us to generate the upper-half factors in the correct ascending order without ever sorting an array.
- if i * i == n: continue: If `n` is 16, Phase 1 already decremented `k` when finding 4. If we don't skip 4 in Phase 2, we would falsely decrement `k` again.

HOW IT WORKS (Example: n = 12, k = 5):
limit = isqrt(12) = 3.
Phase 1:
i=1: k=4
i=2: k=3
i=3: k=2
Phase 2:
i=3: 12%3==0. k=1. (n//i = 4). No return.
i=2: 12%2==0. k=0. Return 12//2 = 6. ✓

KEY TECHNIQUE:
- Mathematics (Square Root Optimization)
- Space Optimization (O(1) Memory Constant Generation)
- Symmetrical traversal

EDGE CASES:
- k is greater than total factors (e.g., n=4, k=4): Loops finish, `k` never hits 0. Safely returns -1. ✓
- n is a prime number (e.g., n=7, k=2): Phase 1 triggers on 1. Phase 2 triggers on 1 (returning 7//1 = 7). ✓

TIME COMPLEXITY: O(sqrt(N)) - The algorithm guarantees traversing a maximum of `2 * sqrt(N)` iterations, meeting the advanced follow-up criteria of LeetCode.
SPACE COMPLEXITY: O(1) - No dynamic arrays, lists, or hash sets are used. We only track `limit`, `i`, and `k` in memory, achieving strict constant space regardless of input size.
"""
