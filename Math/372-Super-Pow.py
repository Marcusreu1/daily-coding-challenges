"""
372. Super Pow
Difficulty: Medium
https://leetcode.com/problems/super-pow/

PROBLEM:
Your task is to calculate a^b mod 1337 where a is a positive integer
and b is an extremely large positive integer given in the form of an array.

EXAMPLES:
Input: a = 2, b = [3]
Output: 8
    2^3 = 8, 8 mod 1337 = 8

Input: a = 2, b = [1, 0]
Output: 1024
    2^10 = 1024, 1024 mod 1337 = 1024

Input: a = 1, b = [4, 3, 3, 8, 5, 2]
Output: 1
    1^anything = 1

Input: a = 2147483647, b = [2, 0, 0]
Output: 1198
    Very large a, moderately large b

CONSTRAINTS:
• 1 <= a <= 2³¹ - 1
• 1 <= b.length <= 2000
• 0 <= b[i] <= 9
• b does not contain leading zeros

KEY INSIGHT 1 - MOD PROPERTY:
(a × b) mod m = ((a mod m) × (b mod m)) mod m

Therefore:
(a^b) mod m = ((a mod m)^b) mod m

KEY INSIGHT 2 - DIGIT DECOMPOSITION:
For b = [b₀, b₁, ..., bₙ]:
    a^b = a^(b₀×10^n + b₁×10^(n-1) + ... + bₙ)

Processing left to right:
    result = result^10 × a^(current_digit)  (mod 1337)

WHY result^10?
    Each new digit shifts the previous exponent one decimal place left
    (multiplies by 10), hence we raise result to the 10th power.

ALGORITHM:
1. Use fast modular exponentiation (binary exponentiation)
2. Process b digit by digit from left to right
3. At each step: result = (result^10 × a^digit) mod 1337
"""

from typing import List


# ============================================================================
# SOLUTION 1: ITERATIVE WITH FAST POWER (Recommended)
# ============================================================================

class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        
        MOD = 1337
        
        def powmod(base: int, exp: int, mod: int) -> int:
            """Fast modular exponentiation: computes base^exp mod mod"""
            result = 1
            base %= mod                                          # Reduce base first
            
            while exp > 0:
                if exp % 2 == 1:                                 # If exp is odd
                    result = result * base % mod
                base = base * base % mod                         # Square the base
                exp //= 2                                        # Halve the exponent
            
            return result
        
        result = 1
        
        for digit in b:                                          # Process each digit
            result = powmod(result, 10, MOD) * powmod(a, digit, MOD) % MOD
        
        return result


# ============================================================================
# SOLUTION 2: RECURSIVE WITH FAST POWER
# ============================================================================

class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        
        MOD = 1337
        
        def powmod(base: int, exp: int) -> int:
            """Recursive fast power mod 1337"""
            if exp == 0:
                return 1
            if exp == 1:
                return base % MOD
            
            if exp % 2 == 0:                                     # Even exponent
                half = powmod(base, exp // 2)
                return half * half % MOD
            else:                                                 # Odd exponent
                return base * powmod(base, exp - 1) % MOD
        
        def solve(b: List[int]) -> int:
            if not b:
                return 1
            
            last_digit = b.pop()                                 # Take last digit
            
            # a^b = (a^(b//10))^10 × a^(b%10)
            return powmod(solve(b), 10) * powmod(a, last_digit) % MOD
        
        return solve(b)


# ============================================================================
# SOLUTION 3: USING PYTHON BUILT-IN POW 
# ============================================================================

class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        
        # Convert b array to actual number
        # WARNING: b can have 2000 digits, Python handles big integers natively
        exponent = int(''.join(map(str, b)))
        
        return pow(a, exponent, 1337)                            # Python's built-in with 3 args


############## ============================================================================
# SOLUTION 4: STEP BY STEP 
############## ============================================================================

class Solution:
    def superPow(self, a: int, b: List[int]) -> int:
        
        MOD = 1337
        
        def fast_pow(base: int, exp: int) -> int:
            """Binary exponentiation: O(log exp)"""
            base %= MOD                                          # Initial reduction
            result = 1
            
            while exp:
                if exp & 1:                                      # If current bit is 1
                    result = result * base % MOD
                base = base * base % MOD                         # Square base
                exp >>= 1                                        # Right shift (divide by 2)
            
            return result
        
        result = 1
        a %= MOD                                                 # Reduce a first
        
        for digit in b:
            # Shift result's exponent left by 1 decimal place (×10)
            # Then multiply by a^digit
            result = fast_pow(result, 10) * fast_pow(a, digit) % MOD
        
        return result


"""
HOW IT WORKS (Detailed Trace):

Example 1: a = 2, b = [1, 0]
───────────────────────────

powmod function traces:

powmod(2, 1, 1337):
    exp=1 (odd): result = 1 × 2 = 2
    exp=0: done
    return 2

powmod(2, 0, 1337):
    exp=0: return 1

Processing digits:

    result = 1

    digit = 1:
        powmod(result, 10) = powmod(1, 10) = 1
        powmod(a, 1) = powmod(2, 1) = 2
        result = (1 × 2) % 1337 = 2

    digit = 0:
        powmod(result, 10) = powmod(2, 10) = 1024
        powmod(a, 0) = powmod(2, 0) = 1
        result = (1024 × 1) % 1337 = 1024

    Return 1024 ✓

────────────────────────────────────────────────────────────────────

Example 2: a = 2, b = [2, 1, 0]  (represents 210)
──────────────────────────────────────────────────

result = 1

digit = 2:
    powmod(1, 10) = 1
    powmod(2, 2) = 4
    result = (1 × 4) % 1337 = 4   [represents 2^2]

digit = 1:
    powmod(4, 10) = 4^10 % 1337   [4^10 = 2^20]
    powmod(2, 1) = 2
    result = (4^10 × 2) % 1337    [represents 2^21]

digit = 0:
    powmod(result, 10) = ...      [exponent becomes 210]
    powmod(2, 0) = 1
    result = (result^10 × 1) %1337 [represents 2^210]

Return 2^210 mod 1337 ✓

────────────────────────────────────────────────────────────────────

FAST POWER TRACE (2^10):

base=2, exp=10

    exp=10 (even): base = 2×2 = 4, exp = 5
    exp=5  (odd):  result = 1×4 = 4, base = 4×4 = 16, exp = 2
    exp=2  (even): base = 16×16 = 256, exp = 1
    exp=1  (odd):  result = 4×256 = 1024, exp = 0
    
    return 1024 ✓  (only 4 steps instead of 10!)

WHY PROCESS LEFT TO RIGHT?

b = [b0, b1, b2] represents b0×100 + b1×10 + b2

a^(b0×100 + b1×10 + b2)
= a^(b0×100) × a^(b1×10) × a^b2

Processing left to right:
    After b0: result = a^b0
    After b1: result = (a^b0)^10 × a^b1 = a^(b0×10 + b1)
    After b2: result = (a^(b0×10+b1))^10 × a^b2
                     = a^(b0×100 + b1×10 + b2) ✓

WHY MODULAR ARITHMETIC WORKS:
┌────────────────────────────────────────────────────────────────┐
│  (a × b) mod m = ((a mod m) × (b mod m)) mod m               │
│                                                                │
│  Proof:                                                        │
│  Let a = q₁m + r₁ and b = q₂m + r₂                           │
│  a × b = (q₁m + r₁)(q₂m + r₂)                                │
│        = q₁q₂m² + q₁r₂m + q₂r₁m + r₁r₂                      │
│        ≡ r₁r₂ (mod m)                                         │
│        = (a mod m)(b mod m) (mod m) ✓                         │
└────────────────────────────────────────────────────────────────┘

BINARY EXPONENTIATION EXPLANATION:
┌────────────────────────────────────────────────────────────────┐
│  Any exponent can be written in binary:                        │
│  10 = 1010₂ = 1×8 + 0×4 + 1×2 + 0×1                          │
│                                                                │
│  a^10 = a^(8+2) = a^8 × a^2                                   │
│                                                                │
│  We compute a^1, a^2, a^4, a^8 by squaring.                   │
│  Then multiply the ones where bit is set.                      │
│                                                                │
│  10 = 1010₂:                                                   │
│  bit 3 (8): 1 → multiply by a^8                               │
│  bit 2 (4): 0 → skip                                          │
│  bit 1 (2): 1 → multiply by a^2                               │
│  bit 0 (1): 0 → skip                                          │
│                                                                │
│  Result = a^8 × a^2 = a^10 ✓                                  │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  a = 1     → 1^anything = 1                                    │
│  b = [0]   → a^0 = 1                                          │
│  b = [1]   → a^1 = a mod 1337                                 │
│  a = 1337  → 1337 mod 1337 = 0 → result = 0                   │
│  b = [0,0] → Shouldn't happen (no leading zeros)              │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(n × log 10) = O(n)
├── n = length of b (up to 2000)
├── For each digit: powmod runs in O(log 10) ≈ O(4)
└── Total: O(n)

SPACE COMPLEXITY: O(1)
├── No extra data structures needed
├── Recursive version uses O(n) stack space

CONCEPTS USED:
• Modular Arithmetic
• Binary Exponentiation (Fast Power)
• Properties of Modular Operations
• Digit-by-Digit Processing
"""
