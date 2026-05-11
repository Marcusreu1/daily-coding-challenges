# 788. Rotated Digits
# Difficulty: Medium
# https://leetcode.com/problems/rotated-digits/

"""
PROBLEM:
An integer x is a good if after rotating each digit individually by 180 degrees, 
we get a valid number that is different from x. Each digit must be rotated.
Given an integer n, return the number of good integers in the range [1, n].

EXAMPLES:
Input: n = 10   → Output: 4
Explanation: 
There are four good numbers in the range [1, 10] : 2, 5, 6, 9.
Note that 1 and 10 are not good numbers, since they remain unchanged after rotating.

Input: n = 1    → Output: 0
Explanation: 1 rotated is 1, which is not different from the original number.

CONSTRAINTS:
- 1 <= n <= 10^4

LOGIC RULES (DIGIT CLASSIFICATION & SET INTERSECTION):
A number is "good" if and only if it meets BOTH of these conditions:
1. It contains NO invalid digits (3, 4, or 7). If it has even one, the rotated number is invalid.
2. It contains AT LEAST ONE rotatable digit (2, 5, 6, or 9). This guarantees the rotated number 
   will be numerically different from the original.
(Digits 0, 1, and 8 are neutral. They don't invalidate the number, but they don't change its value either).

VISUALIZATION (n = 30):
Sets defined: 
invalid_set = {'3', '4', '7'}
rotatable_set = {'2', '5', '6', '9'}

Iteration: i = 25
- Convert to set: {'2', '5'}
- Intersection with invalid_set? None. (Passes Condition 1)
- Intersection with rotatable_set? {'2', '5'}. Yes! (Passes Condition 2)
- Action: count += 1 ✓

Iteration: i = 18
- Convert to set: {'1', '8'}
- Intersection with invalid_set? None. (Passes Condition 1)
- Intersection with rotatable_set? None. (Fails Condition 2, the number wouldn't change)
- Action: skip 

Iteration: i = 23
- Convert to set: {'2', '3'}
- Intersection with invalid_set? {'3'}. Yes. (Fails Condition 1, it becomes an invalid number)
- Action: skip 
"""

# STEP 1: Define the two crucial sets of character digits for O(1) lookups
# STEP 2: Initialize the counter for good numbers
# STEP 3: Iterate through every number from 1 to n (inclusive)
# STEP 4: Convert the number to a string, then to a set of its unique characters
# STEP 5: Check if the number lacks invalid digits AND possesses at least one rotatable digit

class Solution:
    def rotatedDigits(self, n: int) -> int:
        
        invalid_set = {'3', '4', '7'}                                      # Digits that break the number
        rotatable_set = {'2', '5', '6', '9'}                               # Digits that guarantee a change
        
        good_numbers_count = 0                                             # Counter for the result
        
        for i in range(1, n + 1):
            
            num_set = set(str(i))                                          # E.g., 252 -> {'2', '5'}
            
            # Rule 1: Must be completely disjoint from invalid digits
            # Rule 2: Must share at least one element with rotatable digits
            if num_set.isdisjoint(invalid_set) and not num_set.isdisjoint(rotatable_set):
                good_numbers_count += 1                                    # It's a valid and different rotated number!
                
        return good_numbers_count

"""
WHY EACH PART:
- invalid_set & rotatable_set: Using sets allows for extremely fast intersection and disjoint checking compared to 
  iterating through a string character by character.
- set(str(i)): Reduces the number (like 9999) into its unique digit components (like {'9'}). This avoids redundant 
  checks for duplicate digits.
- isdisjoint(): This is a built-in Python set method. `A.isdisjoint(B)` returns True if A and B have NO elements in common. 
  It is mathematically cleaner and generally faster than doing `if not A.intersection(B)`.

HOW IT WORKS (Example dry run for n = 2):

Iteration i = 1:
├── num_set = {'1'}
├── num_set.isdisjoint(invalid_set)? True (No 3,4,7)
├── not num_set.isdisjoint(rotatable_set)? False (No 2,5,6,9)
└── Ignored.

Iteration i = 2:
├── num_set = {'2'}
├── num_set.isdisjoint(invalid_set)? True (No 3,4,7)
├── not num_set.isdisjoint(rotatable_set)? True (It has '2')
└── good_numbers_count becomes 1.

Returns 1. ✓

EDGE CASES:
- Single digit neutrals (e.g., 8): Only contains neutral. Fails condition 2. Returns 0 correctly. ✓
- Numbers with all three types (e.g., 123): Contains 1 (neutral), 2 (rotatable), 3 (invalid). Fails condition 1. Ignored correctly. ✓
- Max constraints (n = 10000): String conversion and set operations are heavily optimized in C under Python's hood, 
  so running this 10,000 times will still finish in just a few milliseconds. ✓

TIME COMPLEXITY: O(N)
Where N is the given number `n`. We iterate N times. 
Inside the loop, converting an integer to string and set takes time proportional to the number of digits, 
which is at most 5 operations (since 10000 has 5 digits). This is O(1) relative to N. Thus, total time is O(N).

SPACE COMPLEXITY: O(1)
The space used by `invalid_set` and `rotatable_set` is constant. The `num_set` holds at most 5 characters. 
We do not scale memory usage with N.
"""
