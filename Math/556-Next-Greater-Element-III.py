"""
556. Next Greater Element III
Difficulty: Medium
https://leetcode.com/problems/next-greater-element-iii/

PROBLEM:
    Given a positive integer n, find the smallest integer which has
    exactly the same digits as n and is greater in value.
    If no such integer exists or it exceeds 32-bit int, return -1.

EXAMPLES:
    Input: n = 12    → Output: 21
    Input: n = 21    → Output: -1
    Input: n = 12443322 → Output: 13222344

CONSTRAINTS:
    1 <= n <= 2^31 - 1

KEY INSIGHT:
    This is exactly the "Next Permutation" algorithm applied to
    the digits of n. Find the next lexicographic permutation of digits.

    4 steps: find pivot → find successor → swap → reverse

CHALLENGES:
    Recognizing this as a Next Permutation problem
    Getting the 4 steps right (pivot, successor, swap, reverse)
    Handling the 32-bit overflow check
    Handling "no next permutation" case (all digits descending)

SOLUTION:
    Convert n to digit list
    Apply Next Permutation algorithm
    Convert back to integer
    Check 32-bit limit
"""


# STEP 1: Convert n to list of digit characters
# STEP 2: Find pivot (rightmost digit smaller than its right neighbor)
# STEP 3: Find successor (rightmost digit greater than pivot)
# STEP 4: Swap pivot and successor
# STEP 5: Reverse everything after pivot position
# STEP 6: Convert back to int and check 32-bit limit


class Solution:
    def nextGreaterElement(self, n: int) -> int:

        digits = list(str(n))                                         # Convert number to list of digit chars
        length = len(digits)

        # --- STEP 1: Find pivot ---
        i = length - 2                                                # Start from second-to-last digit
        while i >= 0 and digits[i] >= digits[i + 1]:                 # Walk left while descending
            i -= 1

        if i == -1:                                                   # All digits descending → no next permutation
            return -1

        # --- STEP 2: Find successor ---
        j = length - 1                                                # Start from rightmost digit
        while digits[j] <= digits[i]:                                 # Find first digit > pivot
            j -= 1

        # --- STEP 3: Swap ---
        digits[i], digits[j] = digits[j], digits[i]                  # Swap pivot with successor

        # --- STEP 4: Reverse suffix ---
        digits[i + 1:] = digits[i + 1:][::-1]                        # Reverse the part after pivot

        # --- STEP 5: Convert and validate ---
        result = int("".join(digits))                                 # Convert back to integer

        return result if result <= 2**31 - 1 else -1                  # Check 32-bit signed int limit


"""
WHY EACH PART:
    list(str(n)):            Easy digit manipulation as characters
    i = length - 2:          Start comparing pairs from the right end
    digits[i] >= digits[i+1]: Moving left while sequence is non-increasing (descending)
    i == -1:                 Entire number is descending → already maximum → no answer
    j = length - 1:          Search for successor from rightmost position
    digits[j] <= digits[i]:  Skip digits that aren't greater than pivot
    swap:                    Put successor in pivot position (increment that position minimally)
    reverse suffix:          Make remaining digits as small as possible (ascending order)
    2**31 - 1 check:         Problem requires 32-bit signed integer validation


HOW IT WORKS (Example: n = 12):

    digits = ['1', '2']

    Step 1 — Find pivot:
    ├── i = 0: '1' >= '2'? NO → pivot = 0
    └── digits = [(1), 2]

    Step 2 — Find successor:
    ├── j = 1: '2' <= '1'? NO → successor = 1
    └── digits = [(1), (2)]

    Step 3 — Swap:
    └── digits = ['2', '1']

    Step 4 — Reverse suffix (after index 0):
    └── ['1'] reversed = ['1'] → digits = ['2', '1']

    result = 21, 21 <= 2^31-1 → return 21 


HOW IT WORKS (Example: n = 21):

    digits = ['2', '1']

    Step 1 — Find pivot:
    ├── i = 0: '2' >= '1'? YES → i = -1
    └── i == -1 → return -1 (21 is already the max permutation)


HOW IT WORKS (Example: n = 12443322):

    digits = ['1','2','4','4','3','3','2','2']

    Step 1 — Find pivot:
    ├── i=6: '2'>='2'? YES
    ├── i=5: '3'>='2'? YES
    ├── i=4: '3'>='3'? YES
    ├── i=3: '4'>='3'? YES
    ├── i=2: '4'>='4'? YES
    ├── i=1: '2'>='4'? NO → pivot = 1
    └── digits = [1,(2),4,4,3,3,2,2]

    Step 2 — Find successor:
    ├── j=7: '2'<='2'? YES
    ├── j=6: '2'<='2'? YES
    ├── j=5: '3'<='2'? NO → successor = 5
    └── digits = [1,(2),4,4,3,(3),2,2]

    Step 3 — Swap:
    └── digits = [1,3,4,4,3,2,2,2]

    Step 4 — Reverse suffix [i+1:]:
    ├── suffix = [4,4,3,2,2,2] → reversed = [2,2,2,3,4,4]
    └── digits = [1,3,2,2,2,3,4,4]

    result = 13222344
    13222344 <= 2147483647 → return 13222344 


WHY THE PIVOT IS THE RIGHTMOST "DIP":
    The suffix after the pivot is DESCENDING = already maximized.
    
    [1, 2, | 4, 4, 3, 3, 2, 2]
            └── descending ──┘
            
    This suffix can't be made any larger.
    To get a bigger number, we MUST change something at or before pivot.
    
    Changing at the pivot (rightmost dip) = smallest possible change.
    Changing further left would increase the number too much.


WHY THE SUCCESSOR IS THE SMALLEST DIGIT > PIVOT:
    In the descending suffix, digits go from large to small (left to right).
    
    Scanning RIGHT to LEFT, the FIRST digit > pivot is the SMALLEST one > pivot.
    
    [4, 4, 3, 3, 2, 2]    pivot = 2
     ↑  ↑  ↑  ↑  ✗  ✗
     all > 2, but 3 (rightmost) is the smallest > 2
    
    Using the smallest successor = minimum increment at pivot position.


WHY REVERSE (NOT SORT) WORKS:
    After the swap, the suffix is STILL descending:
    
    Before swap: [1, 2, 4, 4, 3, (3), 2, 2]  suffix: 4,4,3,3,2,2 (desc)
    After swap:  [1, 3, 4, 4, 3, (2), 2, 2]  suffix: 4,4,3,2,2,2 (desc)
    
    Reversing a descending sequence makes it ascending.
    Ascending = smallest possible arrangement of those digits.
    
    Reverse is O(d), sort would be O(d log d) — same result, slower.


HANDLING SPECIAL CASES:
    All same digits (111):     All descending → return -1 ✓
    Already maximum (4321):    All descending → return -1 ✓
    Already minimum (1234):    Pivot at 2, result = 1243 ✓
    Single digit (5):          No pair to compare → return -1 ✓
    Result > 2^31-1:           Return -1 ✓


KEY TECHNIQUE:
    Next Permutation algorithm:  Classic 4-step process
    Rightmost pivot:             Minimizes the positional change
    Smallest successor:          Minimizes the digit change
    Reverse suffix:              Minimizes the remaining digits
    32-bit validation:           Problem-specific constraint


EDGE CASES:
    n = 1 (single digit):       -1 ✓
    n = 11 (same digits):       -1 ✓
    n = 12:                     21 ✓
    n = 21:                     -1 ✓
    n = 230241:                 230412 ✓
    n = 2147483647 (max int):   -1 (no valid next) ✓
    n = 1999999999:             9199999999 > 2^31-1 → -1 ✓


TIME COMPLEXITY: O(d)
    d = number of digits in n (at most ~10 for 32-bit int)
    Find pivot: O(d)
    Find successor: O(d)
    Swap: O(1)
    Reverse: O(d)
    Overall: O(d)

SPACE COMPLEXITY: O(d)
    List of digit characters
    d is at most 10 for 32-bit integers


CONCEPTS USED:
    Next Permutation algorithm
    Lexicographic ordering
    Two-pointer technique (for reverse)
    String ↔ integer conversion
    32-bit integer overflow handling
    Greedy minimization (smallest change = smallest greater number)
"""
