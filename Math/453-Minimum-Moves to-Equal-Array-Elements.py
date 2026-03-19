"""
453. Minimum Moves to Equal Array Elements
Difficulty: Medium
https://leetcode.com/problems/minimum-moves-to-equal-array-elements/

PROBLEM:
Given an integer array nums of size n, return the minimum number of
moves required to make all array elements equal. In one move, you
can increment n-1 elements of the array by 1.

EXAMPLES:
Input: nums = [1,2,3]  → Output: 3
    [1,2,3] → [2,3,3] → [3,4,3] → [4,4,4] (3 moves)

Input: nums = [1,1,1]  → Output: 0
    Already equal

Input: nums = [5,6,8,8,5]  → Output: 7

CONSTRAINTS:
    n == nums.length
    1 <= n <= 10^5
    -10^9 <= nums[i] <= 10^9

KEY INSIGHT:
Incrementing n-1 elements by 1 is EQUIVALENT to decrementing 1 element
by 1 (same relative change). So the problem becomes: how many single
decrements to make all elements equal? → Decrement everything to min.

    Answer = sum(nums) - n × min(nums)

CHALLENGES:
    Simulating moves directly is too slow
    Need to see the "increment n-1 = decrement 1" equivalence
    Proving that min(nums) is the optimal target

MATHEMATICAL PROOF:
    Incrementing n-1 elements by 1:
        All elements go up by 1, except one stays → relative: one goes DOWN by 1
    
    Decrementing 1 element by 1:
        One element goes down by 1, rest stay → relative: one goes DOWN by 1
    
    Same relative effect! So minimum moves = total decrements to reach min:
        Σ(nums[i] - min) = sum(nums) - n × min(nums)

SOLUTION:
    1. Compute sum and min of the array
    2. Apply formula: sum - n × min
"""

# STEP 1: Get sum and min of the array
# STEP 2: Apply the formula

class Solution:
    def minMoves(self, nums: List[int]) -> int:

        return sum(nums) - len(nums) * min(nums)                         # sum - n × min

"""
WHY EACH PART:

    sum(nums): Total sum of all elements
    len(nums): Number of elements (n)
    min(nums): The minimum value (optimal target)
    sum - n × min: Total decrements needed to bring all elements to min

HOW IT WORKS (Example: nums = [1, 2, 3]):

    sum(nums) = 1 + 2 + 3 = 6
    len(nums) = 3
    min(nums) = 1

    result = 6 - 3 × 1 = 6 - 3 = 3

    Interpretation (decrement view):
    ├── 1 → 1: 0 decrements
    ├── 2 → 1: 1 decrement
    ├── 3 → 1: 2 decrements
    └── Total: 0 + 1 + 2 = 3 ✓

    Interpretation (original increment view):
    ├── Move 1: increment [1,2,_] → [2,3,3]
    ├── Move 2: increment [2,_,3] → [3,3,4]
    ├── Move 3: increment [3,3,_] → [4,4,4]
    └── Total: 3 moves ✓

HOW IT WORKS (Example: nums = [5, 6, 8, 8, 5]):

    sum = 32, n = 5, min = 5
    result = 32 - 5 × 5 = 32 - 25 = 7

    Decrement view:
    ├── 5 → 5: 0
    ├── 6 → 5: 1
    ├── 8 → 5: 3
    ├── 8 → 5: 3
    ├── 5 → 5: 0
    └── Total: 0 + 1 + 3 + 3 + 0 = 7 ✓

WHY "INCREMENT n-1" = "DECREMENT 1":

    Original operation on [1, 2, 3]:
    ├── Increment all except last: [1+1, 2+1, 3] = [2, 3, 3]
    ├── Differences: 3-2=1, 3-3=0
    └── Relative to max: [-1, 0, 0]

    Equivalent decrement on [1, 2, 3]:
    ├── Decrement last only: [1, 2, 3-1] = [1, 2, 2]
    ├── Differences: 2-1=1, 2-2=0
    └── Relative to max: [-1, 0, 0]  ← SAME relative differences!

    Key: we only care about RELATIVE differences between elements,
    not their absolute values. Both operations change the same
    relative structure.

WHY MIN IS THE OPTIMAL TARGET:

    Target BELOW min: impossible with decrements only
    ├── Can't decrement below min without extra moves
    └── Would need to decrement min too → wasteful

    Target AT min: each element decrements by (nums[i] - min)
    ├── Minimum total decrements possible
    └── No wasted moves ✓

    Target ABOVE min: impossible with the original increment operation
    ├── We always leave one element unchanged
    └── The minimum can never "catch up" past itself

    Therefore min is the unique optimal target ✓

WHY sum - n × min EQUALS Σ(nums[i] - min):

    Σ(nums[i] - min) = (nums[0]-min) + (nums[1]-min) + ... + (nums[n-1]-min)
                      = (nums[0] + nums[1] + ... + nums[n-1]) - n × min
                      = sum(nums) - n × min(nums)

    Distributing the subtraction turns n subtractions into just one ✓

ALTERNATIVE VIEW (Working backwards):

    Final state: all elements = some value V
    After m moves: sum increased by m × (n-1) (each move adds n-1)
    Final sum: n × V = sum(nums) + m × (n-1)

    To minimize m, minimize V. Minimum V = min(nums) + m
    (min element gets incremented every move except when it's skipped)

    Actually... the math confirms the same formula:
    m = sum(nums) - n × min(nums) ✓

EDGE CASES:

    All equal [1,1,1]: sum - n×min = 3 - 3 = 0 ✓
    Single element [5]: sum - 1×min = 5 - 5 = 0 ✓
    Two elements [1,5]: 6 - 2×1 = 4 ✓
    Negative nums [-1,0,1]: 0 - 3×(-1) = 0 + 3 = 3 ✓
    Large values (10^9): Formula handles with basic arithmetic ✓
    Already sorted: No special handling needed ✓
    All same except one: sum - n×min = difference of outlier ✓

TIME COMPLEXITY: O(n)
    O(n) for sum(nums)
    O(n) for min(nums)
    O(1) for the arithmetic
    Total: O(n)

SPACE COMPLEXITY: O(1)
    Only arithmetic operations, no extra data structures

CONCEPTS USED:
    Mathematical equivalence (increment n-1 ≡ decrement 1)
    Relative vs absolute values
    Summation formula simplification
    Greedy target selection (minimum element)
    Problem transformation (reframe to simpler equivalent)
"""
