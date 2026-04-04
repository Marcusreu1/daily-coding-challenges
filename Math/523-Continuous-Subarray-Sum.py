"""
523. Continuous Subarray Sum
Difficulty: Medium
https://leetcode.com/problems/continuous-subarray-sum/

PROBLEM:
    Given an integer array nums and an integer k, return true if nums
    has a "good subarray": a contiguous subarray of length >= 2 whose
    sum is a multiple of k (i.e., sum % k == 0).

EXAMPLES:
    Input: nums = [23,2,4,6,7], k = 6  → Output: true  ([2,4] sums to 6)
    Input: nums = [23,2,6,4,7], k = 6  → Output: true  ([23,2,6,4,7] sums to 42)
    Input: nums = [23,2,6,4,7], k = 13 → Output: false

CONSTRAINTS:
    1 <= nums.length <= 10^5
    0 <= nums[i] <= 10^9
    1 <= k <= 2^31 - 1

KEY INSIGHT:
    If prefix_sum[j] % k == prefix_sum[i] % k, then the subarray
    sum from i+1 to j is divisible by k.

    Same remainder = difference is multiple of k.

    Use a hash map {remainder: first_index} to detect repeated remainders.
    Initialize with {0: -1} for subarrays starting from index 0.

CHALLENGES:
    Remembering to initialize {0: -1} for sums from the start
    Ensuring subarray length >= 2 (check index distance)
    Only storing FIRST occurrence (maximizes distance for length check)

SOLUTION:
    Track running prefix sum mod k.
    Store first index of each remainder in hash map.
    If same remainder seen again with distance >= 2, return true.
"""


# STEP 1: Initialize hash map with {0: -1} for sums from array start
# STEP 2: Accumulate prefix sum, compute remainder (mod k)
# STEP 3: If remainder seen before AND distance >= 2, return true
# STEP 4: If remainder is new, store its index (first occurrence only)
# STEP 5: If loop ends without finding, return false


class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:

        remainder_map = {0: -1}                                       # remainder → first index; 0 at "virtual" index -1
        prefix = 0                                                    # Running prefix sum

        for i, num in enumerate(nums):                                # Iterate through array
            prefix += num                                             # Accumulate prefix sum
            remainder = prefix % k                                    # Current remainder mod k

            if remainder in remainder_map:                            # Same remainder seen before?
                if i - remainder_map[remainder] >= 2:                 # Subarray length >= 2?
                    return True                                       # Found a good subarray!
            else:
                remainder_map[remainder] = i                          # Store FIRST occurrence only

        return False                                                  # No good subarray found


"""
WHY EACH PART:
    remainder_map = {0: -1}:  Handles subarrays starting from index 0 whose sum is multiple of k
    prefix += num:            Running prefix sum (no need to store array, just accumulate)
    prefix % k:               Same remainder = their difference is divisible by k
    remainder in map:         Check if we've seen this remainder before
    i - map[remainder] >= 2:  Ensure subarray has at least 2 elements
    else: map[remainder] = i: Only store FIRST occurrence (don't overwrite!)
    return False:             Exhausted all elements, no good subarray exists


HOW IT WORKS (Example: nums = [23,2,4,6,7], k = 6):

    Init: remainder_map = {0: -1}, prefix = 0

    i=0, num=23:
    ├── prefix = 23
    ├── remainder = 23 % 6 = 5
    ├── 5 in map? NO
    └── remainder_map = {0: -1, 5: 0}

    i=1, num=2:
    ├── prefix = 25
    ├── remainder = 25 % 6 = 1
    ├── 1 in map? NO
    └── remainder_map = {0: -1, 5: 0, 1: 1}

    i=2, num=4:
    ├── prefix = 29
    ├── remainder = 29 % 6 = 5
    ├── 5 in map? YES, at index 0
    ├── distance = 2 - 0 = 2 >= 2? YES 
    └── return True!

    Subarray found: nums[1..2] = [2, 4], sum = 6, 6 % 6 = 0 ✓


HOW IT WORKS (Example: nums = [23,2,6,4,7], k = 13):

    Init: remainder_map = {0: -1}, prefix = 0

    i=0: prefix=23,  rem=23%13=10  → map={0:-1, 10:0}
    i=1: prefix=25,  rem=25%13=12  → map={0:-1, 10:0, 12:1}
    i=2: prefix=31,  rem=31%13=5   → map={0:-1, 10:0, 12:1, 5:2}
    i=3: prefix=35,  rem=35%13=9   → map={0:-1, 10:0, 12:1, 5:2, 9:3}
    i=4: prefix=42,  rem=42%13=3   → map={0:-1, 10:0, 12:1, 5:2, 9:3, 3:4}

    No repeated remainders → return False ✓


WHY {0: -1} IS ESSENTIAL:
    nums = [3, 3], k = 6

    WITHOUT {0: -1}:
        i=0: prefix=3,  rem=3  → map={3: 0}
        i=1: prefix=6,  rem=0  → map={3: 0, 0: 1}
        Loop ends → return False WRONG!

    WITH {0: -1}:
        i=0: prefix=3,  rem=3  → map={0:-1, 3:0}
        i=1: prefix=6,  rem=0  → 0 in map at index -1
             distance = 1-(-1) = 2 >= 2 → return True 

    The {0: -1} says: "a prefix sum of 0 existed before the array"
    So if prefix_sum at index j is divisible by k,
    the subarray [0..j] has sum = multiple of k ✓


WHY STORE ONLY FIRST OCCURRENCE:
    If we overwrite with latest index, we might MISS valid subarrays:

    nums = [1, 5, 5, 1], k = 6
    remainders: 1, 0, 5, 0
                      ↑     ↑
               first 0 at -1, second 0 at index 1

    If we stored 0→1 (overwriting -1):
        At i=3, rem=0, distance = 3-1 = 2 → still works here
    
    But in general, keeping first index gives MAXIMUM distance,
    making it more likely to satisfy the >= 2 condition.


WHY THE MATH WORKS (PROOF):
    Let S[i] = prefix sum up to index i
    Let S[j] = prefix sum up to index j, where j > i

    If S[i] % k == S[j] % k:
        S[i] = a*k + r    (for some integers a, r)
        S[j] = b*k + r    (for some integer b, same r)

        S[j] - S[i] = (b-a)*k = multiple of k 

    And S[j] - S[i] = sum of nums[i+1 .. j]
    So that subarray sum is a multiple of k!


HANDLING SPECIAL CASES:
    All zeros [0,0,0]:     prefix stays 0, remainder 0 repeats → true ✓
    Single element [6]:    Length 1 < 2 → false ✓
    k = 1:                 Every integer is multiple of 1 → true if len >= 2 ✓
    Large k:               Remainders just become the prefix sums themselves ✓
    Consecutive zeros:     [5,0,0] → subarray [0,0] sum=0 is multiple of any k ✓


KEY TECHNIQUE:
    Prefix sum:            Reduces subarray sum to difference of two values
    Modular arithmetic:    Same remainder = difference divisible by k
    Hash map:              O(1) lookup for previously seen remainders
    First occurrence:      Maximizes subarray length for >= 2 check
    Virtual index -1:      Handles subarrays starting from beginning


EDGE CASES:
    nums = [0,0]:          sum=0 is multiple of any k → true ✓
    nums = [1,0]:          sum=1, only [1,0] → depends on k ✓
    nums = [0]:            length 1 → false ✓
    nums = [k, k]:         sum=2k → true ✓
    k = 1:                 Any subarray of len >= 2 → true ✓
    Very large k:          May never find multiple → false possible ✓
    All same elements:     Predictable remainders, handles correctly ✓


TIME COMPLEXITY: O(n)
    Single pass through the array
    Hash map operations are O(1) average

SPACE COMPLEXITY: O(min(n, k))
    Hash map stores at most k distinct remainders (0 to k-1)
    Or at most n entries if n < k


CONCEPTS USED:
    Prefix sum
    Modular arithmetic (remainder properties)
    Hash map for O(1) lookups
    Pigeonhole principle (if n > k, must repeat a remainder)
    Virtual index technique ({0: -1})
"""
