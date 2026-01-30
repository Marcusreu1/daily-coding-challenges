# 172. Factorial Trailing Zeroes
# Difficulty: Medium
# https://leetcode.com/problems/factorial-trailing-zeroes/

"""
PROBLEM:
Given an integer n, return the number of trailing zeroes in n!.

Note: Your solution should work in logarithmic time complexity.

EXAMPLES:
Input: n = 3   → Output: 0   (3! = 6, no trailing zeros)
Input: n = 5   → Output: 1   (5! = 120, one trailing zero)
Input: n = 0   → Output: 0   (0! = 1, no trailing zeros)

CONSTRAINTS:
- 0 <= n <= 10^4

KEY INSIGHT:
Trailing zeros come from factors of 10 = 2 × 5.
Since there are always more 2s than 5s in n!, count only 5s.

CHALLENGE:
Numbers like 25, 125, 625 contribute MULTIPLE factors of 5!
- 25 = 5²  → contributes 2 fives
- 125 = 5³ → contributes 3 fives

FORMULA:
trailing_zeros = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ⌊n/625⌋ + ...

Each term counts numbers that contribute an additional factor of 5.

SOLUTION:
Repeatedly divide n by 5 and accumulate the quotients.
"""

# STEP 1: Initialize counter to 0
# STEP 2: While n >= 5, divide n by 5 and add quotient to counter
# STEP 3: Return total count of factors of 5

class Solution:
    def trailingZeroes(self, n: int) -> int:
        
        count = 0
        
        while n >= 5:                                                            # While there are factors of 5
            n //= 5                                                              # Count multiples of current power
            count += n                                                           # Add to total
        
        return count


"""
WHY EACH PART:
- count = 0: Accumulator for total factors of 5
- n >= 5: No more factors of 5 when n < 5
- n //= 5: Divide to count next level of 5s
- count += n: Current quotient = multiples at this power level
- return count: Total factors of 5 = trailing zeros

HOW IT WORKS (Example: n = 25):

┌─ Iteration 1 ─────────────────────────────────────────────┐
│  n = 25, n >= 5? Yes                                      │
│  n //= 5  →  n = 5                                        │
│  count += 5  →  count = 5                                 │
│                                                           │
│  Meaning: 5 numbers are multiples of 5¹                   │
│           (5, 10, 15, 20, 25)                             │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Iteration 2 ─────────────────────────────────────────────┐
│  n = 5, n >= 5? Yes                                       │
│  n //= 5  →  n = 1                                        │
│  count += 1  →  count = 6                                 │
│                                                           │
│  Meaning: 1 number is multiple of 5²                      │
│           (25) - contributes extra factor                 │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─ Iteration 3 ─────────────────────────────────────────────┐
│  n = 1, n >= 5? No                                        │
│  Exit loop                                                │
└───────────────────────────────────────────────────────────┘
                    │
                    ▼
        Return count = 6 ✓

VERIFICATION for n = 25:
25! = 15511210043330985984000000
                          ^^^^^^
                          6 zeros ✓

HOW IT WORKS (Example: n = 100):

n = 100 → n //= 5 = 20,  count = 20
n = 20  → n //= 5 = 4,   count = 20 + 4 = 24
n = 4   → n < 5, exit

Return 24 ✓

Breakdown:
- Multiples of 5:   20 numbers (5,10,15,...,100)
- Multiples of 25:  4 numbers  (25,50,75,100) - extra factor each
- Multiples of 125: 0 numbers
Total = 24

HOW IT WORKS (Example: n = 1000):

n = 1000 → n = 200,  count = 200
n = 200  → n = 40,   count = 240
n = 40   → n = 8,    count = 248
n = 8    → n = 1,    count = 249
n = 1    → exit

Return 249 ✓

WHY THIS FORMULA WORKS:
┌────────────────────────────────────────────────────────────┐
│  Consider n = 130:                                         │
│                                                            │
│  Numbers with factors of 5:                                │
│  ┌─────────┬────────────────────────┬───────────────────┐  │
│  │ Number  │ Factorization          │ 5s contributed    │  │
│  ├─────────┼────────────────────────┼───────────────────┤  │
│  │   5     │ 5                      │ 1                 │  │
│  │  10     │ 2 × 5                  │ 1                 │  │
│  │  15     │ 3 × 5                  │ 1                 │  │
│  │  ...    │ ...                    │ 1 each            │  │
│  │  25     │ 5²                     │ 2                 │  │
│  │  50     │ 2 × 5²                 │ 2                 │  │
│  │  75     │ 3 × 5²                 │ 2                 │  │
│  │ 100     │ 4 × 5²                 │ 2                 │  │
│  │ 125     │ 5³                     │ 3                 │  │
│  │ 130     │ 2 × 5 × 13             │ 1                 │  │
│  └─────────┴────────────────────────┴───────────────────┘  │
│                                                            │
│  Count:                                                    │
│  ⌊130/5⌋ = 26  (all multiples of 5)                        │
│  ⌊130/25⌋ = 5  (extras from 25,50,75,100,125)              │
│  ⌊130/125⌋ = 1 (extra from 125)                            │
│  Total = 32                                                │
└────────────────────────────────────────────────────────────┘

WHY DIVIDE n REPEATEDLY (instead of multiply divisor)?
┌────────────────────────────────────────────────────────────┐
│  OPTION A: Divide n                OPTION B: Multiply 5    │
│  ─────────────────────             ────────────────────    │
│  n //= 5                           divisor *= 5            │
│  count += n                        count += n // divisor   │
│                                                            │
│  Both work! Option A is slightly more elegant.             │
│  n shrinks naturally, no need for separate divisor.        │
└────────────────────────────────────────────────────────────┘

ALTERNATIVE SOLUTION (explicit powers of 5):

class Solution:
    def trailingZeroes(self, n: int) -> int:
        count = 0
        power_of_5 = 5
        
        while power_of_5 <= n:
            count += n // power_of_5
            power_of_5 *= 5
        
        return count

ALTERNATIVE SOLUTION (recursive):

class Solution:
    def trailingZeroes(self, n: int) -> int:
        if n < 5:
            return 0
        return n // 5 + self.trailingZeroes(n // 5)

WHY NOT CALCULATE FACTORIAL DIRECTLY?
┌────────────────────────────────────────────────────────────┐
│  n = 10000                                                 │
│  10000! has over 35,000 digits!                            │
│                                                            │
│  Computing it would be:                                    │
│  • Time: O(n² × digit_multiplication)                      │
│  • Space: O(digits) = O(n log n)                           │
│                                                            │
│  Our formula:                                              │
│  • Time: O(log₅ n)                                         │
│  • Space: O(1)                                             │
│                                                            │
│  Much better!                                              │
└────────────────────────────────────────────────────────────┘

EDGE CASES:
- n = 0: 0! = 1, no zeros → returns 0 ✓
- n = 1: 1! = 1, no zeros → returns 0 ✓
- n = 4: 4! = 24, no zeros → returns 0 ✓
- n = 5: 5! = 120, one zero → returns 1 ✓
- n = 25: Extra factor from 25 → returns 6 ✓
- n = 10000: returns 2499 ✓

VERIFICATION TABLE:
┌──────────┬───────────────────────────────────┬─────────────┐
│    n     │           Calculation             │   Result    │
├──────────┼───────────────────────────────────┼─────────────┤
│    5     │ 5/5 = 1                           │      1      │
│   10     │ 10/5 = 2                          │      2      │
│   25     │ 25/5 + 25/25 = 5 + 1              │      6      │
│   50     │ 50/5 + 50/25 = 10 + 2             │     12      │
│  100     │ 100/5 + 100/25 = 20 + 4           │     24      │
│  125     │ 125/5 + 25 + 5 + 1 = 25+5+1       │     31      │
│ 1000     │ 200 + 40 + 8 + 1                  │    249      │
└──────────┴───────────────────────────────────┴─────────────┘

TIME COMPLEXITY: O(log₅ n)
- Loop runs until n < 5
- Each iteration divides by 5
- Maximum iterations = log₅(n)

SPACE COMPLEXITY: O(1)
- Only using two integer variables
- No additional data structures

CONCEPTS USED:
- Prime factorization insight (10 = 2 × 5)
- Counting factors in factorial
- Logarithmic algorithm design
- Mathematical optimization (avoiding factorial computation)
"""
