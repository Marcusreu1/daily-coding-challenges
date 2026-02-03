# 204. Count Primes
# Difficulty: Medium
# https://leetcode.com/problems/count-primes/

"""
PROBLEM:
Given an integer n, return the number of prime numbers that are
strictly less than n.

EXAMPLES:
Input: n = 10 → Output: 4  (primes: 2, 3, 5, 7)
Input: n = 0  → Output: 0
Input: n = 1  → Output: 0

CONSTRAINTS:
- 0 <= n <= 5 × 10^6

KEY INSIGHT:
Use the Sieve of Eratosthenes (ancient algorithm from 200 BC!).
Instead of checking each number for primality, mark all multiples
of each prime as composite (not prime).

OPTIMIZATIONS:
1. Only iterate up to √n (if no factor ≤ √n, number is prime)
2. Start marking from p² (smaller multiples already marked)
3. Use boolean array for O(1) marking

SOLUTION:
Create boolean array, mark composites, count remaining primes.
"""

# STEP 1: Handle edge cases (n <= 2)
# STEP 2: Create boolean array assuming all are prime
# STEP 3: For each prime p, mark multiples starting from p²
# STEP 4: Count True values (primes)

class Solution:
    def countPrimes(self, n: int) -> int:
        
        if n <= 2:                                                               # No primes less than 2
            return 0
        
        is_prime = [True] * n                                                    # Assume all prime initially
        is_prime[0] = is_prime[1] = False                                        # 0 and 1 are not prime
        
        p = 2
        while p * p < n:                                                         # Only up to √n
            
            if is_prime[p]:                                                      # If p is still prime
                
                for multiple in range(p * p, n, p):                              # Mark multiples from p²
                    is_prime[multiple] = False
            
            p += 1
        
        return sum(is_prime)                                                     # Count True values


"""
WHY EACH PART:
- n <= 2: No primes less than 2 (2 itself is not "less than 2")
- is_prime = [True] * n: Boolean array, index = number
- is_prime[0] = is_prime[1] = False: 0 and 1 are never prime
- while p * p < n: Only need to check up to √n
- if is_prime[p]: Skip if already marked composite
- range(p * p, n, p): Start at p², go up to n-1, step by p
- is_prime[multiple] = False: Mark all multiples as composite
- sum(is_prime): True counts as 1, False as 0

HOW IT WORKS (Example: n = 20):

┌─ Initial State ───────────────────────────────────────────┐
│  is_prime = [F, F, T, T, T, T, T, T, T, T,                │
│              T, T, T, T, T, T, T, T, T, T]                 │
│  indices:    0  1  2  3  4  5  6  7  8  9                 │
│             10 11 12 13 14 15 16 17 18 19                 │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ p = 2, p² = 4 < 20, is_prime[2] = True ──────────────────┐
│  Mark multiples: 4, 6, 8, 10, 12, 14, 16, 18              │
│                                                           │
│  is_prime = [F, F, T, T, F, T, F, T, F, T,                │
│              F, T, F, T, F, T, F, T, F, T]                 │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ p = 3, p² = 9 < 20, is_prime[3] = True ──────────────────┐
│  Mark multiples: 9, 12, 15, 18                            │
│  (12, 18 already False)                                   │
│                                                           │
│  is_prime = [F, F, T, T, F, T, F, T, F, F,                │
│              F, T, F, T, F, F, F, T, F, T]                 │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ p = 4, p² = 16 < 20, is_prime[4] = False ────────────────┐
│  Skip! (4 is not prime)                                   │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ p = 5, p² = 25 >= 20 ────────────────────────────────────┐
│  Exit loop! (√20 ≈ 4.47)                                  │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Count Primes ────────────────────────────────────────────┐
│  is_prime = [F, F, T, T, F, T, F, T, F, F,                │
│              F, T, F, T, F, F, F, T, F, T]                 │
│                  2  3     5     7                          │
│                    11    13          17    19              │
│                                                           │
│  sum(is_prime) = 8 ✓                                      │
└───────────────────────────────────────────────────────────┘

WHY p * p < n (not p < n)?
┌────────────────────────────────────────────────────────────┐
│  Any composite number c < n has a prime factor ≤ √n        │
│                                                            │
│  Proof: If c = a × b and both a,b > √n                    │
│         Then c = a × b > √n × √n = n                      │
│         Contradiction! So at least one factor ≤ √n        │
│                                                            │
│  If c wasn't marked by any prime ≤ √n, then c IS prime    │
└────────────────────────────────────────────────────────────┘

WHY START FROM p * p (not 2 * p)?
┌────────────────────────────────────────────────────────────┐
│  When processing prime p:                                  │
│                                                            │
│  2×p, 3×p, 4×p, ..., (p-1)×p  already marked!             │
│                                                            │
│  • 2×p marked when we processed prime 2                   │
│  • 3×p marked when we processed prime 3                   │
│  • 4×p = 2×(2p) marked when we processed prime 2          │
│  • etc.                                                    │
│                                                            │
│  First unmarked multiple of p is p×p                      │
└────────────────────────────────────────────────────────────┘

SIEVE VISUALIZATION for n = 30:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   2  3  4  5  6  7  8  9 10 11 12 13 14 15                │
│  16 17 18 19 20 21 22 23 24 25 26 27 28 29                │
│                                                            │
│  p=2: Cross out 4,6,8,10,12,14,16,18,20,22,24,26,28       │
│   2  3  ×  5  ×  7  ×  ×  ×  11  ×  13  ×  ×              │
│   ×  17  ×  19  ×  ×  ×  23  ×  ×  ×  ×  ×  29            │
│                                                            │
│  p=3: Cross out 9,15,21,27 (others already crossed)       │
│   2  3  ×  5  ×  7  ×  ×  ×  11  ×  13  ×  ×              │
│   ×  17  ×  19  ×  ×  ×  23  ×  ×  ×  ×  ×  29            │
│                                                            │
│  p=5: Cross out 25 (5²=25, next would be 30 >= n)         │
│   2  3  ×  5  ×  7  ×  ×  ×  11  ×  13  ×  ×              │
│   ×  17  ×  19  ×  ×  ×  23  ×  ×  ×  ×  ×  29            │
│                                                            │
│  p=6: 6² = 36 >= 30, STOP                                  │
│                                                            │
│  Primes: 2,3,5,7,11,13,17,19,23,29 → 10 primes            │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- n = 0: No numbers less than 0 → returns 0 ✓
- n = 1: No numbers less than 1 → returns 0 ✓
- n = 2: Only 0,1 which aren't prime → returns 0 ✓
- n = 3: Only 2 is prime → returns 1 ✓
- n = 5000000: Handles efficiently → returns 348513 ✓

TIME COMPLEXITY: O(n log log n)
- Outer loop: O(√n) iterations
- Inner loop total: n/2 + n/3 + n/5 + n/7 + ...
- Sum of 1/p for primes p ≤ n ≈ log log n
- Total: O(n × log log n)

SPACE COMPLEXITY: O(n)
- Boolean array of size n
- Can be optimized to O(n/2) by only storing odd numbers

CONCEPTS USED:
- Sieve of Eratosthenes (ancient algorithm)
- Prime number theory
- Array marking technique
- Square root optimization
- Starting from p² optimization
"""
