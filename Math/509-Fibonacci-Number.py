"""
509. Fibonacci Number
Difficulty: Easy
https://leetcode.com/problems/fibonacci-number/

PROBLEM:
    The Fibonacci numbers form a sequence where each number is the
    sum of the two preceding ones:
        F(0) = 0, F(1) = 1
        F(n) = F(n-1) + F(n-2) for n > 1
    Given n, calculate F(n).

EXAMPLES:
    Input: n = 2  → Output: 1  (0+1 = 1)
    Input: n = 3  → Output: 2  (1+1 = 2)
    Input: n = 4  → Output: 3  (1+2 = 3)

CONSTRAINTS:
    0 <= n <= 30

KEY INSIGHT:
    To compute F(n), we only need the PREVIOUS TWO values.
    No need to store the entire sequence — just slide two variables forward.

    This is a "sliding window" of size 2 on the Fibonacci sequence.

CHALLENGES:
    Avoiding O(2^n) recursive explosion
    Recognizing we don't need O(n) space — just O(1)

APPROACHES:
    1. Naive recursion:      O(2^n) time, O(n) space   
    2. DP array:             O(n) time,   O(n) space   ✓
    3. Two variables:        O(n) time,   O(1) space    ← we use this

SOLUTION:
    Keep two variables (prev2, prev1) representing F(n-2) and F(n-1).
    At each step, compute current = prev2 + prev1, then slide forward.
    After n-1 steps, prev1 holds F(n).
"""


# STEP 1: Handle base cases (n = 0 or n = 1)
# STEP 2: Initialize two variables for F(0) and F(1)
# STEP 3: Iterate from 2 to n, computing each Fibonacci number
# STEP 4: Slide the window forward each iteration
# STEP 5: Return the result


class Solution:
    def fib(self, n: int) -> int:

        if n <= 1:                                                    # Base cases: F(0)=0, F(1)=1
            return n

        prev2 = 0                                                     # F(0) — two steps behind
        prev1 = 1                                                     # F(1) — one step behind

        for i in range(2, n + 1):                                     # Compute F(2), F(3), ..., F(n)
            current = prev2 + prev1                                   # F(i) = F(i-2) + F(i-1)
            prev2 = prev1                                             # Slide: old F(i-1) becomes new F(i-2)
            prev1 = current                                           # Slide: old F(i) becomes new F(i-1)

        return prev1                                                  # prev1 now holds F(n)


"""
WHY EACH PART:
    n <= 1:              F(0)=0 and F(1)=1 are defined directly, no computation needed
    prev2 = 0:           Represents F(n-2), starting at F(0)
    prev1 = 1:           Represents F(n-1), starting at F(1)
    range(2, n+1):       We already know F(0) and F(1), start computing from F(2)
    current = prev2+prev1: The Fibonacci recurrence: F(n) = F(n-1) + F(n-2)
    prev2 = prev1:       Slide window — what was F(n-1) is now F(n-2)
    prev1 = current:     Slide window — what was F(n) is now F(n-1)
    return prev1:        After the loop, prev1 = F(n)


HOW IT WORKS (Example: n = 6):

    Base case? n=6 > 1 → no

    Init: prev2 = 0, prev1 = 1

    i=2: current = 0 + 1 = 1
    ├── prev2 = 1, prev1 = 1
    └── Window: [F(1)=1, F(2)=1]

    i=3: current = 1 + 1 = 2
    ├── prev2 = 1, prev1 = 2
    └── Window: [F(2)=1, F(3)=2]

    i=4: current = 1 + 2 = 3
    ├── prev2 = 2, prev1 = 3
    └── Window: [F(3)=2, F(4)=3]

    i=5: current = 2 + 3 = 5
    ├── prev2 = 3, prev1 = 5
    └── Window: [F(4)=3, F(5)=5]

    i=6: current = 3 + 5 = 8
    ├── prev2 = 5, prev1 = 8
    └── Window: [F(5)=5, F(6)=8]

    return prev1 = 8 

    Sequence built: 0, 1, 1, 2, 3, 5, 8
                                       ↑ F(6)


HOW IT WORKS (Example: n = 0):

    n <= 1 → return 0  (F(0) = 0)


HOW IT WORKS (Example: n = 1):

    n <= 1 → return 1  (F(1) = 1)


WHY TWO VARIABLES INSTEAD OF AN ARRAY:
    Array approach:
        dp = [0, 1, 1, 2, 3, 5, 8, ...]
        Stores ALL values → O(n) space
        But we only ever READ dp[i-1] and dp[i-2]!

    Two variables approach:
        prev2, prev1 = the only two values we need
        O(1) space — doesn't grow with n

    Visual:
    ┌─────────────────────────────────────────┐
    │ Array:  [0] [1] [1] [2] [3] [5] [8]    │
    │                              ↑   ↑      │
    │               we only need these two!   │
    │                                         │
    │ Vars:              prev2  prev1         │
    │                      ↑      ↑           │
    │                   same info, O(1)!      │
    └─────────────────────────────────────────┘


WHY NAIVE RECURSION IS TERRIBLE:
    fib(5) calls fib(4) + fib(3)
    fib(4) calls fib(3) + fib(2)     ← fib(3) computed AGAIN
    fib(3) calls fib(2) + fib(1)     ← fib(2) computed AGAIN
    ...

    Number of calls grows EXPONENTIALLY:
    ┌──────┬──────────────────┐
    │  n   │  recursive calls │
    ├──────┼──────────────────┤
    │  10  │          177     │
    │  20  │       21,891     │
    │  30  │    2,692,537     │
    │  40  │  331,160,281     │  ← over 300 MILLION! 
    └──────┴──────────────────┘

    Our approach: exactly n-1 iterations. For n=40 → 39 steps 


THE SLIDING WINDOW ANALOGY:
    Think of a train with 2 windows moving along the sequence:

    Position 0:  [0  1] 1  2  3  5  8
    Position 1:   0 [1  1] 2  3  5  8
    Position 2:   0  1 [1  2] 3  5  8
    Position 3:   0  1  1 [2  3] 5  8
    Position 4:   0  1  1  2 [3  5] 8
    Position 5:   0  1  1  2  3 [5  8]  ← F(6) = 8 

    The "train" only needs 2 seats (variables), not the whole track (array)!


HANDLING SPECIAL CASES:
    n = 0:               Return 0 directly (base case) ✓
    n = 1:               Return 1 directly (base case) ✓
    n = 2:               One iteration: 0+1 = 1 ✓
    n = 30:              F(30) = 832040 (fits in int easily) ✓


KEY TECHNIQUE:
    Sliding window:       Only keep the last 2 values needed
    Space optimization:   O(n) DP → O(1) by discarding old values
    Bottom-up iteration:  Avoids recursive overhead and stack overflow
    Variable rotation:    prev2 ← prev1 ← current each step


EDGE CASES:
    n = 0:               F(0) = 0 ✓
    n = 1:               F(1) = 1 ✓
    n = 2:               F(2) = 1 ✓
    n = 10:              F(10) = 55 ✓
    n = 30:              F(30) = 832040 ✓
    Max constraint n=30: Well within int range ✓


TIME COMPLEXITY: O(n)
    Single loop from 2 to n
    Each iteration does O(1) work (one addition, two assignments)

SPACE COMPLEXITY: O(1)
    Only three variables: prev2, prev1, current
    No arrays, no recursion stack


CONCEPTS USED:
    Dynamic programming (bottom-up)
    Space optimization (sliding window / variable rotation)
    Mathematical sequences (Fibonacci definition)
    Iterative vs recursive trade-offs
    Base case handling
"""
