"""
335. Self Crossing
Difficulty: Hard
https://leetcode.com/problems/self-crossing/

PROBLEM:
You are given an array of integers distance.

You start at point (0, 0) on a 2D plane and move distance[0] meters north,
then distance[1] meters west, distance[2] meters south, distance[3] meters
east, and so on. In other words, after each move, your direction changes
counter-clockwise.

Return true if your path crosses itself, false otherwise.

EXAMPLES:
Input: distance = [2,1,1,2] → Output: true
    ┌───┐
    │   │
    │   └───X (crosses first segment)
    │
    └

Input: distance = [1,2,3,4] → Output: false
    (expanding spiral, never crosses)

Input: distance = [1,1,1,1] → Output: true
    (square, last segment touches start)

CONSTRAINTS:
• 1 <= distance.length <= 10⁵
• 1 <= distance[i] <= 10⁵

MOVEMENT PATTERN:
i % 4 == 0  →  North (↑)  +Y
i % 4 == 1  →  West  (←)  -X
i % 4 == 2  →  South (↓)  -Y
i % 4 == 3  →  East  (→)  +X

KEY INSIGHT:
There are only 3 ways a path can cross itself:
1. Current segment crosses segment from 3 steps ago
2. Current segment crosses segment from 4 steps ago
3. Current segment crosses segment from 5 steps ago

Any older crossing would require crossing one of these first!

CASE 1: Cross with i-3 (most common)
              i-2
         ┌──────────┐
         │          │
   i-3   │          │ i-1
         │          │
         └──────────┼───→ i crosses i-3
                    
Conditions:
    d[i] >= d[i-2]  AND  d[i-1] <= d[i-3]

CASE 2: Cross with i-4 (exact overlap)
                i-3
         ┌────────────────┐
         │                │
   i-4   │      i-1       │ i-2
         │   ┌────────────┤
         │   │      i     │
         └───┴────────────┘
         
Conditions:
    d[i-1] == d[i-3]  AND  d[i] + d[i-4] >= d[i-2]

CASE 3: Cross with i-5 (shrinking spiral)
                   i-4
         ┌──────────────────┐
         │                  │
   i-5   │       i-2        │ i-3
         │   ┌──────────┐   │
         │   │    i     │   │
         │   └──────────┘   │
         │        i-1       │
         └──────────────────┘
         
Conditions:
    d[i-2] > d[i-4]  AND
    d[i-1] <= d[i-3]  AND
    d[i-1] + d[i-5] >= d[i-3]  AND
    d[i] + d[i-4] >= d[i-2]
"""

from typing import List


class Solution:
    def isSelfCrossing(self, distance: List[int]) -> bool:
        
        d = distance                                             # Alias for shorter code
        n = len(d)
        
        for i in range(3, n):
            
            # CASE 1: Current line crosses line from 3 steps ago
            # ──────────────────────────────────────────────────
            if d[i] >= d[i-2] and d[i-1] <= d[i-3]:
                return True
            
            # CASE 2: Current line crosses line from 4 steps ago
            # ──────────────────────────────────────────────────
            if i >= 4:
                if d[i-1] == d[i-3] and d[i] + d[i-4] >= d[i-2]:
                    return True
            
            # CASE 3: Current line crosses line from 5 steps ago
            # ──────────────────────────────────────────────────
            if i >= 5:
                if (d[i-2] > d[i-4] and
                    d[i-1] <= d[i-3] and
                    d[i-1] + d[i-5] >= d[i-3] and
                    d[i] + d[i-4] >= d[i-2]):
                    return True
        
        return False                                             # No crossing found

"""
HOW IT WORKS (Trace):

Example 1: distance = [2, 1, 1, 2]
──────────────────────────────────

i=3:
├── CASE 1: d[3]=2 >= d[1]=1? YES ✓
│           d[2]=1 <= d[0]=2? YES ✓
└── CROSSING DETECTED! Return True ✓


Example 2: distance = [1, 2, 3, 4]
──────────────────────────────────

i=3:
├── CASE 1: d[3]=4 >= d[1]=2? YES
│           d[2]=3 <= d[0]=1? NO ✗
└── No crossing

Return False (expanding spiral) ✓


Example 3: distance = [1, 1, 1, 2, 1]
─────────────────────────────────────

i=3:
├── CASE 1: d[3]=2 >= d[1]=1? YES
│           d[2]=1 <= d[0]=1? YES ✓
└── CROSSING! Return True ✓


Example 4: distance = [1, 1, 2, 2, 1, 1]
────────────────────────────────────────

i=3:
├── CASE 1: d[3]=2 >= d[1]=1? YES
│           d[2]=2 <= d[0]=1? NO ✗
└── No crossing

i=4:
├── CASE 1: d[4]=1 >= d[2]=2? NO ✗
├── CASE 2: d[3]=2 == d[1]=1? NO ✗
└── No crossing

i=5:
├── CASE 1: d[5]=1 >= d[3]=2? NO ✗
├── CASE 2: d[4]=1 == d[2]=2? NO ✗
├── CASE 3:
│   ├── d[3]=2 > d[1]=1? YES ✓
│   ├── d[4]=1 <= d[2]=2? YES ✓
│   ├── d[4]+d[0]=2 >= d[2]=2? YES ✓
│   ├── d[5]+d[1]=2 >= d[3]=2? YES ✓
│   └── ALL CONDITIONS MET!
└── CROSSING! Return True ✓


WHY ONLY 3 CASES?

Think of the spiral:
┌─────────────────────────────────────────────────────────────┐
│  The path moves counterclockwise in a spiral pattern.      │
│                                                             │
│  • Case 1: Spiral stays same size or shrinks → crosses 3   │
│            steps back on the "inside turn"                  │
│                                                             │
│  • Case 2: Edge case where parallel lines meet exactly      │
│                                                             │
│  • Case 3: Spiral shrinks enough to cross 5 steps back      │
│                                                             │
│  If spiral expands (d[i] > d[i-2]), no crossing possible!   │
│                                                             │
│  Any crossing with older segments (i-6, i-7, etc.) would    │
│  require first crossing one of these three cases.           │
└─────────────────────────────────────────────────────────────┘

VISUAL: THE THREE CROSSING PATTERNS

CASE 1:                 CASE 2:                 CASE 3:
    ┌───┐                   ┌─────────┐            ┌───────────┐
    │   │                   │         │            │           │
    │   └──X→               │  ┌──────┤            │   ┌───┐   │
    │                       │  │      │            │   │ X │   │
    └────                   └──┴──────┘            │   └───┘   │
                                                   └───────────┘
 Crosses i-3           Touches i-4              Crosses i-5

EDGE CASES:
┌────────────────────────────────────────────────────────────┐
│  n < 4              → Always False (can't cross)           │
│  All same length    → Depends on values                    │
│  Expanding spiral   → Always False                         │
│  distance = [1,1,1,1] → True (forms square, touches)       │
└────────────────────────────────────────────────────────────┘

TIME COMPLEXITY: O(n)
├── Single pass through the array
└── Constant time checks at each position

SPACE COMPLEXITY: O(1)
├── Only using a few variables
└── No extra data structures

COMMON MISTAKES:
Forgetting Case 2 or Case 3
Wrong inequality signs (>= vs >, <= vs <)
Off-by-one errors with indices
Not handling edge cases (n < 4, n < 5)

CONCEPTS USED:
• Geometry (line crossing detection)
• Pattern Recognition
• Case Analysis
• Spiral Path Analysis
"""
