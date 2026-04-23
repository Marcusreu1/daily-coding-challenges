"""
650. 2 Keys Keyboard
Difficulty: Medium
https://leetcode.com/problems/2-keys-keyboard/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

Initially you have one character 'A' on a notepad. You can perform
two operations:

    - Copy All:  Copy everything on the notepad
    - Paste:     Paste the last copied content

Given an integer n, return the MINIMUM number of operations to get
exactly n 'A' characters on the notepad.

EXAMPLES:

    Input: n = 3  → Output: 3
        (Copy All, Paste, Paste → "AAA")

    Input: n = 1  → Output: 0
        (Already have one 'A', no operations needed)

    Input: n = 12 → Output: 7
        (2 + 2 + 3 = 7, via prime factorization 12 = 2 × 2 × 3)

CONSTRAINTS:

    1 <= n <= 1000

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

Multiplying the current count by a factor p costs exactly p operations:
    1 Copy All + (p-1) Pastes = p operations

Therefore, the minimum operations to reach n equals the
SUM OF PRIME FACTORS of n (with repetition).

    n = p1 × p2 × p3 × ...
    answer = p1 + p2 + p3 + ...

Why primes? Because splitting a composite factor into smaller factors
always gives a sum ≤ the original (a + b ≤ a × b for a,b ≥ 2).

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. Recognizing this as a prime factorization problem
2. Understanding WHY multiplying by p costs p operations
3. Proving that prime decomposition gives the optimal answer

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Start with the smallest prime factor (2)
STEP 2: While n is divisible by current factor, divide and add to result
STEP 3: Move to next factor
STEP 4: Repeat until n is fully factorized (n == 1)
"""


class Solution:
    def minSteps(self, n: int) -> int:

        result = 0                                                                # Total operations needed
        factor = 2                                                                # Start with smallest prime

        while n > 1:                                                              # Keep factoring until n = 1
            while n % factor == 0:                                                # While current factor divides n
                result += factor                                                  # Add factor to operation count
                n //= factor                                                      # Divide n by this factor
            factor += 1                                                           # Try next potential factor

        return result                                                             # Sum of all prime factors


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

result = 0:
    Accumulator for total operations. We add each prime factor
    as we find it, since each factor p costs p operations.

factor = 2:
    Start dividing by the smallest prime. This naturally finds
    all prime factors from smallest to largest.

while n > 1:
    We keep going until n has been completely broken down.
    When n = 1, all prime factors have been extracted.

while n % factor == 0:
    Extract all copies of the current factor.
    Example: n=12, factor=2 → 12/2=6, 6/2=3 (extracted two 2's)

result += factor:
    Each prime factor p represents a "multiply by p" step,
    which costs p operations (1 copy + (p-1) pastes).

n //= factor:
    Remove this factor from n. Eventually n reduces to 1.

factor += 1:
    Move to next candidate. We don't need to check if it's prime —
    composite numbers won't divide n because their prime components
    were already extracted in earlier iterations.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 12):
════════════════════════════════════════════════════════════════

    n=12, factor=2, result=0
    ├── 12 % 2 == 0 → result += 2 = 2,  n = 12/2 = 6
    ├── 6 % 2 == 0  → result += 2 = 4,  n = 6/2 = 3
    ├── 3 % 2 != 0  → move on, factor = 3
    ├── 3 % 3 == 0  → result += 3 = 7,  n = 3/3 = 1
    └── n == 1 → STOP

    Result: 7 ✓ (prime factors: 2 + 2 + 3 = 7)

    What this means physically:
    A → AA → AAAA → AAAAAAAAAAAA
    1 → 2  → 4    → 12
        ×2    ×2      ×3
      (2 ops)(2 ops)(3 ops) = 7 total

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 18):
════════════════════════════════════════════════════════════════

    n=18, factor=2, result=0
    ├── 18 % 2 == 0 → result += 2 = 2,  n = 18/2 = 9
    ├── 9 % 2 != 0  → move on, factor = 3
    ├── 9 % 3 == 0  → result += 3 = 5,  n = 9/3 = 3
    ├── 3 % 3 == 0  → result += 3 = 8,  n = 3/3 = 1
    └── n == 1 → STOP

    Result: 8 ✓ (prime factors: 2 + 3 + 3 = 8)

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 7, prime number):
════════════════════════════════════════════════════════════════

    n=7, factor=2, result=0
    ├── 7 % 2 != 0 → factor = 3
    ├── 7 % 3 != 0 → factor = 4
    ├── 7 % 4 != 0 → factor = 5
    ├── 7 % 5 != 0 → factor = 6
    ├── 7 % 6 != 0 → factor = 7
    ├── 7 % 7 == 0 → result += 7 = 7, n = 1
    └── n == 1 → STOP

    Result: 7 ✓ (prime number → only factor is itself)

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: n = 1):
════════════════════════════════════════════════════════════════

    n=1 → while loop doesn't execute
    Result: 0 ✓ (already have one 'A')

════════════════════════════════════════════════════════════════
WHY PRIME FACTORIZATION IS OPTIMAL:
════════════════════════════════════════════════════════════════

Key mathematical property: For a, b ≥ 2:

    a + b  ≤  a × b

Proof: a×b - a - b = a(b-1) - b = (a-1)(b-1) - 1 ≥ 0 when a,b ≥ 2

This means splitting ANY composite factor into smaller factors
gives a sum that is LESS THAN OR EQUAL to the original:

    Factor 6:   costs 6 operations
    Split 2×3:  costs 2 + 3 = 5 operations  ← BETTER

    Factor 4:   costs 4 operations
    Split 2×2:  costs 2 + 2 = 4 operations  ← SAME

    Factor 9:   costs 9 operations
    Split 3×3:  costs 3 + 3 = 6 operations  ← BETTER

So we keep splitting until all factors are prime → minimum sum!

════════════════════════════════════════════════════════════════
WHY WE DON'T NEED A PRIMALITY CHECK:
════════════════════════════════════════════════════════════════

When we try factor = 4, n won't be divisible by 4 because
we already extracted ALL 2's in earlier iterations.

    n = 24:
    ├── factor=2: 24→12→6→3 (extracted three 2's)
    ├── factor=3: 3→1 (extracted one 3)
    └── factor=4: never reached (n is already 1)

The algorithm naturally skips composite factors because their
prime components were already removed!

════════════════════════════════════════════════════════════════
UNDERSTANDING THE COPY-PASTE MECHANISM:
════════════════════════════════════════════════════════════════

    To multiply current count by p:
    ├── Copy All          → 1 operation (clipboard = current)
    ├── Paste × (p - 1)   → p - 1 operations
    └── Total: 1 + (p-1) = p operations

    Example (multiply by 3, starting with 4 A's):
    ├── "AAAA"              → have 4
    ├── Copy All            → clipboard = "AAAA"     (op 1)
    ├── Paste               → "AAAAAAAA"             (op 2)
    ├── Paste               → "AAAAAAAAAAAA"         (op 3)
    └── Now have 12 = 4 × 3, cost was 3 operations ✓

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    n = 1          → 0 (already have one 'A') ✓
    n = 2          → 2 (Copy, Paste) ✓
    n = 3          → 3 (Copy, Paste, Paste) ✓
    n = 4          → 4 (2+2: ×2 then ×2) ✓
    n = prime      → n (no shortcuts, must paste n-1 times) ✓
    n = power of 2 → 2 × (number of times), e.g. 8 → 2+2+2=6 ✓
    n = 1000       → 2+2+2+5+5+5 = 21 (1000 = 2³×5³) ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O(√n)
════════════════════════════════════════════════════════════════

    In the worst case (n is prime), we iterate up to n.
    But for composite numbers, each division reduces n significantly.
    On average, prime factorization runs in O(√n) because the
    largest prime factor ≤ √n (except when n itself is prime).

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(1)
════════════════════════════════════════════════════════════════

    Only a few integer variables (result, factor).
    No additional data structures needed.

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Prime factorization (decomposing n into prime factors)
    Greedy reasoning (smaller factors = fewer operations)
    Mathematical proof (a + b ≤ a × b for a,b ≥ 2)
    Number theory (trial division algorithm)
    Problem reduction (copy-paste → multiplication → factorization)
"""
