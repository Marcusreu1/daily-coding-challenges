"""
477. Total Hamming Distance
Difficulty: Medium
https://leetcode.com/problems/total-hamming-distance/

PROBLEM:
The Hamming distance between two integers is the number of positions
at which the corresponding bits differ. Given an integer array nums,
return the sum of Hamming distances between all pairs nums[i] and nums[j]
where 0 <= i < j < n.

EXAMPLES:
Input: nums = [4,14,2]  → Output: 6
    Hamming(4,14)=2, Hamming(4,2)=2, Hamming(14,2)=2 → 2+2+2=6

Input: nums = [4,14,4]  → Output: 4

CONSTRAINTS:
    1 <= nums.length <= 10^4
    0 <= nums[i] <= 10^9

KEY INSIGHT:
Instead of comparing all O(n²) pairs, analyze each BIT POSITION
independently. For bit position b, if there are 'ones' numbers with
bit b = 1 and 'zeros' numbers with bit b = 0, the contribution to
total Hamming distance is ones × zeros.

CHALLENGES:
    Brute force O(n² × 32) is too slow for n = 10^4
    Need to shift perspective: from "pairs" to "bits"
    Understanding why ones × zeros counts all differing pairs

WHY ones × zeros:
    A pair differs at bit b only if one has 1 and other has 0.
    Each "1-number" pairs with each "0-number" → ones × zeros pairs.

SOLUTION:
    1. For each of 32 bit positions
    2. Count how many numbers have a 1 at that position
    3. Contribution = ones × (n - ones)
    4. Sum all contributions
"""

# STEP 1: Iterate through each bit position (0 to 30)
# STEP 2: Count numbers with bit = 1 at this position
# STEP 3: Contribution = ones × zeros, accumulate total

class Solution:
    def totalHammingDistance(self, nums: List[int]) -> int:

        total = 0                                                        # Total Hamming distance
        n = len(nums)                                                    # Number of elements

        for bit in range(31):                                            # Check each bit position (0-30)
            ones = 0                                                     # Count of numbers with 1 at this bit

            for num in nums:                                             # Check each number
                ones += (num >> bit) & 1                                 # Extract bit and count if 1

            total += ones * (n - ones)                                   # ones × zeros = pairs that differ here

        return total

"""
WHY EACH PART:

    total = 0: Accumulates Hamming distance across all bit positions
    n = len(nums): Need total count to calculate zeros = n - ones
    for bit in range(31): nums[i] ≤ 10^9 < 2^30, so 31 bits suffice
    ones = 0: Fresh count for each bit position
    (num >> bit) & 1: Shift right to bring target bit to position 0, mask it
    ones += ...: Count how many numbers have 1 at this position
    ones * (n - ones): Each "1" paired with each "0" = one differing pair
    total += ...: Accumulate contribution from this bit position

HOW IT WORKS (Example: nums = [4, 14, 2]):

    4  = 0100,  14 = 1110,  2 = 0010
    n = 3

    Bit 0: (4>>0)&1=0, (14>>0)&1=0, (2>>0)&1=0
    ├── ones=0, zeros=3
    ├── contribution = 0 × 3 = 0
    └── total = 0

    Bit 1: (4>>1)&1=0, (14>>1)&1=1, (2>>1)&1=1
    ├── ones=2, zeros=1
    ├── contribution = 2 × 1 = 2
    └── total = 2

    Bit 2: (4>>2)&1=1, (14>>2)&1=1, (2>>2)&1=0
    ├── ones=2, zeros=1
    ├── contribution = 2 × 1 = 2
    └── total = 4

    Bit 3: (4>>3)&1=0, (14>>3)&1=1, (2>>3)&1=0
    ├── ones=1, zeros=2
    ├── contribution = 1 × 2 = 2
    └── total = 6

    Bits 4-30: all zeros → no contribution

    Result: 6 ✓

WHY (num >> bit) & 1 EXTRACTS A SINGLE BIT:

    num = 14 = 1110,  bit = 2

    Step 1: num >> 2 = 1110 >> 2 = 0011 (shift right by 2)
    Step 2: 0011 & 0001 = 0001 = 1 (mask all but last bit)

    Result: bit 2 of 14 is 1 ✓

    Another: num = 4 = 0100, bit = 1
    Step 1: 0100 >> 1 = 0010
    Step 2: 0010 & 0001 = 0000 = 0

    Result: bit 1 of 4 is 0 ✓

WHY ones × zeros COUNTS ALL DIFFERING PAIRS:

    Numbers at bit 2: [4=1, 14=1, 2=0]
    
    Ones group:  {4, 14}    (2 numbers)
    Zeros group: {2}        (1 number)

    Pairs that DIFFER at bit 2:
    ├── (4, 2):  1 vs 0 → different ✓
    ├── (14, 2): 1 vs 0 → different ✓
    └── Total: 2 pairs

    Pairs that DON'T differ at bit 2:
    └── (4, 14): 1 vs 1 → same ✗

    ones × zeros = 2 × 1 = 2 ← matches exactly!

    General: every "1-number" with every "0-number" = one differing pair.
    No pair is counted twice, no pair is missed. Perfect count ✓

BRUTE FORCE vs OPTIMIZED:

    Brute Force O(n² × 32):
    ├── for i in range(n):
    │       for j in range(i+1, n):
    │           total += bin(nums[i] ^ nums[j]).count('1')
    ├── n=10^4 → ~50M pairs × 32 bits ≈ 1.6 × 10^9 ops
    └── TOO SLOW ✗

    Bit-by-bit O(n × 32):
    ├── for bit in range(31):
    │       count ones, multiply by zeros
    ├── n=10^4 → 31 × 10^4 ≈ 310K ops
    └── FAST ✓

    Speedup: ~5000x faster for n = 10^4!

WHY 31 BITS AND NOT 32:

    Constraint: 0 <= nums[i] <= 10^9
    2^30 = 1,073,741,824 > 10^9
    
    So 31 bits (positions 0-30) are enough to cover all values.
    Bit 31 (sign bit) is never set since all values are non-negative.

PERSPECTIVE SHIFT (The key mental model):

    Traditional thinking (pair-centric):
        "For each PAIR, count differing bits"
        → O(n² × 32)

    Better thinking (bit-centric):
        "For each BIT POSITION, count differing pairs"
        → O(32 × n)

    Same answer, fundamentally different approach.
    The bit-centric view eliminates the n² bottleneck.

    This is like asking:
    "How many students disagree on EACH question?"
    vs
    "For EACH pair of students, count disagreements"

EDGE CASES:

    Single element [5]: No pairs → 0 ✓
    Two elements [4,14]: One pair → Hamming(4,14) = 2 ✓
    All same [3,3,3]: All bits same → ones×zeros = 0 everywhere → 0 ✓
    All zeros [0,0,0]: No ones → 0 ✓
    Powers of 2 [1,2,4,8]: Each has exactly one 1-bit ✓
    Maximum value 10^9: Fits in 30 bits → 31 positions enough ✓
    Large n (10^4): O(31n) ≈ 310K operations → fast ✓

TIME COMPLEXITY: O(n × 31) = O(n)
    31 bit positions (constant)
    For each bit, iterate through all n numbers
    Total: 31 × n = O(n)

SPACE COMPLEXITY: O(1)
    Only a few variables: total, ones, bit
    No extra data structures

CONCEPTS USED:
    Bit manipulation (shift and mask)
    Counting by bit position instead of by pair
    Combinatorics (ones × zeros = differing pairs)
    Perspective shift (pair-centric → bit-centric)
    Optimization from O(n²) to O(n)
"""
