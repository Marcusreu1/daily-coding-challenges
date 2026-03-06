"""
384. Shuffle an Array
Difficulty: Medium
https://leetcode.com/problems/shuffle-an-array/

PROBLEM:
Given an integer array nums, design an algorithm to randomly shuffle the array.
All permutations of the array should be equally likely as a result of the shuffling.

Implement the Solution class:
- Solution(int[] nums) Initializes the object with the array nums
- int[] reset() Resets the array to its original configuration and returns it
- int[] shuffle() Returns a random shuffling of the array

EXAMPLES:
Input: ["Solution", "shuffle", "reset", "shuffle"]
       [[[1, 2, 3]], [], [], []]
Output: [null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]

CONSTRAINTS:
• 1 <= nums.length <= 50
• -10⁶ <= nums[i] <= 10⁶
• All elements of nums are unique
• At most 10⁴ calls to reset and shuffle

KEY INSIGHT - FISHER-YATES SHUFFLE:
The standard algorithm for generating uniform random permutations.
- Time: O(n)
- Space: O(1) extra (excluding the copy)

Algorithm (right to left version):
    for i from n-1 down to 1:
        j = random integer in [0, i]
        swap(arr[i], arr[j])

WHY IT'S UNIFORM:
- n choices for last position
- n-1 choices for second-to-last
- ...
- 2 choices for second position
- Total: n! equally likely outcomes
"""

import random
from typing import List


# ============================================================================
# SOLUTION 1: FISHER-YATES SHUFFLE (Standard approach)
# ============================================================================

class Solution:

    def __init__(self, nums: List[int]):
        self.original = nums.copy()                              # Keep copy of original
        self.array = nums                                        # Working array

    def reset(self) -> List[int]:
        """Reset to original configuration."""
        self.array = self.original.copy()                        # Restore from copy
        return self.array

    def shuffle(self) -> List[int]:
        """
        Fisher-Yates Shuffle: O(n) uniform random permutation.
        """
        arr = self.array
        n = len(arr)
        
        # Iterate from last to second element
        for i in range(n - 1, 0, -1):
            # Pick random index from 0 to i (inclusive)
            j = random.randint(0, i)
            
            # Swap elements
            arr[i], arr[j] = arr[j], arr[i]
        
        return arr


# ============================================================================
# SOLUTION 2: FISHER-YATES (Left to right version)
# ============================================================================

class Solution:

    def __init__(self, nums: List[int]):
        self.original = nums.copy()
        self.array = nums

    def reset(self) -> List[int]:
        self.array = self.original.copy()
        return self.array

    def shuffle(self) -> List[int]:
        """
        Fisher-Yates from left to right.
        Equivalent to right-to-left version.
        """
        arr = self.array
        n = len(arr)
        
        for i in range(n):
            # Pick random index from i to n-1 (inclusive)
            j = random.randint(i, n - 1)
            
            # Swap elements
            arr[i], arr[j] = arr[j], arr[i]
        
        return arr


# ============================================================================
# SOLUTION 3: USING random.shuffle (Python built-in)
# ============================================================================

class Solution:

    def __init__(self, nums: List[int]):
        self.original = nums.copy()
        self.array = nums

    def reset(self) -> List[int]:
        self.array = self.original.copy()
        return self.array

    def shuffle(self) -> List[int]:
        """Uses Python's built-in shuffle (implements Fisher-Yates internally)."""
        random.shuffle(self.array)
        return self.array


# ============================================================================
# SOLUTION 4: CREATING NEW SHUFFLED COPY EACH TIME
# ============================================================================

class Solution:

    def __init__(self, nums: List[int]):
        self.nums = nums                                         # Store original reference

    def reset(self) -> List[int]:
        return self.nums                                         # Return original

    def shuffle(self) -> List[int]:
        """Create shuffled copy, don't modify original."""
        shuffled = self.nums.copy()
        
        n = len(shuffled)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        
        return shuffled


"""
HOW FISHER-YATES WORKS (Visual Trace):

═══════════════════════════════════════════════════════════════════
Array: [1, 2, 3, 4, 5]
       [0] [1] [2] [3] [4]
═══════════════════════════════════════════════════════════════════

i = 4: j = random(0, 4) → say j = 2
       swap(arr[4], arr[2]) → swap(5, 3)
       [1, 2, 5, 4, 3]
              ↑     ↑
           swapped  position 4 now "fixed"

i = 3: j = random(0, 3) → say j = 0
       swap(arr[3], arr[0]) → swap(4, 1)
       [4, 2, 5, 1, 3]
        ↑     ↑
       swapped  position 3 now "fixed"

i = 2: j = random(0, 2) → say j = 2
       swap(arr[2], arr[2]) → no change
       [4, 2, 5, 1, 3]
              ↑ position 2 now "fixed"

i = 1: j = random(0, 1) → say j = 0
       swap(arr[1], arr[0]) → swap(2, 4)
       [2, 4, 5, 1, 3]
        ↑  ↑
       swapped  position 1 now "fixed"

Final: [2, 4, 5, 1, 3]

═══════════════════════════════════════════════════════════════════

WHY UNIFORM DISTRIBUTION - PROOF:

For array of n elements:
┌────────────────────────────────────────────────────────────────┐
│  Step 1: n choices for element at position n-1                 │
│  Step 2: n-1 choices for element at position n-2              │
│  Step 3: n-2 choices for element at position n-3              │
│  ...                                                           │
│  Step n-1: 2 choices for element at position 1                │
│                                                                │
│  Total number of outcomes: n × (n-1) × (n-2) × ... × 2 = n!   │
│                                                                │
│  Each permutation is reached by EXACTLY ONE sequence of swaps │
│  Probability of each: 1/n! ✓                                  │
└────────────────────────────────────────────────────────────────┘

MATHEMATICAL PROOF (probability for specific element at specific position):

P(element e ends up at position k) = ?

Case 1: k = n-1 (last position)
    P = 1/n (chosen in first iteration)

Case 2: k < n-1
    P = P(not chosen before k) × P(chosen at step k) × P(not moved after)
    
    For k = n-2:
    P = (n-1)/n × 1/(n-1) = 1/n

    For any k:
    P = (n-1)/n × (n-2)/(n-1) × ... × 1/(n-k) = 1/n ✓

Each element has equal probability (1/n) of ending at any position!

WRONG IMPLEMENTATION - WHY IT FAILS:
┌────────────────────────────────────────────────────────────────┐
│  WRONG: random(0, n-1) for ALL positions                      │
│                                                                │
│  for i in range(n):                                           │
│      j = random.randint(0, n - 1)  # WRONG!                  │
│      arr[i], arr[j] = arr[j], arr[i]                          │
│                                                                │
│  This generates n^n sequences (not n!)                        │
│                                                                │
│  For n = 3:                                                    │
│  - n^n = 27 sequences                                         │
│  - n! = 6 permutations                                        │
│  - 27 / 6 = 4.5 (not integer!)                               │
│  - Some permutations are more likely than others!             │
│                                                                │
│  Example distribution for [1,2,3]:                             │
│  [1,2,3]: 4/27 ≈ 14.8%                                        │
│  [1,3,2]: 5/27 ≈ 18.5%  ← MORE likely!                       │
│  [2,1,3]: 5/27 ≈ 18.5%                                        │
│  [2,3,1]: 5/27 ≈ 18.5%                                        │
│  [3,1,2]: 4/27 ≈ 14.8%  ← LESS likely!                       │
│  [3,2,1]: 4/27 ≈ 14.8%                                        │
│                                                                │
│  Not uniform!                                                  │
└────────────────────────────────────────────────────────────────┘

LEFT-TO-RIGHT VS RIGHT-TO-LEFT:
┌────────────────────────────────────────────────────────────────┐
│  RIGHT-TO-LEFT (our main solution):                            │
│  for i in range(n-1, 0, -1):                                  │
│      j = random.randint(0, i)                                 │
│                                                                │
│  LEFT-TO-RIGHT (equivalent):                                   │
│  for i in range(n):                                           │
│      j = random.randint(i, n-1)                               │
│                                                                │
│  Both produce uniform distribution!                            │
│  Both have O(n) time complexity.                              │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  Single element [5]    → Always returns [5]                   │
│  Two elements [1,2]    → Returns [1,2] or [2,1] (50% each)   │
│  reset() after shuffle → Returns original order               │
│  Multiple shuffles     → Each independent, uniform            │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  __init__: O(n) for copying array                             │
│  reset():  O(n) for copying array                             │
│  shuffle(): O(n) for Fisher-Yates                             │
└────────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY: O(n)
├── Storing original array copy: O(n)
├── Working array: O(n)
└── Total: O(n)

CONCEPTS USED:
• Fisher-Yates (Knuth) Shuffle
• Uniform Random Permutation
• Probability Theory
• In-place Algorithm
"""
