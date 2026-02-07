# 233. Number of Digit One
# Difficulty: Hard
# https://leetcode.com/problems/number-of-digit-one/

"""
PROBLEM:
Given an integer n, count the total number of digit 1 appearing in all
non-negative integers less than or equal to n.

EXAMPLES:
Input: n = 13  → Output: 6   (1,10,11,12,13 contain 6 ones)
Input: n = 0   → Output: 0
Input: n = 100 → Output: 21

CONSTRAINTS:
- 0 <= n <= 10^9

KEY INSIGHT:
Instead of counting ones number by number (O(n)), count how many ones
appear at EACH DIGIT POSITION (ones, tens, hundreds, etc.)

For each position, split the number into:
- higher: digits to the left
- current: digit at current position  
- lower: digits to the right
- divider: 10^position (1, 10, 100, ...)

FORMULA (ones at current position):
- If current > 1:  count = (higher + 1) × divider
- If current == 1: count = (higher × divider) + lower + 1
- If current == 0: count = higher × divider

WHY IT WORKS:
- higher determines how many complete "cycles" of 1s we get
- current determines if current cycle is complete, partial, or absent
- lower determines how much of partial cycle we have (when current==1)

SOLUTION:
Iterate through each digit position, apply formula, sum results.
"""

# STEP 1: Initialize count and divider (start at ones place)
# STEP 2: For each position until divider > n
# STEP 3: Calculate higher, current, lower
# STEP 4: Apply formula based on current digit
# STEP 5: Move to next position (divider *= 10)

class Solution:
    def countDigitOne(self, n: int) -> int:
        
        if n <= 0:                                                               # No positives, no ones
            return 0
        
        count = 0
        divider = 1                                                              # Start at ones place
        
        while divider <= n:
            
            higher = n // (divider * 10)                                         # Digits to the left
            current = (n // divider) % 10                                        # Current digit
            lower = n % divider                                                  # Digits to the right
            
            if current > 1:                                                      # Complete cycle + full current
                count += (higher + 1) * divider
            
            elif current == 1:                                                   # Complete cycles + partial current
                count += (higher * divider) + lower + 1
            
            else:                                                                # current == 0: Only complete cycles
                count += higher * divider
            
            divider *= 10                                                        # Move to next position
        
        return count


"""
WHY EACH PART:
- n <= 0: No positive integers, return 0
- divider = 1: Start at ones place (10^0)
- divider <= n: Process all digit positions
- higher = n // (divider * 10): All digits left of current position
- current = (n // divider) % 10: Digit at current position
- lower = n % divider: All digits right of current position
- current > 1: Full cycles + one more complete cycle at current level
- current == 1: Full cycles + partial cycle (lower + 1 numbers)
- current == 0: Only full cycles (current level doesn't contribute)
- divider *= 10: Move to tens, hundreds, thousands, etc.

HOW IT WORKS (Example: n = 2345):

┌─ Position: Ones (divider = 1) ────────────────────────────┐
│  higher = 2345 // 10 = 234                                │
│  current = 2345 % 10 = 5                                  │
│  lower = 0                                                │
│                                                           │
│  current (5) > 1:                                         │
│  count = (234 + 1) × 1 = 235                              │
│                                                           │
│  (Numbers ending in 1: 1,11,21,...,2341 = 235 numbers)    │
└───────────────────────────────────────────────────────────┘

┌─ Position: Tens (divider = 10) ───────────────────────────┐
│  higher = 2345 // 100 = 23                                │
│  current = (2345 // 10) % 10 = 4                          │
│  lower = 2345 % 10 = 5                                    │
│                                                           │
│  current (4) > 1:                                         │
│  count += (23 + 1) × 10 = 240                             │
│                                                           │
│  (10-19, 110-119, ..., 2310-2319 = 24 groups × 10)        │
└───────────────────────────────────────────────────────────┘

┌─ Position: Hundreds (divider = 100) ──────────────────────┐
│  higher = 2345 // 1000 = 2                                │
│  current = (2345 // 100) % 10 = 3                         │
│  lower = 2345 % 100 = 45                                  │
│                                                           │
│  current (3) > 1:                                         │
│  count += (2 + 1) × 100 = 300                             │
│                                                           │
│  (100-199, 1100-1199, 2100-2199 = 3 groups × 100)         │
└───────────────────────────────────────────────────────────┘

┌─ Position: Thousands (divider = 1000) ────────────────────┐
│  higher = 2345 // 10000 = 0                               │
│  current = (2345 // 1000) % 10 = 2                        │
│  lower = 2345 % 1000 = 345                                │
│                                                           │
│  current (2) > 1:                                         │
│  count += (0 + 1) × 1000 = 1000                           │
│                                                           │
│  (1000-1999 = 1 group × 1000)                             │
└───────────────────────────────────────────────────────────┘

Total = 235 + 240 + 300 + 1000 = 1775

DETAILED ANALYSIS OF THE THREE CASES:

┌────────────────────────────────────────────────────────────┐
│  CASE: current > 1                                         │
│                                                            │
│  Example: n = 234, analyzing tens place                    │
│  higher = 2, current = 3, divider = 10                     │
│                                                            │
│  Tens digit = 1 appears in:                                │
│  • 010-019 (when higher prefix = 0)  → 10 numbers          │
│  • 110-119 (when higher prefix = 1)  → 10 numbers          │
│  • 210-219 (when higher prefix = 2)  → 10 numbers          │
│                                                            │
│  Since current=3 > 1, ALL of 210-219 is included           │
│                                                            │
│  Total = (2 + 1) × 10 = 30                                 │
│          └ prefixes 0,1,2 (that's higher + 1)             │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  CASE: current == 1                                        │
│                                                            │
│  Example: n = 214, analyzing tens place                    │
│  higher = 2, current = 1, lower = 4, divider = 10          │
│                                                            │
│  Tens digit = 1 appears in:                                │
│  • 010-019 (higher prefix = 0)  → 10 numbers (complete)    │
│  • 110-119 (higher prefix = 1)  → 10 numbers (complete)    │
│  • 210-214 (higher prefix = 2)  → 5 numbers (PARTIAL!)     │
│                      ↑                                     │
│             only 210,211,212,213,214                       │
│                                                            │
│  Total = (2 × 10) + (4 + 1) = 25                           │
│          └complete   └partial (lower + 1)                 │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  CASE: current == 0                                        │
│                                                            │
│  Example: n = 204, analyzing tens place                    │
│  higher = 2, current = 0, divider = 10                     │
│                                                            │
│  Tens digit = 1 appears in:                                │
│  • 010-019 (higher prefix = 0)  → 10 numbers               │
│  • 110-119 (higher prefix = 1)  → 10 numbers               │
│  • 210-219:  NOT reached! (we only go to 204)              │
│                                                            │
│  Total = 2 × 10 = 20                                       │
│          └ only prefixes 0 and 1 (that's just higher)     │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION (slightly cleaner):

class Solution:
    def countDigitOne(self, n: int) -> int:
        if n <= 0:
            return 0
        
        count = 0
        position = 1                                                             # 1, 10, 100, ...
        
        while position <= n:
            higher = n // (position * 10)
            current = (n // position) % 10
            lower = n % position
            
            # Formula combined:
            # higher * position: complete cycles
            # + min(max(current - 1 + 1, 0), 1) * position: is current >= 1?
            # + (lower + 1) if current == 1 else 0: partial cycle
            
            count += higher * position
            
            if current == 1:
                count += lower + 1
            elif current > 1:
                count += position
            
            position *= 10
        
        return count

VERIFICATION TABLE:
┌──────────┬─────────────────────────────────────────┬─────────┐
│    n     │              Calculation                │  Result │
├──────────┼─────────────────────────────────────────┼─────────┤
│    0     │  No positives                           │    0    │
│    1     │  Just 1                                 │    1    │
│    9     │  Only 1                                 │    1    │
│   10     │  1, 10 (two 1s)                         │    2    │
│   11     │  1, 10, 11 (four 1s)                    │    4    │
│   13     │  1,10,11,12,13 (six 1s)                 │    6    │
│   99     │  ones:10, tens:10                       │   20    │
│  100     │  ones:10, tens:10, hundreds:1           │   21    │
│  999     │  ones:100, tens:100, hundreds:100       │  300    │
└──────────┴─────────────────────────────────────────┴─────────┘

EDGE CASES:
- n = 0: Returns 0 ✓
- n = 1: Returns 1 ✓
- n = 10: Returns 2 (1 and 10) ✓
- n = 11: Returns 4 (1, 10, 11 has two 1s) ✓
- Large n (10^9): Handles efficiently in O(log n) ✓

TIME COMPLEXITY: O(log₁₀ n)
- We iterate through each digit position
- Number of digits = log₁₀(n) + 1
- Each iteration is O(1)

SPACE COMPLEXITY: O(1)
- Only using a few integer variables
- No additional data structures

CONCEPTS USED:
- Digit position analysis
- Mathematical pattern recognition
- Counting by contribution (each position's contribution)
- Integer division and modulo operations
- Logarithmic algorithm design
"""
