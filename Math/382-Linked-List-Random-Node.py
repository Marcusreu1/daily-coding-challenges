"""
382. Linked List Random Node
Difficulty: Medium
https://leetcode.com/problems/linked-list-random-node/

PROBLEM:
Given a singly linked list, return a random node's value from the linked list.
Each node must have the same probability of being chosen.

Implement the Solution class:
- Solution(ListNode head) Initializes with the head of the list
- int getRandom() Returns a random node's value with equal probability

EXAMPLES:
Input: ["Solution", "getRandom", "getRandom", "getRandom"]
       [[[1, 2, 3]], [], [], []]
Output: [null, 1, 3, 2]
Explanation: Each call to getRandom should return 1, 2, or 3 randomly
             with probability 1/3 each.

CONSTRAINTS:
• Number of nodes in list is in range [1, 10⁴]
• -10⁴ <= Node.val <= 10⁴
• At most 10⁴ calls to getRandom

FOLLOW UP:
What if the linked list is extremely large and its length is unknown?
What if you cannot use extra space (constant space)?

APPROACHES:
1. Precompute size: Count nodes first, then pick random index
2. Reservoir Sampling: Select random element in one pass without knowing size

KEY INSIGHT - RESERVOIR SAMPLING:
To select 1 random element from stream of unknown size:
- For i-th element (1-indexed), select it with probability 1/i
- This guarantees each element has final probability 1/n

PROOF (for n=3, elements A, B, C):
P(A final) = P(select A) × P(not replace with B) × P(not replace with C)
           = 1 × (1-1/2) × (1-1/3) = 1 × 1/2 × 2/3 = 1/3 ✓
P(B final) = P(select B) × P(not replace with C)
           = 1/2 × (1-1/3) = 1/2 × 2/3 = 1/3 ✓
P(C final) = P(select C) = 1/3 ✓
"""

import random
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# SOLUTION 1: PRECOMPUTE SIZE (Simple approach)
# ============================================================================

class Solution:
    """
    Store all values in array, then pick random index.
    Time: O(n) init, O(1) getRandom
    Space: O(n)
    """

    def __init__(self, head: Optional[ListNode]) -> None:
        self.values = []
        
        current = head
        while current:
            self.values.append(current.val)
            current = current.next

    def getRandom(self) -> int:
        return random.choice(self.values)


# ============================================================================
# SOLUTION 2: COUNT AND TRAVERSE (No extra space for values)
# ============================================================================

class Solution:
    """
    Count nodes in init, traverse to random index in getRandom.
    Time: O(n) init, O(n) getRandom
    Space: O(1)
    """

    def __init__(self, head: Optional[ListNode]) -> None:
        self.head = head
        self.length = 0
        
        # Count nodes
        current = head
        while current:
            self.length += 1
            current = current.next

    def getRandom(self) -> int:
        # Pick random index
        idx = random.randint(0, self.length - 1)
        
        # Traverse to that index
        current = self.head
        for _ in range(idx):
            current = current.next
        
        return current.val


# ============================================================================
# SOLUTION 3: RESERVOIR SAMPLING (Best for unknown/infinite size)
# ============================================================================

class Solution:
    """
    Use Reservoir Sampling - no need to know size beforehand.
    Time: O(1) init, O(n) getRandom
    Space: O(1)
    
    Perfect for:
    - Unknown list size
    - Streaming data
    - Memory constraints
    """

    def __init__(self, head: Optional[ListNode]) -> None:
        self.head = head

    def getRandom(self) -> int:
        result = 0
        current = self.head
        i = 1                                                    # 1-indexed counter
        
        while current:
            # Select current node with probability 1/i
            if random.randint(1, i) == 1:
                result = current.val
            
            current = current.next
            i += 1
        
        return result


# ============================================================================
# SOLUTION 4: RESERVOIR SAMPLING (Alternative implementation)
# ============================================================================

class Solution:
    """
    Same as Solution 3, using random.random() instead.
    """

    def __init__(self, head: Optional[ListNode]) -> None:
        self.head = head

    def getRandom(self) -> int:
        result = self.head.val
        current = self.head.next
        count = 2                                                # Start from 2nd node
        
        while current:
            # Select with probability 1/count
            if random.random() < 1.0 / count:
                result = current.val
            
            current = current.next
            count += 1
        
        return result


"""
HOW RESERVOIR SAMPLING WORKS:

═══════════════════════════════════════════════════════════════════
List: 10 → 20 → 30 → 40
═══════════════════════════════════════════════════════════════════

Node 1 (val=10, i=1):
    random(1, 1) = 1
    1 == 1? YES → result = 10
    
    P(select 10) = 1/1 = 100%

Node 2 (val=20, i=2):
    random(1, 2) = 1 or 2
    
    If random = 1 (50%): result = 20
    If random = 2 (50%): result stays 10
    
    P(select 20) = 1/2 = 50%

Node 3 (val=30, i=3):
    random(1, 3) = 1, 2, or 3
    
    If random = 1 (33%): result = 30
    Otherwise (67%): result unchanged
    
    P(select 30) = 1/3 ≈ 33%

Node 4 (val=40, i=4):
    random(1, 4) = 1, 2, 3, or 4
    
    If random = 1 (25%): result = 40
    Otherwise (75%): result unchanged
    
    P(select 40) = 1/4 = 25%

═══════════════════════════════════════════════════════════════════
Final probability for each node = 1/4 = 25% ✓
═══════════════════════════════════════════════════════════════════

MATHEMATICAL PROOF:

For n elements, probability of element k being selected:

P(k selected) = P(select k at step k) × P(not replaced at k+1) × ... × P(not replaced at n)
              = (1/k) × (1 - 1/(k+1)) × (1 - 1/(k+2)) × ... × (1 - 1/n)
              = (1/k) × (k/(k+1)) × ((k+1)/(k+2)) × ... × ((n-1)/n)
              = (1/k) × (k/n)     [telescoping product]
              = 1/n ✓

Example for k=2, n=4:
P(element 2) = (1/2) × (2/3) × (3/4) = 6/24 = 1/4 ✓

WHY THIS IS USEFUL:
┌────────────────────────────────────────────────────────────────┐
│  1. Unknown size: Don't need to know n beforehand              │
│  2. Streaming data: Can process infinite streams               │
│  3. Memory efficient: Only O(1) extra space needed            │
│  4. Single pass: Only traverse list once per getRandom()      │
└────────────────────────────────────────────────────────────────┘

COMPARISON OF APPROACHES:
┌────────────────┬─────────────┬──────────────┬─────────────────┐
│ Approach       │ Init Time   │ getRandom    │ Space           │
├────────────────┼─────────────┼──────────────┼─────────────────┤
│ Store in array │ O(n)        │ O(1)         │ O(n)            │
│ Count+traverse │ O(n)        │ O(n)         │ O(1)            │
│ Reservoir      │ O(1)        │ O(n)         │ O(1)            │
└────────────────┴─────────────┴──────────────┴─────────────────┘

When to use each:
• Store in array: Many getRandom calls, memory available
• Count+traverse: Few getRandom calls, less memory
• Reservoir: Unknown size, streaming, or memory constrained

GENERALIZED RESERVOIR SAMPLING (K elements):
┌────────────────────────────────────────────────────────────────┐
│  To select K random elements from stream:                      │
│                                                                │
│  1. Fill reservoir with first K elements                       │
│  2. For i-th element (i > K):                                 │
│     - Generate random j in [1, i]                              │
│     - If j <= K, replace reservoir[j] with element i          │
│                                                                │
│  Each element has probability K/n of being in final result    │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  Single node      → Always returns that node's value          │
│  All same values  → Returns that value (still uniform)        │
│  Very long list   → Reservoir Sampling handles efficiently    │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  Solution 1 (Array):    O(n) init, O(1) getRandom             │
│  Solution 2 (Count):    O(n) init, O(n) getRandom             │
│  Solution 3 (Reservoir): O(1) init, O(n) getRandom            │
└────────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  Solution 1 (Array):    O(n) - stores all values              │
│  Solution 2 (Count):    O(1) - only stores head and length    │
│  Solution 3 (Reservoir): O(1) - only stores head              │
└────────────────────────────────────────────────────────────────┘

CONCEPTS USED:
• Reservoir Sampling
• Probability Theory
• Linked List Traversal
• Random Number Generation
"""
