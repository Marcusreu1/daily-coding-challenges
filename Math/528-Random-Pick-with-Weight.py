"""
528. Random Pick with Weight
Difficulty: Medium
https://leetcode.com/problems/random-pick-with-weight/

PROBLEM:
    Given an array w where w[i] is the weight of index i,
    implement pickIndex() that returns a random index where the
    probability of picking index i is w[i] / sum(w).

    Higher weight = higher chance of being picked.

EXAMPLES:
    Input: w = [1, 3]
        pickIndex() → 1 (75% of the time)
        pickIndex() → 0 (25% of the time)

    Input: w = [1, 1, 1]
        Each index returned ~33% of the time

CONSTRAINTS:
    1 <= w.length <= 10^4
    1 <= w[i] <= 10^5
    At most 10^4 calls to pickIndex

KEY INSIGHT:
    Build a PREFIX SUM of weights. Each index "owns" a range of
    numbers proportional to its weight. Generate a random number
    and use BINARY SEARCH to find which range it falls into.

    This is like a roulette wheel where bigger sections (weights)
    are hit more often.

CHALLENGES:
    Ensuring exact probability proportions
    Efficiently finding the correct index (binary search vs linear)
    Getting the 1-indexed random range right with bisect_left

SOLUTION:
    __init__: Build prefix sum array
    pickIndex: Random number in [1, total] → binary search on prefix
"""


# STEP 1: Build prefix sum from weights
# STEP 2: Store total weight
# STEP 3: In pickIndex(), generate random number in [1, total]
# STEP 4: Binary search (bisect_left) to find which index owns that number
# STEP 5: Return the index


import random
from bisect import bisect_left

class Solution:

    def __init__(self, w: List[int]):

        self.prefix = []                                              # Prefix sum of weights
        total = 0                                                     # Running sum

        for weight in w:                                              # Build prefix sum
            total += weight                                           # Accumulate weight
            self.prefix.append(total)                                 # Store cumulative total

        self.total = total                                            # Total weight (upper bound for random)

    def pickIndex(self) -> int:

        r = random.randint(1, self.total)                             # Random number 1-indexed in [1, total]

        return bisect_left(self.prefix, r)                            # Find first prefix[i] >= r


"""
WHY EACH PART:
    self.prefix:            Defines the "ownership ranges" for each index
    total += weight:        Running sum builds the prefix array incrementally
    self.total:             Upper bound for our random number generation
    randint(1, total):      1-indexed ensures clean alignment with bisect_left
    bisect_left(prefix, r): Finds the first index whose prefix >= r (the owner of r)


HOW IT WORKS (Example: w = [2, 5, 3]):

    __init__:
    ├── weight=2: total=2,  prefix=[2]
    ├── weight=5: total=7,  prefix=[2, 7]
    ├── weight=3: total=10, prefix=[2, 7, 10]
    └── self.total = 10

    Ownership map:
    ┌───────────────────────────────────────────┐
    │ r:   1  2  3  4  5  6  7  8  9  10       │
    │ idx: 0  0  1  1  1  1  1  2  2   2       │
    │      └──┘  └────────────┘  └───────┘     │
    │    weight=2    weight=5      weight=3     │
    └───────────────────────────────────────────┘

    pickIndex() → r = 6:
    ├── bisect_left([2, 7, 10], 6) = 1
    └── return 1  (6 is in range 3-7, owned by idx 1)

    pickIndex() → r = 2:
    ├── bisect_left([2, 7, 10], 2) = 0
    └── return 0  (2 is in range 1-2, owned by idx 0)

    pickIndex() → r = 9:
    ├── bisect_left([2, 7, 10], 9) = 2
    └── return 2  (9 is in range 8-10, owned by idx 2)


HOW IT WORKS (Example: w = [1, 3]):

    __init__:
    ├── prefix = [1, 4]
    └── total = 4

    Ownership:
        r=1 → idx 0   (1 value  → prob 1/4 = 25%)
        r=2,3,4 → idx 1   (3 values → prob 3/4 = 75%)

    pickIndex() → r = 1: bisect_left([1,4], 1) = 0 
    pickIndex() → r = 3: bisect_left([1,4], 3) = 1 


WHY PREFIX SUM CREATES CORRECT PROBABILITIES:
    Each index i "owns" exactly w[i] consecutive numbers:

    idx 0 owns: [1 ........... prefix[0]]           → w[0] numbers
    idx 1 owns: [prefix[0]+1 .. prefix[1]]          → w[1] numbers
    idx 2 owns: [prefix[1]+1 .. prefix[2]]          → w[2] numbers
    ...

    Since we pick uniformly from [1, total]:
        P(idx i) = w[i] / total ✓

    Example: w = [2, 5, 3], total = 10
        P(idx 0) = 2/10 = 20% ✓
        P(idx 1) = 5/10 = 50% ✓
        P(idx 2) = 3/10 = 30% ✓


WHY bisect_left AND NOT bisect_right:
    prefix = [2, 7, 10]

    bisect_left([2,7,10], 2) = 0  ← r=2 belongs to idx 0 
    bisect_right([2,7,10], 2) = 1 ← r=2 would go to idx 1 

    bisect_left finds the first position where prefix[i] >= r
    This correctly assigns boundary values to their owner.

    With 1-indexed random + bisect_left:
        r = prefix[i] → lands ON the boundary → belongs to idx i ✓


WHY 1-INDEXED (NOT 0-INDEXED):
    prefix = [2, 7, 10]

    0-indexed: randint(0, 9)
        r=0 → bisect_left finds 0... but no prefix is 0!
        bisect_left([2,7,10], 0) = 0 → idx 0 gets 3 values (0,1,2)
        But weight of idx 0 is 2, not 3 

    1-indexed: randint(1, 10)
        r=1 → idx 0, r=2 → idx 0   → 2 values ✓
        r=3..7 → idx 1              → 5 values ✓
        r=8..10 → idx 2             → 3 values ✓


COMPARISON WITH PROBLEM 497 (Random Point in Rectangles):
    Both problems use the EXACT same technique!

    Problem 497: weight = number of points in rectangle
    Problem 528: weight = w[i] directly

    ┌──────────────────┬──────────────────────┐
    │    Problem 497   │    Problem 528       │
    ├──────────────────┼──────────────────────┤
    │ prefix of points │ prefix of weights    │
    │ random in total  │ random in total      │
    │ bisect for rect  │ bisect for index     │
    │ map to (x,y)     │ return index directly│
    └──────────────────┴──────────────────────┘

    Problem 528 is actually SIMPLER — no coordinate mapping needed!


HANDLING SPECIAL CASES:
    Single weight [5]:       prefix=[5], always returns 0 ✓
    Equal weights [1,1,1]:   Each has ~33% probability ✓
    One huge weight [1,999]: idx 1 picked 99.9% of time ✓
    All weight = 1:          Uniform distribution ✓


KEY TECHNIQUE:
    Prefix sum:              Encodes cumulative weight ranges
    Binary search:           O(log n) index lookup per pick
    Weighted sampling:       Bigger weight = bigger range = higher probability
    1-indexed random:        Clean alignment with bisect_left


EDGE CASES:
    w = [1]:                 Always returns 0 ✓
    w = [1, 1]:              50/50 distribution ✓
    w = [1, 99]:             idx 1 picked ~99% ✓
    w = [100000] * 10000:    Uniform, handles large totals ✓
    Single call:             Works correctly ✓
    10^4 calls:              Each O(log n), total O(n + q·log n) ✓


TIME COMPLEXITY:
    __init__:    O(n) — single pass to build prefix sum
    pickIndex(): O(log n) — binary search on prefix array

SPACE COMPLEXITY: O(n)
    Prefix sum array with n entries


CONCEPTS USED:
    Weighted random sampling
    Prefix sum (cumulative distribution function)
    Binary search (bisect_left)
    Probability proportional to weight
    Roulette wheel selection
"""
