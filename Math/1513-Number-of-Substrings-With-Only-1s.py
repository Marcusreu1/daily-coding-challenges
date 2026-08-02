# 1513. Number of Substrings With Only 1s
# Difficulty: Medium
# https://leetcode.com/problems/number-of-substrings-with-only-1s/

"""
PROBLEM:
Given a binary string `s`, return the number of substrings with all characters 1's.
Since the answer may be too large, return it modulo 10^9 + 7.

EXAMPLES:
Input: s = "0110111"
Output: 9
(Explanation: There are 9 substring in total with only 1's characters.
"1" -> 5 times.
"11" -> 3 times.
"111" -> 1 time.
Total = 5 + 3 + 1 = 9.)

Input: s = "101"
Output: 2
(Explanation: Substring "1" is shown 2 times in s.)

Input: s = "111111"
Output: 21
(Explanation: Each substring contains only 1's characters.)

CONSTRAINTS:
- 1 <= s.length <= 10^5
- s[i] is either '0' or '1'.

ALGORITHM LOGIC (Progressive Combinatorics & State Machine):
1. The mathematical total of contiguous substrings in a block of length N is the triangular number (N * (N+1)) / 2.
2. Instead of calculating block lengths and applying the formula, we can simulate this progressively in a single pass O(N).
3. We maintain a counter `current_ones` that tracks the current streak of consecutive '1's.
4. For every '1' encountered, we increment the streak. The brilliant part is that the new '1' mathematically contributes exactly `current_ones` NEW substrings to our total.
5. If we encounter a '0', the continuous streak is broken, so we reset `current_ones` to 0.
6. Since the string length can reach 10^5, the total combinations can exceed standard 32-bit integer limits, so we return the final sum modulo 10^9 + 7.

VISUALIZATION (s = "0110111"):
MOD = 10^9 + 7, ans = 0, current_ones = 0

char '0': streak broken. current_ones = 0.
char '1': current_ones = 1. ans += 1 -> 1.
char '1': current_ones = 2. ans += 2 -> 3.
char '0': streak broken. current_ones = 0.
char '1': current_ones = 1. ans += 1 -> 4.
char '1': current_ones = 2. ans += 2 -> 6.
char '1': current_ones = 3. ans += 3 -> 9.

Loop ends. Return 9 % MOD = 9. ✓
"""

# STEP 1: Define the modulo constant as required by the problem
# STEP 2: Initialize total combinations accumulator and the current consecutive streak counter
# STEP 3: Iterate through each character in the string
# STEP 4: If '1', increment the streak and add the streak length to the total accumulator
# STEP 5: If '0', strictly reset the streak counter to 0
# STEP 6: Return the accumulated total applying the modulo operation

class Solution:
    def numSub(self, s: str) -> int:
        
        MOD = 10**9 + 7
        ans = 0
        current_ones = 0
        
        for char in s:
            if char == '1':
                # Increment the running streak
                current_ones += 1
                
                # A streak of size N adds exactly N new substrings to the total pool
                ans += current_ones
            else:
                # Break the streak
                current_ones = 0
                
        # Return securely wrapped within the required Modulo boundary
        return ans % MOD

"""
WHY EACH PART:
- MOD = 10**9 + 7: A standard competitive programming boundary to prevent memory/value overflow in staticly typed languages under the hood. 10^9 + 7 is chosen because it's a large prime number.
- ans += current_ones: This completely removes the need for complex combinatoric formulas like `N*(N+1)//2`. It accumulates exactly the triangular sum progressively in constant O(1) time per step.
- ans % MOD: Placed at the very end. While we could technically apply modulo on every addition (`ans = (ans + current_ones) % MOD`), doing it once at the end is marginally faster in Python since Python automatically handles arbitrarily large integers during the loop.

HOW IT WORKS (Example: s = "111"):
1st '1': current_ones = 1. ans = 1.
2nd '1': current_ones = 2. ans = 1 + 2 = 3.
3rd '1': current_ones = 3. ans = 3 + 3 = 6.
Return 6. ✓

KEY TECHNIQUE:
- Single Pass State Machine
- Progressive Combinatorics (Triangular Numbers)
- Modular Arithmetic

EDGE CASES:
- String of purely '0's (e.g., "0000"): `current_ones` never increments. `ans` remains 0. Returns 0 % MOD = 0. ✓
- Very large strings (e.g., 100,000 '1's): The algorithm counts up correctly. The raw `ans` becomes ~5,000,050,000, which evaluates cleanly to 500049971 when modulo 10^9+7 is applied at the end. ✓

TIME COMPLEXITY: O(N) - We iterate through the binary string of length N exactly once. The operations inside the loop are basic O(1) arithmetic.
SPACE COMPLEXITY: O(1) - We only track a couple of integer variables (`ans`, `current_ones`), regardless of how large the string grows.
"""
