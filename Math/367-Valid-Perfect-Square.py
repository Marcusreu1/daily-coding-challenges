"""
367. Valid Perfect Square
Difficulty: Easy
https://leetcode.com/problems/valid-perfect-square/

PROBLEM:
Given a positive integer num, return true if num is a perfect square,
otherwise return false.

A perfect square is an integer that is the square of an integer.
In other words, it is the product of some integer with itself.

You must NOT use any built-in library function, such as sqrt.

EXAMPLES:
Input: num = 16 → Output: true  (4² = 16)
Input: num = 14 → Output: false (not a perfect square)
Input: num = 1  → Output: true  (1² = 1)

CONSTRAINTS:
• 1 <= num <= 2³¹ - 1

PERFECT SQUARES: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, ...

APPROACHES:
1. Binary Search: Search for x where x² = num (O(log n))
2. Newton-Raphson: Iterative root finding (O(log log n))
3. Sum of Odds: 1+3+5+...+(2n-1) = n² (O(√n))
4. Brute Force: Try all i until i² >= num (O(√n))
"""


# ============================================================================
# SOLUTION 1: BINARY SEARCH 
# ============================================================================

class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        
        left, right = 1, num
        
        while left <= right:
            mid = left + (right - left) // 2                     # Avoid overflow
            square = mid * mid
            
            if square == num:                                    # Found perfect square
                return True
            elif square < num:                                   # Need larger number
                left = mid + 1
            else:                                                # Need smaller number
                right = mid - 1
        
        return False


# ============================================================================
# SOLUTION 2: NEWTON-RAPHSON METHOD (Fastest)
# ============================================================================

class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        
        if num == 1:
            return True
        
        x = num // 2                                             # Initial guess
        
        while x * x > num:
            x = (x + num // x) // 2                              # Newton's formula
        
        return x * x == num


# ============================================================================
# SOLUTION 3: SUM OF ODD NUMBERS 
# ============================================================================

class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        
        # 1 + 3 + 5 + 7 + ... + (2n-1) = n²
        # Subtract consecutive odd numbers from num
        
        odd = 1
        
        while num > 0:
            num -= odd
            odd += 2                                             # Next odd number
        
        return num == 0                                          # Exactly zero = perfect square


# ============================================================================
# SOLUTION 4: BRUTE FORCE (Simple but slower)
# ============================================================================

class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        
        i = 1
        
        while i * i <= num:
            if i * i == num:
                return True
            i += 1
        
        return False


# ============================================================================
# SOLUTION 5: BINARY SEARCH (Alternative with different bounds)
# ============================================================================

class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        
        if num < 2:
            return True
        
        # Square root of num is at most num/2 for num >= 4
        left, right = 2, num // 2
        
        while left <= right:
            mid = (left + right) // 2
            guess = mid * mid
            
            if guess == num:
                return True
            elif guess < num:
                left = mid + 1
            else:
                right = mid - 1
        
        return False


"""
HOW EACH SOLUTION WORKS:

SOLUTION 1 - BINARY SEARCH:
┌────────────────────────────────────────────────────────────────┐
│  num = 16                                                      │
│  ├── left=1, right=16                                         │
│  ├── mid=8, 8²=64 > 16 → right=7                              │
│  ├── mid=4, 4²=16 == 16 ✓                                     │
│  └── Return True                                              │
│                                                                │
│  num = 14                                                      │
│  ├── left=1, right=14                                         │
│  ├── mid=7, 49 > 14 → right=6                                 │
│  ├── mid=3, 9 < 14 → left=4                                   │
│  ├── mid=5, 25 > 14 → right=4                                 │
│  ├── mid=4, 16 > 14 → right=3                                 │
│  ├── left(4) > right(3) → exit                                │
│  └── Return False                                             │
└────────────────────────────────────────────────────────────────┘

SOLUTION 2 - NEWTON-RAPHSON:
┌────────────────────────────────────────────────────────────────┐
│  Finding root of f(x) = x² - num                               │
│                                                                │
│  Formula: x_new = (x + num/x) / 2                             │
│                                                                │
│  num = 16, x = 8 (initial guess = num/2)                      │
│  ├── 8² = 64 > 16 → x = (8 + 16/8) / 2 = 5                   │
│  ├── 5² = 25 > 16 → x = (5 + 16/5) / 2 = 4                   │
│  ├── 4² = 16 = 16 → exit loop                                │
│  └── 4² == 16? True ✓                                         │
│                                                                │
│  Converges VERY fast: O(log log n)                            │
└────────────────────────────────────────────────────────────────┘

SOLUTION 3 - SUM OF ODD NUMBERS:
┌────────────────────────────────────────────────────────────────┐
│  Mathematical property:                                        │
│  1 + 3 + 5 + ... + (2n-1) = n²                                │
│                                                                │
│  num = 16:                                                     │
│  ├── 16 - 1 = 15, odd = 3                                     │
│  ├── 15 - 3 = 12, odd = 5                                     │
│  ├── 12 - 5 = 7,  odd = 7                                     │
│  ├── 7 - 7 = 0,   odd = 9                                     │
│  ├── num = 0 → exit loop                                      │
│  └── num == 0? True ✓ (subtracted 4 odds → 4² = 16)          │
│                                                                │
│  num = 14:                                                     │
│  ├── 14 - 1 = 13                                              │
│  ├── 13 - 3 = 10                                              │
│  ├── 10 - 5 = 5                                               │
│  ├── 5 - 7 = -2 < 0 → exit loop                               │
│  └── num == 0? False (-2 ≠ 0) ✓                               │
└────────────────────────────────────────────────────────────────┘

VISUAL: WHY SUM OF ODDS = PERFECT SQUARE
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  1² = 1           ■                        = 1                 │
│                                                                │
│  2² = 4           ■ ●                      = 1 + 3             │
│                   ● ●                                          │
│                                                                │
│  3² = 9           ■ ● ○                    = 1 + 3 + 5         │
│                   ● ● ○                                        │
│                   ○ ○ ○                                        │
│                                                                │
│  4² = 16          ■ ● ○ △                  = 1 + 3 + 5 + 7     │
│                   ● ● ○ △                                      │
│                   ○ ○ ○ △                                      │
│                   △ △ △ △                                      │
│                                                                │
│  Each "L-shaped" layer adds an odd number!                    │
│  Layer n has (2n-1) squares                                   │
└────────────────────────────────────────────────────────────────┘

WHY BINARY SEARCH WORKS:
┌────────────────────────────────────────────────────────────────┐
│  f(x) = x² is a strictly increasing function for x > 0        │
│                                                                │
│  If we're looking for x where x² = num:                       │
│  • x² < num → x is too small → search right half             │
│  • x² > num → x is too large → search left half              │
│  • x² = num → found it!                                       │
│                                                                │
│  Search space: [1, num]                                       │
│  Each iteration halves the space → O(log n)                   │
└────────────────────────────────────────────────────────────────┘

NEWTON-RAPHSON DERIVATION:
┌────────────────────────────────────────────────────────────────┐
│  Want to find x where f(x) = x² - num = 0                     │
│                                                                │
│  Newton's method: x_new = x - f(x)/f'(x)                      │
│                                                                │
│  f(x) = x² - num                                              │
│  f'(x) = 2x                                                   │
│                                                                │
│  x_new = x - (x² - num)/(2x)                                  │
│        = x - x/2 + num/(2x)                                   │
│        = x/2 + num/(2x)                                       │
│        = (x + num/x) / 2                                      │
│                                                                │
│  This converges quadratically: O(log log n)!                  │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  num = 1      →  True  (1² = 1)                               │
│  num = 2      →  False (between 1² and 2²)                    │
│  num = 4      →  True  (2² = 4)                               │
│  num = 2^31-1 →  False (46340² = 2147395600 < 2^31-1)        │
│  Large nums   →  Binary search handles efficiently            │
└────────────────────────────────────────────────────────────────┘

OVERFLOW CONSIDERATION:
┌────────────────────────────────────────────────────────────────┐
│  mid * mid could overflow for large numbers                   │
│                                                                │
│  Solutions:                                                    │
│  1. Use (left + right) // 2 might overflow → use              │
│     left + (right - left) // 2 instead                        │
│  2. In Python, integers have arbitrary precision (no overflow)│
│  3. In other languages, use long or check overflow            │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  Binary Search:    O(log n)                                    │
│  Newton-Raphson:   O(log log n)  ← Fastest!                   │
│  Sum of Odds:      O(√n)                                       │
│  Brute Force:      O(√n)                                       │
└────────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  All solutions:    O(1)                                        │
└────────────────────────────────────────────────────────────────┘

COMPARISON WITH SIMILAR PROBLEMS:
┌────────────────────────────────────────────────────────────────┐
│  69. Sqrt(x)          → Find floor(√x), binary search         │
│  367. Valid Perfect   → Check if √x is integer                │
│  Square                                                        │
│  633. Sum of Square   → a² + b² = c, two pointers/hash       │
│       Numbers                                                  │
└────────────────────────────────────────────────────────────────┘

CONCEPTS USED:
• Binary Search
• Newton-Raphson Method
• Mathematical Properties (sum of odds)
• Number Theory
"""
