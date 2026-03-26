"""
479. Largest Palindrome Product
Difficulty: Hard
https://leetcode.com/problems/largest-palindrome-product/

PROBLEM:
Given an integer n, return the largest palindromic integer that can be
represented as the product of two n-digit integers. Since the answer
can be very large, return it modulo 1337.

EXAMPLES:
Input: n = 2  → Output: 987
    Largest palindrome = 9009 = 91 × 99
    9009 % 1337 = 987

Input: n = 1  → Output: 9
    Largest palindrome = 9 = 3 × 3 (or 9 × 1)
    9 % 1337 = 9

CONSTRAINTS:
    1 <= n <= 8

KEY INSIGHT:
Instead of checking all pairs O(n²), CONSTRUCT palindromes from largest
to smallest by mirroring the first half. For each palindrome, check if
it can be factored into two n-digit numbers. The first valid one is the
answer (since we check largest first).

CHALLENGES:
    Brute force over all pairs is too slow for large n
    Must construct palindromes efficiently
    Verifying factorization needs optimization
    n=1 is a special case (single-digit palindromes)

PALINDROME CONSTRUCTION:
    A 2n-digit palindrome is fully defined by its first n digits.
    Mirror first half: "906" → "906" + "609" = "906609"
    Start from largest first half (999...9) and go down.

FACTORIZATION CHECK:
    For palindrome P, check divisors i from upper downward.
    Only need i where i² ≥ P (since if P = a×b, smaller factor ≤ √P).
    If P % i == 0, the quotient is automatically n-digit.

SOLUTION:
    1. Handle n=1 edge case
    2. Construct palindromes from largest first half downward
    3. Verify each palindrome can be factored into two n-digit numbers
    4. Return first valid palindrome mod 1337
"""

# STEP 1: Handle n=1 special case
# STEP 2: Construct palindromes by mirroring first half
# STEP 3: Check if palindrome has valid n-digit factorization
# STEP 4: Return first valid result mod 1337

class Solution:
    def largestPalindrome(self, n: int) -> int:

        if n == 1:                                                       # Special case: 9 = 3×3
            return 9

        upper = 10 ** n - 1                                              # Largest n-digit number (99, 999...)

        for first_half in range(upper, 0, -1):                           # Largest first half downward
            s = str(first_half)                                          # Convert to string
            palindrome = int(s + s[::-1])                                # Mirror: "90" → "9009"

            i = upper                                                    # Try divisors from largest
            while i * i >= palindrome:                                   # Only check i ≥ √palindrome
                if palindrome % i == 0:                                  # Found valid factorization!
                    return palindrome % 1337                             # Return mod 1337
                i -= 1                                                   # Try next smaller divisor

        return 0                                                         # Should never reach here

"""
WHY EACH PART:

    if n == 1: return 9: Algorithm builds 2n-digit palindromes, misses 1-digit ones
    upper = 10**n - 1: Largest n-digit number (99, 999, 9999...)
    range(upper, 0, -1): Start from largest first half, go down
    s + s[::-1]: Mirror string to create palindrome ("90" → "90"+"09" = "9009")
    int(...): Convert palindrome string back to integer
    while i * i >= palindrome: Only check factors ≥ √palindrome
        ├── If P = a×b and a ≤ b, then a ≤ √P
        ├── We iterate i from upper, representing the larger factor b
        └── When i² < P, any remaining factor would be > i → already checked
    palindrome % i == 0: i divides palindrome → valid product!
    palindrome % 1337: Problem requires modulo 1337

HOW IT WORKS (Example: n = 2):

    upper = 99

    first_half = 99 → palindrome = 9999
    ├── i=99: 99² = 9801 < 9999 → while fails immediately
    └── SKIP (9999 > 99×99, impossible to be product of two 2-digit)

    first_half = 98 → palindrome = 9889
    ├── i=99: 9801 < 9889 → while fails
    └── SKIP

    first_half = 97 → palindrome = 9779
    ├── i=99: 9801 ≥ 9779 ✓ → 9779 % 99 = 77 ≠ 0
    ├── i=98: 9604 < 9779 → STOP
    └── No valid factorization

    ... (skipping some) ...

    first_half = 90 → palindrome = 9009
    ├── i=99: 9801 ≥ 9009 ✓ → 9009 % 99 = 0 → FOUND!
    │   9009 / 99 = 91 (2-digit ✓)
    └── return 9009 % 1337 = 987 ✓

WHY CONSTRUCT PALINDROMES INSTEAD OF CHECKING PRODUCTS:

    Brute force (pair-centric):
    ├── Try all pairs (a, b) of n-digit numbers
    ├── Check if a × b is palindrome
    ├── ~(9×10^(n-1))² pairs
    └── n=8: ~8.1 × 10^15 pairs ✗ IMPOSSIBLE

    Our approach (palindrome-centric):
    ├── Construct palindromes from largest to smallest
    ├── Check if each is a valid product
    ├── Usually finds answer in first few palindromes
    └── n=8: checks very few palindromes ✓ FAST

WHY MIRROR CREATES ALL PALINDROMES:

    A 2n-digit palindrome reads same forwards and backwards.
    The second half is DETERMINED by the first half.

    "906609": first half "906" → reverse "609" → concatenate
    "9009":   first half "90"  → reverse "09"  → concatenate

    By iterating all first halves, we generate ALL 2n-digit palindromes.
    Starting from the largest ensures we find the maximum first.

WHY i*i >= palindrome IS THE RIGHT CONDITION:

    If palindrome = a × b, assume a ≤ b (WLOG):
    ├── a ≤ √palindrome ≤ b
    ├── b ≥ √palindrome → b² ≥ palindrome
    └── We iterate b from upper downward while b² ≥ palindrome

    This ensures we check ALL valid larger factors:
    ├── i=upper: check if upper divides palindrome
    ├── i=upper-1: check next...
    └── i=√palindrome: stop (any smaller i would need b > i > upper)

    If palindrome % i == 0:
    ├── i is the larger factor (i ≥ √palindrome)
    ├── palindrome/i is the smaller factor (≤ i ≤ upper)
    └── Both are n-digit → valid! ✓

WHY n=1 IS SPECIAL:

    For n=1, our algorithm builds 2-digit palindromes:
    ├── 99 = 9×11 (11 is not 1-digit) ✗
    ├── 88 = 8×11 ✗
    ├── 77 = 7×11 ✗
    └── ... no 2-digit palindrome is product of two 1-digit numbers

    But the answer is 9 (a 1-digit palindrome):
    ├── 9 = 3×3 ✓ or 9×1 ✓
    └── Must handle separately since algorithm only builds 2n-digit palindromes

WHY THE FIRST PALINDROME FOUND IS THE ANSWER:

    We iterate first_half from upper downward:
    ├── first_half = 99 → palindrome = 9999 (largest possible)
    ├── first_half = 98 → palindrome = 9889 (second largest)
    ├── first_half = 97 → palindrome = 9779
    └── ... strictly decreasing

    Since palindromes are checked in DECREASING order,
    the first one with a valid factorization IS the maximum ✓

EXAMPLE ANSWERS BY n:

    n=1: palindrome = 9       = 3 × 3           → 9 % 1337 = 9
    n=2: palindrome = 9009    = 91 × 99          → 9009 % 1337 = 987
    n=3: palindrome = 906609  = 913 × 993        → 906609 % 1337 = 123
    n=4: palindrome = 99000099 = 9901 × 9999     → 99000099 % 1337 = 597

EDGE CASES:

    n = 1: Special case → returns 9 ✓
    n = 2: First non-trivial case → 9009 → 987 ✓
    n = 8: Large numbers but algorithm converges quickly ✓
    Mod 1337: Applied at the end ✓
    All palindromes checked in decreasing order: First found = largest ✓

TIME COMPLEXITY: O(10^n) worst case
    Outer loop: at most 9×10^(n-1) palindromes
    Inner loop: very few iterations per palindrome (usually < 10)
    In practice, answer found in first few palindromes for most n
    
SPACE COMPLEXITY: O(n)
    String operations for palindrome construction (length 2n)
    Only a few integer variables

CONCEPTS USED:
    Palindrome construction by mirroring
    Top-down search (largest first)
    Factor verification with √P bound
    String manipulation for mirroring
    Modular arithmetic
    Special case handling
"""
