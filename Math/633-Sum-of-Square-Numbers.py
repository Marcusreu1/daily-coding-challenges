"""
633. Sum of Square Numbers
Difficulty: Medium
https://leetcode.com/problems/sum-of-square-numbers/

PROBLEM:
    Given a non-negative integer c, decide whether there are two
    integers a and b such that a² + b² = c.

EXAMPLES:
    Input: c = 5  → Output: true  (1² + 2² = 5)
    Input: c = 3  → Output: false (no valid pair)
    Input: c = 4  → Output: true  (0² + 2² = 4)
    Input: c = 2  → Output: true  (1² + 1² = 2)

CONSTRAINTS:
    0 <= c <= 2^31 - 1

KEY INSIGHT:
    Use TWO POINTERS: a starts at 0, b starts at floor(√c).

    a² + b² == c → found!
    a² + b² <  c → need more → increment a
    a² + b² >  c → need less → decrement b

    Stop when a > b (all pairs checked).

    This is like "two sum" but with squares instead of array values.

CHALLENGES:
    Recognizing this as a two-pointer problem
    Using isqrt for precision (not float sqrt)
    a and b can be 0 or equal
    Large values of c (up to 2^31 - 1)

SOLUTION:
    Set a = 0, b = isqrt(c).
    Move pointers inward based on sum comparison.
    Return true if match found, false if pointers cross.
"""


# STEP 1: Initialize a = 0 (minimum) and b = floor(√c) (maximum useful value)
# STEP 2: While a <= b, compute a² + b²
# STEP 3: If equal to c, return true
# STEP 4: If less, increment a; if more, decrement b
# STEP 5: If loop ends without match, return false


from math import isqrt

class Solution:
    def judgeSquareSum(self, c: int) -> bool:

        a = 0                                                         # Left pointer starts at minimum
        b = isqrt(c)                                                  # Right pointer starts at floor(√c)

        while a <= b:                                                 # While pointers haven't crossed
            total = a * a + b * b                                     # Current sum of squares

            if total == c:                                            # Perfect match found
                return True
            elif total < c:                                           # Sum too small
                a += 1                                                # Need bigger → move a up
            else:                                                     # Sum too big
                b -= 1                                                # Need smaller → move b down

        return False                                                  # No valid pair exists


"""
WHY EACH PART:
    a = 0:               Smallest possible value (0² = 0 is valid)
    b = isqrt(c):        Largest useful b (if b > √c, then b² > c, always too big)
    a <= b:              Stop when pointers cross (avoid duplicate pairs)
    a*a + b*b:           The sum we're testing
    total == c:          Found a valid pair!
    total < c → a++:     Current sum too small, only way to increase is raise a
    total > c → b--:     Current sum too big, only way to decrease is lower b
    return False:        Exhausted all possibilities, no valid pair


HOW IT WORKS (Example: c = 5):

    a = 0, b = isqrt(5) = 2

    a=0, b=2: 0 + 4 = 4 < 5 → a++
    a=1, b=2: 1 + 4 = 5 == 5 → return True 

    1² + 2² = 5 ✓


HOW IT WORKS (Example: c = 3):

    a = 0, b = isqrt(3) = 1

    a=0, b=1: 0 + 1 = 1 < 3 → a++
    a=1, b=1: 1 + 1 = 2 < 3 → a++
    a=2 > b=1 → STOP

    return False  (3 cannot be expressed as sum of two squares)


HOW IT WORKS (Example: c = 0):

    a = 0, b = isqrt(0) = 0

    a=0, b=0: 0 + 0 = 0 == 0 → return True 

    0² + 0² = 0 ✓


HOW IT WORKS (Example: c = 61):

    a = 0, b = isqrt(61) = 7

    a=0, b=7: 0+49 = 49  < 61 → a++
    a=1, b=7: 1+49 = 50  < 61 → a++
    a=2, b=7: 4+49 = 53  < 61 → a++
    a=3, b=7: 9+49 = 58  < 61 → a++
    a=4, b=7: 16+49 = 65 > 61 → b--
    a=4, b=6: 16+36 = 52 < 61 → a++
    a=5, b=6: 25+36 = 61 == 61 → return True 

    5² + 6² = 61 ✓


WHY TWO POINTERS DON'T MISS VALID PAIRS:
    Imagine the search space as a grid:

         b=0  b=1  b=2  b=3  b=4  b=5
    a=0   0    1    4    9   16   25
    a=1   1    2    5   10   17   26
    a=2   4    5    8   13   20   29
    a=3   9   10   13   18   25   34
    a=4  16   17   20   25   32   41
    a=5  25   26   29   34   41   50

    Two pointers trace a STAIRCASE path from top-right to bottom-left.

    When we move a++:
        We KNOW no b >= current b works with current a
        (they'd all be too small, since we already tried max b)

    When we move b--:
        We KNOW no a <= current a works with current b
        (they'd all be too big, since current a is minimum tried)

    The staircase covers ALL relevant cells! 


WHY a <= b (NOT a < b):
    a and b CAN be equal!
    
    c = 2: a=1, b=1 → 1+1 = 2 
    c = 8: a=2, b=2 → 4+4 = 8 
    c = 0: a=0, b=0 → 0+0 = 0 

    If we used a < b, we'd miss these cases!

    We also don't need a > b because:
        (a=3, b=2) is same as (a=2, b=3)
        Already checked when a was 2 and b was 3.


WHY isqrt AND NOT int(sqrt()):
    float sqrt has precision issues:

    Example: c = 2147483647 (2^31 - 1)
        sqrt(2147483647) → 46340.950001... (float)
        int(46340.950001) = 46340 ✓ (happens to work)

    But for some values:
        sqrt(n) might return x.9999999999 instead of (x+1).0
        int() truncates → wrong answer!

    isqrt(c) → EXACT integer square root, always correct 


ALTERNATIVE: HASH SET APPROACH:
    For each a from 0 to √c:
        Check if (c - a²) is a perfect square
        
    def judgeSquareSum(self, c):
        for a in range(isqrt(c) + 1):
            b_sq = c - a * a
            b = isqrt(b_sq)
            if b * b == b_sq:
                return True
        return False

    Same O(√c) time, but two-pointer is more elegant.


HANDLING SPECIAL CASES:
    c = 0:               0² + 0² = 0 → true ✓
    c = 1:               0² + 1² = 1 → true ✓
    c = 2:               1² + 1² = 2 → true ✓
    c = 3:               No pair → false ✓
    Prime c ≡ 1 (mod 4): Always expressible (Fermat's theorem) ✓
    Prime c ≡ 3 (mod 4): Never expressible ✓
    Large c (2^31 - 1):  isqrt handles correctly ✓


KEY TECHNIQUE:
    Two pointers:          Converging search from both ends
    Square root bound:     b never exceeds √c
    Integer sqrt:          isqrt for precision
    Sorted search space:   a² + b² increases with a, decreases with b
    Symmetric pruning:     a ≤ b avoids duplicate checks


EDGE CASES:
    c = 0:               true (0² + 0²) ✓
    c = 1:               true (0² + 1²) ✓
    c = 2:               true (1² + 1²) ✓
    c = 3:               false ✓
    c = 4:               true (0² + 2²) ✓
    c = 2147483647:      false ✓
    c = 2147483646:      true (might need careful sqrt) ✓
    Perfect square c=25: true (0² + 5² or 3² + 4²) ✓


TIME COMPLEXITY: O(√c)
    a goes from 0 up, b goes from √c down
    Each step either a++ or b--
    Total steps ≤ 2 × √c = O(√c)

SPACE COMPLEXITY: O(1)
    Only two integer pointers (a and b)
    No additional data structures


CONCEPTS USED:
    Two-pointer technique
    Number theory (sum of squares)
    Integer square root (isqrt)
    Search space reduction
    Symmetric pair optimization (a ≤ b)
"""
