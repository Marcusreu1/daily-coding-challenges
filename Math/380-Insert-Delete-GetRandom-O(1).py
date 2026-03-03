"""
380. Insert Delete GetRandom O(1)
Difficulty: Medium
https://leetcode.com/problems/insert-delete-getrandom-o1/

PROBLEM:
Implement the RandomizedSet class:
- RandomizedSet() Initializes the object
- bool insert(int val) Inserts val if not present, returns true if inserted
- bool remove(int val) Removes val if present, returns true if removed  
- int getRandom() Returns a random element with equal probability

All operations must work in O(1) average time complexity.

EXAMPLES:
["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
[[], [1], [2], [2], [], [1], [2], []]
Output: [null, true, false, true, 2, true, false, 2]

CONSTRAINTS:
• -2³¹ <= val <= 2³¹ - 1
• At most 2 * 10⁵ calls
• There will be at least one element when getRandom is called

KEY INSIGHT:
No single data structure gives O(1) for all three operations:
- Array: getRandom O(1), but remove O(n)
- HashSet: insert/remove O(1), but getRandom O(n)

SOLUTION: Combine Array + HashMap!
- Array stores the values → getRandom picks random index O(1)
- HashMap maps value → index → find position for remove O(1)

REMOVE TRICK:
To remove in O(1), swap the element with the LAST element,
then pop from the end (which is O(1)).

DATA STRUCTURE:
┌─────────────────────────────────────────────────────────────┐
│  self.list = [val1, val2, val3, ...]                       │
│  self.map  = {val1: 0, val2: 1, val3: 2, ...}             │
│               ↑        ↑                                   │
│            value → index in list                           │
└─────────────────────────────────────────────────────────────┘
"""

import random


class RandomizedSet:

    def __init__(self):
        """Initialize with empty list and empty hashmap."""
        self.list = []                                           # Stores values
        self.map = {}                                            # Maps value → index

    def insert(self, val: int) -> bool:
        """
        Insert val if not present.
        Returns true if inserted, false if already exists.
        Time: O(1)
        """
        if val in self.map:                                      # Already exists
            return False
        
        self.map[val] = len(self.list)                          # Map val → new index
        self.list.append(val)                                    # Add to end of list
        
        return True

    def remove(self, val: int) -> bool:
        """
        Remove val if present.
        Returns true if removed, false if not found.
        Time: O(1)
        
        Trick: Swap with last element, then pop.
        """
        if val not in self.map:                                  # Doesn't exist
            return False
        
        # Get index of element to remove
        idx = self.map[val]
        last_val = self.list[-1]
        
        # Move last element to the position of element to remove
        self.list[idx] = last_val
        self.map[last_val] = idx
        
        # Remove last element (O(1))
        self.list.pop()
        del self.map[val]
        
        return True

    def getRandom(self) -> int:
        """
        Return a random element with equal probability.
        Time: O(1)
        """
        return random.choice(self.list)


# ============================================================================
# ALTERNATIVE IMPLEMENTATION (More explicit)
# ============================================================================

class RandomizedSet:

    def __init__(self):
        self.vals = []                                           # List of values
        self.val_to_idx = {}                                     # value → index mapping

    def insert(self, val: int) -> bool:
        # Check if already present
        if val in self.val_to_idx:
            return False
        
        # Insert at end
        self.val_to_idx[val] = len(self.vals)
        self.vals.append(val)
        
        return True

    def remove(self, val: int) -> bool:
        # Check if present
        if val not in self.val_to_idx:
            return False
        
        # Get positions
        idx_to_remove = self.val_to_idx[val]
        last_idx = len(self.vals) - 1
        last_val = self.vals[last_idx]
        
        # Swap with last (only if not already last)
        if idx_to_remove != last_idx:
            self.vals[idx_to_remove] = last_val
            self.val_to_idx[last_val] = idx_to_remove
        
        # Remove last
        self.vals.pop()
        del self.val_to_idx[val]
        
        return True

    def getRandom(self) -> int:
        rand_idx = random.randint(0, len(self.vals) - 1)
        return self.vals[rand_idx]


"""
HOW IT WORKS (Visual Trace):

═══════════════════════════════════════════════════════════════════
INITIAL STATE:
═══════════════════════════════════════════════════════════════════
    list: []
    map:  {}

═══════════════════════════════════════════════════════════════════
insert(1):
═══════════════════════════════════════════════════════════════════
    1 in map? NO
    map[1] = 0 (current length)
    list.append(1)
    
    list: [1]
    map:  {1: 0}
    return True

═══════════════════════════════════════════════════════════════════
insert(2):
═══════════════════════════════════════════════════════════════════
    2 in map? NO
    map[2] = 1
    list.append(2)
    
    list: [1, 2]
    map:  {1: 0, 2: 1}
    return True

═══════════════════════════════════════════════════════════════════
insert(3):
═══════════════════════════════════════════════════════════════════
    list: [1, 2, 3]
    map:  {1: 0, 2: 1, 3: 2}
    return True

═══════════════════════════════════════════════════════════════════
remove(2):
═══════════════════════════════════════════════════════════════════
    2 in map? YES, idx = 1
    last_val = list[-1] = 3
    
    Step 1: Move last to idx 1
        list[1] = 3
        list: [1, 3, 3]
        
    Step 2: Update map for last_val
        map[3] = 1
        
    Step 3: Pop last
        list.pop()
        list: [1, 3]
        
    Step 4: Delete val from map
        del map[2]
        map: {1: 0, 3: 1}
    
    return True

═══════════════════════════════════════════════════════════════════
getRandom():
═══════════════════════════════════════════════════════════════════
    list: [1, 3]
    random.choice([1, 3])
    return 1 or 3 (50% each)

═══════════════════════════════════════════════════════════════════
insert(2): (re-insert after removal)
═══════════════════════════════════════════════════════════════════
    2 in map? NO (was deleted)
    map[2] = 2
    list.append(2)
    
    list: [1, 3, 2]
    map:  {1: 0, 3: 1, 2: 2}
    return True

═══════════════════════════════════════════════════════════════════
remove(1): (remove first element)
═══════════════════════════════════════════════════════════════════
    1 in map? YES, idx = 0
    last_val = 2
    
    list[0] = 2
    list: [2, 3, 2]
    map[2] = 0
    
    list.pop()
    list: [2, 3]
    
    del map[1]
    map: {3: 1, 2: 0}
    
    return True

═══════════════════════════════════════════════════════════════════
remove(3): (remove last element - special case)
═══════════════════════════════════════════════════════════════════
    3 in map? YES, idx = 1
    last_val = 3 (same as val to remove!)
    
    list[1] = 3 (no change, it's the same)
    map[3] = 1 (no change)
    
    list.pop()
    list: [2]
    
    del map[3]
    map: {2: 0}
    
    return True

WHY THIS WORKS:
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  INSERT O(1):                                                  │
│  ├── HashMap lookup: O(1)                                     │
│  ├── HashMap insert: O(1)                                     │
│  └── List append: O(1) amortized                              │
│                                                                │
│  REMOVE O(1):                                                  │
│  ├── HashMap lookup (find index): O(1)                        │
│  ├── List access (get last): O(1)                             │
│  ├── List assignment (swap): O(1)                             │
│  ├── HashMap update: O(1)                                     │
│  ├── List pop (from end): O(1)                                │
│  └── HashMap delete: O(1)                                     │
│                                                                │
│  GETRANDOM O(1):                                               │
│  ├── Get list length: O(1)                                    │
│  ├── Generate random index: O(1)                              │
│  └── List access by index: O(1)                               │
│                                                                │
└────────────────────────────────────────────────────────────────┘

WHY SWAP WITH LAST?
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  If we remove from middle directly:                            │
│      [1, 2, 3, 4] → remove 2 → [1, _, 3, 4]                  │
│      Need to shift 3 and 4 left: O(n)                         │
│                                                                │
│  With swap-and-pop:                                            │
│      [1, 2, 3, 4] → swap 2 with 4 → [1, 4, 3, 2]             │
│      Pop last → [1, 4, 3]                                     │
│      Only O(1) operations!                                     │
│                                                                │
│  Order doesn't matter for getRandom (all positions equal)     │
│                                                                │
└────────────────────────────────────────────────────────────────┘

WHY EQUAL PROBABILITY?
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  All elements are in a contiguous array.                       │
│  random.choice picks uniformly from [0, n-1].                 │
│  Each element has exactly 1/n probability.                     │
│                                                                │
│  If we used HashSet iteration:                                 │
│  - Would need to iterate to random position: O(n)              │
│  - Or convert to list first: O(n)                             │
│                                                                │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  insert(x) twice      → Second returns false                  │
│  remove(x) not present → Returns false                         │
│  remove last element   → idx_to_remove == last_idx, handled   │
│  Single element list   → getRandom returns that element       │
│  Negative values       → HashMap handles any int              │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  insert():    O(1) average (amortized for list growth)        │
│  remove():    O(1)                                             │
│  getRandom(): O(1)                                             │
└────────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY: O(n)
├── List stores n elements: O(n)
├── HashMap stores n mappings: O(n)
└── Total: O(n)

CONCEPTS USED:
• Hash Map (Dictionary)
• Dynamic Array (List)
• Swap and Pop technique
• Uniform random sampling
"""
