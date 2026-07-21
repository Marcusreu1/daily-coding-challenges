# 1362. Closest Divisors
# Difficulty: Medium
# https://leetcode.com/problems/closest-divisors/

"""
PROBLEM:
Given an integer `num`, find the closest two integers in absolute difference whose product equals `num + 1` or `num + 2`.
Return the two integers in any order.

EXAMPLES:
Input: num = 8
Output: [3, 3]
(Explanation: For num + 1 = 9, the closest divisors are 3 & 3, for num + 2 = 10, the closest divisors are 2 & 5. 
The absolute difference is min(|3-3|, |2-5|) = 0. Therefore, [3, 3] is returned.)

Input: num = 123
Output: [5, 25]
(Explanation: 123 + 1 = 124, 123 + 2 = 125. 
Divisors of 124 closest are [4, 31] (Diff 27). 
Divisors of 125 closest are [5, 25] (Diff 20). 
Return [5, 25].)

Input: num = 999
Output: [40, 25]
(Explanation: 999 + 1 = 1000. Closest divisors are 25 & 40.)

CONSTRAINTS:
- 1 <= num <= 10^9

ALGORITHM LOGIC (Square Root Optimization & Greedy Search):
1. The problem asks for the minimum absolute difference between two divisors of a number N.
2. Mathematically, the difference between divisors a and b (where a * b = N) is minimized when they are as close to sqrt(N) as possible.
3. Instead of starting from 1 and checking all divisors (which is slow for 10^9), we can start exactly at floor(sqrt(num + 2)) and iterate downwards.
4. The first exact divisor we encounter moving down from the square root is GUARANTEED to form the closest divisor pair.
5. We check both `num + 1` and `num + 2` in the same loop to avoid doing two separate searches.
6. We return the first valid pair immediately.

VISUALIZATION (num = 8):
Targets: 9 and 10.
Start `i` at floor(sqrt(10)) = 3.

Loop Iteration 1 (i = 3):
Check num + 1 (9): 9 % 3 == 0 ? True!
Return [3, 9 // 3] -> [3, 3]. ✓
(No need to check 10, because starting from sqrt guarantees this is the absolute minimum difference).
"""

import math

# STEP 1: Import the math module to use `isqrt` for exact integer square roots
# STEP 2: Calculate the starting point as the integer square root of `num + 2`
# STEP 3: Loop backwards from this starting point down to 1
# STEP 4: In each iteration, check if the current number evenly divides `num + 1`
# STEP 5: If it does, instantly return the pair [i, (num + 1) // i]
# STEP 6: If not, check if it evenly divides `num + 2` and return [i, (num + 2) // i] if true

class Solution:
    def closestDivisors(self, num: int) -> list[int]:
        
        # Start at the square root of the larger target and count backwards down to 1
        start_point = math.isqrt(num + 2)
        
        for i in range(start_point, 0, -1):
            
            # Check if `i` is a divisor of num + 1
            if (num + 1) % i == 0:
                return [i, (num + 1) // i]
            
            # Check if `i` is a divisor of num + 2
            if (num + 2) % i == 0:
                return [i, (num + 2) // i]

"""
WHY EACH PART:
- math.isqrt(num + 2): `isqrt` is an optimized C-level function in Python that safely returns the floor of the square root as an integer, avoiding floating-point precision anomalies.
- range(start_point, 0, -1): The `-1` step allows us to perform a greedy search. By starting at the optimal center of factors and walking away, the first success is factually the best answer.
- return inside the loop: This acts as our early exit. Since the answer mathematically exists (at worst, [1, num+1]), the loop will always find a return and terminate, saving immense processing time.
- // (Integer Division): Ensures the returned counterpart is strictly an integer type, satisfying the type hints.

HOW IT WORKS (Example: num = 123):
Target 1: 124. Target 2: 125.
start_point = isqrt(125) = 11.

i = 11: 124%11!=0, 125%11!=0
i = 10: 124%10!=0, 125%10!=0
...
i = 5: 124%5!=0, 125%5 == 0 -> True!
Return [5, 125 // 5] = [5, 25]. ✓

KEY TECHNIQUE:
- Mathematical Number Theory (Factor distribution around square roots).
- Early Exit optimization (Greedy backward tracking).

EDGE CASES:
- num = 1: Targets are 2 and 3. Start at isqrt(3) = 1. `i = 1` immediately matches 2%1==0, returning [1, 2]. ✓
- Extremely large primes (e.g., num + 1 and num + 2 are mostly primes): The loop safely tracks down to 1 and returns [1, target]. Valid and mathematically sound. ✓

TIME COMPLEXITY: O(sqrt(N)) - Where N is `num + 2`. The loop runs at most sqrt(N) times. For the maximum constraint of 10^9, the square root is roughly 31,622. The algorithm executes virtually instantly compared to the 1,000,000,000 operations needed for brute force.
SPACE COMPLEXITY: O(1) - No data structures are created, only lightweight integer pointers.
"""
