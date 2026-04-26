# 670. Maximum Swap
# Difficulty: Medium
# https://leetcode.com/problems/maximum-swap/

"""
PROBLEM:
Given an integer num, you can swap two digits at most once to get the maximum valued number.
Return the maximum valued number you can get.

EXAMPLES:
Input: num = 2736    → Output: 7236 (Swap 2 and 7)
Input: num = 9973    → Output: 9973 (No swap needed)
Input: num = 1993    → Output: 9913 (Swap 1 and the last 9)

CONSTRAINTS:
- 0 <= num <= 10^8

LOGIC RULES:
1. To maximize the number, we want to swap a smaller digit at a higher place value (left) 
   with a larger digit at a lower place value (right).
2. If there are multiple identical maximum digits, we must swap with the one furthest to the right 
   (e.g., in 1993, swapping 1 with the last 9 yields 9913, which is > 9193).

VISUALIZATION (num = 2736):
Number string: ['2', '7', '3', '6']

Last occurrence dictionary:
'2': index 0
'7': index 1
'3': index 2
'6': index 3

Iteration 1 (Value '2' at index 0):
- Check for 9 after index 0 -> No
- Check for 8 after index 0 -> No
- Check for 7 after index 0 -> YES (at index 1)
- Swap '2' and '7' -> ['7', '2', '3', '6']
- Only 1 swap allowed, so we STOP.

Result: 7236 ✓
"""

# STEP 1: Convert the number to a list of characters for mutability
# STEP 2: Record the last occurrence index of each digit
# STEP 3: Iterate through the digits from left to right
# STEP 4: For each digit, look for a larger digit (from 9 down to current + 1)
# STEP 5: If a larger digit exists later in the number, swap and return immediately

class Solution:
    def maximumSwap(self, num: int) -> int:
        
        num_list = list(str(num))                                    # Convert int to list of chars
        
        last_occurrence = {}                                         # Dict to store last indexes
        for i, digit in enumerate(num_list):                         # Iterate to populate dict
            last_occurrence[int(digit)] = i                          # Overwrites to keep the last index
            
        for i, digit in enumerate(num_list):                         # Scan from left to right
            
            for d in range(9, int(digit), -1):                       # Check larger digits (9 down to digit+1)
                
                if last_occurrence.get(d, -1) > i:                   # If larger digit exists AFTER current index
                    
                    num_list[i], num_list[last_occurrence[d]] = num_list[last_occurrence[d]], num_list[i] # Swap!
                    
                    return int(''.join(num_list))                    # Convert back to int and return
                    
        return num                                                   # Return original if no swap made

"""
WHY EACH PART:
- list(str(num)): Strings are immutable in Python. We need a list to swap elements easily.
- last_occurrence dict: By recording the last index, we guarantee that if there are duplicates 
  (like multiple 9s), we take the rightmost one to maximize the swapped value.
- range(9, int(digit), -1): We check the highest possible digits first to ensure we get the absolute maximum.
- > i: We only care about larger digits that appear *after* our current position.
- return inside the loop: The problem strictly limits us to AT MOST ONE swap. Once we do it, we are done.

HOW IT WORKS (Example: 1993):

Initial: num_list = ['1', '9', '9', '3']
last_occurrence = {1: 0, 9: 2, 3: 3} 

Iteration 1 (i=0, digit='1'):
├── d loops from 9 down to 2
├── d=9: last_occurrence.get(9) is 2. Is 2 > 0? YES.
├── Swap index 0 and index 2.
└── num_list becomes ['9', '9', '1', '3']
└── Returns 9913 immediately. ✓

EDGE CASES:
- Already sorted descending (9876): Loop finishes without swapping. Returns 9876. ✓
- Identical digits (9999): Loop finishes without swapping. Returns 9999. ✓
- Duplicates of max (1993): Takes the last 9 to form 9913 instead of 9193. ✓
- Single digit (5): Returns 5. ✓

TIME COMPLEXITY: O(N) 
Where N is the number of digits in num. We iterate through the string a couple of times. 
The inner loop runs at most 9 times (constant time O(1)). Total time is O(N).

SPACE COMPLEXITY: O(N) 
For converting the number to a character list of size N, and a dictionary that stores at most 10 elements O(1).
"""
