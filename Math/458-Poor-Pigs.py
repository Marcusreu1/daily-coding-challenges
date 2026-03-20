"""
458. Poor Pigs
Difficulty: Hard
https://leetcode.com/problems/poor-pigs/

PROBLEM:
There are buckets of liquid, exactly one of which is poisoned.
To figure out which one is poisoned, you can feed some number of pigs.
A pig dies after drinking poison in exactly minutesToDie minutes.
You have minutesToTest minutes total to determine the poisoned bucket.

Return the MINIMUM number of pigs needed.

EXAMPLES:
Input: buckets=4, minutesToDie=15, minutesToTest=15    → Output: 2
Input: buckets=4, minutesToDie=15, minutesToTest=30    → Output: 2
Input: buckets=1000, minutesToDie=15, minutesToTest=60 → Output: 5

CONSTRAINTS:
    1 <= buckets <= 1000
    1 <= minutesToDie <= minutesToTest <= 100

KEY INSIGHT:
Each pig can be in (T+1) states: dies in round 1, 2, ..., T, or survives.
With p pigs, we can distinguish (T+1)^p outcomes → (T+1)^p buckets.
Find minimum p such that (T+1)^p >= buckets.

This is equivalent to: how many digits in base (T+1) to represent
'buckets' values?

CHALLENGES:
    Not obvious that multiple rounds multiply the states
    Need to see the connection to number systems
    Understanding information theory behind the solution

ANALOGY:
    pigs    = digits in a number
    states  = base of the number system
    buckets = range of values to represent

    Binary (1 round):  2^p >= buckets  (each pig: alive/dead)
    Base-5 (4 rounds): 5^p >= buckets  (each pig: 5 possible fates)

SOLUTION:
    1. Calculate rounds T = minutesToTest // minutesToDie
    2. States per pig = T + 1
    3. Find minimum p where (T+1)^p >= buckets
"""

# STEP 1: Calculate number of test rounds
# STEP 2: Find minimum pigs by increasing p until (T+1)^p >= buckets

import math

class Solution:
    def poorPigs(self, buckets: int, minutesToDie: int, minutesToTest: int) -> int:

        rounds = minutesToTest // minutesToDie                           # How many test rounds available
        states = rounds + 1                                              # States per pig (die R1, R2,..., survive)

        if buckets == 1:                                                 # Only 1 bucket → no testing needed
            return 0

        pigs = 0                                                         # Start with 0 pigs
        while states ** pigs < buckets:                                  # Until we can cover all buckets
            pigs += 1                                                    # Add one more pig

        return pigs                                                      # Minimum pigs needed

"""
WHY EACH PART:

    rounds = minutesToTest // minutesToDie: How many sequential tests we can run
    states = rounds + 1: Each pig has (rounds + 1) possible outcomes
        ├── Die in round 1, die in round 2, ..., die in round T
        └── Survive all rounds
    if buckets == 1: return 0: If only 1 bucket, it must be poisoned
    while states ** pigs < buckets: Keep adding pigs until capacity is enough
    pigs += 1: Each additional pig multiplies capacity by (states)

HOW IT WORKS (Example: buckets=4, minutesToDie=15, minutesToTest=15):

    rounds = 15 // 15 = 1
    states = 1 + 1 = 2 (die or survive)

    pigs=0: 2^0 = 1 < 4 → not enough
    pigs=1: 2^1 = 2 < 4 → not enough
    pigs=2: 2^2 = 4 ≥ 4 → enough!

    Result: 2 ✓

    Visual (2×2 grid):
                    Pig B
               Dies    Survives
    Pig A
    Dies       C1        C2
    Survives   C3        C4

HOW IT WORKS (Example: buckets=1000, minutesToDie=15, minutesToTest=60):

    rounds = 60 // 15 = 4
    states = 4 + 1 = 5

    pigs=0: 5^0 = 1     < 1000 → not enough
    pigs=1: 5^1 = 5     < 1000 → not enough
    pigs=2: 5^2 = 25    < 1000 → not enough
    pigs=3: 5^3 = 125   < 1000 → not enough
    pigs=4: 5^4 = 625   < 1000 → not enough
    pigs=5: 5^5 = 3125  ≥ 1000 → enough!

    Result: 5 ✓

WHY (T+1) STATES PER PIG:

    With T=4 rounds, a pig can:
    ├── Die in round 1  (state 0)
    ├── Die in round 2  (state 1)
    ├── Die in round 3  (state 2)
    ├── Die in round 4  (state 3)
    └── Survive all     (state 4)

    That's 5 = T+1 distinguishable outcomes per pig.
    Each outcome tells us something about which bucket is poisoned.

WHY (T+1)^p TOTAL OUTCOMES:

    Each pig independently has (T+1) states.
    p pigs → (T+1) × (T+1) × ... × (T+1) = (T+1)^p combinations.

    Like a number with p digits in base (T+1):
    ├── 2 pigs, 3 states each: 00, 01, 02, 10, 11, 12, 20, 21, 22 = 9
    └── 3^2 = 9 ✓

    Each combination maps to exactly one bucket,
    so we can identify up to (T+1)^p different buckets.

WHY THIS IS LIKE A NUMBER SYSTEM:

    Base 2 (binary):     each digit is 0 or 1     → 2^p values
    Base 10 (decimal):   each digit is 0-9        → 10^p values
    Base (T+1) (pigs):   each pig has 0 to T fate → (T+1)^p values

    "How many pigs for 1000 buckets with 5 states?"
    = "How many base-5 digits to represent 1000?"
    = ceil(log₅(1000)) = 5

TESTING STRATEGY (How pigs actually drink):

    2 pigs, 1 round, 4 buckets in 2×2 grid:

    Pig A drinks: row 1 mix (buckets 3,4)
    Pig B drinks: col 1 mix (buckets 2,4)

    Outcomes:
    ├── A lives, B lives → bucket 1 (untouched by both)
    ├── A lives, B dies  → bucket 2 (only B drank it)
    ├── A dies,  B lives → bucket 3 (only A drank it)
    └── A dies,  B dies  → bucket 4 (both drank it)

ALTERNATIVE FORMULA (using logarithm):

    pigs = ⌈log(buckets) / log(states)⌉

    For buckets=1000, states=5:
    pigs = ⌈log(1000) / log(5)⌉ = ⌈6.907 / 1.609⌉ = ⌈4.29⌉ = 5 ✓

    But the while loop is clearer and avoids floating point issues.

EDGE CASES:

    buckets = 1: No testing needed → 0 ✓
    buckets = 2, 1 round: Need 1 pig (2^1=2) → 1 ✓
    buckets = 1000, 1 round: Need 10 pigs (2^10=1024) → 10 ✓
    minutesToTest = minutesToDie: 1 round → binary testing ✓
    Large rounds: More states per pig → fewer pigs needed ✓
    Exact power: 5^4=625, need 625 buckets → 4 pigs exactly ✓

TIME COMPLEXITY: O(log(buckets) / log(states))
    The while loop runs at most log_{states}(buckets) times
    At most ~10 iterations for buckets ≤ 1000

SPACE COMPLEXITY: O(1)
    Only a few variables: rounds, states, pigs

CONCEPTS USED:
    Information theory (states and distinguishable outcomes)
    Number systems (base T+1 representation)
    Combinatorics (independent outcomes multiply)
    Logarithmic counting
    Problem abstraction (physical setup → math formula)
"""
