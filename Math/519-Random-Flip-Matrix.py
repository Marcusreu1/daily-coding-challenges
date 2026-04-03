"""
519. Random Flip Matrix
Difficulty: Medium
https://leetcode.com/problems/random-flip-matrix/

PROBLEM:
    You are given the number of rows m and columns n of a binary matrix.
    Initially, all values are 0.
    
    Design a class with:
        - flip(): randomly chooses a 0-valued cell uniformly, flips it to 1,
                  and returns its position [row, col]
        - reset(): resets all values back to 0

    All zero cells must have the SAME probability of being chosen.

EXAMPLES:
    Input:
        ["Solution", "flip", "flip", "flip", "reset", "flip"]
        [[3,1], [], [], [], [], []]

    Possible behavior:
        Matrix 3x1 has cells [0,0], [1,0], [2,0]
        flip() → [1,0]
        flip() → [0,0]
        flip() → [2,0]
        reset()
        flip() → any of [0,0], [1,0], [2,0]

CONSTRAINTS:
    1 <= m, n <= 10^4
    1 <= m * n <= 10^8
    At most 1000 calls to flip and reset total

KEY INSIGHT:
    Treat the matrix as a 1D array of size m*n.
    We need to sample WITHOUT replacement uniformly.

    This is a partial Fisher-Yates shuffle:
        - pick a random index r in [0, total-1]
        - map it to its real value
        - swap it with the last available value
        - decrease total

    We use a hash map to simulate the swaps lazily,
    without storing the full array.

CHALLENGES:
    Ensuring uniform random choice among remaining zero cells
    Avoiding O(m*n) memory for very large matrices
    Avoiding repeated random retries on already flipped cells

SOLUTION:
    Keep:
        - total = number of available cells
        - mapping = hash map for lazy swap simulation

    On flip():
        1. Randomly choose r in [0, total-1]
        2. real_index = mapping.get(r, r)
        3. Move the last available index into position r
        4. Decrease total
        5. Convert real_index to [row, col]

    On reset():
        Restore total = m*n and clear mapping
"""


# STEP 1: Flatten matrix conceptually into indices [0 .. m*n-1]
# STEP 2: Keep total = number of remaining zero cells
# STEP 3: In flip(), choose random r in [0, total-1]
# STEP 4: Use mapping to get the real index at r
# STEP 5: Simulate swap with last available index
# STEP 6: Decrease total and convert index back to [row, col]
# STEP 7: In reset(), clear mapping and restore total


import random

class Solution:

    def __init__(self, m: int, n: int):

        self.m = m                                                    # Number of rows
        self.n = n                                                    # Number of columns
        self.total = m * n                                            # Count of still-available cells
        self.mapping = {}                                             # Lazy swap map: virtual index -> real index

    def flip(self) -> List[int]:

        r = random.randint(0, self.total - 1)                         # Random available slot (uniform)

        real_index = self.mapping.get(r, r)                           # Actual cell index represented by r

        last_index = self.mapping.get(self.total - 1, self.total - 1) # Actual value at last available slot
        self.mapping[r] = last_index                                  # Move last available value into slot r

        self.total -= 1                                               # One fewer cell remains available

        return [real_index // self.n, real_index % self.n]            # Convert 1D index -> [row, col]

    def reset(self) -> None:

        self.total = self.m * self.n                                  # Restore all cells as available
        self.mapping.clear()                                          # Forget all lazy swaps


"""
WHY EACH PART:
    self.total:              Tracks how many zero cells are still available
    self.mapping:            Simulates swaps without storing the full m*n array
    randint(0, total-1):     Uniformly chooses one of the remaining available slots
    mapping.get(r, r):       If r was never remapped, it still represents itself
    mapping.get(total-1,...): Finds the real value of the last available slot
    mapping[r] = last_index:  Simulates swapping chosen slot with last slot
    total -= 1:              Shrinks the available range by one
    index // n, index % n:   Converts flattened index back to matrix coordinates
    reset():                 Restores the whole structure in O(1)


HOW IT WORKS (Example: m = 2, n = 3):

    Conceptual flat array:
        index: 0 1 2 3 4 5
        cell :(0,0)(0,1)(0,2)(1,0)(1,1)(1,2)

    Initial state:
        total = 6
        mapping = {}

    flip() with r = 2:
    ├── real_index = mapping.get(2, 2) = 2
    ├── last_index = mapping.get(5, 5) = 5
    ├── mapping[2] = 5
    ├── total = 5
    └── return [2 // 3, 2 % 3] = [0, 2] 

    New implicit available values:
        slot 0 -> 0
        slot 1 -> 1
        slot 2 -> 5
        slot 3 -> 3
        slot 4 -> 4

    flip() with r = 2 again:
    ├── real_index = mapping.get(2, 2) = 5
    ├── last_index = mapping.get(4, 4) = 4
    ├── mapping[2] = 4
    ├── total = 4
    └── return [5 // 3, 5 % 3] = [1, 2] 

    Notice:
        Even though r=2 repeated, real_index changed from 2 to 5
        because slot 2 now represents a DIFFERENT available cell.


WHY THIS IS A PARTIAL FISHER-YATES SHUFFLE:
    Standard Fisher-Yates:
        Pick random slot
        Swap with last unused slot
        Shrink range
        Repeat

    We do EXACTLY that — but lazily with a hash map instead of a full array.

    Full array version:
        arr = [0,1,2,3,4,5]
        r = 2
        swap arr[2], arr[5]
        arr becomes [0,1,5,3,4,2]
        total = 5

    Lazy version:
        mapping[2] = 5
        total = 5

    Same EFFECT, less memory 


WHY THE HASH MAP SAVES MEMORY:
    Full array approach:
        Need to store m*n entries
        If m*n = 10^8, that's impossible / huge memory 

    Hash map approach:
        Only store changed positions
        After k flips, at most O(k) entries
        Since total operations <= 1000, this is tiny 


WHY UNIFORMITY IS GUARANTEED:
    At any moment, the available cells are represented by slots:
        [0, 1, 2, ..., total-1]

    We choose one uniformly:
        r = random.randint(0, total-1)

    Each slot corresponds to exactly ONE remaining cell
    via mapping.get(slot, slot)

    So each remaining zero cell has probability:
        1 / total

    Perfect uniform sampling without replacement ✓


WHY reset() IS O(1):
    We do NOT rebuild the matrix.
    We do NOT set each cell back to zero one by one.

    We simply say:
        total = m*n
        mapping = {}

    This "forgets" all previous flips instantly.


HANDLING SPECIAL CASES:
    1x1 matrix:
        total starts at 1
        flip() always returns [0,0]
        reset() restores it ✓

    Single row or single column:
        Flat index conversion still works ✓

    Large matrix (10^4 x 10^4):
        We never store full matrix, only mapping ✓

    Multiple resets:
        Each reset cleanly restarts the process ✓


KEY TECHNIQUE:
    Matrix flattening:         Convert 2D problem into 1D indices
    Sampling without replacement: Choose among remaining cells only
    Partial Fisher-Yates:      Swap chosen slot with last available slot
    Lazy swap simulation:      Use hash map instead of full array
    Index mapping:             Convert flat index back to [row, col]


EDGE CASES:
    m=1, n=1:                  flip() → [0,0] ✓
    Single row matrix:         Works with row=0, varying col ✓
    Single column matrix:      Works with col=0, varying row ✓
    Full reset after many flips: Restores all cells ✓
    Large dimensions, few flips: Efficient due to hash map ✓


TIME COMPLEXITY:
    __init__ : O(1)
    flip()   : O(1) average
    reset()  : O(1)

SPACE COMPLEXITY: O(k)
    k = number of flips since last reset
    We only store remapped slots, not the full matrix


CONCEPTS USED:
    Fisher-Yates shuffle
    Hash map / dictionary
    Lazy evaluation / implicit array simulation
    Uniform random sampling without replacement
    2D to 1D index mapping
"""
