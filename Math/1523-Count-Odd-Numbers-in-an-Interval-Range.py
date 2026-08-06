# 1523. Count Odd Numbers in an Interval Range
# Difficulty: Easy
# https://leetcode.com/problems/count-odd-numbers-in-an-interval-range/

"""
PROBLEM:
Given two non-negative integers `low` and `high`. Return the count of odd numbers between `low` and `high` (inclusive).

EXAMPLES:
Input: low = 3, high = 7
Output: 3
(Explanation: The odd numbers between 3 and 7 are [3,5,7].)

Input: low = 8, high = 10
Output: 1
(Explanation: The odd numbers between 8 and 10 are [9].)

CONSTRAINTS:
- 0 <= low <= high <= 10^9

ALGORITHM LOGIC (O(1) Prefix Mathematical Difference):
1. A brute-force loop will cause a Time Limit Exceeded (TLE) error because the range can be up to 1 billion.
2. Instead, we can calculate the answer instantly using the mathematical property of odds in an absolute sequence.
3. The count of odd numbers between 1 and any number `N` is always `(N + 1) // 2`.
4. To find the odds strictly in the inclusive range `[low, high]`, we can use the Prefix Sum difference technique:
   Total Odds = (Odds from 1 to high) - (Odds from 1 to low - 1)
5. Odds from 1 to `high` = (high + 1) // 2
6. Odds from 1 to `low - 1` = ((low - 1) + 1) // 2 = low // 2
7. The master equation becomes strictly: (high + 1) // 2 - low // 2. No `if/else` conditions required.

VISUALIZATION (low = 3, high = 7):
Range = [3, 4, 5, 6, 7]

Prefix 1 (1 to 7): 1, 2, 3, 4, 5, 6, 7
Odds in Prefix 1: (7 + 1) // 2 = 4 (which are 1, 3, 5, 7)

Prefix 2 (1 to low-1 -> 1 to 2): 1, 2
Odds in Prefix 2: (3) // 2 = 1 (which is just 1)

Result = Prefix 1 - Prefix 2 -> 4 - 1 = 3. ✓ (The numbers 3, 5, 7).
"""

# STEP 1: Calculate total odd numbers starting from absolute 0 up to 'high'
# STEP 2: Calculate total odd numbers starting from absolute 0 up to 'low - 1'
# STEP 3: Return the difference to isolate the inclusive range

class Solution:
    def countOdds(self, low: int, high: int) -> int:
        
        # O(1) Mathematical Prefix Difference
        return (high + 1) // 2 - low // 2

"""
WHY EACH PART:
- (high + 1) // 2: Mathematically guarantees rounding up for odd numbers to capture the correct count. 7 becomes 8//2 = 4. 6 becomes 7//2 = 3.
- low // 2: This is the mathematically reduced form of `((low - 1) + 1) // 2`. It perfectly counts how many odd numbers are excluded just before our inclusive `low` boundary.
- No `if` statements: By using the prefix difference, we avoid writing nested logic to check if both numbers are even, both odd, or mixed. The math resolves the parity dynamically.

HOW IT WORKS (Example: low = 8, high = 10):
Formula: (10 + 1) // 2 - 8 // 2
11 // 2 - 4
5 - 4
Result: 1. (Correct, only the number 9 is odd). ✓

KEY TECHNIQUE:
- Mathematical Abstraction (Parity counting)
- Prefix Sum Concept (Range subtraction)
- O(1) Constant Time Evaluation

EDGE CASES:
- low == high and both are Even (e.g., 8, 8): 9//2 - 8//2 -> 4 - 4 = 0. ✓
- low == high and both are Odd (e.g., 3, 3): 4//2 - 3//2 -> 2 - 1 = 1. ✓
- low == 0: Formula still works safely as 0 // 2 is 0. Does not break the prefix logic. ✓

TIME COMPLEXITY: O(1) - Pure arithmetic evaluation. It takes the exact same microscopic CPU time for [3, 7] as it does for [1, 999999999].
SPACE COMPLEXITY: O(1) - Zero memory allocated, strictly returning a computed integer.
"""
