"""
365. Water and Jug Problem
Difficulty: Medium
https://leetcode.com/problems/water-and-jug-problem/

PROBLEM:
You are given two jugs with capacities x liters and y liters.
There is an infinite amount of water supply available.
Determine whether it is possible to measure exactly target liters.

Operations allowed:
- Fill any jug completely
- Empty any jug completely  
- Pour from one jug to another until receiving jug is full
  or transferring jug is empty

EXAMPLES:
Input: x = 3, y = 5, target = 4 → Output: true
    Fill 5L jug, pour to 3L, empty 3L, pour remaining 2L to 3L,
    fill 5L again, pour 1L to fill 3L jug → 4L left in 5L jug

Input: x = 2, y = 6, target = 5 → Output: false
    GCD(2,6) = 2, and 5 is not divisible by 2

Input: x = 1, y = 2, target = 3 → Output: true
    Fill both jugs: 1 + 2 = 3

CONSTRAINTS:
• 1 <= x, y, target <= 10³

KEY INSIGHT - BÉZOUT'S THEOREM:
The equation ax + by = target has integer solutions
if and only if target is divisible by GCD(x, y).

In other words: target % GCD(x, y) == 0

ADDITIONAL CONSTRAINT:
target <= x + y (we can't store more than total capacity)

SOLUTION:
Check two conditions:
1. target <= x + y (capacity constraint)
2. target % GCD(x, y) == 0 (Bézout's theorem)
"""




# ============================================================================
# SOLUTION 1: MATHEMATICAL (Bézout's Theorem) - O(log(min(x,y)))
# ============================================================================

from math import gcd

class Solution:
    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        
        # Edge case: target is 0 (already achieved)
        if target == 0:
            return True
        
        # Capacity constraint: can't measure more than total capacity
        if x + y < target:
            return False
        
        # Bézout's theorem: target must be divisible by GCD(x, y)
        return target % gcd(x, y) == 0


# ============================================================================
# SOLUTION 2: BFS (State Space Search) - For understanding the process
# ============================================================================

from collections import deque


class Solution:
    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        
        if target == 0:
            return True
        
        if x + y < target:
            return False
        
        # BFS through all possible states
        visited = set()
        queue = deque([(0, 0)])                                  # Start with both empty
        visited.add((0, 0))
        
        while queue:
            a, b = queue.popleft()                               # Current state
            
            # Check if we've reached target
            if a == target or b == target or a + b == target:
                return True
            
            # Generate all possible next states
            next_states = [
                (x, b),                                          # Fill jug x
                (a, y),                                          # Fill jug y
                (0, b),                                          # Empty jug x
                (a, 0),                                          # Empty jug y
                # Pour x to y
                (max(0, a - (y - b)), min(y, a + b)),
                # Pour y to x
                (min(x, a + b), max(0, b - (x - a)))
            ]
            
            for state in next_states:
                if state not in visited:
                    visited.add(state)
                    queue.append(state)
        
        return False


# ============================================================================
# SOLUTION 3: DFS WITH MEMOIZATION
# ============================================================================

class Solution:
    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        
        if target == 0:
            return True
        
        if x + y < target:
            return False
        
        visited = set()
        
        def dfs(a: int, b: int) -> bool:
            # Check target
            if a == target or b == target or a + b == target:
                return True
            
            # Memoization
            if (a, b) in visited:
                return False
            visited.add((a, b))
            
            # Try all operations
            return (dfs(x, b) or                                 # Fill x
                    dfs(a, y) or                                 # Fill y
                    dfs(0, b) or                                 # Empty x
                    dfs(a, 0) or                                 # Empty y
                    dfs(max(0, a-(y-b)), min(y, a+b)) or         # Pour x→y
                    dfs(min(x, a+b), max(0, b-(x-a))))           # Pour y→x
        
        return dfs(0, 0)


# ============================================================================
# SOLUTION 4: MANUAL GCD (Without math library)
# ============================================================================

class Solution:
    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        
        def compute_gcd(a: int, b: int) -> int:
            """Euclidean algorithm for GCD"""
            while b:
                a, b = b, a % b
            return a
        
        if target == 0:
            return True
        
        if x + y < target:
            return False
        
        return target % compute_gcd(x, y) == 0


"""
WHY BÉZOUT'S THEOREM WORKS:

┌────────────────────────────────────────────────────────────────┐
│  Every operation changes total water by a multiple of x or y  │
│                                                                │
│  Fill x:   +x                                                  │
│  Fill y:   +y                                                  │
│  Empty x:  (effectively -x from what we had)                   │
│  Empty y:  (effectively -y from what we had)                   │
│  Pour:     no change in total                                  │
│                                                                │
│  After all operations: total = ax + by for some integers a,b  │
│                                                                │
│  Bézout's Identity states:                                     │
│  ax + by = c has integer solutions ⟺ GCD(x,y) divides c       │
└────────────────────────────────────────────────────────────────┘

PROOF OF BÉZOUT FOR x=3, y=5:
┌────────────────────────────────────────────────────────────────┐
│  GCD(3, 5) = 1                                                 │
│                                                                │
│  We can express 1 as: 1 = 2(3) + (-1)(5) = 6 - 5 = 1          │
│                                                                │
│  Since GCD = 1, any integer target is a multiple of 1         │
│  So any target (within capacity) is achievable!               │
│                                                                │
│  Examples:                                                     │
│  target = 1: 2(3) - 1(5) = 1                                  │
│  target = 2: -1(3) + 1(5) = 2                                 │
│  target = 4: 3(3) - 1(5) = 4                                  │
│  target = 7: -1(3) + 2(5) = 7                                 │
└────────────────────────────────────────────────────────────────┘

PROOF FOR x=4, y=6:
┌────────────────────────────────────────────────────────────────┐
│  GCD(4, 6) = 2                                                 │
│                                                                │
│  We can only measure multiples of 2!                          │
│                                                                │
│  2 = -1(4) + 1(6) = 2  ✓                                      │
│  4 = 1(4) + 0(6) = 4   ✓                                      │
│  5 = ??? (impossible, 5 not divisible by 2)                   │
│  6 = 0(4) + 1(6) = 6   ✓                                      │
│  8 = 2(4) + 0(6) = 8   ✓                                      │
└────────────────────────────────────────────────────────────────┘

HOW IT WORKS (Trace):

Example 1: x=3, y=5, target=4
├── target == 0? No
├── x + y >= target? 3+5=8 >= 4 ✓
├── GCD(3, 5) = 1
├── 4 % 1 = 0 ✓
└── Return True ✓

Example 2: x=2, y=6, target=5
├── target == 0? No
├── x + y >= target? 2+6=8 >= 5 ✓
├── GCD(2, 6) = 2
├── 5 % 2 = 1 ≠ 0 ✗
└── Return False ✓

Example 3: x=3, y=5, target=10
├── target == 0? No
├── x + y >= target? 3+5=8 >= 10? NO ✗
└── Return False (can't store 10L in 8L total capacity) ✓

BFS STATE EXPLORATION (x=3, y=5, target=4):
┌────────────────────────────────────────────────────────────────┐
│  (0,0) → (3,0), (0,5), ...                                    │
│  (0,5) → (3,5), (0,0), (3,2), ...                             │
│  (3,2) → (0,2), (3,5), (3,0), (0,5), ...                      │
│  (0,2) → (2,0), (0,5), ...                                    │
│  (2,0) → (2,5), (0,0), ...                                    │
│  (2,5) → (3,4) ← FOUND! a+b contains 4? No, but b=4? YES!    │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  target = 0       → True (trivially achieved, do nothing)     │
│  x = 0 or y = 0   → target must equal the non-zero jug       │
│  x = y = target   → True (fill one jug)                       │
│  target > x + y   → False (capacity exceeded)                 │
│  x = y            → GCD(x,x) = x, target must be multiple    │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  Solution 1 (Math):   O(log(min(x, y))) for GCD               │
│  Solution 2 (BFS):    O(x × y) states to explore              │
│  Solution 3 (DFS):    O(x × y) with memoization               │
└────────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  Solution 1 (Math):   O(1)                                     │
│  Solution 2 (BFS):    O(x × y) for visited set                │
│  Solution 3 (DFS):    O(x × y) for visited + recursion stack  │
└────────────────────────────────────────────────────────────────┘

CONCEPTS USED:
• Number Theory (GCD, Bézout's Theorem)
• Euclidean Algorithm
• Graph/State Space Search (BFS/DFS)
• Mathematical Proof
"""
