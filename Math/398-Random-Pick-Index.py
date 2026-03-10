"""
398. Random Pick Index
Difficulty: Medium
https://leetcode.com/problems/random-pick-index/

PROBLEM:
Given an integer array nums with possible duplicates, randomly output
the index of a given target number. You can assume the given target
number must exist in the array.

Implement the Solution class:
    Solution(int[] nums) - Initializes the object with the array nums
    int pick(int target)  - Picks a random index i where nums[i] == target
                            Each valid index must have EQUAL probability

EXAMPLES:
Input: nums = [1,2,3,3,3]
    pick(3) → randomly returns 2, 3, or 4 (each with prob 1/3)
    pick(1) → always returns 0

CONSTRAINTS:
    1 <= nums.length <= 2 * 10^4
    -2^31 <= nums[i] <= 2^31 - 1
    target is guaranteed to exist in nums
    At most 10^4 calls to pick

KEY INSIGHT:
Preprocess the array into a HashMap: value → [list of indices].
Then each pick() is just a random.choice() from that list → O(1).

CHALLENGES:
    Equal probability for all valid indices
    Handling up to 10^4 calls efficiently
    Duplicates mean multiple valid indices per value

WHY NOT RESERVOIR SAMPLING:
    Reservoir Sampling scans the ENTIRE array on every pick() call → O(n).
    With 10^4 calls × 2×10^4 elements = 2×10^8 operations → TOO SLOW.
    HashMap preprocessing: O(n) once, then O(1) per call → MUCH FASTER.

SOLUTION:
    1. Preprocess: map each value to its list of indices
    2. On pick: random.choice from the index list of target
"""

# STEP 1: Build HashMap { value → [indices] } in __init__
# STEP 2: On pick(), retrieve index list and choose randomly

from collections import defaultdict
import random

class Solution:

    def __init__(self, nums: List[int]):
        self.indices = defaultdict(list)                                 # value → [list of indices]
        for i, num in enumerate(nums):                                   # One pass through array
            self.indices[num].append(i)                                  # Store each index under its value

    def pick(self, target: int) -> int:
        return random.choice(self.indices[target])                       # O(1) random pick from valid indices

"""
WHY EACH PART:

    defaultdict(list): Auto-creates empty list for unseen keys
    for i, num in enumerate(nums): Need both index and value
    self.indices[num].append(i): Group indices by their value
    random.choice(self.indices[target]): Picks uniformly at random from list

HOW IT WORKS (Example: nums = [1,2,3,3,3]):

    __init__ builds:
    ├── self.indices[1] = [0]
    ├── self.indices[2] = [1]
    └── self.indices[3] = [2, 3, 4]

    pick(3):
    ├── self.indices[3] = [2, 3, 4]
    ├── random.choice([2, 3, 4])
    └── returns 2, 3, or 4 with equal probability 1/3 ✓

    pick(1):
    ├── self.indices[1] = [0]
    ├── random.choice([0])
    └── always returns 0 ✓

WHY HASHMAP BEATS RESERVOIR SAMPLING:

    Reservoir Sampling:
    ├── __init__: O(1)
    ├── pick:     O(n) per call ← scans ENTIRE array each time
    ├── 10^4 calls × 2×10^4 elements = 2×10^8 ops
    └── TOO SLOW ✗

    HashMap (this solution):
    ├── __init__: O(n) once ← one-time preprocessing
    ├── pick:     O(1) per call ← instant lookup
    ├── 10^4 calls × O(1) = 10^4 ops
    └── FAST ✓

WHY random.choice GIVES EQUAL PROBABILITY:

    random.choice([2, 3, 4]):
    ├── P(2) = 1/3
    ├── P(3) = 1/3
    └── P(4) = 1/3
    Uniform distribution guaranteed by Python's random module ✓

EDGE CASES:

    Single element [5], pick(5): indices[5] = [0] → returns 0 ✓
    Target appears once: List has 1 element → always that index ✓
    Target appears n times: Each index has prob 1/n ✓
    All elements same [3,3,3]: indices[3] = [0,1,2] → works ✓
    Negative numbers: HashMap keys handle negatives ✓
    Multiple pick calls: Each call independent, O(1) each ✓

TIME COMPLEXITY:
    __init__: O(n) - one pass to build HashMap
    pick:     O(1) - dictionary lookup + random choice

SPACE COMPLEXITY: O(n)
    Dictionary stores every index grouped by value

CONCEPTS USED:
    HashMap preprocessing (value → indices)
    Grouping by key pattern
    random.choice for uniform probability
    Space-time trade-off (O(n) space for O(1) pick)
    defaultdict for cleaner code
"""
