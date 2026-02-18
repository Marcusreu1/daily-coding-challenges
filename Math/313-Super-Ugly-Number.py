"""
313. Super Ugly Number
Difficulty: Medium
https://leetcode.com/problems/super-ugly-number/

PROBLEM:
A super ugly number is a positive integer whose prime factors are
all in the given array primes.

Given an integer n and an array of integers primes, return the
nth super ugly number.

The nth super ugly number is guaranteed to fit in a 32-bit signed integer.

EXAMPLES:
Input: n = 12, primes = [2,7,13,19]
Output: 32
Explanation: [1,2,4,7,8,13,14,16,19,26,28,32] is the sequence of
             the first 12 super ugly numbers.

Input: n = 1, primes = [2,3,5]
Output: 1
Explanation: 1 has no prime factors, so it's super ugly by definition.

CONSTRAINTS:
• 1 <= n <= 10⁵
• 1 <= primes.length <= 100
• 2 <= primes[i] <= 1000
• primes[i] is guaranteed to be a prime number
• All values of primes are unique and sorted in ascending order

KEY INSIGHT:
Every super ugly number (except 1) is formed by:
    (previous super ugly number) × (some prime from primes)

Instead of checking each number, we BUILD the sequence!

STRATEGY: Multiple Pointers (DP)
For each prime, maintain a pointer indicating which ugly number to multiply.
At each step, take the minimum of all candidates.

HANDLING DUPLICATES:
When multiple primes generate the same number (e.g., 2×3 = 6 = 3×2),
advance ALL pointers that produced the minimum to avoid duplicates.
"""

from typing import List


class Solution:
    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:
        
        k = len(primes)
        
        ugly = [1] * n                                           # ugly[i] = (i+1)th super ugly number
        
        pointers = [0] * k                                       # pointer for each prime
        
        for i in range(1, n):                                    # Generate ugly[1] to ugly[n-1]
            
            # Calculate candidate from each prime
            candidates = []
            for j in range(k):
                candidate = ugly[pointers[j]] * primes[j]        # ugly[ptr] × prime
                candidates.append(candidate)
            
            # Take minimum as next ugly number
            next_ugly = min(candidates)
            ugly[i] = next_ugly
            
            # Advance ALL pointers that produced the minimum (avoid duplicates)
            for j in range(k):
                if candidates[j] == next_ugly:
                    pointers[j] += 1
        
        return ugly[n - 1]


"""
OPTIMIZED VERSION (same logic, cleaner code):
"""


class Solution:
    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:
        
        ugly = [1] * n
        k = len(primes)
        pointers = [0] * k
        
        for i in range(1, n):
            # Compute all candidates and find minimum
            ugly[i] = min(ugly[pointers[j]] * primes[j] for j in range(k))
            
            # Advance pointers that produced the minimum
            for j in range(k):
                if ugly[pointers[j]] * primes[j] == ugly[i]:
                    pointers[j] += 1
        
        return ugly[-1]


"""
ALTERNATIVE: MIN-HEAP APPROACH
"""

import heapq


class SolutionHeap:
    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:
        
        ugly = [1]
        heap = []
        
        # Initialize heap: (value, prime_index, ugly_index_used)
        for i, p in enumerate(primes):
            heapq.heappush(heap, (p, i, 0))                      # 1 × prime[i]
        
        while len(ugly) < n:
            val, prime_idx, ugly_idx = heapq.heappop(heap)
            
            # Avoid duplicates
            if val != ugly[-1]:
                ugly.append(val)
            
            # Push next candidate for this prime
            next_val = ugly[ugly_idx + 1] * primes[prime_idx]
            heapq.heappush(heap, (next_val, prime_idx, ugly_idx + 1))
        
        return ugly[-1]


"""
HOW IT WORKS (Trace with n=7, primes=[2,7]):

Step 0: ugly = [1], ptr = [0, 0]

Step 1: candidates = [1×2=2, 1×7=7]
        min = 2
        ugly = [1, 2]
        ptr = [1, 0]  (advance ptr for prime 2)

Step 2: candidates = [2×2=4, 1×7=7]
        min = 4
        ugly = [1, 2, 4]
        ptr = [2, 0]

Step 3: candidates = [4×2=8, 1×7=7]
        min = 7
        ugly = [1, 2, 4, 7]
        ptr = [2, 1]  (advance ptr for prime 7)

Step 4: candidates = [4×2=8, 2×7=14]
        min = 8
        ugly = [1, 2, 4, 7, 8]
        ptr = [3, 1]

Step 5: candidates = [8×2=16, 2×7=14]
        min = 14
        ugly = [1, 2, 4, 7, 8, 14]
        ptr = [3, 2]

Step 6: candidates = [8×2=16, 4×7=28]
        min = 16
        ugly = [1, 2, 4, 7, 8, 14, 16]
        ptr = [4, 2]

Return: ugly[6] = 16 ✓

WHY MULTIPLE POINTERS WORK:

┌────────────────────────────────────────────────────────────────┐
│  Each prime has its own "progress" through the ugly array     │
│                                                                │
│  ptr[j] = index of ugly number to multiply by primes[j]       │
│                                                                │
│  This ensures we generate candidates in sorted order!         │
│                                                                │
│  ugly[ptr[j]] × primes[j] is always the smallest candidate    │
│  we haven't used yet for that prime.                          │
└────────────────────────────────────────────────────────────────┘

WHY ADVANCE ALL MATCHING POINTERS:

Example: primes = [2, 3], generating 6

ugly = [1, 2, 3, 4, ...]
ptr = [2, 1]

candidates = [ugly[2]×2, ugly[1]×3] = [3×2, 2×3] = [6, 6]

Both produce 6! If we only advance one pointer:
- Next round: [4×2=8, 2×3=6] → 6 again! DUPLICATE!

Solution: Advance BOTH pointers when both produce minimum.

HANDLING EDGE CASES:
• n = 1                → Return 1 (base case)
• Single prime [2]     → Powers of 2: 1, 2, 4, 8, 16...
• Large n              → Works due to O(n×k) complexity

TIME COMPLEXITY: O(n × k)
├── n iterations to generate n ugly numbers
├── Each iteration: O(k) to find min and update pointers
└── Total: O(n × k)

SPACE COMPLEXITY: O(n + k)
├── O(n) for ugly array
└── O(k) for pointers array

HEAP APPROACH COMPLEXITY:
├── Time: O(n × k × log(k)) - heap operations
└── Space: O(n + k) - ugly array + heap

COMPARISON:
┌─────────────────────────────────────────────────────┐
│  Approach          │  Time       │  Space          │
├─────────────────────────────────────────────────────┤
│  Multiple Pointers │  O(n × k)   │  O(n + k)       │
│  Min-Heap          │  O(nk logk) │  O(n + k)       │
└─────────────────────────────────────────────────────┘

Multiple pointers is faster for this problem!

CONCEPTS USED:
• Dynamic Programming
• Multiple Pointers Technique
• Greedy (always take minimum)
• Number Theory (prime factorization concept)
• Min-Heap (alternative approach)
"""
