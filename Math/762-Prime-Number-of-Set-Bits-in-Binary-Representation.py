"""
762. Prime Number of Set Bits in Binary Representation
Difficulty: Easy
https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/

════════════════════════════════════════════════════════════════
PROBLEM:
════════════════════════════════════════════════════════════════

Given two integers left and right, return the count of numbers
in the inclusive range [left, right] that have a PRIME number
of set bits (1-bits) in their binary representation.

EXAMPLES:

    Input: left=6, right=10  → Output: 4
        6  (110)  → 2 bits → prime ✓
        7  (111)  → 3 bits → prime ✓
        8  (1000) → 1 bit  → not prime ✗
        9  (1001) → 2 bits → prime ✓
        10 (1010) → 2 bits → prime ✓

    Input: left=10, right=15 → Output: 5
        10 (1010) → 2 ✓, 11 (1011) → 3 ✓, 12 (1100) → 2 ✓,
        13 (1101) → 3 ✓, 14 (1110) → 3 ✓, 15 (1111) → 4 ✗

CONSTRAINTS:

    1 <= left <= right <= 10^6
    0 <= number of set bits <= 20 (since 10^6 < 2^20)

════════════════════════════════════════════════════════════════
KEY INSIGHT:
════════════════════════════════════════════════════════════════

Since right ≤ 10^6 < 2^20, the maximum number of set bits is 20.
We only need primes from 2 to 19: {2, 3, 5, 7, 11, 13, 17, 19}

Store these in a SET for O(1) lookup instead of computing
primality each time.

For each number: count bits → check if count is in the prime set.

════════════════════════════════════════════════════════════════
CHALLENGES:
════════════════════════════════════════════════════════════════

1. EFFICIENT BIT COUNTING: Need a fast way to count 1-bits
2. PRIME CHECK: Avoid recomputing primality for every number
3. RANGE SIZE: Up to 10^6 numbers — must be efficient per number

════════════════════════════════════════════════════════════════
SOLUTION:
════════════════════════════════════════════════════════════════

STEP 1: Pre-define set of primes up to 20
STEP 2: For each number in [left, right], count set bits
STEP 3: Check if bit count is in the prime set
STEP 4: Increment counter if prime
"""


class Solution:
    def countPrimeSetBits(self, left: int, right: int) -> int:

        primes = {2, 3, 5, 7, 11, 13, 17, 19}                                   # All primes up to 20
        count = 0                                                                 # Numbers with prime set bits

        for num in range(left, right + 1):                                        # Check every number in range
            set_bits = bin(num).count('1')                                         # Count 1-bits in binary
            if set_bits in primes:                                                # Is the bit count prime?
                count += 1                                                        # Yes → increment counter

        return count


"""
════════════════════════════════════════════════════════════════
WHY EACH PART:
════════════════════════════════════════════════════════════════

primes = {2, 3, 5, 7, 11, 13, 17, 19}:
    Pre-computed set of ALL primes up to 20.
    Since max set bits = 20 (because 10^6 < 2^20), these are
    the only primes we'll ever need to check against.
    Using a set gives O(1) membership testing.

for num in range(left, right + 1):
    Iterate through every number in the inclusive range.
    right + 1 because range() is exclusive on upper bound.

bin(num).count('1'):
    bin(num) converts to binary string like '0b10101'.
    .count('1') counts occurrences of '1' in that string.
    This is Python's cleanest way to count set bits.

    Example: bin(21) = '0b10101' → count('1') = 3

set_bits in primes:
    O(1) lookup in hash set. Much faster than computing
    primality with trial division each time.

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: left=6, right=10):
════════════════════════════════════════════════════════════════

    primes = {2, 3, 5, 7, 11, 13, 17, 19}

    num=6:  bin(6)  = '110'    → count('1') = 2 → 2 ∈ primes ✓ → count=1
    num=7:  bin(7)  = '111'    → count('1') = 3 → 3 ∈ primes ✓ → count=2
    num=8:  bin(8)  = '1000'   → count('1') = 1 → 1 ∉ primes ✗ → count=2
    num=9:  bin(9)  = '1001'   → count('1') = 2 → 2 ∈ primes ✓ → count=3
    num=10: bin(10) = '1010'   → count('1') = 2 → 2 ∈ primes ✓ → count=4

    Return: 4 ✓

════════════════════════════════════════════════════════════════
HOW IT WORKS (Example: left=10, right=15):
════════════════════════════════════════════════════════════════

    num=10: 1010   → 2 bits → prime ✓ → count=1
    num=11: 1011   → 3 bits → prime ✓ → count=2
    num=12: 1100   → 2 bits → prime ✓ → count=3
    num=13: 1101   → 3 bits → prime ✓ → count=4
    num=14: 1110   → 3 bits → prime ✓ → count=5
    num=15: 1111   → 4 bits → NOT prime ✗ → count=5

    Return: 5 ✓

════════════════════════════════════════════════════════════════
WHY A SET INSTEAD OF PRIMALITY FUNCTION:
════════════════════════════════════════════════════════════════

    OPTION A — Compute primality each time:
    ├── def is_prime(n): check divisors up to √n
    ├── Time per check: O(√n) where n ≤ 20
    ├── Technically fine for small n, but unnecessary
    └── More code, more potential bugs

    OPTION B — Pre-computed set (our approach):
    ├── primes = {2, 3, 5, 7, 11, 13, 17, 19}
    ├── Time per check: O(1) hash lookup
    ├── One line, zero computation
    └── Cleanest and fastest ✓

    Why it works: there are only 20 possible bit counts (0-20),
    so we can trivially enumerate which are prime.

════════════════════════════════════════════════════════════════
WHY MAX SET BITS IS 20:
════════════════════════════════════════════════════════════════

    Constraint: right ≤ 10^6

    2^19 = 524,288
    2^20 = 1,048,576

    10^6 = 1,000,000 < 2^20 = 1,048,576

    So any number ≤ 10^6 fits in 20 bits.
    Maximum set bits = 20 (all 1s in 20-bit number).

    Therefore primes up to 20 cover ALL possible cases:
    {2, 3, 5, 7, 11, 13, 17, 19}

════════════════════════════════════════════════════════════════
ALTERNATIVE: BIT MANIPULATION FOR COUNTING:
════════════════════════════════════════════════════════════════

    Instead of bin().count('1'), we could count manually:

    Method 1 — Shift and mask:
        def count_bits(n):
            count = 0
            while n:
                count += n & 1        # Check last bit
                n >>= 1               # Shift right
            return count

    Method 2 — Brian Kernighan's algorithm:
        def count_bits(n):
            count = 0
            while n:
                n &= n - 1            # Remove lowest set bit
                count += 1
            return count

        Why n & (n-1) removes the lowest set bit:
        ├── n     = 10100  (has a 1 at position 2)
        ├── n-1   = 10011  (borrows from that 1)
        └── n&n-1 = 10000  (that 1 is gone!)

    Method 3 — Python built-in:
        bin(n).count('1')  ← clearest, built-in optimized

    All three are valid. bin().count('1') is the most Pythonic.

════════════════════════════════════════════════════════════════
ALTERNATIVE: ONE-LINER SOLUTION:
════════════════════════════════════════════════════════════════

    def countPrimeSetBits(self, left, right):
        primes = {2, 3, 5, 7, 11, 13, 17, 19}
        return sum(bin(n).count('1') in primes for n in range(left, right + 1))

    How it works:
    ├── Generator expression iterates range
    ├── bin(n).count('1') in primes returns True/False
    ├── sum() counts True values (True = 1, False = 0)
    └── Very Pythonic, same time complexity

════════════════════════════════════════════════════════════════
COMMON SET BIT COUNTS FOR REFERENCE:
════════════════════════════════════════════════════════════════

    Bits   Count    Prime?
    ─────────────────────────
     0       0        ✗
     1       1        ✗
     2       2        ✓  ← smallest prime
     3       3        ✓
     4       4        ✗  (2×2)
     5       5        ✓
     6       6        ✗  (2×3)
     7       7        ✓
     8       8        ✗  (2×4)
     9       9        ✗  (3×3)
    10      10        ✗  (2×5)
    11      11        ✓
    12      12        ✗  (2×6)
    13      13        ✓
    14      14        ✗  (2×7)
    15      15        ✗  (3×5)
    16      16        ✗  (2×8)
    17      17        ✓
    18      18        ✗  (2×9)
    19      19        ✓
    20      20        ✗  (2×10)

    Only 8 out of 21 possible values are prime.

════════════════════════════════════════════════════════════════
EDGE CASES:
════════════════════════════════════════════════════════════════

    left = right = 1         → bin(1)='1' → 1 bit → not prime → 0 ✓
    left = right = 3         → bin(3)='11' → 2 bits → prime → 1 ✓
    left = 1, right = 1      → only 1, 1 bit, not prime → 0 ✓
    All numbers have 1 bit   → powers of 2 → all return 0 ✓
    left = right = 10^6      → single number check ✓
    left = 1, right = 10^6   → 10^6 iterations → still fast ✓

════════════════════════════════════════════════════════════════
TIME COMPLEXITY: O((right - left) × log(right))
════════════════════════════════════════════════════════════════

    (right - left + 1) numbers to check
    Each number: counting bits takes O(log(num)) ≈ O(20)
    Set lookup: O(1)

    Total: O((right - left) × log(right))

    For max input: 10^6 × 20 = 2 × 10^7 → fast ✓

════════════════════════════════════════════════════════════════
SPACE COMPLEXITY: O(1)
════════════════════════════════════════════════════════════════

    Prime set: fixed size of 8 elements → O(1)
    Counter variable: O(1)
    bin() creates a temporary string of at most 22 chars → O(1)

════════════════════════════════════════════════════════════════
CONCEPTS USED:
════════════════════════════════════════════════════════════════

    Bit counting (popcount — counting set bits in binary)
    Prime numbers (pre-computed set for bounded range)
    Hash set for O(1) lookup (membership testing)
    Binary representation (understanding base-2 encoding)
    Bounded analysis (max 20 bits → only 8 relevant primes)
"""
