"""
381. Insert Delete GetRandom O(1) - Duplicates allowed
Difficulty: Hard
https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/

PROBLEM:
Implement the RandomizedCollection class:
- RandomizedCollection() Initializes the object
- bool insert(int val) Inserts val, returns true if NOT already present
- bool remove(int val) Removes ONE instance of val, returns true if removed
- int getRandom() Returns random element with probability proportional to frequency

All operations must work in O(1) average time complexity.

EXAMPLES:
["RandomizedCollection","insert","insert","insert","getRandom","remove","getRandom"]
[[],[1],[1],[2],[],[1],[]]
Output: [null,true,false,true,2,true,1]
Explanation:
    insert(1) → true  (1 is new)
    insert(1) → false (1 exists, but we still insert another copy)
    insert(2) → true  (2 is new)
    getRandom → 1 or 2 (1 has 66% chance, 2 has 33% chance)
    remove(1) → true  (remove ONE instance of 1)
    getRandom → 1 or 2 (now both have 50% chance)

CONSTRAINTS:
• -2³¹ <= val <= 2³¹ - 1
• At most 2 * 10⁵ calls
• There will be at least one element when getRandom is called

KEY INSIGHT:
Similar to problem 380, but now each value can have MULTIPLE indices.
Use HashMap of value → SET of indices (not just one index).

DATA STRUCTURE:
┌─────────────────────────────────────────────────────────────────┐
│  self.list = [val1, val2, val1, val3, ...]                     │
│  self.map  = {                                                  │
│      val1: {0, 2, ...},   ← SET of indices                     │
│      val2: {1},                                                 │
│      val3: {3}                                                  │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘

REMOVE TRICK:
Same as 380: swap with last element, then pop.
But now we must update the SET of indices for both values.
"""

import random
from collections import defaultdict


class RandomizedCollection:

    def __init__(self):
        """Initialize with empty list and empty hashmap of sets."""
        self.list = []                                           # Stores values
        self.map = defaultdict(set)                              # Maps value → set of indices

    def insert(self, val: int) -> bool:
        """
        Insert val (even if it exists).
        Returns true if val was NOT present before.
        Time: O(1)
        """
        is_new = val not in self.map or len(self.map[val]) == 0
        
        self.map[val].add(len(self.list))                        # Add new index to set
        self.list.append(val)                                    # Add to end of list
        
        return is_new

    def remove(self, val: int) -> bool:
        """
        Remove ONE instance of val.
        Returns true if val was present.
        Time: O(1)
        """
        if val not in self.map or len(self.map[val]) == 0:       # Not present
            return False
        
        # Get one index of val (any one)
        idx = self.map[val].pop()
        
        last_idx = len(self.list) - 1
        last_val = self.list[last_idx]
        
        if idx != last_idx:                                      # Need to swap
            # Move last element to idx
            self.list[idx] = last_val
            
            # Update indices for last_val
            self.map[last_val].discard(last_idx)                 # Remove old index
            self.map[last_val].add(idx)                          # Add new index
        
        # Remove last element
        self.list.pop()
        
        # Clean up empty set
        if len(self.map[val]) == 0:
            del self.map[val]
        
        return True

    def getRandom(self) -> int:
        """
        Return a random element with probability proportional to frequency.
        Time: O(1)
        """
        return random.choice(self.list)


# ============================================================================
# ALTERNATIVE IMPLEMENTATION (More explicit)
# ============================================================================

class RandomizedCollection:

    def __init__(self):
        self.vals = []                                           # List of values
        self.idx_map = defaultdict(set)                          # value → set of indices

    def insert(self, val: int) -> bool:
        # Check if this is a new value
        not_present = len(self.idx_map[val]) == 0
        
        # Add new index
        new_idx = len(self.vals)
        self.idx_map[val].add(new_idx)
        self.vals.append(val)
        
        return not_present

    def remove(self, val: int) -> bool:
        # Check if value exists
        if len(self.idx_map[val]) == 0:
            return False
        
        # Get any index where val is located
        remove_idx = self.idx_map[val].pop()
        
        # Get info about last element
        last_idx = len(self.vals) - 1
        last_val = self.vals[last_idx]
        
        # If not removing the last element, swap
        if remove_idx != last_idx:
            # Put last_val at remove_idx
            self.vals[remove_idx] = last_val
            
            # Update last_val's indices
            self.idx_map[last_val].discard(last_idx)
            self.idx_map[last_val].add(remove_idx)
        
        # Remove last element from list
        self.vals.pop()
        
        # Clean up if val has no more instances
        if len(self.idx_map[val]) == 0:
            del self.idx_map[val]
        
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)


"""
HOW IT WORKS (Detailed Trace):

═══════════════════════════════════════════════════════════════════
INITIAL STATE:
═══════════════════════════════════════════════════════════════════
    list: []
    map:  {}

═══════════════════════════════════════════════════════════════════
insert(1):
═══════════════════════════════════════════════════════════════════
    1 in map with indices? NO → is_new = True
    map[1].add(0)
    list.append(1)
    
    list: [1]
    map:  {1: {0}}
    return True

═══════════════════════════════════════════════════════════════════
insert(1): (duplicate)
═══════════════════════════════════════════════════════════════════
    1 in map with indices? YES → is_new = False
    map[1].add(1)
    list.append(1)
    
    list: [1, 1]
    map:  {1: {0, 1}}
    return False (but value WAS inserted!)

═══════════════════════════════════════════════════════════════════
insert(2):
═══════════════════════════════════════════════════════════════════
    2 in map with indices? NO → is_new = True
    map[2].add(2)
    list.append(2)
    
    list: [1, 1, 2]
    map:  {1: {0, 1}, 2: {2}}
    return True

═══════════════════════════════════════════════════════════════════
insert(1): (another duplicate)
═══════════════════════════════════════════════════════════════════
    list: [1, 1, 2, 1]
    map:  {1: {0, 1, 3}, 2: {2}}
    return False

═══════════════════════════════════════════════════════════════════
getRandom():
═══════════════════════════════════════════════════════════════════
    list: [1, 1, 2, 1]
    Probabilities: 1→75%, 2→25%
    return random.choice(list)

═══════════════════════════════════════════════════════════════════
remove(1): (remove from middle - COMPLEX CASE)
═══════════════════════════════════════════════════════════════════
    BEFORE:
    list: [1, 1, 2, 1]
           0  1  2  3
    map:  {1: {0, 1, 3}, 2: {2}}
    
    Step 1: Get any index of 1
        idx = map[1].pop() → let's say idx = 1
        map[1] = {0, 3}
    
    Step 2: Get last element info
        last_idx = 3
        last_val = 1
    
    Step 3: idx (1) != last_idx (3), need to swap
        list[1] = 1 (the last_val)
        list: [1, 1, 2, 1]  (no visual change since both are 1)
        
        map[1].discard(3)   → map[1] = {0}
        map[1].add(1)       → map[1] = {0, 1}
    
    Step 4: Remove last element
        list.pop()
        list: [1, 1, 2]
    
    Step 5: Check if map[1] is empty? NO ({0, 1})
    
    AFTER:
    list: [1, 1, 2]
    map:  {1: {0, 1}, 2: {2}}
    return True

═══════════════════════════════════════════════════════════════════
remove(2): (remove last element - SIMPLER)
═══════════════════════════════════════════════════════════════════
    BEFORE:
    list: [1, 1, 2]
    map:  {1: {0, 1}, 2: {2}}
    
    idx = map[2].pop() → idx = 2
    map[2] = {} (empty)
    
    last_idx = 2
    last_val = 2
    
    idx == last_idx → no swap needed
    
    list.pop()
    list: [1, 1]
    
    map[2] is empty → del map[2]
    
    AFTER:
    list: [1, 1]
    map:  {1: {0, 1}}
    return True

═══════════════════════════════════════════════════════════════════
remove(1): (when there are still duplicates)
═══════════════════════════════════════════════════════════════════
    BEFORE:
    list: [1, 1]
    map:  {1: {0, 1}}
    
    idx = map[1].pop() → idx = 1
    map[1] = {0}
    
    last_idx = 1, idx = 1 → same!
    No swap needed.
    
    list.pop()
    list: [1]
    
    map[1] = {0}, not empty, keep it
    
    AFTER:
    list: [1]
    map:  {1: {0}}
    return True

═══════════════════════════════════════════════════════════════════

WHY SET FOR INDICES?
┌────────────────────────────────────────────────────────────────┐
│  Operations needed:                                             │
│  • add(idx):     O(1) in set ✓                                 │
│  • discard(idx): O(1) in set ✓                                 │
│  • pop():        O(1) in set ✓ (get any element)              │
│  • len():        O(1) in set ✓                                 │
│                                                                │
│  If we used a list:                                            │
│  • remove(idx):  O(n) to find and remove ✗                    │
│                                                                │
│  Set gives us O(1) for all operations!                         │
└────────────────────────────────────────────────────────────────┘

WHY discard() INSTEAD OF remove()?
┌────────────────────────────────────────────────────────────────┐
│  set.remove(x):  raises KeyError if x not in set              │
│  set.discard(x): does nothing if x not in set                  │
│                                                                │
│  discard is safer when we're not 100% sure the element exists │
└────────────────────────────────────────────────────────────────┘

EDGE CASES:
┌────────────────────────────────────────────────────────────────┐
│  insert(x) when x exists   → Still inserts, returns False     │
│  remove(x) when x missing  → Returns False                     │
│  remove last instance      → Clean up empty set from map       │
│  remove(x) where x is last → No swap needed                    │
│  All same value [1,1,1,1]  → Works, 100% probability for 1    │
└────────────────────────────────────────────────────────────────┘

DIFFERENCE FROM PROBLEM 380:
┌────────────────────────────────────────────────────────────────┐
│  380 (no duplicates):                                          │
│  • map: {val: single_index}                                    │
│  • insert returns False and does nothing if exists             │
│                                                                │
│  381 (duplicates):                                             │
│  • map: {val: SET of indices}                                  │
│  • insert returns False but STILL inserts if exists            │
│  • remove must update SET, not single value                    │
└────────────────────────────────────────────────────────────────┘

TIME COMPLEXITY:
┌────────────────────────────────────────────────────────────────┐
│  insert():    O(1) average                                     │
│  remove():    O(1) average                                     │
│  getRandom(): O(1)                                             │
└────────────────────────────────────────────────────────────────┘

SPACE COMPLEXITY: O(n)
├── List stores n elements: O(n)
├── Map stores n indices across all sets: O(n)
└── Total: O(n)

CONCEPTS USED:
• Hash Map with Set values
• Swap and Pop technique
• defaultdict for cleaner code
• Uniform random sampling with frequency
"""
