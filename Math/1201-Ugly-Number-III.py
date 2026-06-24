# 1201. Ugly Number III
# Difficulty: Medium
# https://leetcode.com/problems/ugly-number-iii/

"""
PROBLEM:
Write a program to find the n-th ugly number.
Ugly numbers are positive integers which are divisible by `a` or `b` or `c`.

EXAMPLES:
Input: n = 3, a = 2, b = 3, c = 5
Output: 4
Explanation: The ugly numbers are 2, 3, 4, 5, 6, 8, 9, 10... The 3rd is 4.

Input: n = 4, a = 2, b = 3, c = 4
Output: 6
Explanation: The ugly numbers are 2, 3, 4, 6, 8, 9, 10, 12... The 4th is 6.

CONSTRAINTS:
- 1 <= n, a, b, c <= 10^9
- 1 <= a * b * c <= 10^18
- It is guaranteed that the result will be in range [1, 2 * 10^9].

ALGORITHMIC INTUITION (THE "TRICK"):
The naive approach is to loop from 1 upwards, checking if every number is divisible 
by a, b, or c until we find 'n' ugly numbers. But since n can be 10^9, this O(N) 
approach causes a Time Limit Exceeded (TLE) error.

Instead of GENERATING the numbers, we guess the answer using Binary Search.
If we pick a random number K, can we instantly know how many ugly numbers exist from 1 to K?
Yes, using Set Theory's "Inclusion-Exclusion Principle":
Count(K) = (K//a) + (K//b) + (K//c) 
           - (K//lcm(a,b)) - (K//lcm(a,c)) - (K//lcm(b,c)) 
           + (K//lcm(a,b,c))

If Count(K) >= n, our guess K might be the answer, or the answer is smaller. (Search Left)
If Count(K) < n, our guess K is too small. (Search Right)
"""

# STEP 1: Define a helper function to calculate LCM (Least Common Multiple).
# STEP 2: Precalculate the LCMs for (a,b), (a,c), (b,c), and (a,b,c).
# STEP 3: Define the Inclusion-Exclusion counting function.
# STEP 4: Set Binary Search boundaries: left = 1, right = 2 * 10^9.
# STEP 5: Run Binary Search. Adjust left/right based on the count function.
# STEP 6: Return the left boundary when the search converges.

import math

class Solution:
    def nthUglyNumber(self, n: int, a: int, b: int, c: int) -> int:
        
        # Step 1: Helper for Least Common Multiple
        def lcm(x: int, y: int) -> int:
            return (x * y) // math.gcd(x, y)
            
        # Step 2: Precompute all necessary LCM intersections
        ab = lcm(a, b)
        ac = lcm(a, c)
        bc = lcm(b, c)
        abc = lcm(ab, c)
        
        # Step 3: Count how many ugly numbers are <= k
        def count_ugly_up_to(k: int) -> int:
            return (
                (k // a) + (k // b) + (k // c)
                - (k // ab) - (k // ac) - (k // bc)
                + (k // abc)
            )
            
        # Step 4: Binary search boundaries (per constraints, max answer is 2*10^9)
        left = 1
        right = 2 * 10**9
        
        # Step 5: Binary Search on the answer space
        while left < right:
            mid = left + (right - left) // 2
            
            if count_ugly_up_to(mid) >= n:
                right = mid    # The answer could be `mid` or smaller
            else:
                left = mid + 1 # `mid` is too small, answer must be larger
                
        # Step 6: Left and right converge to the exact n-th ugly number
        return left

"""
WHY EACH PART:
- lcm helper: Python's math.lcm is only available in 3.9+. Using (x*y)//gcd is mathematically robust and universally compatible.
- right = 2 * 10**9: We don't need to search to infinity. LeetCode guarantees the answer fits in standard 32-bit integer limits.
- count_ugly_up_to(mid) >= n: We use `>=` because multiple numbers can yield the same count (e.g., if mid is not an ugly number itself). The binary search naturally compresses to the FIRST number that achieves the count 'n', which is guaranteed to be an ugly number.

HOW IT WORKS (Example: n=3, a=2, b=3, c=5):
LCMs: ab=6, ac=10, bc=15, abc=30

Binary Search:
Initial: L = 1, R = 2*10^9. 
... (After many iterations skipping ahead) ...
Let's look at boundaries around the answer:

Guess mid = 3:
├── count(3) = (3//2) + (3//3) + (3//5) - ... = 1 + 1 + 0 = 2 ugly numbers
└── 2 < n (3). So L = 4.

Guess mid = 4:
├── count(4) = (4//2) + (4//3) + (4//5) - (4//6)... = 2 + 1 + 0 - 0 = 3 ugly numbers
└── 3 >= n (3). So R = 4.

Converged at L = 4. Return 4. ✓

TIME COMPLEXITY: O(log(2 * 10^9)) - The binary search halves the search space each time. It takes exactly 31 iterations to find the answer. Extremely fast!
SPACE COMPLEXITY: O(1) - Only a few variables for boundaries and LCMs are stored.

CONCEPTS USED:
- Binary Search (On Answer Space)
- Number Theory (GCD / LCM)
- Set Theory (Inclusion-Exclusion Principle)
"""
