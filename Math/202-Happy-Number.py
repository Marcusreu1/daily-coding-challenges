# 202. Happy Number
# Difficulty: Easy
# https://leetcode.com/problems/happy-number/

"""
PROBLEM:
Write an algorithm to determine if a number n is happy.

A happy number is defined by:
- Starting with any positive integer
- Replace number with sum of squares of its digits
- Repeat until number equals 1 (happy) or loops endlessly (not happy)

EXAMPLES:
Input: n = 19 → Output: true
  19 → 82 → 68 → 100 → 1 ✓

Input: n = 2 → Output: false
  2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle!)

CONSTRAINTS:
- 1 <= n <= 2^31 - 1

KEY INSIGHT:
This is a CYCLE DETECTION problem!
- If we reach 1 → happy (1 → 1 → 1... is a "good" cycle)
- If we see a repeated number → infinite cycle → not happy

APPROACHES:
1. HashSet: Store seen numbers, detect repeat (O(log n) space)
2. Floyd's Tortoise & Hare: Two pointers, O(1) space ⭐

SOLUTION:
Use Floyd's algorithm - slow pointer moves 1 step, fast moves 2 steps.
If they meet at 1 → happy. If they meet elsewhere → cycle → not happy.
"""

# STEP 1: Define helper to calculate sum of squared digits
# STEP 2: Use two pointers (slow and fast)
# STEP 3: Move slow 1 step, fast 2 steps
# STEP 4: If fast reaches 1 → happy; if slow == fast → not happy

class Solution:
    def isHappy(self, n: int) -> bool:
        
        def get_next(num: int) -> int:                                           # Sum of squared digits
            total = 0
            while num > 0:
                digit = num % 10                                                 # Extract last digit
                total += digit * digit                                           # Add square
                num //= 10                                                       # Remove last digit
            return total
        
        slow = n                                                                 # Tortoise 
        fast = get_next(n)                                                       # Hare (starts 1 step ahead)
        
        while fast != 1 and slow != fast:                                        # Until happy or cycle
            slow = get_next(slow)                                                # Move 1 step
            fast = get_next(get_next(fast))                                      # Move 2 steps
        
        return fast == 1                                                         # Happy if reached 1


"""
WHY EACH PART:
- get_next(): Calculates next number in sequence (sum of squared digits)
- num % 10: Extracts rightmost digit
- digit * digit: Square the digit
- num //= 10: Remove rightmost digit, continue with rest
- slow = n: Tortoise starts at n
- fast = get_next(n): Hare starts one step ahead
- fast != 1: If fast reaches 1, we're done (happy)
- slow != fast: If they meet, there's a cycle (not happy)
- slow moves 1x: get_next(slow)
- fast moves 2x: get_next(get_next(fast))
- return fast == 1: True if happy, False if cycle

HOW IT WORKS (Example: n = 19):

Sequence: 19 → 82 → 68 → 100 → 1 → 1 → 1...

┌─ Initial State ───────────────────────────────────────────┐
│  slow = 19                                                │
│  fast = get_next(19) = 82                                 │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Iteration 1 ─────────────────────────────────────────────┐
│  fast != 1? Yes (82 ≠ 1)                                  │
│  slow != fast? Yes (19 ≠ 82)                              │
│  Continue loop:                                           │
│  slow = get_next(19) = 82                                 │
│  fast = get_next(get_next(82)) = get_next(68) = 100       │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Iteration 2 ─────────────────────────────────────────────┐
│  fast != 1? Yes (100 ≠ 1)                                 │
│  slow != fast? Yes (82 ≠ 100)                             │
│  Continue loop:                                           │
│  slow = get_next(82) = 68                                 │
│  fast = get_next(get_next(100)) = get_next(1) = 1         │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Iteration 3 ─────────────────────────────────────────────┐
│  fast != 1? No (fast = 1)                                 │
│  Exit loop!                                               │
│                                                           │
│  return fast == 1 → return True ✓                         │
└───────────────────────────────────────────────────────────┘

HOW IT WORKS (Example: n = 2, NOT happy):

Sequence: 2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle!)

The tortoise and hare will eventually meet inside the cycle.
When slow == fast and fast != 1 → return False

FLOYD'S ALGORITHM VISUALIZATION:
┌────────────────────────────────────────────────────────────┐
│  Why does the fast pointer catch the slow one in a cycle? │
│                                                            │
│  Imagine a circular track:                                 │
│                                                            │
│       ┌──→ 4 ──→ 16 ──→ 37 ──┐                            │
│       │                      │                            │
│       │                      ▼                            │
│      20                     58                            │
│       ▲                      │                            │
│       │                      ▼                            │
│       └── 42 ←── 145 ←── 89 ←┘                            │
│                                                            │
│  Fast moves 2x speed, so it gains 1 position per iteration │
│  Eventually, it "laps" the slow pointer and they meet!     │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION (Pythonic get_next):

class Solution:
    def isHappy(self, n: int) -> bool:
        
        def get_next(num: int) -> int:
            return sum(int(d) ** 2 for d in str(num))                            # Convert to string
        
        slow, fast = n, get_next(n)
        
        while fast != 1 and slow != fast:
            slow = get_next(slow)
            fast = get_next(get_next(fast))
        
        return fast == 1

# Note: String conversion is less efficient but more readable

KNOWN CYCLE FOR UNHAPPY NUMBERS:
┌────────────────────────────────────────────────────────────┐
│  ALL unhappy numbers eventually enter this cycle:          │
│                                                            │
│  4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4                │
│                                                            │
│  Alternative solution: just check if we hit 4!             │
│                                                            │
│  class Solution:                                           │
│      def isHappy(self, n: int) -> bool:                    │
│          while n != 1 and n != 4:                          │
│              n = sum(int(d)**2 for d in str(n))            │
│          return n == 1                                     │
└────────────────────────────────────────────────────────────┘

WHY NUMBERS ALWAYS SHRINK (eventually):
┌────────────────────────────────────────────────────────────┐
│  Max sum of squared digits for d-digit number:             │
│                                                            │
│  Digits    Max Number    Max Sum of Squares                │
│  ──────    ──────────    ─────────────────                 │
│    1          9              81                            │
│    2          99             162                           │
│    3          999            243                           │
│    4          9999           324                           │
│   13       9999999999999     1053                          │
│                                                            │
│  For n > 243, sum of squares < n                           │
│  Numbers quickly fall below 243 and stay bounded           │
│  → Finite states → Must cycle or reach 1                   │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- n = 1: Already happy → returns True ✓
- n = 7: 7→49→97→130→10→1 → returns True ✓
- n = 2: Enters cycle → returns False ✓
- Large n: Quickly reduces, handled correctly ✓

TIME COMPLEXITY: O(log n)
- get_next() is O(log n) - number of digits
- Number of steps before cycle/1 is bounded
- Each step processes O(log n) digits

SPACE COMPLEXITY: O(1) for Floyd's method
- Only storing two integers (slow, fast)
- HashSet method would be O(log n) for stored numbers

CONCEPTS USED:
- Floyd's Cycle Detection (Tortoise and Hare)
- Digit manipulation (mod 10, divide 10)
- Mathematical proof of bounded sequence
- Two-pointer technique
"""
