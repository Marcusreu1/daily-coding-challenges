"""
343. Integer Break
Difficulty: Medium
https://leetcode.com/problems/integer-break/

PROBLEM:
Given an integer n, break it into the sum of k positive integers,
where k >= 2, and maximize the product of those integers.

Return the maximum product you can get.

EXAMPLES:
Input: n = 2 → Output: 1
    2 = 1 + 1, product = 1×1 = 1

Input: n = 10 → Output: 36
    10 = 3 + 3 + 4, product = 3×3×4 = 36

CONSTRAINTS:
• 2 <= n <= 58

KEY INSIGHT:
The number 3 is "magical" for maximizing products!

Why? For same sum S:
    3^(S/3) > 2^(S/2)
    
    Proof: Compare 3² vs 2³ for sum=6
           9 > 8 ✓

Rules:
1. NEVER use 1 (multiplying by 1 adds nothing)
2. Prefer 3s over 2s
3. If remainder is 1, use 4 (or 2+2) instead of 3+1
   Because 2×2 = 4 > 3×1 = 3

FORMULA:
┌────────────────────────────────────────────┐
│  n % 3 == 0  →  3^(n/3)                   │
│  n % 3 == 1  →  3^((n-4)/3) × 4           │
│  n % 3 == 2  →  3^(n//3) × 2              │
└────────────────────────────────────────────┘
"""


# ============================================================================
# SOLUTION 1: MATHEMATICAL (O(1) or O(log n) with pow)
# ============================================================================

class Solution:
    def integerBreak(self, n: int) -> int:
        
        # Base cases (must break into at least 2 parts)
        if n == 2:                                               # 2 = 1 + 1
            return 1
        if n == 3:                                               # 3 = 1 + 2
            return 2
        
        # General case: use as many 3s as possible
        remainder = n % 3
        
        if remainder == 0:                                       # n divisible by 3
            return 3 ** (n // 3)
        
        elif remainder == 1:                                     # Would leave 1, use 4 instead
            return 3 ** (n // 3 - 1) * 4
        
        else:                                                    # remainder == 2
            return 3 ** (n // 3) * 2


# ============================================================================
# SOLUTION 2: DYNAMIC PROGRAMMING
# ============================================================================

class Solution:
    def integerBreak(self, n: int) -> int:
        
        dp = [0] * (n + 1)                                       # dp[i] = max product for i
        
        dp[1] = 1                                                # Base case
        
        for i in range(2, n + 1):
            for j in range(1, i):
                # Option 1: j × (i-j) without further breaking (i-j)
                # Option 2: j × dp[i-j] with further breaking (i-j)
                dp[i] = max(dp[i], j * max(i - j, dp[i - j]))
        
        return dp[n]


# ============================================================================
# SOLUTION 3: GREEDY WITH LOOP
# ============================================================================

class Solution:
    def integerBreak(self, n: int) -> int:
        
        if n == 2:
            return 1
        if n == 3:
            return 2
        
        product = 1
        
        while n > 4:                                             # Keep taking 3s
            product *= 3
            n -= 3
        
        return product * n                                       # Multiply remaining (2, 3, or 4)


"""
WHY EACH SOLUTION WORKS:

SOLUTION 1 - MATHEMATICAL:
┌────────────────────────────────────────────────────────────┐
│  The key insight is that 3 maximizes the product.          │
│                                                            │
│  Mathematical proof:                                       │
│  For fixed sum S, we want to maximize the product.         │
│  If we use k equal parts: S/k each, product = (S/k)^k     │
│                                                            │
│  Taking derivative to find optimal k:                      │
│  d/dk[(S/k)^k] = 0  →  optimal part size ≈ e ≈ 2.718      │
│                                                            │
│  Since we need integers: 3 is closer to e than 2!          │
│  And 3 gives better product: 3² = 9 > 2³ = 8 for sum 6    │
│                                                            │
│  Exception: Don't use 3+1, use 2+2 instead (4 > 3)        │
└────────────────────────────────────────────────────────────┘

SOLUTION 2 - DYNAMIC PROGRAMMING:
┌────────────────────────────────────────────────────────────┐
│  dp[i] = maximum product achievable by breaking i          │
│                                                            │
│  For each i, try all possible first cuts j:               │
│      i = j + (i-j)                                        │
│                                                            │
│  Two choices for (i-j):                                    │
│  1. Keep (i-j) as is:     j × (i-j)                       │
│  2. Break (i-j) further:  j × dp[i-j]                     │
│                                                            │
│  dp[i] = max(j × max(i-j, dp[i-j])) for all j             │
└────────────────────────────────────────────────────────────┘

SOLUTION 3 - GREEDY:
┌────────────────────────────────────────────────────────────┐
│  Keep taking 3s while n > 4                                │
│                                                            │
│  Why n > 4?                                                │
│  • n = 5: 3×2 = 6 > 5, so take 3                          │
│  • n = 4: 3×1 = 3 < 4, so STOP and use 4 directly         │
│  • n = 3: use 3 directly                                  │
│  • n = 2: use 2 directly                                  │
│                                                            │
│  The remaining n (2, 3, or 4) is multiplied at the end    │
└────────────────────────────────────────────────────────────┘

HOW IT WORKS (Trace):

Example: n = 10

MATHEMATICAL:
├── 10 % 3 = 1 (remainder is 1)
├── Use formula: 3^((10-4)/3) × 4 = 3² × 4 = 9 × 4 = 36 ✓

DP:
├── dp[2] = 1
├── dp[3] = 2 (1×2)
├── dp[4] = max(1×3, 2×2, 3×1) = 4
├── dp[5] = max(1×4, 2×3, 3×2) = 6
├── dp[6] = max(1×5, 2×4, 3×3, 2×dp[4], 3×dp[3]) = 9
├── dp[7] = max(..., 3×dp[4]) = 3×4 = 12
├── dp[8] = max(..., 3×dp[5]) = 3×6 = 18
├── dp[9] = max(..., 3×dp[6]) = 3×9 = 27
├── dp[10] = max(..., 3×dp[7]) = 3×12 = 36 ✓

GREEDY:
├── n = 10, n > 4, product = 1 × 3 = 3, n = 7
├── n = 7, n > 4, product = 3 × 3 = 9, n = 4
├── n = 4, n <= 4, STOP
├── return 9 × 4 = 36 ✓

VISUAL: WHY 3 IS OPTIMAL

┌────────────────────────────────────────────────────────────┐
│  Sum = 12, different ways to break:                        │
│                                                            │
│  12 = 6 + 6           →  6 × 6 = 36                       │
│  12 = 4 + 4 + 4       →  4 × 4 × 4 = 64                   │
│  12 = 3 + 3 + 3 + 3   →  3 × 3 × 3 × 3 = 81  ✓ BEST      │
│  12 = 2 + 2 + 2 + 2 + 2 + 2  →  2^6 = 64                  │
│                                                            │
│  More 3s = Higher product!                                 │
└────────────────────────────────────────────────────────────┘

WHY NOT USE 1?
┌────────────────────────────────────────────────────────────┐
│  n = 5                                                     │
│  5 = 1 + 4  →  1 × 4 = 4                                  │
│  5 = 2 + 3  →  2 × 3 = 6  ✓                               │
│                                                            │
│  1 adds to sum but multiplies by 1 = no gain!             │
│  Always combine 1 with something else: 1+2=3, 1+3=4       │
└────────────────────────────────────────────────────────────┘

WHY 2+2 INSTEAD OF 3+1?
┌────────────────────────────────────────────────────────────┐
│  n = 4                                                     │
│  4 = 3 + 1  →  3 × 1 = 3                                  │
│  4 = 2 + 2  →  2 × 2 = 4  ✓                               │
│                                                            │
│  When n % 3 == 1, we'd have a leftover 1                  │
│  Instead: "borrow" one 3, making 3+1 = 4 = 2×2            │
│  Result: replace 3×1 with 2×2 (gain +1)                   │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────┐
│  n = 2  →  1 (must break: 1+1)                            │
│  n = 3  →  2 (must break: 1+2)                            │
│  n = 4  →  4 (2+2 or 1+3, best is 2×2)                    │
│  n = 58 →  1549681956 (max constraint)                    │
└────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1 (Math):    O(log n) for exponentiation         │
│                        or O(1) if using iterative multiply │
│  Solution 2 (DP):      O(n²)                               │
│  Solution 3 (Greedy):  O(n)                                │
│  Solution 4 (Memo):    O(n²)                               │
└────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY:
┌────────────────────────────────────────────────────────────┐
│  Solution 1 (Math):    O(1)                                │
│  Solution 2 (DP):      O(n)                                │
│  Solution 3 (Greedy):  O(1)                                │
│  Solution 4 (Memo):    O(n)                                │
└────────────────────────────────────────────────────────────┘

CONCEPTS USED:
• Mathematical Optimization
• Dynamic Programming
• Greedy Algorithm
• Number Theory
• Calculus (derivative to find optimal)
"""
