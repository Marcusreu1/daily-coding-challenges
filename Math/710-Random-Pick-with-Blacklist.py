# 710. Random Pick with Blacklist
# Difficulty: Hard
# https://leetcode.com/problems/random-pick-with-blacklist/

"""
PROBLEM:
You are given an integer n and an array of unique integers blacklist. Design an algorithm 
to pick a random integer in the range [0, n - 1] that is not in blacklist. 
Any integer that is in the allowed range must have an equal probability of being returning.
Optimize your algorithm such that it minimizes the number of calls to the built-in random function.

EXAMPLES:
Input:
["Solution", "pick", "pick", "pick"]
[[7, [2, 3, 5]], [], [], []]
Output:
[null, 0, 4, 1]

CONSTRAINTS:
- 1 <= n <= 10^9
- 0 <= blacklist.length <= min(10^5, n - 1)
- All the values of blacklist are unique.

LOGIC RULES (VIRTUAL ARRAY MAPPING):
1. The total number of valid integers is `m = n - len(blacklist)`.
2. We want to generate a random number strictly in the range `[0, m - 1]` (The Safe Zone).
3. Some blacklisted numbers might fall inside this Safe Zone. We need to remap them to valid 
   numbers that reside in the Danger Zone `[m, n - 1]`.
4. We map (Blacklisted in Safe Zone) -> (Valid in Danger Zone).

VISUALIZATION (n = 7, blacklist = [2, 3, 5]):
Total numbers: [0, 1, 2, 3, 4, 5, 6]
Valid count (m) = 7 - 3 = 4. 
Random generation range: [0, 3]

Safe Zone [0, 1, 2, 3]: Contains blacklisted numbers {2, 3}.
Danger Zone [4, 5, 6]: Contains blacklisted number {5}. Available valid numbers: {4, 6}.

Mapping Process:
- 2 is blacklisted in Safe Zone -> map to last available valid number -> 6
- 3 is blacklisted in Safe Zone -> map to next available valid number -> 4
Mapping dictionary: {2: 6, 3: 4}

Pick Process (random between 0 and 3):
- If random is 0 -> 0 is not in map -> return 0
- If random is 1 -> 1 is not in map -> return 1
- If random is 2 -> 2 is in map -> return 6
- If random is 3 -> 3 is in map -> return 4
All 4 valid numbers have exactly 25% chance of appearing! ✓
"""

# STEP 1: Find the size of the safe zone (n - len(blacklist))
# STEP 2: Convert blacklist to a set for O(1) lookups
# STEP 3: Iterate through blacklist elements that fall in the safe zone
# STEP 4: Map these elements to valid numbers in the tail (danger zone)
# STEP 5: In pick(), generate a random number in safe zone and return its mapped value or itself

import random

class Solution:

    def __init__(self, n: int, blacklist: list[int]):
        
        self.valid_len = n - len(blacklist)                               # Length of the Safe Zone
        self.mapping = {}                                                 # Dictionary for re-routing
        
        bl_set = set(blacklist)                                           # Hash set for O(1) lookups
        last = n - 1                                                      # Pointer starting at the very end
        
        for b in blacklist:
            if b < self.valid_len:                                        # If blacklisted number is in the Safe Zone
                
                while last in bl_set:                                     # Find the next available valid number at the tail
                    last -= 1
                    
                self.mapping[b] = last                                    # Map the blacklisted number to the valid tail number
                last -= 1                                                 # Move tail pointer for the next iteration

    def pick(self) -> int:
        
        x = random.randint(0, self.valid_len - 1)                         # Pick random in Safe Zone
        return self.mapping.get(x, x)                                     # Return mapped value if it exists, else return x

"""
WHY EACH PART:
- self.valid_len: Restricts our random generation so we never directly pick from the tail end.
- set(blacklist): We do `last in bl_set` inside a while loop. A list would make this O(B), 
  but a set makes it O(1), saving us from Time Limit Exceeded.
- while last in bl_set: Ensures we don't accidentally map a Safe Zone blacklisted number 
  to a Danger Zone blacklisted number.
- self.mapping.get(x, x): Python dictionary method. If `x` is a key, it returns its value. 
  If not, it defaults to returning `x`.

HOW IT WORKS (Example: n=4, blacklist=[0, 1]):

Initial state:
valid_len = 4 - 2 = 2. Safe zone is [0, 1]. Danger zone is [2, 3].
bl_set = {0, 1}
last = 3

Looping blacklist [0, 1]:
├── b = 0 (0 < 2 is True):
│   ├── Is last (3) in bl_set? No.
│   ├── mapping[0] = 3
│   └── last becomes 2
├── b = 1 (1 < 2 is True):
│   ├── Is last (2) in bl_set? No.
│   ├── mapping[1] = 2
│   └── last becomes 1

Final mapping: {0: 3, 1: 2}.
When pick() generates 0 or 1, it will perfectly return 3 or 2. ✓

EDGE CASES:
- Empty blacklist: valid_len = n. Mapping is empty. Returns pure random. ✓
- All blacklisted except one: valid_len = 1. Pick always generates 0. Returns the single mapped valid element. ✓
- Blacklist only contains numbers in the Danger Zone: Mapping loop doesn't trigger. Random perfectly picks from Safe Zone. ✓

TIME COMPLEXITY: 
- __init__: O(B) where B is the length of the blacklist. Converting to set takes O(B). The while loop only skips 
  over blacklisted numbers, so across all iterations it runs at most B times.
- pick: O(1) time. Random generation and dictionary lookup are constant time.

SPACE COMPLEXITY: O(B) 
For the `bl_set` and the `mapping` dictionary, which both store at most B elements.
"""
