# 1247. Minimum Swaps to Make Strings Equal
# Difficulty: Medium
# https://leetcode.com/problems/minimum-swaps-to-make-strings-equal/

"""
PROBLEM:
You are given two strings s1 and s2 of equal length consisting of letters "x" and "y" only. 
Your task is to make these two strings equal to each other. You can swap any two characters 
that belong to different strings, which means: swap s1[i] and s2[j].
Return the minimum number of swaps required to make s1 and s2 equal, or return -1 if it is impossible.

EXAMPLES:
Input: s1 = "xx", s2 = "yy"       → Output: 1 
(Swap s1[0] and s2[1] -> s1 = "yx", s2 = "yx")

Input: s1 = "xy", s2 = "yx"       → Output: 2 
(Swap s1[0] and s2[0] -> s1 = "yy", s2 = "xx", then swap s1[0] and s2[1] -> s1 = "xy", s2 = "xy")

Input: s1 = "xx", s2 = "xy"       → Output: -1 
(Impossible to make them equal)

CONSTRAINTS:
- 1 <= s1.length, s2.length <= 1000
- s1, s2 only contain 'x' or 'y'

SWAP LOGIC RULES:
We only care about the indices where s1[i] != s2[i]. There are only two types of mismatches:
Type 1 ("xy"): s1[i] = 'x' and s2[i] = 'y'
Type 2 ("yx"): s1[i] = 'y' and s2[i] = 'x'

Rule A (Same type pairs):
It takes EXACTLY 1 swap to fix two mismatches of the SAME type.
- Two "xy" pairs -> 1 swap
- Two "yx" pairs -> 1 swap

Rule B (Different type pairs):
It takes EXACTLY 2 swaps to fix two mismatches of DIFFERENT types.
- One "xy" pair + One "yx" pair -> 2 swaps

Impossibility Rule:
If the total number of mismatches (xy_count + yx_count) is odd, we can't pair them all up. Return -1.

VISUALIZATION:

Scenario A: Fixing two "xy" mismatches (1 Swap)
    s1:  x  x       Swap s1[0]       s1:  y  x
         |  |       and s2[1]        
    s2:  y  y       --------->       s2:  y  x  (MATCH!)

Scenario B: Fixing one "xy" and one "yx" (2 Swaps)
    s1:  x  y       Swap s1[0]       s1:  y  y      Swap s1[0]       s1:  x  y
         |  |       and s2[0]             |  |      and s2[1]             |  |
    s2:  y  x       --------->       s2:  x  x      --------->       s2:  x  y  (MATCH!)
"""

# STEP 1: Initialize counters for both types of mismatches
# STEP 2: Iterate through both strings simultaneously to count mismatches
# STEP 3: Check if the total amount of mismatches is odd (return -1 if true)
# STEP 4: Calculate swaps for identical pairs (integer division by 2)
# STEP 5: Calculate swaps for leftover pairs (modulo 2)
# STEP 6: Return the total sum of swaps

class Solution:
    def minimumSwap(self, s1: str, s2: str) -> int:
        
        xy_mismatches = 0                                                # Count of s1='x', s2='y'
        yx_mismatches = 0                                                # Count of s1='y', s2='x'
        
        for i in range(len(s1)):                                         # Iterate through strings
            
            if s1[i] == 'x' and s2[i] == 'y':                            # Found 'xy' mismatch
                xy_mismatches += 1
                
            elif s1[i] == 'y' and s2[i] == 'x':                          # Found 'yx' mismatch
                yx_mismatches += 1
                
        if (xy_mismatches + yx_mismatches) % 2 != 0:                     # Total mismatches must be even
            return -1                                                    # Otherwise, impossible to fix
            
        swaps = (xy_mismatches // 2) + (yx_mismatches // 2)              # 1 swap per identical pair
        swaps += (xy_mismatches % 2) + (yx_mismatches % 2)               # 2 swaps per mixed leftover pair
        
        return swaps                                                     # Return final calculated swaps

"""
WHY EACH PART:
- xy_mismatches, yx_mismatches: We categorize the problem. Perfect matches (x-x, y-y) require 0 swaps, so we ignore them completely.
- (xy_mismatches + yx_mismatches) % 2 != 0: Every swap affects exactly two characters across the strings. If the total number of errors is odd, one character will always be left mismatched.
- (xy_mismatches // 2): This groups mismatches into identical pairs (Rule A). Each pair takes 1 swap.
- (xy_mismatches % 2): This checks if there is a leftover 'xy' mismatch. If there is, there MUST be exactly one leftover 'yx' mismatch (because we already proved the total is even). Adding both modulo results yields 2, which perfectly aligns with Rule B (2 swaps needed).

HOW IT WORKS (Example: s1 = "xxyyxyxyxx", s2 = "xyyxyxxxyx"):

Iteration Phase:
We compare characters at each index:
Index 1: s1='x', s2='y' -> xy_mismatches = 1
Index 4: s1='x', s2='y' -> xy_mismatches = 2
Index 6: s1='y', s2='x' -> yx_mismatches = 1
Index 7: s1='x', s2='y' -> xy_mismatches = 3
Index 9: s1='x', s2='y' -> xy_mismatches = 4
(Total: xy=4, yx=1) -> Total = 5 (ODD). Returns -1 immediately.

Let's trace a valid example: s1 = "xxyy", s2 = "yyxx"
Index 0: 'x' vs 'y' -> xy=1
Index 1: 'x' vs 'y' -> xy=2
Index 2: 'y' vs 'x' -> yx=1
Index 3: 'y' vs 'x' -> yx=2

Calculation Phase:
Total mismatches = 4 (Even, we proceed).
swaps = (2 // 2) + (2 // 2) -> 1 + 1 = 2
swaps += (2 % 2) + (2 % 2)  -> 0 + 0 = 0
Total swaps = 2 ✓

KEY TECHNIQUE:
- Greedy Approach / Math simplification: Instead of simulating the swaps, we abstract the problem into mathematical pairs.
- Categorization: Grouping problems into isolated "types" makes the math predictable and constant time after counting.

EDGE CASES:
- Strings are already equal ("xx", "xx"): Returns 0 ✓
- Odd total mismatch count ("xxx", "yyy"): Returns -1 ✓
- Only one type of mismatch ("xxxx", "yyyy"): Calculates purely using integer division ✓
- Completely alternating ("xyxy", "yxyx"): Calculates purely using leftover combinations ✓

TIME COMPLEXITY: O(N) - Where N is the length of the string. We loop through the strings exactly once.
SPACE COMPLEXITY: O(1) - We only store two integer counters regardless of the string length.

CONCEPTS USED:
- Greedy algorithms
- String traversal
- Modulo arithmetic
- Mathematical abstraction
"""
