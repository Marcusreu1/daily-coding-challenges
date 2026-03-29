"""
492. Construct the Rectangle
Difficulty: Easy
https://leetcode.com/problems/construct-the-rectangle/

PROBLEM:
    A web developer needs a rectangular web page with area = `area` pixels.
    Find length L and width W such that:
        - L * W == area
        - L >= W
        - L - W is as small as possible (most "square-like" shape)
    Return [L, W].

EXAMPLES:
    Input: area = 4  → Output: [2, 2]  (perfect square)
    Input: area = 37 → Output: [37, 1] (prime number, only option)
    Input: area = 122122 → Output: [427, 286]

CONSTRAINTS:
    1 <= area <= 10^7

KEY INSIGHT:
    The most "square-like" rectangle has L and W as close
    as possible to √area. Start W from floor(√area) and
    go DOWN until W divides area evenly.

    The FIRST valid W we find gives the MINIMUM difference L - W.

CHALLENGES:
    Understanding why √area is the optimal starting point
    Handling prime numbers (only divisible by 1 and itself)

SOLUTION:
    Start W at floor(√area)
    Decrease W until area % W == 0
    Return [area // W, W]
"""


# STEP 1: Start W from floor(√area)
# STEP 2: Decrease W until it divides area evenly
# STEP 3: Calculate L = area // W
# STEP 4: Return [L, W]


from math import isqrt

class Solution:
    def constructRectangle(self, area: int) -> List[int]:

        w = isqrt(area)                                               # Start from √area rounded down

        while area % w != 0:                                          # Find first W that divides area evenly
            w -= 1                                                    # Go down toward 1

        return [area // w, w]                                         # [L, W] where L = area/W >= W


"""
WHY EACH PART:
    isqrt(area):      Integer square root — best starting point for most square-like shape
    area % w != 0:    W must divide area exactly (no fractional pixels!)
    w -= 1:           Try next smaller candidate
    area // w:        L is simply area divided by W
    [area // w, w]:   L first (larger), W second (smaller) — guaranteed since w <= √area


HOW IT WORKS (Example: area = 24):

    √24 ≈ 4.89 → isqrt(24) = 4

    Iteration 1: w = 4
    ├── 24 % 4 == 0? → YES 
    └── STOP! First valid W found

    L = 24 // 4 = 6
    Return [6, 4] ✓


HOW IT WORKS (Example: area = 37 — prime number):

    √37 ≈ 6.08 → isqrt(37) = 6

    Iteration 1: w = 6 → 37 % 6 = 1 → NO 
    Iteration 2: w = 5 → 37 % 5 = 2 → NO 
    Iteration 3: w = 4 → 37 % 4 = 1 → NO 
    Iteration 4: w = 3 → 37 % 3 = 1 → NO 
    Iteration 5: w = 2 → 37 % 2 = 1 → NO 
    Iteration 6: w = 1 → 37 % 1 = 0 → YES 

    L = 37 // 1 = 37
    Return [37, 1] ✓


HOW IT WORKS (Example: area = 4 — perfect square):

    √4 = 2 → isqrt(4) = 2

    Iteration 1: w = 2
    ├── 4 % 2 == 0? → YES 
    └── STOP!

    L = 4 // 2 = 2
    Return [2, 2] ✓


WHY isqrt AND NOT sqrt:
    sqrt(area) returns a FLOAT → precision issues with large numbers
    isqrt(area) returns exact INTEGER → always correct

    Example:
        sqrt(10**14) might give 9999999.9999999... 
        isqrt(10**14) gives exactly 10000000 ✓


WHY START FROM √area GOING DOWN:
    Factors come in PAIRS: if W divides area, then L = area/W also does
    
    All factors of 24: (1,24) (2,12) (3,8) (4,6)
                                              ↑
                                         closest pair to √24
    
    Starting from √area DOWN guarantees we find the
    closest pair FIRST → minimum L - W


WHY L >= W IS GUARANTEED:
    Since w starts at √area and only goes DOWN:
        w <= √area
        L = area / w >= area / √area = √area >= w ✓


HANDLING SPECIAL CASES:
    Perfect square (area=9):    √9 = 3, W=3 divides → [3,3] ✓
    Prime number (area=7):      Falls all the way to W=1 → [7,1] ✓
    area = 1:                   √1 = 1, W=1 divides → [1,1] ✓
    Large area (10^7):          isqrt handles it, loop runs at most √(10^7) ≈ 3162 times ✓


KEY TECHNIQUE:
    Factor pair search:   Factors come in pairs around √n
    Start from √n:        Guarantees closest pair found first
    Integer square root:  Avoids floating point precision issues
    Downward search:      Simple while loop, guaranteed to terminate (W=1 always works)


EDGE CASES:
    area = 1:             [1, 1] ✓
    area = 2 (prime):     [2, 1] ✓
    area = 4 (square):    [2, 2] ✓
    area = 10000000:      Works within time ✓
    area = 9999991 (prime): [9999991, 1] ✓


TIME COMPLEXITY: O(√n)
    Worst case (prime number): loop from √n down to 1
    Best case (perfect square): loop runs once → O(1)

SPACE COMPLEXITY: O(1)
    Only a few integer variables


CONCEPTS USED:
    Number theory (factors, divisibility)
    Square root optimization (factor pairs)
    Integer arithmetic (isqrt for precision)
    Greedy approach (first valid = best valid)
"""
